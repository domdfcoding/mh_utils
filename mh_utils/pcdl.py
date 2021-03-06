#!/usr/bin/env python3
#
#  pcdl.py
"""
Utilities for handing Agilent Personal Compound Database/Library files.

.. versionadded:: 0.2.0
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import time
from typing import List, Optional, Tuple

# 3rd party
import attr
from attr_utils.serialise import serde
from chemistry_tools.formulae import Formula
from chemistry_tools.names import get_IUPAC_sort_order
from chemistry_tools.pubchem.description import get_common_name, get_compound_id
from chemistry_tools.pubchem.errors import NotFoundError
from chemistry_tools.pubchem.properties import get_properties
from domdf_python_tools.typing import PathLike
from pandas import DataFrame  # type: ignore

__all__ = ["PCDLCompound", "compound_list_2_pandas", "make_pcdl_csv"]

DataFrame.__module__ = "pandas"


@serde
@attr.s(slots=True)
class PCDLCompound:
	"""
	Represents a compound in a PDCL CSV file.

	:param name:

	.. versionadded:: 0.2.0
	"""

	#: The name of the compound.
	name: str = attr.ib()

	#: The IUPAC name of the compound.
	iupac_name: str = attr.ib()

	#: The CAS RN of the compound.
	cas: Optional[str] = attr.ib(default=None)

	#: The formula of the compound.
	formula: Optional[Formula] = attr.ib(default=None)

	#: The exact mass of the compound.
	exact_mass: Optional[float] = attr.ib(default=None)

	#: The PubChem ID of the compound.
	pubchem_id: Optional[str] = attr.ib(default=None)

	@classmethod
	def from_tuple(cls, compound: Tuple[str, Optional[str]]) -> "PCDLCompound":
		"""
		Construct a :class:`~.PCDLCompound` from a tuple of ``(name, cas)``.

		:param compound:
		"""

		pubchem_id: Optional[str]

		try:
			name = get_common_name(compound[0])
			pubchem_id = get_compound_id(compound[0])
		except NotFoundError:
			name = compound[0]
			pubchem_id = None

		cas = compound[1]

		try:
			properties = get_properties(name, "IUPACName, MolecularFormula")[0]
			iupac_name = properties["IUPACName"]
			formula = properties["MolecularFormula"]
			exact_mass = formula.monoisotopic_mass
		except NotFoundError:
			# print(compound[0])
			iupac_name = name
			formula = None
			exact_mass = None

		return cls(
				name=name,
				iupac_name=iupac_name,
				cas=cas,
				formula=formula,
				exact_mass=exact_mass,
				pubchem_id=pubchem_id,
				)

	def as_list(self) -> List[str]:
		"""
		Returns the :class:`~.PCDLCompound` as a list.
		"""

		row: List[str] = [self.name, self.cas or '', self.iupac_name]

		if self.formula:
			row.append(self.formula.hill_formula)
		else:
			row.append('')

		if self.exact_mass:
			row.append(str(self.exact_mass))
		else:
			row.append('')

		if self.pubchem_id:
			row.append(str(self.pubchem_id))
		else:
			row.append('')

		return row


def compound_list_2_pandas(compound_list: List[PCDLCompound]) -> DataFrame:
	"""
	Convert a list of compounds into a :class:`pandas.DataFrame`.

	:param compound_list:

	:rtype:

	.. versionadded:: 0.2.0
	"""

	columns = ["Name", "CAS", "IUPAC", "Formula", "Mass", "PubChem"]
	data: List[List[str]] = []

	for compound in compound_list:
		if compound.formula:
			data.append(compound.as_list())

	df = DataFrame(data, columns=columns)
	df = df.reindex([
			"Name",
			"Formula",
			"Mass",
			"Retention Time",
			"Retention Index",
			"Cation",
			"Anion",
			"CAS",
			"ChemSpider",
			"PubChem",
			"Synonyms",
			"IUPAC",
			"NumSpectra",
			"CCS Count",
			],
					axis=1)

	names = df["IUPAC"]
	sort_order = get_IUPAC_sort_order(names)
	df = df.loc[df["IUPAC"].map(sort_order).sort_values(ascending=True).index]

	return df


def make_pcdl_csv(
		target_compounds: List[Tuple[str, str]],
		outfile: PathLike,
		) -> DataFrame:
	"""
	Given a list of target compounds and their CAS numbers (as 2-element tuples),
	construct a CSV file suitable for conversion to a PCDL.

	:param target_compounds:
	:param outfile: The filename to save the CSV output as.

	:returns: A :class:`pandas.DataFrame` representing the content of the CSV output file.

	.. versionadded:: 0.2.0
	"""  # noqa: D400

	compound_list: List[PCDLCompound] = []

	for name, cas in target_compounds:
		compound = PCDLCompound.from_tuple((name, cas))
		time.sleep(0.25)
		compound_list.append(compound)

	compounds_df = compound_list_2_pandas(compound_list)
	compounds_df.to_csv(outfile, index=False)

	return compounds_df

#!/usr/bin/env python3
#
#  utils.py
"""
CSV utility functions.

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
from typing import Optional

# 3rd party
import pandas  # type: ignore
import sdjson
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

# this package
from mh_utils.csv_parser import Sample, SampleList

__all__ = ["drop_columns", "reorder_columns", "concatenate_json"]

pandas.DataFrame.__module__ = "pandas"


def drop_columns(df: pandas.DataFrame, *, axis: int = 1, inplace: bool = True, **kwargs) -> pandas.DataFrame:
	"""
	Drop columns from the MassHunter CSV file.

	:param df: The :class:`pandas.DataFrame` to drop columns in.
	:param axis: Which axis to drop columns on.
	:param inplace: Whether to modify the :class:`pandas.DataFrame` in place.
	:param kwargs: Additional keyword arguments passed to :meth:`pandas.DataFrame.drop`.
	"""

	# Columns where I have no idea what they represent
	unknown_cols = [
			"HMP",
			"KEGG",
			"LMP",
			"METLIN",
			"Notes",
			"Swiss-Prot",
			"CE",
			"Tgt Hit Pos",
			"Score Diff",
			"FV",
			"Saturated",
			"Vol",
			"Cpds/Group",
			"Group",
			"Std Dev",
			"Score (MFE)",
			"Vol %",
			"EIC/TIC% Area",
			"EIC/TIC% Height",
			"TIC% Area",
			"TIC% Height",
			"TWC% Area",
			"TWC% Height",
			"Purity Comments",
			"Purity Result",
			"Purity Value",
			"Score (Frag Coelution)",
			"FIs Conf.",
			"FIs Conf. %",
			"Score (Frag Ratio)",
			"FragMassDiff(ppm)",
			"FIs Eval.",
			"Source",
			"Flags",
			]

	db_cols = [
			"Mass (DB)",
			"Diff (DB, mDa)",
			"Diff (DB, ppm)",
			"RT (Lib/DB)",
			"RT Diff (Lib/DB)",
			"Score (DB)",
			"Shared (DB)",
			"Unique (DB)",
			]

	mfg_cols = [
			"Diff (MFG, mDa)",
			"Mass (MFG)",
			"Diff (MFG, ppm)",
			"Score (MFG)",
			]

	lib_cols = ["Lib/DB", "Score (Lib)"]

	new_df = df.drop([
			*unknown_cols,
			*db_cols,
			*mfg_cols,
			*lib_cols,
			], axis=axis, inplace=inplace, **kwargs)

	if inplace:
		return df
	else:
		return new_df


def reorder_columns(df: pandas.DataFrame) -> pandas.DataFrame:
	"""
	Reorder columns from the MassHunter CSV file.

	:param df: The :class:`pandas.DataFrame` to reorder columns in.
	"""

	# Make sure to remove columns that got deleted above
	output_col_order = [
			"Sample Name",
			"Cpd",
			"CAS",
			"Name",
			"Hits",
			"Abund",
			"Mining Algorithm",
			"Area",
			"Base Peak",
			"Mass",
			"Avg Mass",
			"Score",
			"m/z",
			"m/z (prod.)",
			"RT",
			"Start",
			"End",
			"Width",
			"Diff (Tgt, mDa)",
			"Diff (Tgt, ppm)",
			"Score (Tgt)",
			"Flags (Tgt)",
			"Flag Severity (Tgt)",
			"Flag Severity Code (Tgt)",
			"Mass (Tgt)",
			"RT (Tgt)",
			"RT Diff (Tgt)",
			"Sample Type",
			"Formula",
			"Height",
			"Ions",
			"Polarity",
			"Z Count",
			"Max Z",
			"Min Z",
			"Label",
			"File",
			"Instrument Name",
			"Position",
			"User Name",
			"Acq Method",
			"DA Method",
			"IRM Calibration status",
			]

	# Omitted columns
	# "ID Source", "ID Techniques Applied"
	# "MS/MS Count",		because blank

	return df[output_col_order]


def concatenate_json(*files: PathLike, outfile: Optional[PathLike] = None) -> SampleList:
	r"""
	Concatenate multiple JSON files together and return a list of :class:`Sample`
	objects in the concatenated json output.

	:param \*files: The files to concatenate.
	:param outfile: The file to save the output as. If :py:obj:`None` no file will be saved.
	"""  # noqa: D400

	all_samples = SampleList()

	for json_file in files:
		samples = PathPlus(json_file).load_json(
				json_library=sdjson,  # type: ignore
				)
		# TODO: https://github.com/python/mypy/issues/5018
		# If it ever gets fixed

		for sample in samples:
			all_samples.append(Sample(**sample))

	if outfile is not None:
		PathPlus(outfile).dump_json(
				all_samples,
				json_library=sdjson,  # type: ignore
				indent=2,
				)
		# TODO: https://github.com/python/mypy/issues/5018
		# If it ever gets fixed

	return all_samples

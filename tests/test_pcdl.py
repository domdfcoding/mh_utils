# 3rd party
import pytest
from pytest_regressions.dataframe_regression import DataFrameRegressionFixture  # type: ignore
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from mh_utils.pcdl import make_pcdl_csv

target_compounds = [
		# ("Compound", "CAS"),
		("4-hydroxy-4-methyl-2-pentanone", "123-42-2"),
		("Acetic acid", "64-19-7"),
		("Formic acid", "64-18-6"),
		("Hexanoic acid, bis(1-methyl ethyl) ester", "105-79-3"),
		("2-Ethyl-1-hexanol", "104-76-7"),
		("Hexylene glycol", "107-41-5"),
		("2-Ethylhexanal", "123-05-7"),
		("Acetaldehyde ", "75-07-0"),
		("Butyraldehyde", "123-72-8"),
		("Formaldehyde", "50-00-0"),
		("Heptanal", "111-71-7"),
		("Hexanal", "66-25-1"),
		("Isobutyraldehyde", "78-84-2"),
		("Isovaleraldehyde", "590-86-3"),
		("Nonanal", "124-19-6"),
		("Propionaldehyde", "123-38-6"),
		("Valeraldehyde", "110-62-3"),
		("Butadiene", "106-99-0"),
		("Benzene", "71-43-2"),
		("Aurin", "603-45-2"),
		("Picric acid", "88-89-1"),
		("Diphenylurea", "102-07-8"),
		("Ethyldiphenylurea", "18168-01-9"),
		("Methyldiphenylurea", "13114-72-2"),
		("1,3-Benzenediol", "108-46-3"),
		("2-hydroxybenzaldehyde", "90-02-8"),
		("3-hydroxybenzaldehyde", "100-83-4"),
		("4-hydroxybenzaldehyde", "123-08-0"),
		("Benzaldehyde", "100-52-7"),
		("Aniline", "62-53-3"),
		("O-nitroaniline", "88-74-4"),
		("Butyl centralite", "85209-46-7"),
		("Ethyl Centralite", "85-98-3"),
		("Methyl centralite", "611-92-7"),
		("Dinitro-ortho-cresol", "497-56-3"),
		("Dinitrocresol", "534-52-1"),
		("m-Cresol", "108-39-4"),
		("o-Cresol", "95-48-7"),
		("p-Cresol", "106-44-5"),
		("1,2-Dicyanobenzene", "91-15-6"),
		("1,3-Dicyanobenzene", "626-17-5"),
		("1,4-Dicyanobenzene", "623-26-7"),
		("isocyanatobenzene", "103-71-9"),
		("Diphenylamine", "122-39-4"),
		("2-Nitrodiphenylamine", "119-75-5"),
		("2,2'-dinitrodiphenylamine", "18264-71-6"),
		("2,2',4,4'-tetranitrodiphenylamine", ' '),
		("2,2',4,4',6,6'-hexanitrodiphenylamine", "131-73-7"),
		("2,2',4,4'6-pentanitrodiphenylamine", ' '),
		("2,4-dinitrodiphenylamine", "961-68-2"),
		("2,4,4'-trinitrodiphenylamine", ' '),
		("2,4,6-trinitrodiphenylamine", ' '),
		("2,4'-dinitrodiphenylamine", "612-36-2"),
		("4-Nitrodiphenylamine", "836-30-6"),
		("4,4-dinitrodiphenylamine", ' '),
		("4,4'-dinitrodiphenylamine", "1821-27-8"),
		("4-nitroso-2-nitrodiphenylamine", ' '),
		("N-nitroso-2-nitrodiphenylamine", "21565-15-1"),
		("N-nitroso-2,2’-dinitrodiphenylamine", ' '),
		("N-nitroso-2,2’,4-trinitrodiphenylamine", ' '),
		("N-nitroso-2,4-dinitrodiphenylamine", ' '),
		("N-nitroso-2,4'-dinitrodiphenylamine", ' '),
		("N-nitroso-4-nitrodiphenylamine", "3665-70-1"),
		("N-nitroso-4,4-dinitrodiphenylamine", ' '),
		("N-nitroso-4,4'-dinitrodiphenylamine", ' '),
		("2-nitrosodiphenylamine", ' '),
		("4-nitrosodiphenylamine", "156-10-5"),
		("N-4-dinitrosodiphenylamine", ' '),
		("N-nitrosodiphenylamine", "86-30-6"),
		("Ethylbenzene", "100-41-4"),
		("2-Ethylbenzoic acid", "612-19-1"),
		("3-Ethylbenzoic acid", "619-20-5"),
		("4-Ethylbenzoic acid", "619-64-7"),
		("Benzofuran", "271-89-6"),
		("1,2,3-Trimethylbenzene", "526-73-8"),
		("1,2,4-Trimethylbenzene", "95-63-6"),
		("1,3,5-Trimethylbenzene", "108-67-8"),
		("Acenaphthylene", "206-96-8"),
		("Azulene", "275-51-4"),
		("Naphthalene", "91-20-3"),
		("2-Naphthol", "135-19-3"),
		("1,4-Dimethylnaphthalene", "571-58-4"),
		("2,6-Dimethylnaphthalene", "581-42-0"),
		("2-Ethylnaphthalene", "939-27-5"),
		("1-Methylnaphthalene", "90-12-0"),
		("2-Methylnaphthalene", "91-57-6"),
		("1,3-Dinitrobenzene", "99-65-0"),
		("1,3,5-Trinitrobenzene", "99-35-4"),
		("Nitrobenzene", "98-95-3"),
		("bis(p-tert-butylphenyl)ether", "24085-65-2"),
		("Phenazine", "92-82-0"),
		("Phenoxazine", "135-67-1"),
		("Quinoxaline", "91-19-0"),
		("Tetracene", "92-24-0"),
		("Triphenyl bismuth", "603-33-8"),
		("Benzoxazole", "273-50-0"),
		("2-nitrophenol", "88-75-5"),
		("Diazodinitrophenol", "4682-03-5"),
		("Diazonitrophenol", ' '),
		("Phenol", "108-95-2"),
		("Acetophenone", "98-86-2"),
		("Benzophenone", "119-61-9"),
		("4-Methylbiphenyl", "644-08-6"),
		("Biphenyl", "1486-01-7"),
		("N,N-diphenylformamide", "607-00-1"),
		("3-phenyl-2-propanol", "104-55-2"),
		("Butyl phthalate", "131-70-4"),
		("Diamyl phthalate", "131-18-0"),
		("Dibutyl phthalate", "84-74-2"),
		("Diethyl phthalate", "84-66-2"),
		("Dimethyl phthalate", "131-11-3"),
		("Dioctyl phthalate", "117-84-0"),
		("Diphenyl Phthalate", "84-62-8"),
		("Ethyl phthalate", "2306-33-4"),
		("Monomethyl phthalate", "4376-18-5"),
		("1,2-Benzoquinone", "583-63-1"),
		("1,4-Benzoquinone", "106-51-4"),
		("Toluene", "108-88-3"),
		("2,3-Dinitrotoluene", "602-01-7"),
		("2,4-Dinitrotoluene", "121-14-2"),
		("2,5-Dinitrotoluene", "619-15-8"),
		("2,6-Dinitrotoluene", "606-20-2"),
		("3,4-Dinitrotoluene", "610-39-9"),
		("2-amine-4,6-dinitrotoluene", "35572-78-2"),
		("4-amine-2,6-dinitrotoluene", "19406-51-0"),
		("m-Tolunitrile", "620-22-4"),
		("o-Tolunitrile", "529-19-1"),
		("p-Tolunitrile", "104-85-8"),
		("2-Nitrotoluene", "88-72-2"),
		("3-Nitrotoluene", "99-08-1"),
		("4-Nitrotoluene", "99-99-0"),
		("2,4,6-Trinitrotoluene", "118-96-7"),
		("m-Xylene", "108-38-3"),
		("o-Xylene", "95-47-6"),
		("p-Xylene", "106-42-3"),
		("Borneol", "507-70-0"),
		("Camphor", "76-22-2"),
		("D-Camphor", "464-49-3"),
		("DL-Camphor", "21368-68-3"),
		("L-Camphor", "464-48-2"),
		("3-nitrocarbazole", "3077-85-8"),
		("9-phenyl-9H-carbazole", "1150-62-5"),
		("Carbazole", "86-74-8"),
		("Dextrin", ' '),
		("Starch", ' '),
		("1-Naphthalenecarbonitrile", "86-53-3"),
		("2-Naphthalenecarbonitrile", "613-46-7"),
		("2-Pyridinecarbonitrile", "100-70-9"),
		("3-Pyridinecarbonitrile", "100-54-9"),
		("4-Pyridinecarbonitrile", "100-48-1"),
		("Methyl cellulose", "9004-67-5"),
		("Nitrocellulose", "9004-70-0"),
		("Cyanides", ' '),
		("Acenaphthene", "83-32-9"),
		("Benzo[b]thiophene", "95-15-8"),
		("2-Furaldehyde", "98-01-1"),
		("furan", "110-00-9"),
		("4-dibenzofuranamine", "50548-43-1"),
		("dibenzofuran", "132-64-9"),
		("Anthracene", "120-12-7"),
		("Benz[a]anthracene ", "56-55-3"),
		("Biphenylene", "259-79-0"),
		("Chrysene", "218-01-9"),
		("Fluoranthene", " ‎206-44-0"),
		("Fluorene", "88-73-7"),
		("Indene", "95-13-6"),
		("Phenanthrene", "85-01-8"),
		("Benzo[a]pyrene", "50-32-8"),
		("Pyrene", "129-00-0"),
		("2-ethylquinoline", "1613-34-9"),
		("2,2’-biquinoline", "119-91-5"),
		("Isoquinoline", "119-65-3"),
		("Quinoline", "91-22-5"),
		("Gum Arabic", ' '),
		("Gum tragacanth", ' '),
		("Karaya gum", ' '),
		("2,3-Dimetyl-2,3-dinitrobutane", "3964-18-9"),
		("2,4-Dinitroanisole", "119-27-7"),
		("3,5-Dinitroaniline", "618-87-1"),
		("Cyclonite (Hexahydro-1,3,5-trinitro-1,3,5-triazine)", "121-82-4"),
		("Di-n-propyl adipate", "106-19-4"),
		("N-methyl-p-nitroaniline", "100-15-2"),
		("Nitroguanidine", "556-88-7"),
		("Octogen (Octahydro-1,3,5,7-tetranitro-1,3,5,7-tetrazocine)", "2691-41-0"),
		("potassium 4,6-dinitrobenzofuroxan", ' '),
		("Oxamide", "471-46-5"),
		("2-nitro-N-(4-nitrophenyl)benzamine", "78411-60-6"),
		("2,4,6-Trinitrophenylmethylni-tramine", "479-45-8"),
		("1,2-Dinitroglycerin", "621-65-8"),
		("1,3-Dinitroglycerin", "623-87-0"),
		("Nitroglycerin", "55-63-0"),
		("Diethylene glycol dinitrate ", "693-21-0"),
		("Ethylene glycol dinitrate", "628-96-6"),
		("Triethylene glycol dinitrate", "111-22-8"),
		("Pentaerythritol Tetranitrate", "78-11-5"),
		("1,2,3-Butanetriol trinitrate", "84002-64-2"),
		("Trimethylolethane trinitrate", "3032-55-1"),
		("2-propenenitrile", "107-13-1"),
		("acetonitrile", "75-05-8"),
		("Benzonitrile", "100-47-0"),
		("Benzylnitrile", "140-29-4"),
		("Charcoal", "7440-44-0"),
		("Dimethyl Sebacate", "106-79-6"),
		("Graphite", "7782-42-5"),
		("Sodium alginate", "9005-38-3"),
		("Candelilla Wax", "8006-44-8"),
		("Paraffin Oil", "8012-95-1"),
		("Petrolatum", ' '),
		("Acaroid resin", ' '),
		("Urethane", "51-79-6"),
		("1-(5-tetrazolyl)-4-guanyltetrazene hydrate", "31330-63-9"),
		("Acrolein", "107-02-8"),
		("Benzothiazole", "95-16-9"),
		("Dibutyl Sebacate", "109-43-3"),
		("Glyceryl Triacetate (1,3-Diacetyloxypropan-2-yl acetate)", "102-76-1"),
		("Indole", "120-72-9"),
		("Methylformate", "107-31-3"),
		("Pentaerythritol dioleate", "25151-96-6"),
		("Phytane", "638-36-8"),
		("Styrene", "100-42-5"),
		]


@pytest.mark.flaky(reruns=5, reruns_delay=120)
def test_make_pcdl_csv(
		tmp_pathplus,
		file_regression: FileRegressionFixture,
		dataframe_regression: DataFrameRegressionFixture,
		):

	dataframe_regression.check(make_pcdl_csv(target_compounds, tmp_pathplus / "all_compounds_pcdl.csv"))
	file_regression.check(
			(tmp_pathplus / "all_compounds_pcdl.csv").read_text(),
			encoding="UTF-8",
			extension="_csv.csv",
			)

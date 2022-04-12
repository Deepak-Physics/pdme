import atheris

with atheris.instrument_imports():
	import pdme
	import pdme.util.normal_form
	import sys

def test_pdme(pt):
	pdme.util.normal_form.flip_chunk_to_positive_px(pt)

atheris.Setup(sys.argv, test_pdme)
atheris.Fuzz()

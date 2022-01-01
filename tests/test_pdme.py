from pdme import __version__
import pdme


def test_version():
	assert __version__ == '0.0.1'
	assert pdme.get_version() == __version__

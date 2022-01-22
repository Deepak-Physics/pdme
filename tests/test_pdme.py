from pdme import __version__
import pdme


def test_version():
	assert pdme.get_version() == __version__

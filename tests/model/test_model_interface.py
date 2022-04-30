from pdme.model import Model
import pytest


def test_model_interface_not_implemented_one_dipoles():
	model = Model()

	model.point_length = lambda: 2

	with pytest.raises(NotImplementedError):
		model.get_dipoles(5)


def test_model_interface_not_implemented_n_dipoles():
	model = Model()

	model.point_length = lambda: 2

	with pytest.raises(NotImplementedError):
		model.get_n_single_dipoles(5, 10)

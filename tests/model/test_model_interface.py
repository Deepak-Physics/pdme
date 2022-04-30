from pdme.model import DipoleModel
import pytest


def test_model_interface_not_implemented_one_dipoles():
	model = DipoleModel()

	model.point_length = lambda: 2

	with pytest.raises(NotImplementedError):
		model.get_dipoles(5)


def test_model_interface_not_implemented_n_dipoles():
	model = DipoleModel()

	model.point_length = lambda: 2

	with pytest.raises(NotImplementedError):
		model.get_monte_carlo_dipole_inputs(5, 10)

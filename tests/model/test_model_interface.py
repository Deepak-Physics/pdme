from pdme.model import Model
from pdme.measurement import DotMeasurement
import pytest


def test_model_interface_not_implemented_point_length():
	model = Model()
	with pytest.raises(NotImplementedError):
		model.point_length()


def test_model_interface_not_implemented_cost():
	model = Model()

	model.point_length = lambda: 2

	with pytest.raises(NotImplementedError):
		cost = model.costs([DotMeasurement(0, [1, 2, 3], 4)])
		cost([1, 2])


def test_model_interface_not_implemented_jac():
	model = Model()

	model.point_length = lambda: 2

	with pytest.raises(NotImplementedError):
		jac = model.jac([DotMeasurement(0, [1, 2, 3], 4)])
		jac([1, 2])

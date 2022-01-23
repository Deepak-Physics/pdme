from pdme.model import UnrestrictedModel
from pdme.measurement import DotMeasurement
import logging
import numpy


def test_unrestricted_plane_model_repr():
	model = UnrestrictedModel(1, 2, 3, 4, 5, 6, 7, 6)
	assert repr(model) == "UnrestrictedModel(1, 2, 3, 4, 5, 6, 7, 6)"


def test_unrestricted_model_cost_and_jac_single():
	model = UnrestrictedModel(1, -1, 1, -1, 1, -1, 1, 1)
	measured_v = 0.000191292  # from dipole with p=(0, 0, 2) at (1, 2, 4) with w = 1
	dot = DotMeasurement(measured_v, (1, 2, 0), 5)
	pt = numpy.array([0, 0, 2, 2, 2, 4, 2])

	cost_function = model.costs([dot])

	expected_cost = [0.0000946746]
	actual_cost = cost_function(pt)

	numpy.testing.assert_allclose(actual_cost, expected_cost, err_msg="Cost wasn't as expected.", rtol=1e-6, atol=1e-11)

	jac_function = model.jac([dot])

	expected_jac = [
		[
			0.00007149165379592005, 0, 0.0002859666151836802,
			-0.0001009293935942401, 0, -0.0002607342667851202,
			0.0001035396365320221
		]
	]
	actual_jac = jac_function(pt)

	logging.warning(actual_jac)

	numpy.testing.assert_allclose(actual_jac, expected_jac, err_msg="Jac wasn't as expected.", rtol=1e-6, atol=1e-11)

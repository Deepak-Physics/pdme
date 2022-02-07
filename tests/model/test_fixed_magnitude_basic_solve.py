from pdme.model import FixedMagnitudeModel
from pdme.measurement import OscillatingDipole, OscillatingDipoleArrangement
import logging
import numpy
import itertools


def test_fixed_magnitude_model_solve_basic():
	# Initialise our dipole arrangement and create dot measurements along a square.
	dipoles = OscillatingDipoleArrangement([OscillatingDipole((2, 0, 0), (1, 2, 4), 1)])
	dot_inputs = list(itertools.chain.from_iterable(
		(([1, 2, 0.01], f), ([1, 1, -0.2], f), ([1.5, 2, 0.01], f), ([1.5, 1, -0.2], f), ([2, 1, 0], f), ([2, 2, 0], f), ([0, 2, -.1], f), ([0, 1, 0.04], f), ([2, 0, 0], f), ([1, 0, 0], f)) for f in numpy.arange(1, 10, 2)
	))
	dots = dipoles.get_dot_measurements(dot_inputs)

	model = FixedMagnitudeModel(-5, 5, -5, 5, -5, 5, 2, 1)

	# from the dipole, these are the unspecified variables in ((0, 0, 2), (1, 2, 4), 1)
	expected_solution = [numpy.pi / 2, 0, 1, 2, 4, 1]

	result = model.solve(dots)
	logging.info(result)
	assert result.success
	numpy.testing.assert_allclose(result.normalised_x, expected_solution, err_msg="Even well specified problem solution was wrong.", rtol=1e-6, atol=1e-11)

	solved_dipoles = model.solution_as_dipoles(result.normalised_x)

	assert len(solved_dipoles) == 1
	numpy.testing.assert_allclose(solved_dipoles[0].p, (2, 0, 0), err_msg="Shove it in a dipole correctly.", rtol=1e-6, atol=1e-11)
	numpy.testing.assert_allclose(solved_dipoles[0].s, (1, 2, 4), err_msg="Shove it in a dipole correctly.", rtol=1e-6, atol=1e-11)
	numpy.testing.assert_allclose(solved_dipoles[0].w, 1, err_msg="Shove it in a dipole correctly.", rtol=1e-6, atol=1e-11)


def test_fixed_magnitude_model_repr():
	model = FixedMagnitudeModel(-5, 5, -5, 5, -5, 5, 2, 1)
	assert repr(model) == "FixedMagnitudeModel(-5, 5, -5, 5, -5, 5, 2, 1)"

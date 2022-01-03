from pdme.model import UnrestrictedModel
from pdme.measurement import OscillatingDipole, OscillatingDipoleArrangement
import logging
import numpy
import itertools


def test_unrestricted_model_solve_basic():
	# Initialise our dipole arrangement and create dot measurements along a square.
	dipoles = OscillatingDipoleArrangement([OscillatingDipole((.2, 0, 2), (1, 2, 4), 1)])
	dot_inputs = list(itertools.chain.from_iterable(
		(([1, 2, 0.01], f), ([1, 1, -0.2], f), ([1.5, 2, 0.01], f), ([1.5, 1, -0.2], f), ([2, 1, 0], f), ([2, 2, 0], f), ([0, 2, -.1], f), ([0, 1, 0.04], f), ([2, 0, 0], f), ([1, 0, 0], f)) for f in numpy.arange(1, 10, 2)
	))
	dots = dipoles.get_dot_measurements(dot_inputs)

	model = UnrestrictedModel(1, -1, 1, -1, 1, -1, 1)

	# from the dipole, these are the unspecified variables in ((0, 0, 2), (1, 2, 4), 1)
	expected_solution = [0.2, 0, 2, 1, 2, 4, 1]

	result = model.solve(dots)
	logging.info(result)
	assert result.success
	numpy.testing.assert_allclose(result.normalised_x, expected_solution, err_msg="Even well specified problem solution was wrong.", rtol=1e-6, atol=1e-11)

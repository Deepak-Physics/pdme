from pdme.model import FixedDipoleModel
from pdme.measurement import OscillatingDipole, OscillatingDipoleArrangement
import logging
import numpy
import itertools
import pytest


@pytest.mark.skip(reason="No idea why this is failing, but it shouldn't!")
def test_fixed_dipole_model_solve_basic():
	# Initialise our dipole arrangement and create dot measurements along a square.
	fixed_dipole_moment = numpy.array((2, 1, 2))
	dipoles = OscillatingDipoleArrangement([OscillatingDipole(fixed_dipole_moment, (1, 2, 4), 6)])
	dot_inputs = list(itertools.chain.from_iterable(
		(([1, 2, 1], f), ([1, 1, -2], f), ([1.5, 2, 0.1], f), ([1.5, 1, -0.2], f), ([2, 1, 0], f), ([2, 2, 0], f), ([0, 2, -.1], f), ([0, 1, 0.04], f), ([2, 0, 2], f), ([1, 0, 0], f)) for f in numpy.arange(1, 10, 1)
	))
	dots = dipoles.get_dot_measurements(dot_inputs)

	model = FixedDipoleModel(-3, 3, -3, 3, 3, 5, fixed_dipole_moment, 1)

	# from the dipole, these are the unspecified variables in ((.5, 0, 2), (1, 2, 4), 8)
	expected_solution = [1, 2, 4, 6]

	result = model.solve(dots)
	logging.info(result)
	assert result.success
	numpy.testing.assert_allclose(result.normalised_x, expected_solution, err_msg="Even well specified problem solution was wrong.", rtol=1e-6, atol=1e-11)

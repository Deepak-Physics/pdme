from pdme.model import FixedZPlaneModel
from pdme.measurement import OscillatingDipole, OscillatingDipoleArrangement
import logging
import numpy
import itertools
import pdme.solver


def test_fixed_z_plane_model_solve_basic():
	# Initialise our dipole arrangement and create dot measurements along a square.
	dipoles = OscillatingDipoleArrangement([OscillatingDipole((0, 0, 2), (1, 2, 4), 1)])
	dot_inputs = list(itertools.chain.from_iterable(
		(([1, 2, 0], f), ([1, 1, 0], f), ([2, 1, 0], f), ([2, 2, 0], f)) for f in numpy.arange(1, 10, 2)
	))
	dots = dipoles.get_dot_measurements(dot_inputs)

	model = FixedZPlaneModel(4, -10, 10, -10, 10, 1)

	# from the dipole, these are the unspecified variables in ((0, 0, pz), (sx, sy, 4), w)
	expected_solution = [2, 1, 2, 1]

	result = pdme.solver.sol(model, dots)
	logging.info(result)
	assert result.success
	numpy.testing.assert_allclose(result.x, expected_solution, err_msg="Even well specified problem solution was wrong.", rtol=1e-6, atol=1e-11)

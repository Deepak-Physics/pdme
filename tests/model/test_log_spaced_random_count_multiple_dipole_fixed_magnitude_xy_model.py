from pdme.model import LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel
import numpy
import logging
import pytest


_logger = logging.getLogger(__name__)


def test_random_count_multiple_dipole_xy_wrong_probability():
	with pytest.raises(ValueError):
		LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel(
			-10, 10, -5, 5, 2, 3, 1, 2, 10, 5, 2
		)


def test_repr_random_count_multiple_dipole_fixed_mag_xy():
	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel(
		-10, 10, -5, 5, 2, 3, 1, 2, 10, 5, 0.5
	)
	assert (
		repr(model)
		== "LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel(-10, 10, -5, 5, 2, 3, 1, 2, 10, 5, 0.5)"
	), "Repr should be what I want."


def test_random_count_multiple_dipole_fixed_mag_model_get_dipoles_multiple_xy():

	p_fixed = 10
	dipole_count = 5

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel(
		-10, 10, -5, 5, 2, 3, 0, 5, p_fixed, dipole_count, 0.5
	)

	dipole_arrangement = model.get_dipoles(20, numpy.random.default_rng(1234))
	dipoles = dipole_arrangement.dipoles

	assert (
		len(dipoles) == dipole_count
	), "Should have had multiple dipole based on count generated."


def test_random_count_multiple_dipole_fixed_mag_model_get_dipoles_invariant_xy():

	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	max_frequency = 5

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel(
		x_min, x_max, y_min, y_max, z_min, z_max, 0, max_frequency, p_fixed, 1, 0.5
	)
	model.rng = numpy.random.default_rng(1234)

	dipole_arrangement = model.get_dipoles(5)
	dipoles = dipole_arrangement.dipoles

	assert len(dipoles) == 1, "Should have only had one dipole generated."
	for i in range(10):
		dipole_arrangement = model.get_dipoles(max_frequency)
		dipoles = dipole_arrangement.dipoles

		assert len(dipoles) in (
			0,
			1,
		), "Should have either zero or one dipole generated."

		if len(dipoles) > 0:
			min_s = numpy.array([x_min, y_min, z_min])
			max_s = numpy.array([x_max, y_max, z_max])

			numpy.testing.assert_equal(
				numpy.logical_and(min_s < dipoles[0].s, max_s > dipoles[0].s),
				True,
				f"Dipole location [{dipoles[0].s}] should have been between min [{min_s}] and max [{max_s}] bounds.",
			)
			assert (
				dipoles[0].w < 10 ** max_frequency and dipoles[0].w > 10**0
			), "Dipole frequency should have been between 0 and max."

			numpy.testing.assert_allclose(
				numpy.linalg.norm(dipoles[0].p),
				p_fixed,
				err_msg="Should have had the expected dipole moment magnitude.",
			)

			_logger.warning(dipoles[0].p)
			numpy.testing.assert_allclose(
				dipoles[0].p[2],
				0,
				err_msg="Should have had zero z magnitude.",
			)


def test_random_count_multiple_dipole_fixed_mag_model_get_dipoles_invariant_monte_carlo_xy():

	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	max_frequency = 5
	monte_carlo_n = 20

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel(
		x_min, x_max, y_min, y_max, z_min, z_max, 0, max_frequency, p_fixed, 1, 0.5
	)
	model.rng = numpy.random.default_rng(1234)

	dipole_arrangement = model.get_dipoles(5)
	dipoles = dipole_arrangement.dipoles

	assert len(dipoles) == 1, "Should have only had one dipole generated."
	for i in range(10):
		dipoles = model.get_monte_carlo_dipole_inputs(monte_carlo_n, max_frequency)

		min_s = numpy.array([x_min, y_min, z_min])
		max_s = numpy.array([x_max, y_max, z_max])

		_logger.warning(dipoles)
		_logger.warning(dipoles[:, 0, 0:3])
		_logger.warning(dipoles[:, 0, 3:6])
		_logger.warning(dipoles[:, 0, 6])

		ps = dipoles[:, 0, 0:3]
		ss = dipoles[:, 0, 3:6]
		ws = dipoles[:, 0, 6]

		numpy.testing.assert_equal(
			numpy.logical_and(min_s < ss, max_s > ss).all(),
			True,
			f"Dipole location [{ss}] should have been between min [{min_s}] and max [{max_s}] bounds.",
		)
		assert (ws < 10**max_frequency).all() and (
			ws > 10**0
		).all(), "Dipole frequency should have been between 0 and max."

		norms = numpy.linalg.norm(ps, axis=1)
		filtered_norms = norms[norms > 0]
		numpy.testing.assert_allclose(
			filtered_norms,
			p_fixed,
			err_msg="Should have had the expected dipole moment magnitude.",
		)

		numpy.testing.assert_allclose(
			ps[:, 2],
			0,
			err_msg="Should have had zero z magnitude.",
		)


def test_random_count_multiple_dipole_shape():

	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	max_frequency = 5
	num_dipoles = 13
	monte_carlo_n = 11

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel(
		x_min,
		x_max,
		y_min,
		y_max,
		z_min,
		z_max,
		0,
		max_frequency,
		p_fixed,
		num_dipoles,
		0.5,
	)
	model.rng = numpy.random.default_rng(1234)

	actual_shape = model.get_monte_carlo_dipole_inputs(
		monte_carlo_n, max_frequency
	).shape

	numpy.testing.assert_equal(
		actual_shape,
		(monte_carlo_n, num_dipoles, 7),
		err_msg="shape was wrong for monte carlo outputs",
	)

	actual_shape = model.get_monte_carlo_dipole_inputs(
		monte_carlo_n, max_frequency, rng_to_use=numpy.random.default_rng(1515)
	).shape

	numpy.testing.assert_equal(
		actual_shape,
		(monte_carlo_n, num_dipoles, 7),
		err_msg="shape was wrong for monte carlo outputs",
	)

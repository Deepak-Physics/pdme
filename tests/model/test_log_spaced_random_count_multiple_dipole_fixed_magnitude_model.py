from pdme.model import LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel
import numpy
import logging
import pytest


_logger = logging.getLogger(__name__)


def test_random_count_multiple_dipole_wrong_probability():
	with pytest.raises(ValueError):
		LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel(
			-10, 10, -5, 5, 2, 3, 1, 2, 10, 5, 2
		)


def test_repr_random_count_multiple_dipole_fixed_mag():
	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel(
		-10, 10, -5, 5, 2, 3, 1, 2, 10, 5, 0.5
	)
	assert (
		repr(model)
		== "LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel(-10, 10, -5, 5, 2, 3, 1, 2, 10, 5, 0.5)"
	), "Repr should be what I want."


def test_random_count_multiple_dipole_fixed_mag_model_get_dipoles():

	p_fixed = 10

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel(
		-10, 10, -5, 5, 2, 3, 0, 5, p_fixed, 1, 0.5
	)

	dipole_arrangement = model.get_dipoles(5, numpy.random.default_rng(1234))
	dipoles = dipole_arrangement.dipoles

	assert len(dipoles) == 1, "Should have only had one dipole generated."
	expected_p = numpy.array([8.60141814, -4.50270821, -2.3960853])
	expected_s = numpy.array([-4.76615152, -1.80902942, 2.11809123])
	expected_w = 10**1.2088314662639255

	numpy.testing.assert_allclose(
		dipoles[0].p,
		expected_p,
		err_msg="Random multiple dipole p wasn't as expected",
	)
	numpy.testing.assert_allclose(
		dipoles[0].s,
		expected_s,
		err_msg="Random multiple dipole s wasn't as expected",
	)
	numpy.testing.assert_allclose(
		dipoles[0].w, expected_w, err_msg="Random multiple dipole w wasn't as expected"
	)
	numpy.testing.assert_allclose(
		numpy.linalg.norm(dipoles[0].p),
		p_fixed,
		err_msg="Should have had the expected dipole moment magnitude.",
	)


def test_random_count_multiple_dipole_fixed_mag_model_get_dipoles_multiple():

	p_fixed = 10
	dipole_count = 5

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel(
		-10, 10, -5, 5, 2, 3, 0, 5, p_fixed, dipole_count, 0.5
	)

	dipole_arrangement = model.get_dipoles(20, numpy.random.default_rng(1234))
	dipoles = dipole_arrangement.dipoles

	assert (
		len(dipoles) == dipole_count
	), "Should have had multiple dipole based on count generated."


def test_random_count_multiple_dipole_fixed_mag_model_get_dipoles_invariant():

	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	max_frequency = 5

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel(
		x_min, x_max, y_min, y_max, z_min, z_max, 0, max_frequency, p_fixed, 1, 0.5
	)
	model.rng = numpy.random.default_rng(1234)

	dipole_arrangement = model.get_dipoles(5)
	dipoles = dipole_arrangement.dipoles

	assert len(dipoles) == 1, "Should have only had one dipole generated."
	expected_p = numpy.array([8.60141814, -4.50270821, -2.3960853])
	expected_s = numpy.array([-4.76615152, -1.80902942, 2.11809123])
	expected_w = 10**1.2088314662639255

	numpy.testing.assert_allclose(
		dipoles[0].p,
		expected_p,
		err_msg="Random multiple dipole p wasn't as expected",
		rtol=1e-06,
	)
	numpy.testing.assert_allclose(
		dipoles[0].s, expected_s, err_msg="Random multiple dipole s wasn't as expected"
	)
	numpy.testing.assert_allclose(
		dipoles[0].w, expected_w, err_msg="Random multiple dipole w wasn't as expected"
	)
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


def test_random_count_multiple_dipole_fixed_mag_model_get_n_dipoles():

	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	max_frequency = 5

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel(
		x_min, x_max, y_min, y_max, z_min, z_max, 0, max_frequency, p_fixed, 1, 0.5
	)
	model.rng = numpy.random.default_rng(1234)

	dipole_array = model.get_monte_carlo_dipole_inputs(1, max_frequency)
	expected_dipole_array = numpy.array(
		[
			[
				[
					9.60483896,
					-1.41627817,
					-2.3960853,
					-4.76615152,
					-1.80902942,
					2.11809123,
					10**1.2088314662639255,
				]
			]
		]
	)

	numpy.testing.assert_allclose(
		dipole_array,
		expected_dipole_array,
		err_msg="Should have had the expected output dipole array.",
		rtol=1e-6,
	)
	numpy.testing.assert_allclose(
		model.get_monte_carlo_dipole_inputs(
			1, max_frequency, numpy.random.default_rng(1234)
		),
		expected_dipole_array,
		err_msg="Should have had the expected output dipole array, even with explicitly passed rng.",
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

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeModel(
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

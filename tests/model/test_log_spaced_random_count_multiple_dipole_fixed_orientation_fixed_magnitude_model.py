from pdme.model import (
	LogSpacedRandomCountMultipleDipoleFixedMagnitudeFixedOrientationModel,
)

import numpy
import logging
import pytest


_logger = logging.getLogger(__name__)


def test_random_count_fixedorientation_multiple_dipole_wrong_probability():
	with pytest.raises(ValueError):
		LogSpacedRandomCountMultipleDipoleFixedMagnitudeFixedOrientationModel(
			-10, 10, -5, 5, 2, 3, 1, 2, 10, 0, 0, 5, 2
		)


def test_repr_random_count_multiple_dipole_fixed_orientation_mag():
	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeFixedOrientationModel(
		-10, 10, -5, 5, 2, 3, 1, 2, 10, 0, 1, 5, 0.5
	)
	assert (
		repr(model)
		== "LogSpacedRandomCountMultipleDipoleFixedMagnitudeFixedOrientationModel(-10, 10, -5, 5, 2, 3, 1, 2, 10, 0, 1, 5, 0.5)"
	), "Repr should be same as instantiation."


def test_random_count_multiple_dipole_fixed_mag_model_get_dipoles_invariant():

	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	theta = 0
	phi = 0
	max_frequency = 5

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeFixedOrientationModel(
		x_min,
		x_max,
		y_min,
		y_max,
		z_min,
		z_max,
		0,
		max_frequency,
		p_fixed,
		theta,
		phi,
		1,
		0.5,
	)
	model.rng = numpy.random.default_rng(1234)

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
				dipoles[0].p,
				numpy.array([0, 0, p_fixed]),
				err_msg="Should have had the expected dipole moment.",
			)

	custom_rng = numpy.random.default_rng(1234)
	for i in range(10):
		dipole_arrangement = model.get_dipoles(max_frequency, custom_rng)
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
				dipoles[0].p,
				numpy.array([0, 0, p_fixed]),
				err_msg="Should have had the expected dipole moment.",
			)


def test_random_count_multiple_dipole_fixed_or_fixed_mag_model_get_n_dipoles(snapshot):
	# TODO: this test is a bit garbage just calls things without testing.
	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	theta = numpy.pi / 2
	phi = 0
	max_frequency = 5

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeFixedOrientationModel(
		x_min,
		x_max,
		y_min,
		y_max,
		z_min,
		z_max,
		0,
		max_frequency,
		p_fixed,
		theta,
		phi,
		1,
		0.5,
	)
	model.rng = numpy.random.default_rng(1234)

	actual_inputs = model.get_monte_carlo_dipole_inputs(1, max_frequency)
	assert actual_inputs.tolist() == snapshot
	actual_monte_carlo_inputs = model.get_monte_carlo_dipole_inputs(
		1, max_frequency, numpy.random.default_rng(1234)
	)
	assert actual_monte_carlo_inputs.tolist() == snapshot

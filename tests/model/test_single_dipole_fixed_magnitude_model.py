from pdme.model import SingleDipoleFixedMagnitudeModel
import numpy
import logging


_logger = logging.getLogger(__name__)


def test_single_dipole_fixed_mag_model_get_dipoles():

	p_fixed = 10

	model = SingleDipoleFixedMagnitudeModel(-10, 10, -5, 5, 2, 3, p_fixed)

	dipole_arrangement = model.get_dipoles(5, numpy.random.default_rng(1234))
	dipoles = dipole_arrangement.dipoles

	assert len(dipoles) == 1, "Should have only had one dipole generated."
	expected_p = numpy.array([-2.20191453, 2.06264523, 9.5339953])
	expected_s = numpy.array([8.46492468, -2.38307576, 2.31909706])
	expected_w = 0.5904561648332141

	numpy.testing.assert_allclose(
		dipoles[0].p, expected_p, err_msg="Random single dipole p wasn't as expected"
	)
	numpy.testing.assert_allclose(
		dipoles[0].s, expected_s, err_msg="Random single dipole s wasn't as expected"
	)
	numpy.testing.assert_allclose(
		dipoles[0].w, expected_w, err_msg="Random single dipole w wasn't as expected"
	)
	numpy.testing.assert_allclose(
		numpy.linalg.norm(dipoles[0].p),
		p_fixed,
		err_msg="Should have had the expected dipole moment magnitude.",
	)


def test_single_dipole_fixed_mag_model_get_dipoles_invariant():

	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	max_frequency = 5

	model = SingleDipoleFixedMagnitudeModel(
		x_min, x_max, y_min, y_max, z_min, z_max, p_fixed
	)
	model.rng = numpy.random.default_rng(1234)

	dipole_arrangement = model.get_dipoles(5)
	dipoles = dipole_arrangement.dipoles

	assert len(dipoles) == 1, "Should have only had one dipole generated."
	expected_p = numpy.array([-2.20191453, 2.06264523, 9.5339953])
	expected_s = numpy.array([8.46492468, -2.38307576, 2.31909706])
	expected_w = 0.5904561648332141

	numpy.testing.assert_allclose(
		dipoles[0].p, expected_p, err_msg="Random single dipole p wasn't as expected"
	)
	numpy.testing.assert_allclose(
		dipoles[0].s, expected_s, err_msg="Random single dipole s wasn't as expected"
	)
	numpy.testing.assert_allclose(
		dipoles[0].w, expected_w, err_msg="Random single dipole w wasn't as expected"
	)
	for i in range(10):
		dipole_arrangement = model.get_dipoles(max_frequency)
		dipoles = dipole_arrangement.dipoles

		assert len(dipoles) == 1, "Should have only had one dipole generated."

		min_s = numpy.array([x_min, y_min, z_min])
		max_s = numpy.array([x_max, y_max, z_max])

		numpy.testing.assert_equal(
			numpy.logical_and(min_s < dipoles[0].s, max_s > dipoles[0].s),
			True,
			f"Dipole location [{dipoles[0].s}] should have been between min [{min_s}] and max [{max_s}] bounds.",
		)
		assert (
			dipoles[0].w < max_frequency and dipoles[0].w > 0
		), "Dipole frequency should have been between 0 and max."
		numpy.testing.assert_allclose(
			numpy.linalg.norm(dipoles[0].p),
			p_fixed,
			err_msg="Should have had the expected dipole moment magnitude.",
		)


def test_single_dipole_fixed_mag_model_get_n_dipoles():

	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	max_frequency = 5

	model = SingleDipoleFixedMagnitudeModel(
		x_min, x_max, y_min, y_max, z_min, z_max, p_fixed
	)
	model.rng = numpy.random.default_rng(1234)

	dipole_array = model.get_monte_carlo_dipole_inputs(1, max_frequency)
	expected_dipole_array = numpy.array(
		[
			[
				9.60483896,
				-1.41627817,
				-2.3960853,
				8.46492468,
				-2.38307576,
				2.31909706,
				1.47236493,
			]
		]
	)

	numpy.testing.assert_allclose(
		dipole_array,
		expected_dipole_array,
		err_msg="Should have had the expected output dipole array.",
	)
	numpy.testing.assert_allclose(
		model.get_monte_carlo_dipole_inputs(1, max_frequency, numpy.random.default_rng(1234)),
		expected_dipole_array,
		err_msg="Should have had the expected output dipole array, even with explicitly passed rng.",
	)

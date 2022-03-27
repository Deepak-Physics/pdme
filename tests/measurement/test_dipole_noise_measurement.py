import numpy
import pdme.measurement


def test_static_dipole():
	d1 = pdme.measurement.OscillatingDipole((1, 2, 3), (4, 5, 6), 7)
	d2 = pdme.measurement.OscillatingDipole((2, 5, 3), (4, -5, -6), 2)
	dipoles = pdme.measurement.OscillatingDipoleArrangement([d1, d2])

	dot_position1 = (-1, -1, -1)
	dot_frequency1 = 11
	expected_v1 = 0.00001421963287022476
	expected_v2 = 0.00001107180225755457

	numpy.testing.assert_allclose(d1.s_at_position(dot_position1, dot_frequency1), expected_v1, err_msg="Voltage at dot isn't as expected.")

	dot_measurements = dipoles.get_dot_measurements([(dot_position1, dot_frequency1)])
	assert len(dot_measurements) == 1, "Should have only had one dot measurement."
	measurement = dot_measurements[0]
	numpy.testing.assert_allclose(measurement.r, dot_position1, err_msg="Dot position should have been passed over")
	numpy.testing.assert_allclose(measurement.f, dot_frequency1, err_msg="Dot frequency should have been passed over")
	numpy.testing.assert_allclose(measurement.v, expected_v1 + expected_v2, err_msg="Voltage at dot isn't as expected.")


def test_dipole_dot_pair():
	d1 = pdme.measurement.OscillatingDipole((1, 2, 3), (4, 5, 6), 7)
	dipoles = pdme.measurement.OscillatingDipoleArrangement([d1])

	dot_position1 = (-1, -1, -1)
	dot_position2 = (1, 2, 3)
	dot_frequency = 8
	expected_sij = 0.000083328037100902801698

	numpy.testing.assert_allclose(d1.s_for_dot_pair(dot_position1, dot_position2, dot_frequency), expected_sij, err_msg="Sij for dot pair isn't as expected.")
	numpy.testing.assert_allclose([m.v for m in dipoles.get_dot_pair_measurements([(dot_position1, dot_position2, dot_frequency)])], [expected_sij], err_msg="Sij for dot pair isn't as expected via dipole.")


def test_range_pairs():
	d1 = pdme.measurement.OscillatingDipole((1, 2, 3), (4, 5, 6), 7)
	dipoles = pdme.measurement.OscillatingDipoleArrangement([d1])

	dot_position1 = (-1, -1, -1)
	dot_position2 = (1, 2, 3)
	dot_frequency = 8
	expected_sij = 0.000083328037100902801698

	actuals = dipoles.get_percent_range_dot_pair_measurements([(dot_position1, dot_position2, dot_frequency)], 0.5, 1.5)
	assert len(actuals) == 1, "should have only been one pair"
	actual = actuals[0]
	numpy.testing.assert_allclose([actual.v_low, actual.v_high], expected_sij * numpy.array([0.5, 1.5]), err_msg="Sij for dot pair isn't as expected via dipole with range.")


def test_range_dipole_measurements():
	d1 = pdme.measurement.OscillatingDipole((1, 2, 3), (4, 5, 6), 7)
	d2 = pdme.measurement.OscillatingDipole((2, 5, 3), (4, -5, -6), 2)
	dipoles = pdme.measurement.OscillatingDipoleArrangement([d1, d2])

	dot_position1 = (-1, -1, -1)
	dot_frequency1 = 11
	expected_v1 = 0.00001421963287022476
	expected_v2 = 0.00001107180225755457

	numpy.testing.assert_allclose(d1.s_at_position(dot_position1, dot_frequency1), expected_v1, err_msg="Voltage at dot isn't as expected.")

	range_dot_measurements = dipoles.get_percent_range_dot_measurements([(dot_position1, dot_frequency1)], 0.5, 1.5)
	assert len(range_dot_measurements) == 1, "Should have only had one dot measurement."
	range_measurement = range_dot_measurements[0]
	numpy.testing.assert_allclose(range_measurement.r, dot_position1, err_msg="Dot position should have been passed over")
	numpy.testing.assert_allclose(range_measurement.f, dot_frequency1, err_msg="Dot frequency should have been passed over")
	numpy.testing.assert_allclose(range_measurement.v_low, (expected_v1 + expected_v2) / 2, err_msg="Lower voltage at dot isn't as expected.")
	numpy.testing.assert_allclose(range_measurement.v_high, (expected_v1 + expected_v2) * 3 / 2, err_msg="Lower oltage at dot isn't as expected.")

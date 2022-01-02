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

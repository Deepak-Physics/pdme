import numpy
import pdme.measurement


def test_dipole_to_array():
	d1 = pdme.measurement.OscillatingDipole((1, 2, 3), (4, 5, 6), 7)
	d2 = pdme.measurement.OscillatingDipole((1.5, 2.5, 3.5), (4.5, 5.5, 6.5), 7.5)

	expected1 = numpy.array([1, 2, 3, 4, 5, 6, 7])
	numpy.testing.assert_array_equal(
		expected1, d1.to_flat_array(), err_msg="Didn't convert 1 correctly to array"
	)

	expected2 = numpy.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5])
	numpy.testing.assert_array_equal(
		expected2, d2.to_flat_array(), err_msg="Didn't convert 2 correctly to array"
	)

	arrangement = pdme.measurement.OscillatingDipoleArrangement([d1, d2])
	numpy.testing.assert_array_equal(
		[expected1, expected2], arrangement.to_numpy_array(), err_msg="Didn't convert multiple dipoles right"
	)

import numpy
import pdme.measurement.input_types
from pdme.measurement.dot_measure import DotRangeMeasurement
from pdme.measurement.dot_pair_measure import DotPairRangeMeasurement


def test_inputs_to_array():
	i1 = ([1, 2, 3], 5)
	i2 = ([-1, 4, -2], 9)

	actual = pdme.measurement.input_types.dot_inputs_to_array([i1, i2])
	expected = numpy.array([[1, 2, 3, 5], [-1, 4, -2, 9]])

	numpy.testing.assert_allclose(
		actual, expected, err_msg="Didn't convert to array properly"
	)


def test_pair_inputs_to_array():
	i1 = ([1, 2, 3], [-1, 4, -2], 5)
	i2 = ([-1, 4, -2], [6, 7, 8], 9)

	actual = pdme.measurement.input_types.dot_pair_inputs_to_array([i1, i2])
	expected = numpy.array(
		[
			[[1, 2, 3, 5], [-1, 4, -2, 5]],
			[[-1, 4, -2, 9], [6, 7, 8, 9]],
		]
	)

	numpy.testing.assert_allclose(
		actual, expected, err_msg="Didn't convert to array properly"
	)


def test_ranges_to_array():
	m1 = DotRangeMeasurement(1, 2, 100, 1000)
	m2 = DotRangeMeasurement(0.5, 3, 100, 1000)

	(
		actual_lows,
		actual_highs,
	) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays([m1, m2])
	numpy.testing.assert_allclose(actual_lows, [1, 0.5], err_msg="Lows were wrong")
	numpy.testing.assert_allclose(actual_highs, [2, 3], err_msg="Highs were wrong")


def test_pair_ranges_to_array():
	m1 = DotPairRangeMeasurement(1, 2, 100, 1000, 10000)
	m2 = DotPairRangeMeasurement(0.5, 3, 100, 1000, 10000)

	(
		actual_lows,
		actual_highs,
	) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays([m1, m2])
	numpy.testing.assert_allclose(actual_lows, [1, 0.5], err_msg="Lows were wrong")
	numpy.testing.assert_allclose(actual_highs, [2, 3], err_msg="Highs were wrong")

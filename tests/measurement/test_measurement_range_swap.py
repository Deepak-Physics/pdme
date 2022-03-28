from pdme.measurement import DotRangeMeasurement
from pdme.measurement import DotPairRangeMeasurement
import numpy


def test_swap_high_low():
	actual_high = 2
	actual_low = 1
	m1 = DotRangeMeasurement(actual_high, actual_low, 100, 1000)
	m2 = DotRangeMeasurement(actual_low, actual_high, 100, 1000)

	numpy.testing.assert_array_equal([m1.v_low, m1.v_high], [actual_low, actual_high], err_msg="Highs were wrong with swap")
	numpy.testing.assert_array_equal([m2.v_low, m2.v_high], [actual_low, actual_high], err_msg="Highs were wrong without swap")


def test_swap_high_low_negative():
	actual_high = -1
	actual_low = -2
	m1 = DotRangeMeasurement(actual_high, actual_low, 100, 1000)
	m2 = DotRangeMeasurement(actual_low, actual_high, 100, 1000)

	numpy.testing.assert_array_equal([m1.v_low, m1.v_high], [actual_low, actual_high], err_msg="Highs were wrong with swap, negative")
	numpy.testing.assert_array_equal([m2.v_low, m2.v_high], [actual_low, actual_high], err_msg="Highs were wrong without swap, negative")


def test_swap_high_low_pair():
	actual_high = 2
	actual_low = 1
	m1 = DotPairRangeMeasurement(actual_high, actual_low, 100, 1000, 10000)
	m2 = DotPairRangeMeasurement(actual_low, actual_high, 100, 1000, 10000)

	numpy.testing.assert_array_equal([m1.v_low, m1.v_high], [actual_low, actual_high], err_msg="Highs were wrong with swap")
	numpy.testing.assert_array_equal([m2.v_low, m2.v_high], [actual_low, actual_high], err_msg="Highs were wrong without swap")


def test_swap_high_low_pair_negative():
	actual_high = -1
	actual_low = -2
	m1 = DotPairRangeMeasurement(actual_high, actual_low, 100, 1000, 10000)
	m2 = DotPairRangeMeasurement(actual_low, actual_high, 100, 1000, 10000)

	numpy.testing.assert_array_equal([m1.v_low, m1.v_high], [actual_low, actual_high], err_msg="Highs were wrong with swap, negative")
	numpy.testing.assert_array_equal([m2.v_low, m2.v_high], [actual_low, actual_high], err_msg="Highs were wrong without swap, negative")

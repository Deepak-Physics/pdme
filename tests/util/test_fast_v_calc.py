import numpy
import pdme.util.fast_v_calc


def test_fast_v_calc():
	d1 = [1, 2, 3, 4, 5, 6, 7]
	d2 = [2, 5, 3, 4, -5, -6, 2]

	dipoles = numpy.array([d1, d2])

	dot_inputs = numpy.array([[-1, -1, -1, 11], [2, 3, 1, 5.5]])
	# expected_ij is for dot i, dipole j
	expected_11 = 0.00001421963287022476
	expected_12 = 0.00001107180225755457
	expected_21 = 0.000345021108583681380388722
	expected_22 = 0.0000377061050587914705139781

	expected = numpy.array([[expected_11, expected_21], [expected_12, expected_22]])

	numpy.testing.assert_allclose(pdme.util.fast_v_calc.fast_vs_for_dipoles(dot_inputs, dipoles), expected, err_msg="Voltages at dot aren't as expected.")


def test_between():
	low = numpy.array([1, 2, 3])
	high = numpy.array([6, 7, 8])

	#      FALSE        FALSE       TRUE
	a = [[0, 1, 2], [0, 9, 5], [4, 5, 6]]

	actual = pdme.util.fast_v_calc.between(a, low, high)
	expected = numpy.array([False, False, True])

	numpy.testing.assert_array_equal(actual, expected, err_msg="Between calc wrong")

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

	numpy.testing.assert_allclose(
		pdme.util.fast_v_calc.fast_vs_for_dipoles(dot_inputs, dipoles),
		expected,
		err_msg="Voltages at dot aren't as expected.",
	)


def test_fast_v_calc_multidipoles():
	d1 = [1, 2, 3, 4, 5, 6, 7]
	d2 = [2, 5, 3, 4, -5, -6, 2]

	dipoles = numpy.array([[d1, d2]])

	dot_inputs = numpy.array([[-1, -1, -1, 11], [2, 3, 1, 5.5]])
	# expected_ij is for dot i, dipole j
	expected_11 = 0.00001421963287022476
	expected_12 = 0.00001107180225755457
	expected_21 = 0.000345021108583681380388722
	expected_22 = 0.0000377061050587914705139781

	expected = numpy.array([[expected_11 + expected_12, expected_21 + expected_22]])

	numpy.testing.assert_allclose(
		pdme.util.fast_v_calc.fast_vs_for_dipoleses(dot_inputs, dipoles),
		expected,
		err_msg="Voltages at dot aren't as expected for multidipole calc.",
	)


def test_fast_v_calc_big_multidipole():

	dipoles = numpy.array(
		[
			[
				[1, 1, 5, 6, 3, 1, 1],
				[5, 3, 2, 13, 1, 1, 2],
				[-5, -5, -3, -1, -3, 8, 3],
			],
			[
				[-3, -1, -2, -2, -6, 3, 4],
				[8, 0, 2, 0, 1, 5, 5],
				[1, 4, -4, -1, -3, -5, 6],
			],
		]
	)

	dot_inputs = numpy.array(
		[
			[1, 1, 0, 1],
			[2, 5, 6, 2],
			[3, 1, 3, 3],
			[0.5, 0.5, 0.5, 4],
		]
	)

	expected = numpy.array(
		[
			[
				0.0010151687742365581690202135,
				0.00077627527320628609782627266,
				0.00043313471258511003340648713,
				0.000077184305988088453637005111,
			],
			[
				0.000041099091967966890657097060,
				0.0019377687238977568792327845,
				0.0085903193415282984161225029,
				0.00014557676715208209310911838,
			],
		]
	)

	numpy.testing.assert_allclose(
		pdme.util.fast_v_calc.fast_vs_for_dipoleses(dot_inputs, dipoles),
		expected,
		err_msg="Voltages at dot aren't as expected for multidipole calc.",
	)


def test_between():
	low = numpy.array([1, 2, 3])
	high = numpy.array([6, 7, 8])

	# 	  FALSE		FALSE	   TRUE
	a = [[0, 1, 2], [0, 9, 5], [4, 5, 6]]

	actual = pdme.util.fast_v_calc.between(a, low, high)
	expected = numpy.array([False, False, True])

	numpy.testing.assert_array_equal(actual, expected, err_msg="Between calc wrong")


def test_fast_v_calc_asymmetric_multidipoles_but_symmetric():
	# expected format is [px, py, pz, sx, sy, sz, e1, e2, w]
	d1 = [1, 2, 3, 4, 5, 6, 1, 1, 7 / 2]
	d2 = [2, 5, 3, 4, -5, -6, 2, 2, 2 / 2]

	dipoles = numpy.array([[d1, d2]])

	dot_inputs = numpy.array([[-1, -1, -1, 11], [2, 3, 1, 5.5]])
	# expected_ij is for dot i, dipole j
	expected_11 = 0.00001421963287022476
	expected_12 = 0.00001107180225755457
	expected_21 = 0.000345021108583681380388722
	expected_22 = 0.0000377061050587914705139781

	expected = numpy.array([[expected_11 + expected_12, expected_21 + expected_22]])

	numpy.testing.assert_allclose(
		pdme.util.fast_v_calc.fast_vs_for_asymmetric_dipoleses(
			dot_inputs, dipoles, 1e10
		),
		expected,
		err_msg="Voltages at dot aren't as expected for multidipole calc.",
	)


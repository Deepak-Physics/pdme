import numpy
import pdme.util.fast_v_calc

import pdme.measurement


def dipole_from_array(arr: numpy.ndarray) -> pdme.measurement.OscillatingDipole:
	return pdme.measurement.OscillatingDipole(arr[0:3], arr[3:6], arr[6])


def s_potential_from_arrays(
	dipole_array: numpy.ndarray, dotf_array: numpy.ndarray
) -> float:
	dipole = dipole_from_array(dipole_array)
	r = dotf_array[0:3]
	f = dotf_array[3]
	return dipole.s_electric_potential_at_position(r, f)


def test_fast_v_calc():
	d1 = [1, 2, 3, 4, 5, 6, 7]
	d2 = [2, 5, 3, 4, -5, -6, 2]

	dipoles = numpy.array([d1, d2])

	dot_inputs = numpy.array([[-1, -1, -1, 11], [2, 3, 1, 5.5]])

	expected_11 = s_potential_from_arrays(dipoles[0], dot_inputs[0])
	expected_12 = s_potential_from_arrays(dipoles[1], dot_inputs[0])
	expected_21 = s_potential_from_arrays(dipoles[0], dot_inputs[1])
	expected_22 = s_potential_from_arrays(dipoles[1], dot_inputs[1])

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

	expected_11 = s_potential_from_arrays(dipoles[0][0], dot_inputs[0])
	expected_12 = s_potential_from_arrays(dipoles[0][1], dot_inputs[0])
	expected_21 = s_potential_from_arrays(dipoles[0][0], dot_inputs[1])
	expected_22 = s_potential_from_arrays(dipoles[0][1], dot_inputs[1])

	expected = numpy.array([[expected_11 + expected_12, expected_21 + expected_22]])

	numpy.testing.assert_allclose(
		pdme.util.fast_v_calc.fast_vs_for_dipoleses(dot_inputs, dipoles),
		expected,
		err_msg="Voltages at dot aren't as expected for multidipole calc.",
	)


def test_fast_v_calc_big_multidipole():

	dipoleses = numpy.array(
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

	expected = [
		[
			sum(
				[
					s_potential_from_arrays(dipole_array, dot_input)
					for dipole_array in dipole_config
				]
			)
			for dot_input in dot_inputs
		]
		for dipole_config in dipoleses
	]

	numpy.testing.assert_allclose(
		pdme.util.fast_v_calc.fast_vs_for_dipoleses(dot_inputs, dipoleses),
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

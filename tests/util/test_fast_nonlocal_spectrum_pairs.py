import numpy
import pdme.util.fast_nonlocal_spectrum
import pdme.measurement
import logging
import pytest

_logger = logging.getLogger(__name__)


def dipole_from_array(arr: numpy.ndarray) -> pdme.measurement.OscillatingDipole:
	return pdme.measurement.OscillatingDipole(arr[0:3], arr[3:6], arr[6])


def s_potential_from_arrays(
	dipole_array: numpy.ndarray, dotf_pair_array: numpy.ndarray
) -> float:
	dipole = dipole_from_array(dipole_array)
	r1 = dotf_pair_array[0][0:3]
	f1 = dotf_pair_array[0][3]
	r2 = dotf_pair_array[1][0:3]
	return dipole.s_electric_potential_for_dot_pair(r1, r2, f1)


def test_fast_nonlocal_calc_multidipole():
	d1 = [1, 2, 3, 4, 5, 6, 7]
	d2 = [1, 2, 3, 4, 5, 6, 8]
	d3 = [2, 5, 3, 4, -5, -6, 2]
	d4 = [-3, 2, 1, 4, 5, 6, 10]

	dipoleses = numpy.array([[d1, d2], [d3, d4]])

	dot_pairs = numpy.array(
		[[[-1, -2, -3, 11], [-1, 2, 5, 11]], [[-1, -2, -3, 6], [2, 4, 6, 6]]]
	)
	# expected_ij is for pair i, dipole j

	expected = numpy.array(
		[
			[
				sum(
					[
						s_potential_from_arrays(dipole_array, dot_pair)
						for dipole_array in dipoles
					]
				)
				for dot_pair in dot_pairs
			]
			for dipoles in dipoleses
		]
	)

	# this is a bit silly but just set the logger to debug so that the coverage stats don't get affected by the debug statements.
	pdme.util.fast_nonlocal_spectrum._logger.setLevel(logging.DEBUG)

	numpy.testing.assert_allclose(
		pdme.util.fast_nonlocal_spectrum.fast_s_nonlocal_dipoleses(
			dot_pairs, dipoleses
		),
		expected,
		err_msg="nonlocal voltages at dot aren't as expected for dipoleses.",
	)


def test_fast_nonlocal_frequency_check_multidipole():
	d1 = [1, 2, 3, 4, 5, 6, 7]

	dipoles = numpy.array([[d1]])

	dot_pairs = numpy.array([[[-1, -2, -3, 11], [-1, 2, 5, 10]]])

	with pytest.raises(ValueError):
		pdme.util.fast_nonlocal_spectrum.fast_s_nonlocal_dipoleses(dot_pairs, dipoles)


def test_fast_nonlocal_calc_multidipole_phase_snapshot(snapshot):
	d1 = [1, 2, 3, 4, 5, 6, 7]
	d2 = [1, 2, 3, 4, 5, 6, 8]
	d3 = [2, 5, 3, 4, -5, -6, 2]
	d4 = [-3, 2, 1, 4, 5, 6, 10]

	dipoleses = numpy.array([[d1, d2], [d3, d4]])

	dot_pairs = numpy.array(
		[[[-1, -2, -3, 11], [-1, 2, 5, 11]], [[-1, -2, -3, 6], [2, 4, 6, 6]]]
	)

	# this is a bit silly but just set the logger to debug so that the coverage stats don't get affected by the debug statements.
	pdme.util.fast_nonlocal_spectrum._logger.setLevel(logging.DEBUG)

	actual_phases = pdme.util.fast_nonlocal_spectrum.signarg(
		pdme.util.fast_nonlocal_spectrum.fast_s_nonlocal_dipoleses(dot_pairs, dipoleses)
	)
	assert actual_phases.tolist() == snapshot


def test_fast_spin_qubit_frequency_tarucha_calc(snapshot):
	d1 = [1, 2, 3, 0, 0, 0, 5]
	d2 = [6, 7, 8, 5, 4, 3, 8]
	dipoleses = numpy.array([[d1], [d2]])

	dot_pairs = numpy.array(
		[[[1, 0, 0, 1], [1, 0, 0, 1]], [[1, 0, 0, 1], [3, 0, 0, 1]]]
	)

	actual = (
		pdme.util.fast_nonlocal_spectrum.fast_s_spin_qubit_tarucha_nonlocal_dipoleses(
			dot_pairs, dipoleses
		)
	)

	pdme.util.fast_nonlocal_spectrum._logger.setLevel(logging.DEBUG)
	_logger.info(actual)
	assert actual.tolist() == snapshot

import numpy
import pdme.util.fast_nonlocal_spectrum
import logging
import pytest

_logger = logging.getLogger(__name__)


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
	expected_11 = 0.000021124454334947546213
	expected_12 = 0.000022184755131682365135
	expected_13 = 0.0000053860643617855849275
	expected_14 = -0.0000023069501696755220764
	expected_21 = 0.00022356021100884617796
	expected_22 = 0.00021717277640859343002
	expected_23 = 0.000017558321044891869169
	expected_24 = -0.000034714318479634499683

	expected = numpy.array(
		[
			[expected_11 + expected_12, expected_21 + expected_22],
			[expected_13 + expected_14, expected_23 + expected_24],
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

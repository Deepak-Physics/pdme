from pdme.model import SingleDipoleFixedMagnitudeModel
import numpy
import logging


_logger = logging.getLogger(__name__)


def test_single_dipole_fixed_mag_model_get_dipoles():

	p_fixed = 10

	model = SingleDipoleFixedMagnitudeModel(-10, 10, -5, 5, 2, 3, p_fixed)

	dipole_arrangement = model.get_dipoles(5, numpy.random.default_rng(1234))
	dipoles = dipole_arrangement.dipoles

	assert len(dipoles) == 1, "Should have only had one dipole generated."
	expected_p = numpy.array([-2.20191453, 2.06264523, 9.5339953])
	expected_s = numpy.array([8.46492468, -2.38307576, 2.31909706])
	expected_w = 0.5904561648332141

	_logger.error(dipoles[0].p)
	_logger.error(dipoles[0].s)
	_logger.error(dipoles[0].w)
	numpy.testing.assert_allclose(
		dipoles[0].p, expected_p, err_msg="Random single dipole p wasn't as expected"
	)
	numpy.testing.assert_allclose(
		dipoles[0].s, expected_s, err_msg="Random single dipole s wasn't as expected"
	)
	numpy.testing.assert_allclose(
		dipoles[0].w, expected_w, err_msg="Random single dipole w wasn't as expected"
	)
	numpy.testing.assert_allclose(
		numpy.linalg.norm(dipoles[0].p),
		p_fixed,
		err_msg="Should have had the expected dipole moment magnitude.",
	)

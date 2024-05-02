import pdme.calculations
import pytest
import numpy
import numpy.testing


# generated in mathematica to compare here
beta_test_data = [
	[-2, -2, 0.8072976151],
	[-1, -2, 0.008105366193],
	[0, -2, 0.00008105691406],
	[1, -2, 8.105694659e-7],
	[2, -2, 8.105694691e-9],
	[-2, -1, 5.768008783],
	[-1, -1, 0.08072976151],
	[0, -1, 0.0008105366193],
	[1, -1, 8.105691406e-6],
	[2, -1, 8.105694659e-8],
	[-2, 0, 1.951840272],
	[-1, 0, 0.5768008783],
	[0, 0, 0.008072976151],
	[1, 0, 0.00008105366193],
	[2, 0, 8.105691406e-7],
	[-2, 1, 0.1999506642],
	[-1, 1, 0.1951840272],
	[0, 1, 0.05768008783],
	[1, 1, 0.0008072976151],
	[2, 1, 8.105366193e-6],
	[-2, 2, 0.01999995065],
	[-1, 2, 0.01999506642],
	[0, 2, 0.01951840272],
	[1, 2, 0.005768008783],
	[2, 2, 0.00008072976151],
]


@pytest.mark.parametrize("f, w, expected", beta_test_data)
def test_calculations_beta_func(f, w, expected):
	# there's nothing special about the 5 * 10^ f and 10^w passing in logs
	# this was just to get a variety of orders of magnitude in results.
	actual = pdme.calculations.telegraph_beta(5 * 10**f, 10**w)
	numpy.testing.assert_allclose(actual, expected, atol=0, rtol=1e-8)


def test_multiple_electric_potential_alphas(snapshot):
	"""
	Manually compare these with mathematica stuff because manually including a list is a bit annoying.
	Basically just visually compare the snapshot values to make sure they're actually correct.
	"""
	dipole_ps = [
		numpy.array([1, 2, 3]),
		numpy.array([-4, -3, -2]),
	]
	dipole_ss = [
		numpy.array([0, 0, 1]),
		numpy.array([1, 1, 1]),
		numpy.array([0, -0.5, 0.5]),
	]

	test_rs = [
		numpy.array([5, 5, 5]),
		numpy.array([-4, -6, 2]),
	]

	actuals = [
		pdme.calculations.electric_potential(p, s, r)
		for p in dipole_ps
		for s in dipole_ss
		for r in test_rs
	]

	assert actuals == snapshot


def test_multiple_electric_field_alphas(snapshot):
	"""
	Manually compare these with mathematica stuff because manually including a list is a bit annoying.
	Basically just visually compare the snapshot values to make sure they're actually correct.
	"""
	dipole_ps = [
		numpy.array([1, 2, 3]),
		numpy.array([-4, -3, -2]),
	]
	dipole_ss = [
		numpy.array([0, 0, 1]),
		numpy.array([1, 1, 1]),
		numpy.array([0, -0.5, 0.5]),
	]

	test_rs = [
		numpy.array([5, 5, 5]),
		numpy.array([-4, -6, 2]),
	]

	actuals = [
		pdme.calculations.electric_field(p, s, r).tolist()
		for p in dipole_ps
		for s in dipole_ss
		for r in test_rs
	]

	assert actuals == snapshot

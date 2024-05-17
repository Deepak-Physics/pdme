import pdme.subspace_simulation
import pdme.subspace_simulation.mcmc_costs
import numpy


def test_proportional_costs(snapshot):
	a = numpy.array([2, 4, 5, 6, 7, 8, 10])
	b = numpy.array([51, 13, 1, 31, 0.001, 3, 1])

	actual_result = pdme.subspace_simulation.proportional_cost(a, b).tolist()
	assert actual_result == snapshot


def test_squared_costs_manual():
	target = numpy.array([100, 400, 900])
	approx1 = numpy.array([0, 400, 800])
	approx2 = numpy.array([200, 400, 600])

	expected1 = 1.0123456790123457
	expected2 = 1.1111111111111111

	actual1 = pdme.subspace_simulation.mcmc_costs.relative_square_diffs(approx1, target)
	assert actual1 == expected1

	actual2 = pdme.subspace_simulation.mcmc_costs.relative_square_diffs(approx2, target)
	assert actual2 == expected2

	combined_actual = pdme.subspace_simulation.mcmc_costs.relative_square_diffs(
		numpy.array([approx1, approx2]), target
	)
	numpy.testing.assert_allclose(combined_actual, [expected1, expected2], rtol=1e-14)

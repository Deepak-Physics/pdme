import pdme.subspace_simulation
import numpy


def test_proportional_costs(snapshot):
	a = numpy.array([2, 4, 5, 6, 7, 8, 10])
	b = numpy.array([51, 13, 1, 31, 0.001, 3, 1])

	actual_result = pdme.subspace_simulation.proportional_cost(a, b).tolist()
	assert actual_result == snapshot

import numpy
import pdme.subspace_simulation


def test_sort_dipoles_by_freq(snapshot):
	orig = numpy.array(
		[
			[1, 2, 3, 4, 5, 6, 7],
			[100, 200, 300, 400, 500, 600, 0.07],
			[10, 200, 30, 41, 315, 0.31, 100],
		]
	)

	actual_sorted = pdme.subspace_simulation.sort_array_of_dipoles_by_frequency(orig)
	assert actual_sorted.tolist() == snapshot

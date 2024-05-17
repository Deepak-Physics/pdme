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


def test_sort_dipoleses_by_freq(snapshot):
	sample_1 = numpy.array(
		[
			[1, 2, 3, 4, 5, 6, 7],
			[100, 200, 300, 400, 500, 600, 0.07],
			[10, 200, 30, 41, 315, 0.31, 100],
		]
	)

	sample_2 = numpy.array(
		[
			[1, 1, 1, 1, 1, 1, 100],
			[33, 33.3, 33, 3.3, 0.33, 0.3, 300],
			[22, 22.2, 2.2, 222, 22, 2, 200],
		]
	)

	original_samples = numpy.array([sample_1, sample_2])

	actual_sorted = pdme.subspace_simulation.sort_array_of_dipoleses_by_frequency(
		original_samples
	)
	assert actual_sorted.tolist() == snapshot

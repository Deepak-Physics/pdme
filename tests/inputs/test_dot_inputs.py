import pdme.inputs


def test_inputs_with_frequency_range():
	dot1 = [1, 2, 3]
	dot2 = [2, 4, 6]

	frequencies = [5, 7, 9]

	expected = [
		([1, 2, 3], 5),
		([1, 2, 3], 7),
		([1, 2, 3], 9),
		([2, 4, 6], 7),
		([2, 4, 6], 9),
		([2, 4, 6], 5),
	]

	actual = pdme.inputs.inputs_with_frequency_range([dot1, dot2], frequencies)

	assert sorted(actual) == sorted(expected), "Did not actually match dot inputs!"


def test_input_pairs_with_frequency_range():
	dot1 = [1, 2, 3]
	dot2 = [2, 4, 6]

	frequencies = [5, 7, 9]

	expected = [
		([1, 2, 3], [2, 4, 6], 5),
		([1, 2, 3], [2, 4, 6], 7),
		([1, 2, 3], [2, 4, 6], 9),
	]

	actual = pdme.inputs.input_pairs_with_frequency_range([dot1, dot2], frequencies)

	assert sorted(actual) == sorted(expected), "Did not actually match dot inputs!"

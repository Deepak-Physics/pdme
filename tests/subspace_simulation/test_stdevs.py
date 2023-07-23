import pytest
import pdme.subspace_simulation


def test_empty():
	with pytest.raises(ValueError):
		pdme.subspace_simulation.MCMCStandardDeviation([])


def test_return_one(snapshot):
	stdev = pdme.subspace_simulation.DipoleStandardDeviation(
		1,
		2,
		3,
		4,
		5,
		6,
	)
	stdevs = pdme.subspace_simulation.MCMCStandardDeviation([stdev])

	assert stdevs[3] == snapshot
	assert stdevs[3] == stdev


def test_return_four(snapshot):
	stdev_list = [
		pdme.subspace_simulation.DipoleStandardDeviation(1, 2, 3, 4, 5, 6),
		pdme.subspace_simulation.DipoleStandardDeviation(10, 20, 30, 40, 50, 60),
		pdme.subspace_simulation.DipoleStandardDeviation(0.1, 0.2, 0.3, 0.4, 0.5, 0.6),
	]
	stdevs = pdme.subspace_simulation.MCMCStandardDeviation(stdev_list)

	assert stdevs[0] == snapshot
	assert stdevs[1] == snapshot
	assert stdevs[2] == snapshot
	assert stdevs[3] == snapshot
	assert stdevs[4] == snapshot
	assert stdevs[5] == snapshot

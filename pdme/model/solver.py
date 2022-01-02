import numpy
import scipy.optimize


def sol(self, initial_dipole=(0.1, 0.1, 0.1), initial_position=(.1, .1, .1), initial_frequency=1, use_root=True):
	initial = numpy.tile(numpy.concatenate((initial_dipole, initial_position, initial_frequency), axis=None), self.n)

	result = scipy.optimize.least_squares(self.costs(), initial, jac=self.jac(), ftol=1e-15, gtol=3e-16)
	return result

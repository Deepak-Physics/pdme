import numpy
import scipy.optimize
from pdme.model import Model
from pdme.measurement import DotMeasurement
from typing import Sequence


def sol(model: Model, dots: Sequence[DotMeasurement], initial_pt=None, bounds=(-numpy.inf, numpy.inf)):
	if initial_pt is None:
		initial = numpy.tile(.1, model.n() * model.point_length())
	else:
		if len(initial_pt) != model.point_length():
			raise ValueError(f"The initial point {initial_pt} does not have the model's expected length: {model.point_length()}")
		initial = numpy.tile(initial_pt, model.n())

	result = scipy.optimize.least_squares(model.costs(dots), initial, jac=model.jac(dots), ftol=1e-15, gtol=3e-16, bounds=bounds)
	return result

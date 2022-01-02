import numpy
from typing import Callable, Sequence
from pdme.measurement import DotMeasurement
import logging


class Model():
	"""
	Interface for models.
	"""

	def point_length(self) -> int:
		raise NotImplementedError

	def v_for_point_at_dot(self, dot: DotMeasurement, pt: numpy.ndarray) -> float:
		raise NotImplementedError

	def cost_for_dot(self, dot: DotMeasurement, pts: numpy.ndarray) -> float:
		# creates numpy.ndarrays in groups of self.point_length().
		# Will throw problems for irregular points, but that's okay for now.
		pt_length = self.point_length()
		chunked_pts = [pts[i: i + pt_length] for i in range(0, len(pts), pt_length)]
		return sum(self.v_for_point_at_dot(dot, pt) for pt in chunked_pts) - dot.v

	def costs(self, dots: Sequence[DotMeasurement]) -> Callable[[numpy.ndarray], numpy.ndarray]:
		'''
		Returns a function that returns the cost for the given list of DotMeasurements for a particular model-dependent phase space point.
		Default implementation assumes a single dot cost from which to build the list.

		Parameters
		----------
		dots: A list of dot measurements to use to find the cost functions.

		Returns
		----------
		Returns the model's cost function.
		'''
		logging.debug(f"Constructing costs for dots: {dots}")

		def costs_to_return(pts: numpy.ndarray) -> numpy.ndarray:
			return numpy.array([self.cost_for_dot(dot, pts) for dot in dots])

		return costs_to_return

	def jac_for_point_at_dot(self, dot: DotMeasurement, pt: numpy.ndarray) -> numpy.ndarray:
		raise NotImplementedError

	def jac_for_dot(self, dot: DotMeasurement, pts: numpy.ndarray) -> numpy.ndarray:
		# creates numpy.ndarrays in groups of self.point_length().
		# Will throw problems for irregular points, but that's okay for now.
		pt_length = self.point_length()
		chunked_pts = [pts[i: i + pt_length] for i in range(0, len(pts), pt_length)]
		return numpy.append([], [self.jac_for_point_at_dot(dot, pt) for pt in chunked_pts])

	def jac(self, dots: Sequence[DotMeasurement]) -> Callable[[numpy.ndarray], numpy.ndarray]:
		'''
		Returns a function that returns the cost function's Jacobian for the given list of DotMeasurements for a particular model-dependent phase space point.
		Default implementation assumes a single dot jacobian from which to build the list.

		Parameters
		----------
		dots: A list of dot measurements to use to find the cost functions and their Jacobian.

		Returns
		----------
		Returns the model's cost function's Jacobian.
		'''
		def jac_to_return(pts: numpy.ndarray) -> numpy.ndarray:
			return numpy.array([self.jac_for_dot(dot, pts) for dot in dots])

		return jac_to_return

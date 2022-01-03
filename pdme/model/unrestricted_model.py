import numpy
from dataclasses import dataclass
from typing import Sequence, Tuple
import scipy.optimize
from pdme.model.model import Model
from pdme.measurement import DotMeasurement


class UnrestrictedModel(Model):
	'''
	Model of oscillating dipoles with no restrictions.
	Additionally, each dipole is assumed to be orientated in the plus or minus z direction.

	Parameters
	----------
	n : int
		The number of dipoles to assume.
	'''
	def __init__(self, xmin: float, xmax: float, ymin: float, ymax: float, zmin: float, zmax: float, n: int) -> None:
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.zmin = zmin
		self.zmax = zmax
		self._n = n

	def __repr__(self) -> str:
		return f'UnrestrictedModel({self.xmin}, {self.xmax}, {self.ymin}, {self.ymax}, {self.zmin}, {self.zmax}, {self.n()})'

	def point_length(self) -> int:
		'''
			Dipole is unconstrained in this model.
			All seven degrees of freedom: (px, py, pz, sx, sy, sz, w).
		'''
		return 7

	def n(self) -> int:
		return self._n

	def v_for_point_at_dot(self, dot: DotMeasurement, pt: numpy.ndarray) -> float:
		p = pt[0:3]
		s = pt[3:6]
		w = pt[6]

		diff = dot.r - s
		alpha = p.dot(diff) / (numpy.linalg.norm(diff)**3)
		b = (1 / numpy.pi) * (w / (w**2 + dot.f**2))
		return alpha**2 * b

	def jac_for_point_at_dot(self, dot: DotMeasurement, pt: numpy.ndarray) -> numpy.ndarray:
		p = pt[0:3]
		s = pt[3:6]
		w = pt[6]

		diff = dot.r - s
		alpha = p.dot(diff) / (numpy.linalg.norm(diff)**3)
		b = (1 / numpy.pi) * (w / (w**2 + dot.f**2))

		p_divs = 2 * alpha * diff / (numpy.linalg.norm(diff)**3) * b

		r_divs = (-p / (numpy.linalg.norm(diff)**3) + 3 * p.dot(diff) * diff / (numpy.linalg.norm(diff)**5)) * 2 * alpha * b

		f2 = dot.f**2
		w2 = w**2

		w_div = alpha**2 * (1 / numpy.pi) * ((f2 - w2) / ((f2 + w2)**2))

		return numpy.concatenate((p_divs, r_divs, w_div), axis=None)


@dataclass
class UnrestrictedDiscretisation():
	'''
	Representation of a discretisation of a UnrestrictedModel.
	Also captures a rough maximum value of dipole.

	Parameters
	----------
	model : UnrestrictedModel
		The parent model of the discretisation.
	num_x : int
		The number of partitions of the x axis.
	num_y : int
		The number of partitions of the y axis.
	num_z : int
		The number of partitions of the z axis.
	max_p : int
		The maximum p coordinate in any direction.
	'''
	model: UnrestrictedModel
	num_x: int
	num_y: int
	num_z: int
	max_p: int

	def __post_init__(self):
		self.cell_count = self.num_x * self.num_y * self.num_z
		self.x_step = (self.model.xmax - self.model.xmin) / self.num_x
		self.y_step = (self.model.ymax - self.model.ymin) / self.num_y
		self.z_step = (self.model.zmax - self.model.zmin) / self.num_z

	def bounds(self, index: Tuple[float, float, float]) -> Tuple:
		xi, yi, zi = index

		# For this model, a point is (px, py, pz, sx, sx, sy, w).
		# We want to keep w unbounded, restrict sx, sy, sz based on step and all of p generally.
		return (
			[
				-self.max_p, -self.max_p, -self.max_p,
				xi * self.x_step + self.model.xmin, yi * self.y_step + self.model.ymin, zi * self.z_step + self.model.zmin,
				-numpy.inf
			],
			[
				self.max_p, self.max_p, self.max_p,
				(xi + 1) * self.x_step + self.model.xmin, (yi + 1) * self.y_step + self.model.ymin, (zi + 1) * self.z_step + self.model.zmin,
				numpy.inf
			]
		)

	def all_indices(self) -> numpy.ndindex:
		# see https://github.com/numpy/numpy/issues/20706 for why this is a mypy problem.
		return numpy.ndindex((self.num_x, self.num_y, self.num_z))  # type:ignore

	def solve_for_index(self, dots: Sequence[DotMeasurement], index: Tuple[float, float, float]) -> scipy.optimize.OptimizeResult:
		bounds = self.bounds(index)
		sx_mean = (bounds[0][3] + bounds[1][3]) / 2
		sy_mean = (bounds[0][4] + bounds[1][4]) / 2
		sz_mean = (bounds[0][5] + bounds[1][5]) / 2
		return self.model.solve(dots, initial_pt=numpy.array([.1, .1, .1, sx_mean, sy_mean, sz_mean, .1]), bounds=bounds)

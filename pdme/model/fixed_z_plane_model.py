import numpy
from pdme.model import Model
from pdme.measurement import DotMeasurement


class FixedZPlaneModel(Model):
	'''
	Model of oscillating dipoles constrained to lie within a plane.
	Additionally, each dipole is assumed to be orientated in the plus or minus z direction.

	Parameters
	----------
	z : float
		The z position of the plane where dipoles are constrained to lie.
	xmin : float
		The minimum x value for dipoles.
	xmax : float
		The maximum x value for dipoles.
	ymin : float
		The minimum y value for dipoles.
	ymax : float
		The maximum y value for dipoles.
	n : int
		The number of dipoles to assume.
	'''
	def __init__(self, z: float, xmin: float, xmax: float, ymin: float, ymax: float, n: int) -> None:
		self.z = z
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.n = n

	def __repr__(self) -> str:
		return f'FixedZPlaneModel({self.z}, {self.xmin}, {self.xmax}, {self.ymin}, {self.ymax}, {self.n})'

	def point_length(self) -> int:
		'''
			Dipole is constrained in this model to have (px, py, pz) = (0, 0, pz) and (sx, sy, sz) = (sx, sy, self.z).
			With some frequency w, there are four degrees of freedom: (pz, sx, sy, w).
		'''
		return 4

	def v_for_point_at_dot(self, dot: DotMeasurement, pt: numpy.ndarray) -> float:
		p = numpy.array([0, 0, pt[0]])
		s = numpy.array([pt[1], pt[2], self.z])
		w = pt[3]

		diff = dot.r - s
		alpha = p.dot(diff) / (numpy.linalg.norm(diff)**3)
		b = (1 / numpy.pi) * (w / (w**2 + dot.f**2))
		return alpha**2 * b

	def jac_for_point_at_dot(self, dot: DotMeasurement, pt: numpy.ndarray) -> numpy.ndarray:
		p = numpy.array([0, 0, pt[0]])
		s = numpy.array([pt[1], pt[2], self.z])
		w = pt[3]

		diff = dot.r - s
		alpha = p.dot(diff) / (numpy.linalg.norm(diff)**3)
		b = (1 / numpy.pi) * (w / (w**2 + dot.f**2))

		p_divs = 2 * alpha * diff[2] / (numpy.linalg.norm(diff)**3) * b  # only need the z component.

		r_divs = (-p[0:2] / (numpy.linalg.norm(diff)**3) + 3 * p.dot(diff) * diff[0:2] / (numpy.linalg.norm(diff)**5)) * 2 * alpha * b

		f2 = dot.f**2
		w2 = w**2

		w_div = alpha**2 * (1 / numpy.pi) * ((f2 - w2) / ((f2 + w2)**2))

		return numpy.concatenate((p_divs, r_divs, w_div), axis=None)

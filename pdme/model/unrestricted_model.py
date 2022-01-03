import numpy
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
	def __init__(self, n: int) -> None:
		self._n = n

	def __repr__(self) -> str:
		return f'UnrestrictedModel({self.n()})'

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

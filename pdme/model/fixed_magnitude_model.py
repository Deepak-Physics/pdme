import numpy
import numpy.random
from pdme.model.model import Model
from pdme.measurement import (
	DotMeasurement,
	OscillatingDipole,
	OscillatingDipoleArrangement,
)


class FixedMagnitudeModel(Model):
	"""
	Model of oscillating dipole with a fixed magnitude, but free rotation.

	Parameters
	----------
	pfixed : float
	The fixed dipole magnitude.

	n : int
	The number of dipoles to assume.
	"""

	def __init__(
		self,
		xmin: float,
		xmax: float,
		ymin: float,
		ymax: float,
		zmin: float,
		zmax: float,
		pfixed: float,
		n: int,
	) -> None:
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.zmin = zmin
		self.zmax = zmax
		self.pfixed = pfixed
		self._n = n
		self.rng = numpy.random.default_rng()

	def __repr__(self) -> str:
		return f"FixedMagnitudeModel({self.xmin}, {self.xmax}, {self.ymin}, {self.ymax}, {self.zmin}, {self.zmax}, {self.pfixed}, {self.n()})"

	def solution_single_dipole(self, pt: numpy.ndarray) -> OscillatingDipole:
		# assume length is 6, who needs error checking.
		p_theta = pt[0]
		p_phi = pt[1]
		s = pt[2:5]
		w = pt[5]

		p = numpy.array(
			[
				self.pfixed * numpy.sin(p_theta) * numpy.cos(p_phi),
				self.pfixed * numpy.sin(p_theta) * numpy.sin(p_phi),
				self.pfixed * numpy.cos(p_theta),
			]
		)
		return OscillatingDipole(p, s, w)

	def point_length(self) -> int:
		"""
		Dipole is constrained magnitude, but free orientation.
		Six degrees of freedom: (p_theta, p_phi, sx, sy, sz, w).
		"""
		return 6

	def get_dipoles(self, frequency: float) -> OscillatingDipoleArrangement:
		theta = numpy.arccos(self.rng.uniform(-1, 1))
		phi = self.rng.uniform(0, 2 * numpy.pi)
		px = self.pfixed * numpy.sin(theta) * numpy.cos(phi)
		py = self.pfixed * numpy.sin(theta) * numpy.sin(phi)
		pz = self.pfixed * numpy.cos(theta)
		s_pts = numpy.array(
			(
				self.rng.uniform(self.xmin, self.xmax),
				self.rng.uniform(self.ymin, self.ymax),
				self.rng.uniform(self.zmin, self.zmax),
			)
		)
		return OscillatingDipoleArrangement(
			[OscillatingDipole(numpy.array([px, py, pz]), s_pts, frequency)]
		)

	def get_n_single_dipoles(
		self, n: int, max_frequency: float, rng_to_use: numpy.random.Generator = None
	) -> numpy.ndarray:
		# psw

		rng: numpy.random.Generator
		if rng_to_use is None:
			rng = self.rng
		else:
			rng = rng_to_use

		theta = 2 * numpy.pi * rng.random(n)
		phi = numpy.arccos(2 * rng.random(n) - 1)
		px = self.pfixed * numpy.cos(theta) * numpy.sin(phi)
		py = self.pfixed * numpy.sin(theta) * numpy.sin(phi)
		pz = self.pfixed * numpy.cos(phi)

		sx = rng.uniform(self.xmin, self.xmax, n)
		sy = rng.uniform(self.ymin, self.ymax, n)
		sz = rng.uniform(self.zmin, self.zmax, n)

		w = rng.uniform(1, max_frequency, n)

		return numpy.array([px, py, pz, sx, sy, sz, w]).T

	def n(self) -> int:
		return self._n

	def v_for_point_at_dot(self, dot: DotMeasurement, pt: numpy.ndarray) -> float:
		p_theta = pt[0]
		p_phi = pt[1]
		s = pt[2:5]
		w = pt[5]

		p = numpy.array(
			[
				self.pfixed * numpy.sin(p_theta) * numpy.cos(p_phi),
				self.pfixed * numpy.sin(p_theta) * numpy.sin(p_phi),
				self.pfixed * numpy.cos(p_theta),
			]
		)
		diff = dot.r - s
		alpha = p.dot(diff) / (numpy.linalg.norm(diff) ** 3)
		b = (1 / numpy.pi) * (w / (w**2 + dot.f**2))
		return alpha**2 * b

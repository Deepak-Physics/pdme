import numpy
import numpy.random
from pdme.measurement import (
	OscillatingDipoleArrangement,
)
import logging


_logger = logging.getLogger(__name__)


class Model:
	"""
	Interface for models.
	"""

	def get_dipoles(self, frequency: float) -> OscillatingDipoleArrangement:
		raise NotImplementedError

	def get_n_single_dipoles(
		self, n: int, max_frequency: float, rng: numpy.random.Generator = None
	) -> numpy.ndarray:
		raise NotImplementedError

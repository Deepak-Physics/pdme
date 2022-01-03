from pdme.model.fixed_z_plane_model import FixedZPlaneModel, FixedZPlaneDiscretisation
from pdme.measurement import OscillatingDipole, OscillatingDipoleArrangement
import itertools
import logging
import numpy

def main():
	dipoles = OscillatingDipoleArrangement([OscillatingDipole((0, 0, 2), (1, 2, 4), 1)])
	dot_inputs = list(itertools.chain.from_iterable(
		(([1, 2, 0], f), ([1, 1, 0], f), ([2, 1, 0], f), ([2, 2, 0], f)) for f in numpy.arange(1, 10, 2)
	))
	dots = dipoles.get_dot_measurements(dot_inputs)

	model = FixedZPlaneModel(4, -10, 10, -10, 10, 1)
	discretisation = FixedZPlaneDiscretisation(model, 2, 5, 10)
	for index in discretisation.all_indices():
		result = discretisation.solve_for_index(dots, index)
		if result.success and result.cost <= 1e-10:
			answer = result.normalised_x
		else:
			answer = None
		logging.info(f"{index} : {discretisation.bounds(index)}")
		logging.info(f"{index} : {answer}")
		logging.info("\n")

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	main()

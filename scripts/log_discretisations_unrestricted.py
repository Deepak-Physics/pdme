from pdme.model.unrestricted_model import UnrestrictedModel, UnrestrictedDiscretisation
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

	model = UnrestrictedModel(-10, 10, -10, 10, -10, 10, 1)
	discretisation = UnrestrictedDiscretisation(model, 4, 4, 4, 10)
	count = 0
	success = 0
	for index in discretisation.all_indices():
		count += 1
		result = discretisation.solve_for_index(dots, index)
		if result.success and result.cost <= 1e-10:
			answer = result.normalised_x
			success += 1
		else:
			answer = None
		logging.debug(f"{index} : {discretisation.bounds(index)}")
		logging.debug(f"{index} : {answer}\n")
	logging.info(f"Out of {count} cells, {success} were successful")

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	main()

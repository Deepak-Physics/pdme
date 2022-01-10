from pdme.model.unrestricted_model import UnrestrictedModel, UnrestrictedDiscretisation
from pdme.measurement import OscillatingDipole, OscillatingDipoleArrangement
import itertools
import logging
import multiprocessing
import numpy


def get_a_result(discretisation, dots, index):
	return (index, discretisation.solve_for_index(dots, index))

def main():
	dipoles = OscillatingDipoleArrangement([OscillatingDipole((-0.184772459487974, -5.408149759441951, 7.1877726347903454), (-4.629467853322026, -5.4309905972000045, 3.566486068367097), 6)])
	dot_inputs = list(itertools.chain.from_iterable(
		(([1, 2, 0], f), ([1, 1, 0], f), ([2, 1, 0], f), ([2, 2, 0], f)) for f in numpy.arange(1, 10, 2)
	))
	dots = dipoles.get_dot_measurements(dot_inputs)

	model = UnrestrictedModel(-10, 10, -10, 10, 3.5, 4.5, 1)
	discretisation = UnrestrictedDiscretisation(model, 6, 6, 3, 5, 5, 5, 10)
	
	with multiprocessing.Pool(multiprocessing.cpu_count()-1 or 1) as pool:
		results = pool.starmap(get_a_result, zip(itertools.repeat(discretisation), itertools.repeat(dots), discretisation.all_indices()))
	
	count = 0
	success = 0
	for idx, result in results:
		count += 1
		if result.success and result.cost <= 1e-10 and numpy.linalg.norm(result.x[0:3]) < 10:
			answer = result.normalised_x
			success += 1
		else:
			answer = None
		logging.debug(f"{idx} : {discretisation.bounds(idx)}")
		logging.debug(f"{idx} : {answer}\n")
	logging.info(len(results))
	logging.info(f"Out of {count} cells, {success} were successful")

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	main()

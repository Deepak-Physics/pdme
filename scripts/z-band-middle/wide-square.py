from pdme.model.unrestricted_model import UnrestrictedModel, UnrestrictedDiscretisation
from pdme.measurement import OscillatingDipole, OscillatingDipoleArrangement
import itertools
import logging
import multiprocessing
import numpy
import csv
import random


FILENAME = "z-band-middle-all-dots-widesquare-morepts.csv"
csv_fields = ["dipole_mom", "dipole_loc", "dipole_freq", "low_success", "low_count", "medium_success", "medium_count", "high_success", "high_count"]


def get_uniform_sphere():
	r = random.random()**.3333 * 10
	a = random.uniform(-10, 10)
	b = random.uniform(-10, 10)
	c = random.uniform(-10, 10)
	f = (a**2 + b**2 + c**2)**.5
	return (a * r / f, b * r / f, c * r / f)


def get_pt():
	return (get_uniform_sphere(), (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(3.5, 4.5)))


def get_a_result(discretisation, dots, index):
	return (index, discretisation.solve_for_index(dots, index))


def main():
	
	with open(FILENAME, "a", newline="") as outfile:
		# csv fields
		writer = csv.DictWriter(outfile, fieldnames=csv_fields, dialect='unix')
		writer.writeheader()
	
	for run in range(1, 501):
		
		p_pts, s_pts = get_pt()
		dipoles = OscillatingDipoleArrangement([OscillatingDipole(p_pts, s_pts, run)])
		logging.info(f"gonna work on point {(p_pts, s_pts, run)}")
		dot_inputs = list(itertools.chain.from_iterable(
			(([-2, 2, 0], f), ([-2, -2, 0], f), ([2, -2, 0], f), ([2, 2, 0], f)) for f in numpy.arange(1, 10, 2)
		))
		dots = dipoles.get_dot_measurements(dot_inputs)

		model_low = UnrestrictedModel(-10, 10, -10, 10, 2.5, 3.5, 1)
		discretisation_low = UnrestrictedDiscretisation(model_low, 6, 6, 3, 5, 5, 5, 10)

		model_medium = UnrestrictedModel(-10, 10, -10, 10, 3.5, 4.5, 1)
		discretisation_medium = UnrestrictedDiscretisation(model_medium, 6, 6, 3, 5, 5, 5, 10)

		model_high = UnrestrictedModel(-10, 10, -10, 10, 4.5, 5.5, 1)
		discretisation_high = UnrestrictedDiscretisation(model_high, 6, 6, 3, 5, 5, 5, 10)
		
		with multiprocessing.Pool(multiprocessing.cpu_count()-1 or 1) as pool:
			results_low = pool.starmap(get_a_result, zip(itertools.repeat(discretisation_low), itertools.repeat(dots), discretisation_low.all_indices()))

		with multiprocessing.Pool(multiprocessing.cpu_count()-1 or 1) as pool:
			results_medium = pool.starmap(get_a_result, zip(itertools.repeat(discretisation_medium), itertools.repeat(dots), discretisation_medium.all_indices()))

		with multiprocessing.Pool(multiprocessing.cpu_count()-1 or 1) as pool:
			results_high = pool.starmap(get_a_result, zip(itertools.repeat(discretisation_high), itertools.repeat(dots), discretisation_high.all_indices()))
		
		count_low = 0
		success_low = 0
		for idx, result in results_low:
			count_low += 1
			if result.success and result.cost <= 1e-10 and numpy.linalg.norm(result.x[0:3]) < 10:
				answer = result.normalised_x
				success_low += 1
			else:
				answer = None

		count_medium = 0
		success_medium = 0
		for idx, result in results_medium:
			count_medium += 1
			if result.success and result.cost <= 1e-10 and numpy.linalg.norm(result.x[0:3]) < 10:
				answer = result.normalised_x
				success_medium += 1
			else:
				answer = None

		count_high = 0
		success_high = 0
		for idx, result in results_high:
			count_high += 1
			if result.success and result.cost <= 1e-10 and numpy.linalg.norm(result.x[0:3]) < 10:
				answer = result.normalised_x
				success_high += 1
			else:
				answer = None

		logging.info(f"Low   : Out of {count_low} cells, {success_low} were successful")
		logging.info(f"Medium: Out of {count_medium} cells, {success_medium} were successful")
		logging.info(f"High  : Out of {count_high} cells, {success_high} were successful")
		
		with open(FILENAME, "a", newline='') as outfile:
			writer = csv.DictWriter(outfile, fieldnames=csv_fields, dialect='unix')
			writer.writerow({
				"dipole_mom": p_pts,
				"dipole_loc": s_pts,
				"dipole_freq": run,
				"low_success": success_low,
				"high_success": success_high,
				"medium_success": success_medium,
				"low_count": count_low,
				"medium_count": count_medium,
				"high_count": count_high
			})

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	main()

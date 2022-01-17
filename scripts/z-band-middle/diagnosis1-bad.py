from pdme.model.unrestricted_model import UnrestrictedModel, UnrestrictedDiscretisation
from pdme.measurement import OscillatingDipole, OscillatingDipoleArrangement
import itertools
import logging
import multiprocessing
import numpy
import csv
import random

FILENAME = "z-band-middle-all-dots-narrowsquare-diagnosis1-bad.csv"
csv_fields = ["model", "index_px", "index_py", "index_pz", "index_sx", "index_sy", "index_sz", "bounds_px", "bounds_py", "bounds_pz", "bounds_sx", "bounds_sy", "bounds_sz", "actual_dipole_moment", "actual_dipole_position", "actual_dipole_freq", "success", "found_dipole_moment", "found_dipole_position", "found_dipole_frequency"]

def get_a_result(discretisation, dots, index):
	return (index, discretisation.solve_for_index(dots, index))

def main():

	with open(FILENAME, "a", newline="") as outfile:
		# csv fields
		writer = csv.DictWriter(outfile, fieldnames=csv_fields, dialect='unix')
		writer.writeheader()

	bad_dipole_moment = (1.4907798255452713, -0.11155216212225307, 8.598957203397196)
	bad_dipole_position = (-1.8204699606457453, 0.46178206204345074, 3.8691572159777703)
	bad_dipole_freq = 31
	
	# good_dipole_moment = (-1.9443892410744588, -6.221537995677158, 5.592388480581515)
	# good_dipole_position = (1.8087672324818271, -5.012714179961428, 4.171331614506319)
	# good_dipole_freq = 22
	# 
	# good_dipoles = OscillatingDipoleArrangement([OscillatingDipole(good_dipole_moment, good_dipole_position, good_dipole_freq)])
	bad_dipoles = OscillatingDipoleArrangement([OscillatingDipole(bad_dipole_moment, bad_dipole_position, bad_dipole_freq)])

	dot_inputs = list(itertools.chain.from_iterable(
		(([-.25, .25, 0], f), ([-.25, -.25, 0], f), ([.25, -.25, 0], f), ([.25, .25, 0], f)) for f in numpy.arange(1, 10, 2)
		))
	
	bad_dots = bad_dipoles.get_dot_measurements(dot_inputs)
	
	model_low = UnrestrictedModel(-10, 10, -10, 10, 2.5, 3.5, 1)
	discretisation_low = UnrestrictedDiscretisation(model_low, 6, 6, 3, 5, 5, 5, 10)

	model_medium = UnrestrictedModel(-10, 10, -10, 10, 3.5, 4.5, 1)
	discretisation_medium = UnrestrictedDiscretisation(model_medium, 6, 6, 3, 5, 5, 5, 10)

	model_high = UnrestrictedModel(-10, 10, -10, 10, 4.5, 5.5, 1)
	discretisation_high = UnrestrictedDiscretisation(model_high, 6, 6, 3, 5, 5, 5, 10)
		
	with multiprocessing.Pool(multiprocessing.cpu_count()-1 or 1) as pool:
		results_low = pool.starmap(get_a_result, zip(itertools.repeat(discretisation_low), itertools.repeat(bad_dots), discretisation_low.all_indices()))

	with multiprocessing.Pool(multiprocessing.cpu_count()-1 or 1) as pool:
		results_medium = pool.starmap(get_a_result, zip(itertools.repeat(discretisation_medium), itertools.repeat(bad_dots), discretisation_medium.all_indices()))

	with multiprocessing.Pool(multiprocessing.cpu_count()-1 or 1) as pool:
		results_high = pool.starmap(get_a_result, zip(itertools.repeat(discretisation_high), itertools.repeat(bad_dots), discretisation_high.all_indices()))


	with open(FILENAME, "a", newline='') as outfile:
		writer = csv.DictWriter(outfile, fieldnames=csv_fields, dialect='unix')

		for idx, result in results_low:
			pxi, pyi, pzi, sxi, syi, szi = idx
			
			bounds = discretisation_low.bounds(idx)

			actual_success = result.success and result.cost <= 1e-10 and numpy.linalg.norm(result.x[0:3]) < 10

			writer.writerow({
				"model": "low",
				"index_px": pxi,
				"index_py": pyi,
				"index_pz": pzi,
				"index_sx": sxi,
				"index_sy": syi,
				"index_sz": szi,
				"bounds_px": (bounds[0][0], bounds[1][0]),
				"bounds_py": (bounds[0][1], bounds[1][1]),
				"bounds_pz": (bounds[0][2], bounds[1][2]),
				"bounds_sx": (bounds[0][3], bounds[1][3]),
				"bounds_sy": (bounds[0][4], bounds[1][4]),
				"bounds_sz": (bounds[0][5], bounds[1][5]),
				"actual_dipole_moment": bad_dipole_moment,
				"actual_dipole_position": bad_dipole_position,
				"actual_dipole_freq": bad_dipole_freq,
				"success": actual_success,
				"found_dipole_moment": result.normalised_x[0:3] if actual_success else None,
				"found_dipole_position": result.normalised_x[3:6] if actual_success else None,
				"found_dipole_frequency": result.normalised_x[6] if actual_success else None
			})

		for idx, result in results_medium:
			pxi, pyi, pzi, sxi, syi, szi = idx
			
			bounds = discretisation_medium.bounds(idx)

			actual_success = result.success and result.cost <= 1e-10 and numpy.linalg.norm(result.x[0:3]) < 10

			writer.writerow({
				"model": "medium",
				"index_px": pxi,
				"index_py": pyi,
				"index_pz": pzi,
				"index_sx": sxi,
				"index_sy": syi,
				"index_sz": szi,
				"bounds_px": (bounds[0][0], bounds[1][0]),
				"bounds_py": (bounds[0][1], bounds[1][1]),
				"bounds_pz": (bounds[0][2], bounds[1][2]),
				"bounds_sx": (bounds[0][3], bounds[1][3]),
				"bounds_sy": (bounds[0][4], bounds[1][4]),
				"bounds_sz": (bounds[0][5], bounds[1][5]),
				"actual_dipole_moment": bad_dipole_moment,
				"actual_dipole_position": bad_dipole_position,
				"actual_dipole_freq": bad_dipole_freq,
				"success": actual_success,
				"found_dipole_moment": result.normalised_x[0:3] if actual_success else None,
				"found_dipole_position": result.normalised_x[3:6] if actual_success else None,
				"found_dipole_frequency": result.normalised_x[6] if actual_success else None
			})

		for idx, result in results_high:
			pxi, pyi, pzi, sxi, syi, szi = idx
			
			bounds = discretisation_high.bounds(idx)

			actual_success = result.success and result.cost <= 1e-10 and numpy.linalg.norm(result.x[0:3]) < 10

			writer.writerow({
				"model": "high",
				"index_px": pxi,
				"index_py": pyi,
				"index_pz": pzi,
				"index_sx": sxi,
				"index_sy": syi,
				"index_sz": szi,
				"bounds_px": (bounds[0][0], bounds[1][0]),
				"bounds_py": (bounds[0][1], bounds[1][1]),
				"bounds_pz": (bounds[0][2], bounds[1][2]),
				"bounds_sx": (bounds[0][3], bounds[1][3]),
				"bounds_sy": (bounds[0][4], bounds[1][4]),
				"bounds_sz": (bounds[0][5], bounds[1][5]),
				"actual_dipole_moment": bad_dipole_moment,
				"actual_dipole_position": bad_dipole_position,
				"actual_dipole_freq": bad_dipole_freq,
				"success": actual_success,
				"found_dipole_moment": result.normalised_x[0:3] if actual_success else None,
				"found_dipole_position": result.normalised_x[3:6] if actual_success else None,
				"found_dipole_frequency": result.normalised_x[6] if actual_success else None
			})



if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	main()

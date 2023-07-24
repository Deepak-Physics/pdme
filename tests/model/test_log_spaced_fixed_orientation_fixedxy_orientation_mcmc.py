from pdme.model import (
	LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel,
)
import pdme.inputs
import pdme.measurement.input_types
import pdme.subspace_simulation
import numpy

SEED_TO_USE = 42


def get_cost_function():
	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	max_frequency = 5

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel(
		x_min,
		x_max,
		y_min,
		y_max,
		z_min,
		z_max,
		0,
		max_frequency,
		p_fixed,
		1,
		0.5,
	)
	model.rng = numpy.random.default_rng(SEED_TO_USE)

	freqs = [0.01, 0.1, 1, 10, 100]
	dot_positions = [[-1.5, 0, 0], [-0.5, 0, 0], [0.5, 0, 0], [1.5, 0, 0]]
	dot_inputs = pdme.inputs.inputs_with_frequency_range(dot_positions, freqs)
	dot_input_array = pdme.measurement.input_types.dot_inputs_to_array(dot_inputs)

	actual_dipoles = model.get_dipoles(0, numpy.random.default_rng(SEED_TO_USE))
	actual_measurements = actual_dipoles.get_dot_measurements(dot_inputs)
	actual_measurements_array = numpy.array([m.v for m in actual_measurements])

	def cost_to_use(sample_dipoles: numpy.ndarray) -> numpy.ndarray:
		return pdme.subspace_simulation.proportional_costs_vs_actual_measurement(
			dot_input_array, actual_measurements_array, sample_dipoles
		)

	return cost_to_use


def test_log_spaced_fixedxy_orientation_mcmc_basic(snapshot):

	x_min = -10
	x_max = 10
	y_min = -5
	y_max = 5
	z_min = 2
	z_max = 3
	p_fixed = 10
	max_frequency = 5

	model = LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel(
		x_min,
		x_max,
		y_min,
		y_max,
		z_min,
		z_max,
		0,
		max_frequency,
		p_fixed,
		1,
		0.5,
	)
	model.rng = numpy.random.default_rng(1234)

	seed = model.get_monte_carlo_dipole_inputs(1, -1)[0]

	cost_function = get_cost_function()
	stdev = pdme.subspace_simulation.DipoleStandardDeviation(2, 2, 1, 0.25, 0.5, 1)
	stdevs = pdme.subspace_simulation.MCMCStandardDeviation([stdev])

	chain = model.get_mcmc_chain(
		seed, cost_function, 10, cost_function(seed)[0], stdevs, rng_arg=numpy.random.default_rng(1515)
	)

	assert chain == snapshot

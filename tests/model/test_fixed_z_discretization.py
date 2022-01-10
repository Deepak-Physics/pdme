from pdme.model.fixed_z_plane_model import FixedZPlaneModel, FixedZPlaneDiscretisation
import numpy


def test_fixed_z_plane_model_discretization():
	model = FixedZPlaneModel(4, -10, 10, -10, 10, 1)
	discretisation = FixedZPlaneDiscretisation(model, 1, 2, 5, 15)
	# x: (-10, 0) and (0, 10)
	# y: (-10, -6, -2, 2, 6, 10)
	assert discretisation.cell_count == 10
	assert discretisation.pz_step == 30
	assert discretisation.x_step == 10
	assert discretisation.y_step == 4
	numpy.testing.assert_allclose(discretisation.bounds((0, 0, 0)), ((-15, -10, -10, -numpy.inf), (15, 0, -6, numpy.inf)))
	numpy.testing.assert_allclose(list(discretisation.all_indices()), list(numpy.ndindex((1, 2, 5))))

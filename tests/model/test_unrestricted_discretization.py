from pdme.model.unrestricted_model import UnrestrictedModel, UnrestrictedDiscretisation
import numpy


def test_unrestricted_model_discretization():
	model = UnrestrictedModel(-10, 10, -10, 10, -10, 10, 1)
	discretisation = UnrestrictedDiscretisation(model, 2, 5, 1, 15)
	# x: (-10, 0) and (0, 10)
	# y: (-10, -6, -2, 2, 6, 10)
	assert discretisation.cell_count == 10
	assert discretisation.x_step == 10
	assert discretisation.y_step == 4
	assert discretisation.z_step == 20
	numpy.testing.assert_allclose(discretisation.bounds((0, 0, 0)), ((-15, -15, -15, -10, -10, -10, -numpy.inf), (15, 15, 15, 0, -6, 10, numpy.inf)))
	numpy.testing.assert_allclose(list(discretisation.all_indices()), list(numpy.ndindex((2, 5, 1))))

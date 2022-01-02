from pdme.model.fixed_z_plane_model import FixedZPlaneModel


def test_fixed_z_plane_model_repr():
	model = FixedZPlaneModel(1, 2, 3, 4, 5, 6)
	assert repr(model) == "FixedZPlaneModel(1, 2, 3, 4, 5, 6)"

import numpy as np


def transform_coordinate_2d(coord, matrix):
    x = matrix[0, 0] * coord[0] + matrix[0, 1] * coord[1] + matrix[0, 2]
    y = matrix[1, 0] * coord[0] + matrix[1, 1] * coord[1] + matrix[1, 2]
    return x, y


def transform_coordinate_3d(coord, matrix):
    x = matrix[0, 0] * coord[0] + matrix[0, 1] * coord[1] + matrix[0, 2] * coord[2] + matrix[0, 3]
    y = matrix[1, 0] * coord[0] + matrix[1, 1] * coord[1] + matrix[1, 2] * coord[2] + matrix[1, 3]
    z = matrix[2, 0] * coord[0] + matrix[2, 1] * coord[1] + matrix[2, 2] * coord[2] + matrix[2, 3]
    return x, y, z


def check_coordinate(coord, shape):
    if any(co < 0 or round(co, 0) >= sh for co, sh in zip(coord, shape)):
        return False
    return True


# TODO support linear (order=1) interpolation
def interpolate(input_, coord, order):
    rounded_coord = tuple(int(round(co, 0)) for co in coord)
    return input_[rounded_coord]


# TODO what we do with the new shape does not make much sense (shifts don't have any effect).
# we need to define the input and output coordinate systems
# and their relation through the world coordinate system somehow
def apply_affine_transformation(a, matrix, order=0, fill_value=0.):
    adim = a.ndim
    mdim = matrix.shape[0] - 1
    # TODO only support 2d for now
    dim = 2
    assert adim == mdim == dim
    # TODO only support nearest interpolation for now
    assert order == 0

    transform_coordinate = transform_coordinate_2d if dim == 2 else transform_coordinate_3d

    # get the inverse matrix
    inv_matrix = np.linalg.inv(matrix)

    # find the output shape by transforming the corners of a
    shape = a.shape
    corners = [(0, 0), (shape[0], 0), (0, shape[1]), shape]
    transformed_corners = [transform_coordinate(corner, matrix)
                           for corner in corners]
    starts = [min(corner[d] for corner in transformed_corners) for d in range(dim)]
    stops = [max(corner[d] for corner in transformed_corners) for d in range(dim)]
    out_shape = tuple(int(sto - sta) for sta, sto in zip(starts, stops))

    # make output array
    b = np.zeros(out_shape)

    # iterate over all pixels of `b`, find coordinates in `a` via inv_matrix and interpolate value
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            # we have to add starts here (I think ...) in order to stay in the right coordinate space
            coord = (i + starts[0], j + starts[1])
            transformed_coord = transform_coordinate(coord, inv_matrix)
            if not check_coordinate(transformed_coord, shape):
                b[i, j] = fill_value
                continue
            b[i, j] = interpolate(a, transformed_coord, order)

    return b

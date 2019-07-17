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


def transform_shape(shape, matrix, transform_coordinate):
    dim = len(shape)
    corners = [(0, 0), (shape[0], 0), (0, shape[1]), shape]
    transformed_corners = [transform_coordinate(corner, matrix)
                           for corner in corners]
    starts = [min(corner[d] for corner in transformed_corners) for d in range(dim)]
    stops = [max(corner[d] for corner in transformed_corners) for d in range(dim)]
    out_shape = tuple(int(sto - sta) for sta, sto in zip(starts, stops))
    return out_shape, starts


# TODO implement interpolation orders:
# 0: nearest
# 1: linear
# 2: quadratic
# 3: cubic
def apply_affine_transformation(a, matrix, order=0, fill_value=0.,
                                output_shape=None, origin=None):
    """ Apply affine transformation to 2d or 3d input.

    Arguments:
        a [np.ndarray] - input array, must be 2d or 3d
        matrix [np.ndarray] - affine matrix,
            must be (3, 3) for 2d and (4, 4) for 3d
        order [int] - interpolation order
            0 = nearest interpolation, 1 = linear interpolation (default: 0)
        output_shape [tuple]: shape for the ouput,
            by default uses the full extent after transformation (default: None)
        origin [listlike]: origin of the output relative to input origin
            by default uses the transformed origin (default: None)
    """

    adim = a.ndim
    mdim = matrix.shape[0] - 1
    # TODO only support 2d for now
    dim = 2
    assert adim == mdim == dim
    # TODO only support nearest interpolation for now
    assert order == 0

    transform_coordinate = transform_coordinate_2d if dim == 2 else transform_coordinate_3d

    # TODO handle singular matrix here
    # get the inverse affine matrix
    inv_matrix = np.linalg.inv(matrix)

    # find the extent of the transformed image and the position
    # of the left corner w.r.t the pre-transformed left corner
    shape = a.shape
    # extent, offset = transform_shape(shape, matrix, transform_coordinate)
    extent, offset = transform_shape(shape, inv_matrix, transform_coordinate)

    # if the oputput shae was not specified, set it to the full extent
    if output_shape is None:
        output_shape = extent

    # if the new origin was not specified, set it to the offset
    if origin is None:
        origin = offset

    # make output array
    b = np.zeros(output_shape)

    # iterate over all pixels of `b`, find coordinates in `a` via inv_matrix and interpolate value
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            # we add the origin here to get to the correct position in the original image
            coord = (i + origin[0], j + origin[1])
            transformed_coord = transform_coordinate(coord, matrix)
            if not check_coordinate(transformed_coord, shape):
                b[i, j] = fill_value
                continue
            b[i, j] = interpolate(a, transformed_coord, order)

    return b

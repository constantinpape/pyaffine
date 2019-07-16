import numpy as np


def update_parameters(scale, rotation, shear, shift, dim):
    if scale is None:
        scale = [1.] * dim
    if rotation is None:
        rotation = [0.] if dim == 2 else [0.] * 3
    if shear is None:
        # TODO how many shear angles do we have in 3d ?
        shear = [0.] * (dim - 1)
    if shift is None:
        shift = [0.] * dim
    return scale, rotation, shear, shift


def affine_matrix_2d(scale=None, rotation=None, shear=None, shift=None):
    matrix = np.zeros((3, 3))
    scale, rotation, shear, shift = update_parameters(scale,
                                                      rotation,
                                                      shear,
                                                      shift,
                                                      dim=2)
    # make life easier
    cos, sin = np.cos, np.sin
    sx, sy = scale
    phi = np.deg2rad(rotation)[0]
    shear_angle = np.deg2rad(shear)[0]

    # TODO shear from skimage confuses me ...
    # set the main transformation matrix
    matrix[0, 0] = sx * cos(phi)
    matrix[0, 1] = - sy * sin(phi + shear_angle)

    matrix[1, 0] = sx * sin(phi)
    matrix[1, 1] = sy * cos(phi + shear_angle)

    # set the shift
    matrix[:2, 2] = shift

    # set extra element
    matrix[2, 2] = 1
    return matrix


def affine_matrix_3d(scale=None, rotation=None, shear=None, shift=None):
    matrix = np.zeros((4, 4))
    scale, rotation, shear, shift = update_parameters(scale,
                                                      rotation,
                                                      shear,
                                                      shift,
                                                      dim=3)

    # make life easier
    cos, sin = np.cos, np.sin
    sx, sy, sz = scale
    phi, theta, psi = np.deg2rad(rotation)

    # TODO this is missing shear !
    matrix[0, 0] = sx * cos(theta) * cos(psi)
    matrix[0, 1] = sy * (-cos(phi) * sin(psi) + sin(phi) * sin(theta) * cos(psi))
    matrix[0, 2] = sz * (sin(phi) * sin(psi) + cos(phi) * sin(theta) * cos(psi))

    matrix[1, 0] = sx * cos(theta) * sin(psi)
    matrix[1, 1] = sy * (cos(phi) * cos(psi) + sin(phi) * sin(theta) * sin(psi))
    matrix[1, 2] = sz * (- sin(phi) * cos(theta) + cos(phi) * sin(theta) * sin(psi))

    matrix[2, 0] = -sx * sin(theta)
    matrix[2, 1] = sy * sin(phi) * sin(theta)
    matrix[2, 2] = sz * cos(phi) * cos(theta)

    # set the shift
    matrix[:3, 3] = shift

    # set extra elemnt
    matrix[3, 3] = 1
    return matrix


def affine_matrix(scale=None, rotation=None, shear=None, shift=None):

    # validate the input parameters
    parameters = [scale, rotation, shear, shift]
    assert not all(param is None
                   for param in parameters)

    # determine and validate the dimension
    lens = [None if param is None else len(param)
            for param in parameters]
    # for scale and shift len = dimension
    # for rotation and shear len = 3 if dim == 3 else len = 1
    dims = [ll if ii in (0, 3) else 2 if ll == 1 else 3
            for ii, ll in enumerate(lens) if ll is not None]
    assert len(set(dims)) == 1
    dim = dims[0]

    matrix = affine_matrix_2d(scale, rotation, shear, shift) if dim == 2 else\
        affine_matrix_3d(scale, rotation, shear, shift)
    return matrix

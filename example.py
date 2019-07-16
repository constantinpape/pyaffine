import numpy as np
from pyaffine import affine_matrix, apply_affine_transformation


def random():
    matrix = affine_matrix(scale=[2, 2], shift=[1, -1])
    print(matrix)
    x = np.random.rand(100, 100)
    y = apply_affine_transformation(x, matrix)
    print(y.shape)


def example():
    # x = np.ones((5, 5))
    x = np.arange(25).reshape((5, 5))
    matrix = affine_matrix(scale=[2, 2], rotation=[90.])
    y = apply_affine_transformation(x, matrix)
    print(y)


example()

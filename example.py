import numpy as np
import matplotlib.pyplot as plt
from skimage.data import astronaut
from skimage.transform import warp, AffineTransform
from pyaffine import affine_matrix, apply_affine_transformation


def rotate_the_astronaut():
    im = astronaut()[..., 0]

    angle = 90

    # use skimage
    trafo = AffineTransform(rotation=np.deg2rad(angle))
    warped_sk = warp(im, trafo.inverse, preserve_range=True)
    print(im.shape)
    print(warped_sk.shape)

    # use py-affine
    matrix = affine_matrix(rotation=[angle])
    warped_py = apply_affine_transformation(im, matrix)
    print(warped_py.shape)

    fig, ax = plt.subplots(3)
    ax[0].imshow(im, cmap='gray')
    ax[1].imshow(warped_sk, cmap='gray')
    ax[2].imshow(warped_py, cmap='gray')
    plt.show()


def scale_the_astronaut():
    im = astronaut()[..., 0]

    scale = [.5, 2]

    # use skimage
    trafo = AffineTransform(scale=scale)
    warped_sk = warp(im, trafo.inverse, preserve_range=True)
    print(im.shape)
    print(warped_sk.shape)

    # use py-affine
    matrix = affine_matrix(scale=scale)
    warped_py = apply_affine_transformation(im, matrix)
    print(warped_py.shape)

    fig, ax = plt.subplots(3)
    ax[0].imshow(im, cmap='gray')
    ax[1].imshow(warped_sk, cmap='gray')
    ax[2].imshow(warped_py, cmap='gray')
    plt.show()


if __name__ == '__main__':
    rotate_the_astronaut()
    # scale_the_astronaut()

import unittest
import numpy as np

import sys
sys.path.append('..')


# FIXME scale is inverted
# Dummy Test
class TestAffine(unittest.TestCase):
    def test_apply(self):
        from pyaffine import affine_matrix, apply_affine_transformation
        matrix = affine_matrix(scale=[.5, .5])
        self.assertEqual(matrix.shape, (3, 3))
        x = np.random.rand(100, 100)
        y = apply_affine_transformation(x, matrix)
        self.assertEqual(y.shape, (200, 200))


if __name__ == '__main__':
    unittest.main()

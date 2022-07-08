from homework_3.matrix_manipulation_ctypes import MatrixManipulation
from homework_3.matrix_manipulation_numpy import *

import unittest
import os


class TestMatrixManipulation(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        this_file_dir = os.path.dirname(os.path.abspath(__file__))
        so_library_path = os.path.join(
            this_file_dir, "build/libmatrix_manipulation_cuda.so")
        self._lib = MatrixManipulation(so_library_path)
        self._a = np.ones([5, 5])
        self._a[1, 1] = 5
        self._a[2, 2] = 5

        self._b = np.ones([5, 5])
        self._b[2, 2] = 90

    def test_matrix_multiply(self):
        result, _ = self._lib.matrix_multiply(self._a, self._b)
        numpy_result, _ = multiply_square_two_matrixes(
            self._a, self._b)
        self.assertTrue(np.allclose(result, numpy_result))

    def test_threshold(self):
        THRESHOLD = 2.0
        result, _ = self._lib.threshold(self._a, THRESHOLD)
        numpy_result, _ = threshold_reverse(
            self._a, THRESHOLD)
        self.assertTrue(np.allclose(result, numpy_result))

    def test_reversed_threshold(self):
        THRESHOLD = 2.0
        result, _ = self._lib.reversed_threshold(self._a, THRESHOLD)
        numpy_result, _ = threshold(
            self._a, THRESHOLD)
        self.assertTrue(np.allclose(result, numpy_result))

    def test_add(self):
        result, _ = self._lib.add(self._a, self._b)
        numpy_result, _ = add(
            self._a, self._b)
        self.assertTrue(np.allclose(result, numpy_result))

    def test_sum(self):
        result, _ = self._lib.sum(self._a)
        numpy_result, _ = sum(
            self._a)
        self.assertAlmostEqual(result, numpy_result)


if __name__ == '__main__':
    unittest.main()

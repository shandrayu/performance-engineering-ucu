import ctypes
import numpy as np
import os
import unittest
from homework_3.matrix_manipulation_numpy import *
from common.tools import measure_time

# TODO: Bad design. Time measurement incorporated into functionality
class MatrixManipulation:
    """
    A wrapper class for c library matrix manipulation functions.

    Credits: 
        - practice session, lecture 3
        - https://gist.github.com/lud4ik/3403220
    """

    def __init__(self, so_library_path) -> None:
        _lib = ctypes.cdll.LoadLibrary(so_library_path)

        self._matrix_multiply = _lib.matrix_multiply
        self._matrix_multiply.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(
            ctypes.c_double), ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        self._matrix_multiply.restype = None

        self._threshold = _lib.threshold
        self._threshold.argtypes = [ctypes.POINTER(
            ctypes.c_double),  ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
        self._threshold.restype = None

        self._reversed_threshold = _lib.reversed_threshold
        self._reversed_threshold.argtypes = [ctypes.POINTER(
            ctypes.c_double),  ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
        self._reversed_threshold.restype = None

        self._add = _lib.add
        self._add.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(
            ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        self._add.restype = None

        self._sum = _lib.sum
        self._sum.argtypes = [ctypes.POINTER(ctypes.c_double),  ctypes.c_int]
        self._sum.restype = ctypes.c_double

    @measure_time
    def matrix_multiply(self, lhs: np.array, rhs: np.array) -> np.array:
        assert(lhs.dtype == np.float64)
        assert(rhs.dtype == np.float64)

        lhs_pointer = lhs.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        rhs_pointer = rhs.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        result = np.zeros_like(lhs)
        result_pointer = result.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        self._matrix_multiply(lhs_pointer, rhs_pointer, ctypes.c_int(
            lhs.shape[0]), ctypes.c_int(lhs.shape[1]), result_pointer)

        return result

    @measure_time
    def threshold(self, array: np.array, threshold: np.float64) -> np.array:
        assert(array.dtype == np.float64)

        array_pointer = array.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        result = np.zeros_like(array)
        result_pointer = result.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        self._threshold(array_pointer, ctypes.c_int(
            array.shape[0]*array.shape[1]), ctypes.c_double(threshold), result_pointer)

        return result

    @measure_time
    def reversed_threshold(self, array: np.array, threshold: np.float64) -> np.array:
        assert(array.dtype == np.float64)

        array_pointer = array.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        result = np.zeros_like(array)
        result_pointer = result.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        self._reversed_threshold(array_pointer, ctypes.c_int(
            array.shape[0]*array.shape[1]), ctypes.c_double(threshold), result_pointer)

        return result

    @measure_time
    def add(self, lhs: np.array, rhs: np.array) -> np.array:
        assert(lhs.dtype == np.float64)
        assert(rhs.dtype == np.float64)

        lhs_pointer = lhs.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        rhs_pointer = rhs.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        result = np.zeros_like(lhs)
        result_pointer = result.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        self._add(lhs_pointer, rhs_pointer, ctypes.c_int(
            lhs.shape[0]*lhs.shape[1]), result_pointer)

        return result
    
    @measure_time
    def sum(self, array: np.array) -> np.float64:
        assert(array.dtype == np.float64)

        array_pointer = array.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        result = self._sum(array_pointer, ctypes.c_int(
            array.shape[0]*array.shape[1]))

        return result


class TestMatrixManipulation(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        this_file_dir = os.path.dirname(os.path.abspath(__file__))
        so_library_path = os.path.join(
            this_file_dir, "build/libmatrix_manipulation.so")
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
        numpy_result, _ = threshold(
            self._a, THRESHOLD)
        self.assertTrue(np.allclose(result, numpy_result))

    def test_reversed_threshold(self):
        THRESHOLD = 2.0
        result, _ = self._lib.reversed_threshold(self._a, THRESHOLD)
        numpy_result, _ = threshold_reverse(
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

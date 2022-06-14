from common.tools import measure_time

import numpy as np


@measure_time
def multiply_square_two_matrixes(lhs, rhs):
    return np.matmul(lhs, rhs)


@measure_time
def threshold(array, threshold):
    """
    1 if value <= threshold
    0 otherwise
    """
    return np.where(array <= threshold, 1, 0)


@measure_time
def threshold_reverse(array, threshold):
    """
    1 if value > threshold
    0 otherwise
    """
    return np.where(array > threshold, 1, 0)


@measure_time
def add(lhs, rhs):
    return lhs + rhs


@measure_time
def sum(array):
    return np.sum(array)

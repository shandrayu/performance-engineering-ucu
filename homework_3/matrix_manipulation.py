import numpy as np
import random
import time
import math
from tqdm import tqdm
from common.tools import save_execution_time_plot, save_to_csv


def measure_time(func):

    def wrapper_func(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        execution_time_sec = end - start
        return result, execution_time_sec

    return wrapper_func


def generate_random_matrix(M, N):
    return [[random.uniform(0, 100) for _ in range(M)] for _ in range(N)]


def is_matrix_equal(lhs, rhs):
    # TODO: add dimension comparison
    if type(lhs) is list:
        M = len(lhs)
        N = len(lhs[0])
    elif type(lhs) is np.array:
        M, N = lhs.shape

    for i in range(M):
        for j in range(N):
            assert math.isclose(
                lhs[i][j], rhs[i][j]), f"Elements at position [{i}][{j}] are not equal: {lhs[i][j]} is not {rhs[i][j]}"


def store_execution_time(store_execution_time, func, *arg):
    result, time_elapsed = func(*arg)
    store_execution_time.append(time_elapsed)
    return result


@measure_time
def a_multiply_square_two_matrixes(lhs, rhs):
    # Doest not guarantee the square matrix as every list amy have different length
    assert(len(lhs) == len(lhs[0]))
    # Doest not guarantee the square matrix as every list amy have different length
    assert(len(rhs) == len(rhs[0]))
    assert(len(lhs) == len(rhs))
    N = len(lhs)
    result = [[0 for _ in range(N)] for _ in range(N)]

    for row in range(N):
        for col in range(N):
            for k in range(N):
                result[row][col] += lhs[row][k] * rhs[k][col]

    return result


@measure_time
def a_threshold(array, threshold):
    """
    1 if value <= threshold
    0 otherwise
    """
    result = [[1 if element <= threshold else 0 for element in row]
              for row in array]
    return result


@measure_time
def a_reversed_threshold(array, threshold):
    """
    1 if value > threshold
    0 otherwise
    """
    result = [[1 if element > threshold else 0 for element in row]
              for row in array]
    return result


@measure_time
def a_add(lhs, rhs):
    result = [[a + b for a in a_row for b in b_row]
              for a_row in lhs for b_row in rhs]
    return result

@measure_time
def a_sum(array):
    row_sum = list(map(sum, array))
    return sum(row_sum)

@measure_time
def b_numpy_multiply_square_two_matrixes(lhs, rhs):
    return np.matmul(lhs, rhs)


@measure_time
def b_numpy_threshold(array, threshold):
    """
    1 if value <= threshold
    0 otherwise
    """
    return np.where(array <= threshold, 1, 0)


@measure_time
def b_numpy_threshold_reverse(array, threshold):
    """
    1 if value > threshold
    0 otherwise
    """
    return np.where(array > threshold, 1, 0)


@measure_time
def b_add(lhs, rhs):
    return lhs + rhs

@measure_time
def b_sum(array):
    return np.sum(array)


def store_time_and_graph(array_times, filename, graph_title, scaler=1):
    array_times = np.array(array_times) * 10**9
    save_to_csv(array_times, filename)
    save_execution_time_plot(
        array_times, graph_title)


def main():
    a_1_by_elements_times = []
    a_2_threshold_times = []
    a_3_reversed_threshold_times = []
    a_4_add_times = []
    a_5_sum_times = []
    b_1_numpy_multiplication_times = []
    b_2_numpy_threshold_times = []
    b_3_numpy_reverse_threshold_times = []
    b_4_numpy_add_times = []
    b_5_sum_times = []

    MIN_MATRIX_SIZE = 5
    MAX_MATRIX_SIZE = 100
    THRESHOLD = 50
    for matrix_size in tqdm(range(MIN_MATRIX_SIZE, MAX_MATRIX_SIZE)):
        A = generate_random_matrix(matrix_size, matrix_size)
        B = generate_random_matrix(matrix_size, matrix_size)
        A_numpy = np.array(A)
        B_numpy = np.array(B)

        a1 = store_execution_time(
            a_1_by_elements_times, a_multiply_square_two_matrixes, A, B)
        b1 = store_execution_time(
            b_1_numpy_multiplication_times, b_numpy_multiply_square_two_matrixes, A_numpy, B_numpy)
        is_matrix_equal(a1, b1)

        a2 = store_execution_time(
            a_2_threshold_times, a_threshold, A, THRESHOLD)
        b2 = store_execution_time(
            b_2_numpy_threshold_times, b_numpy_threshold, A_numpy, THRESHOLD)
        is_matrix_equal(a2, b2)

        a3 = store_execution_time(
            a_3_reversed_threshold_times, a_reversed_threshold, A, THRESHOLD)
        b3 = store_execution_time(
            b_3_numpy_reverse_threshold_times, b_numpy_threshold_reverse, A_numpy, THRESHOLD)
        is_matrix_equal(a3, b3)

        a4 = store_execution_time(
            a_4_add_times, a_add, A, B)
        b4 = store_execution_time(b_4_numpy_add_times, a_add, A_numpy, B_numpy)
        is_matrix_equal(a4, b4)

        a5 = store_execution_time(
            a_5_sum_times, a_sum, A)
        b5 = store_execution_time(b_5_sum_times, b_sum, A_numpy)
        assert math.isclose(a5, b5), f"Sum is not equal: {a5} is not {b5}"

    # A
    store_time_and_graph(
        a_1_by_elements_times, "a_1_by_elements_times", "Pure Python matrix multiplication")
    store_time_and_graph(
        a_2_threshold_times, "a_2_threshold_times", "Pure Python matrix threshold")
    store_time_and_graph(
        a_3_reversed_threshold_times, "a_3_reversed_threshold_times", "Pure Python matrix reversed threshold")
    store_time_and_graph(
        a_4_add_times, "a_4_add_times", "Pure Python matrix element-wise addition")
    store_time_and_graph(
        a_5_sum_times, "a_5_sum_times", "Pure Python matrix element sum")

    # B
    store_time_and_graph(b_1_numpy_multiplication_times,
                         "b_1_numpy_multiplication_times", "Numpy matrix multiplication")
    store_time_and_graph(b_2_numpy_threshold_times,
                         "b_2_numpy_threshold_times", "Numpy matrix threshold")
    store_time_and_graph(b_3_numpy_reverse_threshold_times,
                         "b_3_numpy_reverse_threshold_times", "Numpy matrix reverse threshold")
    store_time_and_graph(b_4_numpy_add_times,
                         "b_4_numpy_add_times", "Numpy matrix element-wise addition")
    store_time_and_graph(b_5_sum_times,
                         "b_5_sum_times", "Numpy matrix element sum")

    # C


if __name__ == "__main__":
    main()

import numpy as np
from tqdm import tqdm
from common.tools import save_execution_time_plot, save_to_csv, is_matrix_equal, generate_random_matrix
import matrix_manipulation_numpy as mm_numpy
import matrix_manipulation_native as mm_native
from matrix_manipulation_ctypes import MatrixManipulation
import math
import os


def store_execution_time(store_execution_time, func, *arg):
    result, time_elapsed = func(*arg)
    store_execution_time.append(time_elapsed)
    return result


def store_time_and_graph(array_times, filename, graph_title, scaler=1):
    array_times = np.array(array_times) * 10**9
    save_to_csv(array_times, filename)
    save_execution_time_plot(
        array_times, graph_title)


def main():
    # TODO: technically speaking copypaste. Pack into the one list of lists
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
    c_1_numpy_multiplication_times = []
    c_2_numpy_threshold_times = []
    c_3_numpy_reverse_threshold_times = []
    c_4_numpy_add_times = []
    c_5_sum_times = []

    MIN_MATRIX_SIZE = 5
    MAX_MATRIX_SIZE = 100
    THRESHOLD = 100

    this_file_dir = os.path.dirname(os.path.abspath(__file__))
    so_library_path = os.path.join(
        this_file_dir, "build/libmatrix_manipulation.so")
    lib = MatrixManipulation(so_library_path)

    for matrix_size in tqdm(range(MIN_MATRIX_SIZE, MAX_MATRIX_SIZE)):
        A = generate_random_matrix(matrix_size, matrix_size)
        B = generate_random_matrix(matrix_size, matrix_size)
        A_numpy = np.array(A)
        B_numpy = np.array(B)

        a1 = store_execution_time(
            a_1_by_elements_times, mm_native.multiply_square_two_matrixes, A, B)
        b1 = store_execution_time(
            b_1_numpy_multiplication_times, mm_numpy.multiply_square_two_matrixes, A_numpy, B_numpy)
        _ = store_execution_time(
            c_1_numpy_multiplication_times, lib.matrix_multiply, A_numpy, B_numpy)
        is_matrix_equal(a1, b1)

        a2 = store_execution_time(
            a_2_threshold_times, mm_native.threshold, A, THRESHOLD)
        b2 = store_execution_time(
            b_2_numpy_threshold_times, mm_numpy.threshold, A_numpy, THRESHOLD)
        _ = store_execution_time(
            c_2_numpy_threshold_times, lib.threshold, A_numpy, THRESHOLD)
        is_matrix_equal(a2, b2)

        a3 = store_execution_time(
            a_3_reversed_threshold_times, mm_native.reversed_threshold, A, THRESHOLD)
        b3 = store_execution_time(
            b_3_numpy_reverse_threshold_times, mm_numpy.threshold_reverse, A_numpy, THRESHOLD)
        _ = store_execution_time(
            c_3_numpy_reverse_threshold_times, lib.reversed_threshold, A_numpy, THRESHOLD)
        is_matrix_equal(a3, b3)

        a4 = store_execution_time(
            a_4_add_times, mm_native.add, A, B)
        b4 = store_execution_time(
            b_4_numpy_add_times, mm_numpy.add, A_numpy, B_numpy)
        _ = store_execution_time(
            c_4_numpy_add_times, lib.add, A_numpy, B_numpy)
        is_matrix_equal(a4, b4)

        a5 = store_execution_time(
            a_5_sum_times, mm_native.asum, A)
        b5 = store_execution_time(
            b_5_sum_times, mm_numpy.sum, A_numpy)
        _ = store_execution_time(
            c_5_sum_times, lib.sum, A_numpy)
        assert math.isclose(a5, b5), f"Sum is not equal: {a5} is not {b5}"

    # TODO copypaste
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
    store_time_and_graph(c_1_numpy_multiplication_times,
                         "c_1_numpy_multiplication_times", "ctypes matrix multiplication")
    store_time_and_graph(c_2_numpy_threshold_times,
                         "c_2_numpy_threshold_times", "ctypes matrix threshold")
    store_time_and_graph(c_3_numpy_reverse_threshold_times,
                         "c_3_numpy_reverse_threshold_times", "ctypes matrix reverse threshold")
    store_time_and_graph(c_4_numpy_add_times,
                         "c_4_numpy_add_times", "ctypes matrix element-wise addition")
    store_time_and_graph(c_5_sum_times,
                         "c_5_sum_times", "ctypes matrix element sum")

if __name__ == "__main__":
    main()

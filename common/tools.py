import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import random
import time
from typing import Dict, Tuple
import os


def save_execution_time_plot(array: np.array, title: str) -> None:
    plt.close()
    array_ms = array
    plt.plot(array_ms)
    plt.title(title)
    plt.xlabel("Array size")
    plt.ylabel("Execution time, ns")
    plt.grid('on')
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(
        f"{title.lower().replace(' ', '-')}-{array.shape[0]}.png", dpi=100)


def save_several_execution_time_plot(arrays: Dict[str, np.array], title: str, limit_x, limit_y) -> None:
    plt.close()
    for name, array in arrays.items():
        plt.plot(array, label=name)
    plt.title(title)
    plt.xlabel("Array size")
    plt.ylabel("Execution time, ns")
    plt.ylim((0, limit_y))
    plt.xlim((0, limit_x))
    plt.grid('on')
    plt.legend()
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(
        f"{title.lower().replace(' ', '-')}-{array.shape[0]}.png", dpi=100)


def load_csv_to_npy(filename: str) -> Tuple[str, np.array]:
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = []
        for row in reader:
            rows.append(row)
        formatted_array = np.array(rows).astype(np.int64)

    return header, formatted_array


def save_to_csv(timestamps_array: np.array, filename) -> None:
    formatted_array = timestamps_array.astype(np.int64)
    with open(f'{filename}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow([str('Execution time, nanoseconds')])
        for execution_time in formatted_array:
            writer.writerow([str(execution_time)])
    file.close()


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


def plot_several_graphs(graphs_list, title, limit_x, limit_y, data_dir=""):
    if not data_dir:
        this_file_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(this_file_dir, 'data')
    arrays_to_plot = {}
    for array_filename in graphs_list:
        _, array = load_csv_to_npy(os.path.join(
            data_dir, array_filename))
        arrays_to_plot[array_filename] = array

    save_several_execution_time_plot(
        arrays_to_plot, title, limit_x, limit_y)

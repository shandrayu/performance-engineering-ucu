import random
import numpy as np
import time
from tqdm import tqdm
from plot import save_execution_time_plot


def multiply_arrays_by_elements(array_size: int) -> float:
    rand_array_lhs = [random.uniform(0, 100) for idx in range(array_size)]
    rand_array_rhs = [random.uniform(0, 100) for idx in range(array_size)]

    start = time.time()
    result = [None] * array_size
    for idx in range(array_size):
        result[idx] = rand_array_lhs[idx] * rand_array_rhs[idx]
    end = time.time()

    execution_time = end - start
    return execution_time


def multiply_numpy_arrays(array_size: int) -> float:
    rand_array_lhs = np.random.rand(1, array_size)
    rand_array_rhs = np.random.rand(1, array_size)

    start = time.time()
    result = rand_array_rhs * rand_array_lhs
    end = time.time()

    execution_time = end - start
    return execution_time


if __name__ == "__main__":
    MAX_ARRAY_SIZE = 10000
    arrays_by_elements_times = []
    numpy_arrays_times = []
    for size in tqdm(range(MAX_ARRAY_SIZE)):
        arrays_by_elements_times.append(multiply_arrays_by_elements(size))
        numpy_arrays_times.append(multiply_numpy_arrays(size))

    save_execution_time_plot(np.array(arrays_by_elements_times),
                             "By-element multiplication")
    save_execution_time_plot(
        np.array(numpy_arrays_times), "Numpy multiplication")

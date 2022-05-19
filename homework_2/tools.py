import matplotlib.pyplot as plt
import numpy as np
import csv
from typing import Dict, Tuple


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


def save_several_execution_time_plot(arrays: Dict[str, np.array], title: str) -> None:
    plt.close()
    for name, array in arrays.items():
        plt.plot(array, label=name)
    plt.title(title)
    plt.xlabel("Array size")
    plt.ylabel("Execution time, ns")
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

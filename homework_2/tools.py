import matplotlib.pyplot as plt
import numpy as np
import csv

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
    fig.savefig(f"{title.lower().replace(' ', '-')}-{array.shape[0]}.png", dpi=100)


def save_to_csv(timestamps_array: np.array, filename) -> None:
    formatted_array = timestamps_array.astype(np.int64)
    with open(f'{filename}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow([str('Execution time, nanoseconds')])
        for execution_time in formatted_array:
             writer.writerow([str(execution_time)])
    file.close()
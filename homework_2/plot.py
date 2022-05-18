import matplotlib.pyplot as plt
import numpy as np


def save_execution_time_plot(array, title: str) -> None:
    plt.close()
    array_ms = np.array(array) * 1000
    plt.plot(array_ms)
    plt.title(title)
    plt.xlabel("Array size")
    plt.ylabel("Execution time, ms")
    plt.grid('on')
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(f"{title.lower().replace(' ', '-')}-{len(array)}.png", dpi=100)

import matplotlib.pyplot as plt
import numpy as np


def save_execution_time_plot(array: np.array, title: str, scaler: int = 1000) -> None:
    plt.close()
    array_ms = array * scaler
    plt.plot(array_ms)
    plt.title(title)
    plt.xlabel("Array size")
    plt.ylabel("Execution time")
    plt.grid('on')
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(f"{title.lower().replace(' ', '-')}-{array.shape[0]}.png", dpi=100)

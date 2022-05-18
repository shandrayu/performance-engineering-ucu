import csv
import numpy as np
import os

from plot import save_execution_time_plot


def plot_graph_from_csv(filename, plot_name_suffix):
    '''
    Credit: https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/
    '''

    file = open(filename)
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)
    formatted_array = np.array(rows).astype(np.int64)
    save_execution_time_plot(formatted_array,
                             " ".join(header)+'-'+plot_name_suffix, 1)
    file.close()


if __name__ == "__main__":
    this_file_dir = os.path.dirname(os.path.abspath(__file__))
    plot_graph_from_csv(os.path.join(
        this_file_dir, 'data/execution_time_O0.csv'), 'O0')
    plot_graph_from_csv(os.path.join(
        this_file_dir, 'data/execution_time_O3.csv'), 'O3')

import csv
import numpy as np
import os

from tools import save_execution_time_plot, load_csv_to_npy


def plot_graph_from_csv(filename, plot_name_suffix):
    '''
    Credit: https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/
    '''

    header, formatted_array = load_csv_to_npy(filename)
    save_execution_time_plot(formatted_array,
                             " ".join(header)+'-'+plot_name_suffix)


if __name__ == "__main__":
    this_file_dir = os.path.dirname(os.path.abspath(__file__))
    plot_graph_from_csv(os.path.join(
        this_file_dir, 'data', 'execution_time_O0.csv'), 'O0')
    plot_graph_from_csv(os.path.join(
        this_file_dir, 'data', 'execution_time_O3.csv'), 'O3')
    plot_graph_from_csv(os.path.join(
        this_file_dir, 'data', 'execution_time_intristics_O0.csv'), 'intristics-O0')
    plot_graph_from_csv(os.path.join(
        this_file_dir, 'data', 'execution_time_intristics_O3.csv'), 'intristics-O3')

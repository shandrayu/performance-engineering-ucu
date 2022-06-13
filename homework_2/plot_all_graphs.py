import os

from common.tools import save_several_execution_time_plot, load_csv_to_npy

if __name__ == "__main__":
    arrays_list = ['execution_time_O0.csv', 'execution_time_O3.csv',
                   'execution_time_intristics_O0.csv', 'execution_time_intristics_O3.csv',
                   'numpy_arrays_times_python.csv', 'arrays_by_elements_times_python.csv']

    this_file_dir = os.path.dirname(os.path.abspath(__file__))
    arrays_to_plot = {}
    for array_filename in arrays_list:
        _, array = load_csv_to_npy(os.path.join(
            this_file_dir, 'data', array_filename))
        arrays_to_plot[array_filename] = array

    save_several_execution_time_plot(
        arrays_to_plot, 'Execution time for all experiments', 3500, 0.2*10**6)

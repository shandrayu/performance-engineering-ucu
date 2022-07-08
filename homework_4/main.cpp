#include <stdlib.h>

#include <algorithm>
#include <chrono>
#include <ctime>
#include <fstream>
#include <iostream>
#include <map>
#include <random>
#include <string>
#include <vector>

#include "matrix_manipulation.cuh"

// TODO: copy-pase from HW2. Make common if time allows
// TODO: Modified random vector generator.
// Credit
// https://stackoverflow.com/questions/21516575/fill-a-vector-with-random-numbers-c
std::vector<double> generate_random_vector(std::size_t size) {
  constexpr double kMinValue = 0;
  constexpr double kMaxValue = 500;
  static std::uniform_real_distribution<double> distribution(kMinValue,
                                                             kMaxValue);
  static std::default_random_engine generator;
  std::vector<double> v(size);
  std::generate(v.begin(), v.end(), []() { return distribution(generator); });
  return v;
}

// TODO: copy-pase from HW2. Make common if time allows
void write_time_to_csv(std::string filename,
                       const std::vector<int64_t>& execution_times) {
  std::ofstream csv_file(filename);
  csv_file << "Execution time, nanoseconds\n";
  for (const auto& time : execution_times) {
    csv_file << time << "\n";
  }
}

// Not thread-safe in any way, will work only for linear workflow
struct TimeContainerFiller {
  TimeContainerFiller(std::vector<int64_t>& time_container)
      : time_container_(time_container) {
    start_ = std::chrono::high_resolution_clock::now();
  }
  ~TimeContainerFiller() {
    auto end = std::chrono::high_resolution_clock::now();
    auto duration =
        std::chrono::duration_cast<std::chrono::microseconds>(end - start_)
            .count();
    time_container_.push_back(duration);
  }

 private:
  std::chrono::time_point<std::chrono::high_resolution_clock> start_;
  std::vector<int64_t>& time_container_;
};

template <typename T>
void PrintVector(const std::vector<T>& vector) {
  std::cout << "Size: " << vector.size() << std::endl;
  for (const auto& val : vector) {
    std::cout << val << " ";
  }
  std::cout << std::endl;
}

template <typename T>
void PrintMatrix(const std::vector<T>& vector, int width) {
  std::cout << "Size: " << vector.size() << std::endl;
  for (int row = 0; row < vector.size(); row++) {
  }
  int idx = 0;
  std::cout << "[";
  for (const auto& val : vector) {
    if (idx % width == 0) {
      if (idx != 0) {
        std::cout << "]," << std::endl;
      }
      std::cout << "[";
    }
    std::cout << val;
    if (idx % width != width - 1) {
      std::cout << ", ";
    }
    idx++;
  }
  std::cout << "]]" << std::endl;
}

int main() {
  constexpr std::size_t kMaxMatrixSize = 5;
  constexpr double kThreshold = 250.0;
  std::vector<std::string> experiment_names = {
      "matrix_multiplication", "threshold", "reversed_threshold",
      "element_wise_sum", "sum"};

  std::map<std::string, std::vector<int64_t>> execution_times;

  for (const auto& experiment_name : experiment_names) {
    execution_times[experiment_name] = std::vector<int64_t>();
    execution_times[experiment_name].reserve(kMaxMatrixSize);
  }

  for (int array_size = 1; array_size <= kMaxMatrixSize; array_size++) {
    // And pretend this is a matrix
    auto first_matrix = generate_random_vector(array_size * array_size);
    auto second_matrix = generate_random_vector(array_size * array_size);
    auto result = std::vector<double>(array_size * array_size, 0.0);

    {
      TimeContainerFiller timer(
          execution_times[std::string("matrix_multiplication")]);
      // PrintMatrix(first_matrix, array_size);
      // PrintMatrix(second_matrix, array_size);
      matrix_multiply(first_matrix.data(), second_matrix.data(), array_size,
                      array_size, result.data());
      // PrintMatrix(result, array_size);
      (void)result;
    }
    {
      TimeContainerFiller timer(execution_times["threshold"]);
      threshold(first_matrix.data(), array_size * array_size, kThreshold,
                result.data());
      (void)result;
    }
    {
      TimeContainerFiller timer(execution_times["reversed_threshold"]);
      reversed_threshold(first_matrix.data(), array_size * array_size,
                         kThreshold, result.data());
      (void)result;
    }
    {
      TimeContainerFiller timer(execution_times["element_wise_sum"]);
      add(first_matrix.data(), second_matrix.data(), array_size * array_size,
          result.data());
      (void)result;
    }
    {
      TimeContainerFiller timer(execution_times["element_wise_sum"]);
      PrintVector(first_matrix);
      auto sum_result = sum(first_matrix.data(), array_size * array_size);
      PrintVector<double>({sum_result});
      (void)sum_result;
    }
  }

  for (const auto& experiment_name : experiment_names)
    write_time_to_csv(experiment_name + ".csv",
                      execution_times[experiment_name]);

  return 0;
}

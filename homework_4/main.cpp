#include <stdlib.h>

#include <algorithm>
#include <chrono>
#include <ctime>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "matrix_manipulation.cuh"

// TODO: copy-pase from HW2. Make common if time allows
// Credit
// https://stackoverflow.com/questions/2704521/generate-random-double-numbers-in-c
// TODO: Hack to avoid generator functions with parameters
const double fMin = 0.0;
const double fMax = 500;
double fRand() {
  double f = (double)rand() / RAND_MAX;
  return fMin + f * (fMax - fMin);
}

// TODO: copy-pase from HW2. Make common if time allows
// Credit
// https://stackoverflow.com/questions/21516575/fill-a-vector-with-random-numbers-c
std::vector<double> generate_random_vector(std::size_t size) {
  std::srand(unsigned(std::time(nullptr)));
  std::vector<double> v(size);
  std::generate(v.begin(), v.end(), fRand);
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

void matrix_multiply(const double* lhs, const double* rhs, int width,
                     int height, double* result) {}

// void threshold(const double* array, int data_size, double threshold,
//                double* result) {}

void reversed_threshold(const double* array, int data_size, double threshold,
                        double* result) {}
void element_wise_sum(const double* lhs, const double* rhs, int data_size,
                      double* result) {}

double sum(double* array, int data_size) {
  double result = 0.0;
  return result;
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

int main() {
  constexpr std::size_t kMaxMatrixSize = 15;
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

      matrix_multiply(first_matrix.data(), second_matrix.data(), array_size,
                      array_size, result.data());
      (void)result;
    }
    {
      TimeContainerFiller timer(execution_times["threshold"]);
      for (const auto& val : first_matrix) {
        std::cout << val << " ";
      }
      std::cout << std::endl;
      homework_4::threshold(first_matrix.data(), array_size * array_size,
                            kThreshold, result.data());

      std::cout << result.size() << std::endl;
      for (const auto& val : result) {
        std::cout << val << " ";
      }
      std::cout << std::endl;
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
      element_wise_sum(first_matrix.data(), second_matrix.data(),
                       array_size * array_size, result.data());
      (void)result;
    }
    {
      TimeContainerFiller timer(execution_times["element_wise_sum"]);
      auto sum_result = sum(first_matrix.data(), array_size * array_size);
      (void)sum_result;
    }
  }

  for (const auto& experiment_name : experiment_names)
    write_time_to_csv(experiment_name + ".csv",
                      execution_times[experiment_name]);

  return 0;
}

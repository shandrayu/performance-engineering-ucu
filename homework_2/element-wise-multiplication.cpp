#include <immintrin.h>

#include <algorithm>
#include <cassert>
#include <chrono>
#include <ctime>
#include <fstream>
#include <string>
#include <vector>

// Credit
// https://stackoverflow.com/questions/2704521/generate-random-double-numbers-in-c
// TODO: Hack to avoid generator functions with parameters
const double fMin = 0.0;
const double fMax = 500;
double fRand() {
  double f = (double)rand() / RAND_MAX;
  return fMin + f * (fMax - fMin);
}

// Credit
// https://stackoverflow.com/questions/21516575/fill-a-vector-with-random-numbers-c
std::vector<double> generate_random_vector(std::size_t size) {
  std::srand(unsigned(std::time(nullptr)));
  std::vector<double> v(size);
  std::generate(v.begin(), v.end(), fRand);
  return v;
}

std::vector<double> element_wise_multiply(const std::vector<double>& lhs,
                                          const std::vector<double>& rhs) {
  std::vector<double> result;
  assert(lhs.size() == rhs.size());
  result.reserve(lhs.size());
  for (std::size_t idx = 0; idx < lhs.size(); ++idx) {
    result.push_back(lhs[idx] * rhs[idx]);
  }
  return result;
}

std::vector<double> intristics_multiply(const std::vector<double>& lhs,
                                        const std::vector<double>& rhs) {
  std::vector<double> result;
  assert(lhs.size() == rhs.size());

  const int kDoubleStepSize = 4;
  const int kResultSize = lhs.size();
  // Resize output array to fit storeu_pd operation
  int new_size =
      kResultSize + (kDoubleStepSize - kResultSize % kDoubleStepSize);
  result.resize(new_size);

  const double* lhs_ptr = lhs.data();
  const double* rhs_ptr = rhs.data();
  double* result_ptr = result.data();
  for (int idx = 0; idx < new_size; idx += kDoubleStepSize) {
    __m256d one_vec = _mm256_loadu_pd(lhs_ptr + idx);
    __m256d other_vec = _mm256_loadu_pd(rhs_ptr + idx);
    __m256d mult_vec = _mm256_mul_pd(one_vec, other_vec);
    _mm256_storeu_pd(result_ptr + idx, mult_vec);
  }
  result.resize(kResultSize);
  return result;
}

void write_time_to_csv(std::string filename,
                       const std::vector<int64_t>& execution_times) {
  std::ofstream csv_file(filename);
  csv_file << "Execution time, nanoseconds\n";
  for (const auto& time : execution_times) {
    csv_file << time << "\n";
  }
}

int main() {
  const std::size_t kMaxArraySize = 10000;

  std::vector<int64_t> execution_times;
  execution_times.reserve(kMaxArraySize);
  std::vector<int64_t> execution_times_intristics;
  execution_times_intristics.reserve(kMaxArraySize);

  for (int array_size = 1; array_size <= kMaxArraySize; array_size ++) {
    auto first_vector = generate_random_vector(array_size);
    auto second_vector = generate_random_vector(array_size);

    auto start = std::chrono::high_resolution_clock::now();
    auto result = element_wise_multiply(first_vector, second_vector);
    auto end = std::chrono::high_resolution_clock::now();

    execution_times.push_back(
        std::chrono::duration_cast<std::chrono::nanoseconds>(end - start)
            .count());
    ///
    auto start_i = std::chrono::high_resolution_clock::now();
    auto result_i = intristics_multiply(first_vector, second_vector);
    auto end_i = std::chrono::high_resolution_clock::now();

    execution_times_intristics.push_back(
        std::chrono::duration_cast<std::chrono::nanoseconds>(end_i - start_i)
            .count());
  }

  write_time_to_csv("execution_time.csv", execution_times);
  write_time_to_csv("execution_time_intristics.csv",
                    execution_times_intristics);

  return 0;
}
#include <algorithm>
#include <cassert>
#include <chrono>
#include <ctime>
#include <fstream>
#include <string>
#include <vector>

// Credit
// https://stackoverflow.com/questions/21516575/fill-a-vector-with-random-numbers-c
std::vector<int> generate_random_vector(std::size_t size) {
  std::srand(unsigned(std::time(nullptr)));
  std::vector<int> v(size);
  std::generate(v.begin(), v.end(), std::rand);
  return v;
}

std::vector<int> element_wise_multiply(const std::vector<int>& lhs,
                                       const std::vector<int>& rhs) {
  std::vector<int> result;
  assert(lhs.size() == rhs.size());
  result.resize(lhs.size());
  for (std::size_t idx = 0; idx < lhs.size(); ++idx) {
    result.push_back(lhs[idx] * rhs[idx]);
  }
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

  for (std::size_t array_size = 1; array_size <= kMaxArraySize; ++array_size) {
    auto first_vector = generate_random_vector(array_size);
    auto second_vector = generate_random_vector(array_size);

    auto start = std::chrono::high_resolution_clock::now();
    auto result = element_wise_multiply(first_vector, second_vector);
    auto end = std::chrono::high_resolution_clock::now();

    execution_times.push_back(
        std::chrono::duration_cast<std::chrono::nanoseconds>(end - start)
            .count());
  }

  write_time_to_csv("execution_time.csv", execution_times);

  return 0;
}
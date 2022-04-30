#include <cpr/cpr.h>

#include <chrono>
#include <fstream>
#include <iostream>
#include <sstream>
#include <thread>
#include <vector>

void i_like_to_repeat_myself(int N);
void sleeping_beauty();
void avid_writer();
void does_not_download_anything_really();

int main() {
  std::cout << "Main started..." << std::endl;
  i_like_to_repeat_myself(45);
  sleeping_beauty();
  avid_writer();
  does_not_download_anything_really();
  return 0;
}

struct Timer {
  Timer(const std::string name) : name_(name) {
    std::cout << "Started " << name_ << "..." << std::endl;
    start_ = std::chrono::high_resolution_clock::now();
  }
  ~Timer() {
    auto end = std::chrono::high_resolution_clock::now();
    auto duration =
        std::chrono::duration_cast<std::chrono::microseconds>(end - start_);
    std::cout << name_ << " finished, duration " << duration.count()
              << " microseconds (" << duration.count() / 1000.f / 1000.f
              << " seconds)" << std::endl;
  }

 private:
  const std::string name_;
  std::chrono::time_point<std::chrono::high_resolution_clock> start_;
};

unsigned int fib(int order) {
  if (order == 0) return 0;
  if (order == 1) return 1;
  return fib(order - 1) + fib(order - 2);
}

void i_like_to_repeat_myself(int N) {
  Timer timer("i_like_to_repeat_myself");
  std::vector<unsigned int> fibs;
  fibs.reserve(N);
  for (auto order = 0; order < N; ++order) {
    fibs.push_back(fib(order));
  }

  std::stringstream ss;
  for (auto number : fibs) {
    ss << number << " ";
  }
  std::cout << ss.str() << std::endl;
}

void sleeping_beauty() {
  // Credits
  // https://stackoverflow.com/questions/23609507/pause-program-execution-for-5-seconds-in-c
  // https://www.geeksforgeeks.org/measure-execution-time-function-cpp/

  Timer timer("sleeping_beauty");
  const std::chrono::seconds kSleepForDuration(5);
  std::this_thread::sleep_for(kSleepForDuration);
}

void avid_writer() {
  Timer timer("avid_writer");

  const std::string kFilename = "some_file.txt";
  std::ofstream file(kFilename);
  const int kBigNumber = 10000000;
  for (auto idx = 0; idx < kBigNumber; ++idx) {
    file << idx << " ";
    const int kMagicNumber = 4;
    if (idx % kMagicNumber == 0) {
      file.flush();
    }
  }
  file.close();
}

void does_not_download_anything_really() {
  Timer timer("does_not_download_anything_really");
  const std::string kSomeRelease =
      "https://github.com/joyent/node/tarball/v0.7.1";
  cpr::Response r = cpr::Get(cpr::Url{kSomeRelease});
  std::cout << "downloaded_bytes " << r.downloaded_bytes << std::endl;
}

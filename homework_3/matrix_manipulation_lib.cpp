#include <cstdlib>

extern "C" {
void matrix_multiply(const double* lhs, const double* rhs, int width,
                     int height, double* result) {
  for (int row = 0; row < height; ++row) {
    for (int col = 0; col < width; ++col) {
      result[row * width + col] = 0;
      for (int k = 0; k < height; ++k) {
        result[row * width + col] +=
            lhs[row * width + k] * rhs[k * width + col];
      }
    }
  }
}

void threshold(const double* array, int data_size, double threshold,
               double* result) {
  for (int idx = 0; idx < data_size; ++idx) {
    if (array[idx] <= threshold) {
      result[idx] = 1;
    } else {
      result[idx] = 0;
    }
  }
}

void reversed_threshold(const double* array, int data_size, double threshold,
                        double* result) {
  for (int idx = 0; idx < data_size; ++idx) {
    if (array[idx] <= threshold) {
      result[idx] = 0;
    } else {
      result[idx] = 1;
    }
  }
}

void add(const double* lhs, const double* rhs, int data_size, double* result) {
  for (int idx = 0; idx < data_size; ++idx) {
    result[idx] = lhs[idx] + rhs[idx];
  }
}

double sum(double* array, int data_size) {
  double result = 0.0;
  for (int idx = 0; idx < data_size; ++idx) {
    result += array[idx];
  }
  return result;
}
}
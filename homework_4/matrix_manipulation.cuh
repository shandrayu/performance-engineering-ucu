#pragma once

namespace homework_4 {
void matrix_multiply(const double* lhs, const double* rhs, int width,
                     int height, double* result);
void threshold(const double* array, int data_size, double threshold,
               double* result);
void reversed_threshold(const double* array, int data_size, double threshold,
                        double* result);
void element_wise_sum(const double* lhs, const double* rhs, int data_size,
                      double* result);
double sum(double* array, int data_size);
}  // namespace homework_4

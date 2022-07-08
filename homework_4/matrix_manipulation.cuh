#pragma once

extern "C" {
void matrix_multiply(const double* lhs, const double* rhs, int width,
                     int height, double* result);
void threshold(const double* array, std::size_t data_size, double threshold,
               double* result);
void reversed_threshold(const double* array, std::size_t data_size,
                        double threshold, double* result);
void element_wise_sum(const double* first_array, const double* second_array,
                      std::size_t data_size, double* result);
double sum(double* array, std::size_t data_size);
}
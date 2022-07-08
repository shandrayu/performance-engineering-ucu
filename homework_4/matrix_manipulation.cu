#include <cuda_runtime.h>
#include <device_launch_parameters.h>
// #include <stdlib.h>
#include <stdio.h>

#include "matrix_manipulation.cuh"

namespace {
constexpr int kThreadsPerBlock = 256;

// Credit: lecture notes
inline cudaError_t checkCudaErr(cudaError_t err, const char* msg) {
  if (err != cudaSuccess) {
    fprintf(stderr, "CUDA Runtime error at %s: %s\n", msg,
            cudaGetErrorString(err));
  }
  return err;
}

__global__ void ThresholdKernel(const double* array, int data_size,
                                double threshold, double* result) {
  int idx = threadIdx.x + blockIdx.x * blockDim.x;

  if (idx >= data_size) {
    return;
  }

  const auto value = array[idx];

  result[idx] = value <= threshold ? 0 : 1;
}
}  // namespace

namespace homework_4 {
void matrix_multiply(const double* lhs, const double* rhs, int width,
                     int height, double* result) {}

void threshold(const double* array, int data_size, double threshold,
               double* result) {
  double* array_gpu;
  double* result_gpu;
  const int data_size_bytes = data_size * sizeof(double);
  cudaMalloc(&array_gpu, data_size_bytes);
  cudaMalloc(&result_gpu, data_size_bytes);
  cudaMemcpy(array_gpu, array, data_size_bytes, cudaMemcpyHostToDevice);
  checkCudaErr(cudaGetLastError(), "cudaMemcpy");

  const dim3 Threads(kThreadsPerBlock);
  const int block_x = (data_size / kThreadsPerBlock) + 1;
  const dim3 Blocks(block_x);
  ThresholdKernel<<<Blocks, Threads>>>(array_gpu, data_size, threshold,
                                       result_gpu);

  cudaMemcpy(result, result_gpu, data_size_bytes, cudaMemcpyDeviceToHost);
  checkCudaErr(cudaGetLastError(), "cudaMemcpy");

  cudaFree(array_gpu);
  cudaFree(result_gpu);
  checkCudaErr(cudaGetLastError(), "cudaFree");
}

void reversed_threshold(const double* array, int data_size, double threshold,
                        double* result) {}
void element_wise_sum(const double* lhs, const double* rhs, int data_size,
                      double* result) {}

double sum(double* array, int data_size) {
  double result = 0.0;
  return result;
}
}  // namespace homework_4
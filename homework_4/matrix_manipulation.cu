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

__global__ void ThresholdKernel(const double* array, std::size_t data_size,
                                double threshold, double* result) {
  int idx = threadIdx.x + blockIdx.x * blockDim.x;

  if (idx >= data_size) {
    return;
  }

  const auto value = array[idx];

  result[idx] = value < threshold ? 0 : 1;
}

__global__ void ReversedThresholdKernel(const double* array,
                                        std::size_t data_size, double threshold,
                                        double* result) {
  int idx = threadIdx.x + blockIdx.x * blockDim.x;

  if (idx >= data_size) {
    return;
  }

  const auto value = array[idx];

  result[idx] = value < threshold ? 1 : 0;
}

__global__ void ElementWiseSumKernel(const double* first_array,
                                     const double* second_array,
                                     std::size_t data_size, double* result) {
  int idx = threadIdx.x + blockIdx.x * blockDim.x;

  if (idx >= data_size) {
    return;
  }

  result[idx] = first_array[idx] + second_array[idx];
}
}  // namespace

namespace homework_4 {
template <typename T>
struct CudaArrayContainer {
  CudaArrayContainer(const T* data, std::size_t num_elements)
      : num_elements_(num_elements) {
    data_size_bytes_ = num_elements_ * sizeof(T);
    cudaMalloc(&gpu_data_, data_size_bytes_);
    checkCudaErr(cudaGetLastError(), "cudaMalloc");
  }
  ~CudaArrayContainer() {
    cudaFree(gpu_data_);
    checkCudaErr(cudaGetLastError(), "cudaFree");
  }
  T* GetGpuPtr() const { return gpu_data_; }
  std::size_t GetNumElements() const { return num_elements_; }
  std::size_t GetDataSizeBytes() const { return data_size_bytes_; }

  void CopyToHost(T* host_pointer) const {
    cudaMemcpy(host_pointer, GetGpuPtr(), GetDataSizeBytes(),
               cudaMemcpyDeviceToHost);
    checkCudaErr(cudaGetLastError(), "cudaMemcpy");
  }

  void CopyFromHost(const T* host_pointer) const {
    cudaMemcpy(GetGpuPtr(), host_pointer, GetDataSizeBytes(),
               cudaMemcpyHostToDevice);
    checkCudaErr(cudaGetLastError(), "cudaMemcpy");
  }

 private:
  T* gpu_data_;
  std::size_t num_elements_;
  std::size_t data_size_bytes_;
};

void matrix_multiply(const double* lhs, const double* rhs, int width,
                     int height, double* result) {}

void threshold(const double* array, std::size_t data_size, double threshold,
               double* result) {
  CudaArrayContainer<double> array_gpu(array, data_size);
  CudaArrayContainer<double> result_gpu(result, data_size);

  array_gpu.CopyFromHost(array);

  const dim3 Threads(kThreadsPerBlock);
  const int block_x = (data_size / kThreadsPerBlock) + 1;
  const dim3 Blocks(block_x);
  ThresholdKernel<<<Blocks, Threads>>>(array_gpu.GetGpuPtr(),
                                       array_gpu.GetNumElements(), threshold,
                                       result_gpu.GetGpuPtr());

  result_gpu.CopyToHost(result);
}

void reversed_threshold(const double* array, std::size_t data_size,
                        double threshold, double* result) {
  CudaArrayContainer<double> array_gpu(array, data_size);
  CudaArrayContainer<double> result_gpu(result, data_size);

  array_gpu.CopyFromHost(array);

  const dim3 Threads(kThreadsPerBlock);
  const int block_x = (data_size / kThreadsPerBlock) + 1;
  const dim3 Blocks(block_x);
  ReversedThresholdKernel<<<Blocks, Threads>>>(
      array_gpu.GetGpuPtr(), array_gpu.GetNumElements(), threshold,
      result_gpu.GetGpuPtr());

  result_gpu.CopyToHost(result);
}

void element_wise_sum(const double* first_array, const double* second_array,
                      std::size_t data_size, double* result) {
  CudaArrayContainer<double> first_array_gpu(first_array, data_size);
  CudaArrayContainer<double> second_array_gpu(second_array, data_size);
  CudaArrayContainer<double> result_gpu(result, data_size);

  first_array_gpu.CopyFromHost(first_array);
  second_array_gpu.CopyFromHost(second_array);

  const dim3 Threads(kThreadsPerBlock);
  const int block_x = (data_size / kThreadsPerBlock) + 1;
  const dim3 Blocks(block_x);
  ElementWiseSumKernel<<<Blocks, Threads>>>(
      first_array_gpu.GetGpuPtr(), second_array_gpu.GetGpuPtr(),
      first_array_gpu.GetNumElements(), result_gpu.GetGpuPtr());

  result_gpu.CopyToHost(result);
}

double sum(double* array, std::size_t data_size) {
  double result = 0.0;
  return result;
}
}  // namespace homework_4
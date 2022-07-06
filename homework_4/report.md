# Homework 4. GPGPU calculations (CUDA)

## Description

1. Two square matrixes A and B are multiplied and result is stored to C
2. Threshold of the matrix

   - if value <= threshold 0
   - 1 otherwise

3. Threshold of the matrix reversed

   - if value <= threshold 1
   - 0 otherwise

4. Sum element-wise two matrixes
5. Find sum of all elements in the matrix

## A. Create program with Python + NumPy

Same as in `homework_3/matrix_manipulation_numpy.py` but different rules for a threshold. `matrix_manipulation_numpy.threshold_reverse` corresponds to task 3, and  `matrix_manipulation_numpy.threshold` to task 2.

## B. Create program with CUDA and C/C++

## C. Create program with Python extension for CUDA C/C++ library

## D. Create program with CUDA toolkit, for example cuBLAS or NVBLAS or Thrust

Reference https://docs.nvidia.com/cuda/index.html

## Results

cmake_minimum_required(VERSION 3.14)

project(Homework4 VERSION 0.1 LANGUAGES CXX CUDA)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CUDA_STANDARD 14)

add_library(matrix_manipulation_cuda SHARED matrix_manipulation.cu)
target_compile_options(matrix_manipulation_cuda PUBLIC "$<$<CONFIG:RELEASE>:-Wall -fPIC>" )

add_library(matrix_manipulation_cublas SHARED matrix_manipulation_cublas.cpp)
# target_link_libraries(matrix_manipulation_cublas -lcublas)

add_executable(time_measurement_binary main.cpp)

target_link_libraries(time_measurement_binary PRIVATE matrix_manipulation_cuda)
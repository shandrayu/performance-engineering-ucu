cmake_minimum_required(VERSION 3.14)

project(Homework4 VERSION 0.1 LANGUAGES CXX CUDA)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CUDA_STANDARD 14)

add_library(matrix_manipulation_cuda matrix_manipulation.cu)

add_executable(time_measurement_binary main.cpp)

target_link_libraries(time_measurement_binary PRIVATE matrix_manipulation_cuda)
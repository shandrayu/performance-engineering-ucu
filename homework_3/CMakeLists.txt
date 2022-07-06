cmake_minimum_required(VERSION 3.10)

project(Homework3)
set(CMAKE_CXX_STANDARD 17)

add_library(matrix_manipulation SHARED matrix_manipulation_lib.cpp)
add_compile_options(matrix_manipulation -Wall -fPIC)

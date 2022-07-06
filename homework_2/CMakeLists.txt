cmake_minimum_required(VERSION 3.10)

project(Homework2)
set(CMAKE_CXX_STANDARD 17)

add_executable(multiplication element-wise-multiplication.cpp)
target_compile_options(multiplication PRIVATE -march=native)

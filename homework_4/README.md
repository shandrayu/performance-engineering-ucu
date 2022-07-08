# Homework 3

## CUDA setup

### Ubuntu

Install CUDA toolkit

```bash
sudo apt-get update
sudo apt-get -y install cuda
```

Add lines to `~/.bashrc` or execute in terminal.

```bash
export CUDA_HOME=/usr/local/cuda
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64 
export PATH=$PATH:$CUDA_HOME/bin
```

## How to build library

Prepare

```bash
mkdir build && cd build
cmake ..
```

Build

```bash
cmake -DCMAKE_CXX_FLAGS="-O3" . && cmake --build .
```
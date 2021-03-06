# Homework 2. Vectorization

## Experiment setup

Run and measure execution time for different size arrays. Maximum array size is 10000.

## Python

### Element-wise multiplication

![python-by-element-multiplication-10000](data/python-by-element-multiplication-10000.png)

Graph has a linear trend.

### Numpy multiplication

![python-numpy-multiplication-10000](data/python-numpy-multiplication-10000.png)

Graph also has a linear trend but the line coefficient is much smaller than in element-wise multiplication.

## C++

### O-0 optimization

Command line

```bash
cmake -DCMAKE_CXX_FLAGS="-O0" .
cmake --build .
```

![execution-time--nanoseconds-o0-10000](data/execution-time--nanoseconds-o0-10000.png)

Graph has a linear trend.

### O-3 optimization

Command line

```bash
cmake -DCMAKE_CXX_FLAGS="-O3" .
cmake --build .  
```

![execution-time--nanoseconds-o3-10000](data/execution-time--nanoseconds-o3-10000.png)

Graph is piece-wise, exponential.

### Intristics

### O-0 optimization

Command line

```bash
cmake -DCMAKE_CXX_FLAGS="-O0" .
cmake --build .  
```

![execution-time--nanoseconds-o3-10000](data/execution-time--nanoseconds-intristics-o0-10000.png)

### O-3 optimization

Command line

```bash
cmake -DCMAKE_CXX_FLAGS="-O3" .
cmake --build .  
```

![execution-time--nanoseconds-o3-10000](data/execution-time--nanoseconds-intristics-o3-10000.png)

## Conclusion

![execution-time-for-all-experiments-10000](data/execution-time-for-all-experiments-10000.png)

![execution-time-for-all-experiments-10000-zoom](data/execution-time-for-all-experiments-10000-zoom.png)

- Numpy array multiplication is a winner.
- Intristics and element-wise multiplication (O3) are almost the same for large array sizes. But intristics is better for smaller array sizes (less than 3000).

from common.tools import measure_time


@measure_time
def multiply_square_two_matrixes(lhs, rhs):
    # Doest not guarantee the square matrix as every list amy have different length
    assert(len(lhs) == len(lhs[0]))
    # Doest not guarantee the square matrix as every list amy have different length
    assert(len(rhs) == len(rhs[0]))
    assert(len(lhs) == len(rhs))
    N = len(lhs)
    result = [[0 for _ in range(N)] for _ in range(N)]

    for row in range(N):
        for col in range(N):
            for k in range(N):
                result[row][col] += lhs[row][k] * rhs[k][col]

    return result


@measure_time
def threshold(array, threshold):
    """
    1 if value <= threshold
    0 otherwise
    """
    result = [[1 if element <= threshold else 0 for element in row]
              for row in array]
    return result


@measure_time
def reversed_threshold(array, threshold):
    """
    1 if value > threshold
    0 otherwise
    """
    result = [[1 if element > threshold else 0 for element in row]
              for row in array]
    return result


@measure_time
def add(lhs, rhs):
    result = [[a + b for a, b in zip(a_row, b_row)]
              for a_row, b_row in zip(lhs, rhs)]
    return result


@measure_time
def asum(array):
    row_sum = list(map(sum, array))
    return sum(row_sum)

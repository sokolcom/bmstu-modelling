import numpy as np


def aug_matrix(matrix):
    size = len(matrix)
    result = np.array([0 for i in range(size)])
    result[size - 1] = 1
    
    return result


def coeff_matrix(_matrix):
    matrix = np.array(_matrix)
    n = len(_matrix)
    result = np.zeros((n, n))

    for state in range(n - 1):
        for col in range(n):
            result[state, state] -= matrix[state, col]
        for row in range(n):
            result[state, row] += matrix[row, state]

    for state in range(n):
        result[n - 1, state] = 1

    return result


def linalg_solve(matrix):
    return np.linalg.solve(coeff_matrix(matrix), aug_matrix(matrix))
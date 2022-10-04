import random


PRECISION = 3


def create_matrix():
    size = int(input("Введите количество состояний (< 10): "))
    if size > 10:
        raise ValueError(f"Size too big  size (size = {size} > 10)")
    
    matrix = [[] for _ in range(size)]
    print("Введите матрицу построчно:")
    for i in range(size):
        matrix[i] = list(map(float, input().split()))

    return size, matrix


def generate_matrix(size):
    return [
        [round(random.random(), PRECISION) if i != j else 0.0 for j in range(size)]
        for i in range(size)
    ]


def print_output(title, caption, data):
    print("##################")
    print(title)
    for i in range(len(data)):
        print(f"{caption}{i}", round(abs(data[i]), PRECISION))
    print("##################")


def get_predef_intensity(size):
    if size not in [4, 5]:
        raise KeyError(f"No predefined intensity matrix for 'size' = {size}")

    if size == 4:
        return [
            [0, 3, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 2],
            [3, 0, 0, 0]
        ]
    elif size == 5:
        return [
            [   0,  0.8,    0,  0.4,    0],
            [   0,    0,  2.15,   0,    0],
            [   0,  1.2,    0,  1.2,    0],
            [   2,    0,    0,    0,  0.5],
            [0.75,    0,    0,    0,    0]
        ]


def get_start_probas(n, flag=True):
    if flag:
        return [1 / n] * n
    else:
        return [1] + [0] * (n - 1)
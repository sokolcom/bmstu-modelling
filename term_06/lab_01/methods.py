import numpy as np
from numba import jit


__all__ = (
    "calculate",
    "euler_method",
    "runge_kutta_method",
    "picard_1",
    "picard_2",
    "picard_3",
    "picard_4"
)


@jit
def f(x, y):
    """u'(x) = x^2 + u^2(x)"""
    return x * x + y * y


@jit
def euler_method(x_n, y_n, h):
    """Euler's method (explicit scheme)"""
    return y_n + h * f(x_n, y_n)


@jit
def runge_kutta_method(x_n, y_n, h):
    """Runge-Kutta method (2nd order)"""

    alpha = 1  # alpha=1 or alpha=1/2
    k1 = f(x_n, y_n)
    k2 = f(x_n + h / (2 * alpha), y_n + h / (2 * alpha) * k1)
    return y_n + h * ((1 - alpha) * k1 + alpha * k2)


@jit
def picard_1(x):
    """Picard's method (1st approximation)"""
    return x ** 3 / 3


# def picard_2(x):
#     "Picard's method (2nd approximation)"
#     return picard_1(x) * (x ** 4 / 21 + 1)


# def picard_3(x):
#     "Picard's method (3rd approximation)"
#     return picard_1(x) * (x ** 12 / 19845 + 2 * x ** 8 / 693) + picard_2(x)


# def picard_4(x):
#     "Picard's method (4th approximation)"
#     return picard_1(x) * (x ** 28 / 36_625_634_325 + 4 * x ** 24 / 1_113_959_385 + 662 * x ** 20 / 3_479_404_005 + \
#         82 * x ** 16 / 12_442_815) + \
        # (picard_1(x) * 28 * x ** 12 / 19855) / 11 + picard_3(x) # 13 * x ** 12 / 72765 + 2 * x ** 8 / 693 + x ** 4 / 21 + 1)

@jit
def picard_2(x):
    """Picard's method (2nd approximation)"""
    return picard_1(x) * ((x ** 4) * (1 / 21) + 1)


@jit
def picard_3(x):
    """Picard's method (3rd approximation)"""
    return picard_1(x) * ((x ** 12) * (1 / 19845) + 2 * (x ** 8) * (1 / 693)) + picard_2(x)


@jit
def picard_4(x):
    """Picard's method (4th approximation)"""
    return picard_1(x) * ((x ** 28) * (1 / 36_625_634_325) + 4 * (x ** 24) * (1 / 1_113_959_385) + 662 * (x ** 20) * (1 / 3_479_404_005) + \
        82 * (x ** 16) * (1 / 12_442_815) + 4 * (x ** 12) * (1 / 31185)) + picard_3(x)

    # return picard_1(x) * ((x ** 28) * (1 / 36_625_634_325) + 4 * (x ** 24) * (1 / 1_113_959_385) + 662 * (x ** 20) * (1 / 3_479_404_005) + \
    #     82 * (x ** 16) * (1 / 12_442_815)) + \
    #     (picard_1(x) * 28 * (x ** 12) * (1 / 19855)) / 11 + picard_3(x)  # 13 * (x ** 12) * (1 / 72765) + 2 * (x ** 8) * (1 / 693) + (x ** 4) * (1 / 21) + 1)


def calculate(method, start=1, end=2, step=1e-7):
    picards = [picard_1, picard_2, picard_3, picard_4]
    # x_values, y_values = np.array([start, ], dtype=np.float64), np.array([start, ], dtype=np.float64)
    x_values, y_values = [2.0, ], [317.6217834, ]

    for current in np.arange(start + step, end + step, step):
        result = method(current - step, y_values[-1], step) if method not in picards else method(current)

        if result <= 10e+300:
            x_values.append(round(current, 5)), y_values.append(round(result, 8)) # = np.append(x_values, round(current, 5)), np.append(y_values, round(result, 8))
        else:
            break
            # x_values.append(round(current, 5)), y_values.append(round(result, 8)) # = np.append(x_values, round(current, 5)), np.append(y_values, float('inf'))
            
    return (x_values, y_values)

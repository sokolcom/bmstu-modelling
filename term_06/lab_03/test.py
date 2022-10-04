import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.interpolate import InterpolatedUnivariateSpline
from decimal import *


def my_alpha(x):
    return interpolate(x, T_lambda_table[0], T_lambda_table[1])


def my_k(x):
    return interpolate(x, T_k_table[1], T_k_table[0])


def p(x):
    return (4 * (my_k(x)**4) * n_p * n_p * sigma)*x


def f(x):
    return 4 * x * n_p * n_p * sigma * T0


def A(n):
    return approc_plus_half(my_alpha, n) / h


def C(n):
    return approc_minus_half(my_alpha, n) / h


def B(n):
    return A(n) + C(n) + p(n) * h


def D(n):
    return f(n) * h


def approc_plus_half(func, n):
    return (func(n) + func(n + h)) / 2


def approc_minus_half(func, n):
    return (func(n - h) + func(n)) / 2


def left():
    k0 = approc_plus_half(my_k, 0) + (h * h * approc_plus_half(p, 0) / 8) + ((h * h * p(0)) / 4)
    M0 = -approc_plus_half(my_k, 0) + (h * h * approc_plus_half(p, 0) / 8)
    P0 = h * F0 + (h * h / 4) * (approc_plus_half(f, 0) + f(0))
    return k0, M0, P0


def right():
    kN = (approc_minus_half(my_k, N) / h) - (h * approc_minus_half(p, N) / 8)
    MN = -my_alpha(N) - (approc_minus_half(my_k, N) / h) - (h * p(N) / 4) - (h * approc_minus_half(p, N) / 8)
    PN = -(h / 4) * (f(N) + approc_minus_half(f, N)) - T0 * my_alpha(N)
    return kN, MN, PN


def interpolate(x, first_ar, second_ar):
    order = 1
    s = InterpolatedUnivariateSpline(first_ar, second_ar, k=order)
    return float(s(float(x)))


def find_abs_max_y(y_n, len):
    cur_max = -1e10
    for i in range(len-1):
        if (abs((y_n[i+1]-y_n[i])/y_n[i+1]) > cur_max):
            cur_max = abs((y_n[i+1]-y_n[i])/y_n[i+1])
    if ((cur_max <= eps_1) and (cur_max != -1e10)):
        return False
    # print(cur_max)
    return True


def simpson(func, left, right, n):
    h = (right - left) / n
    ans = h / 3
    even = 0.0
    odd = 0.0
    for i in range(1, n):
        if i % 2 == 0:
            even += func(left + h * i)
        else:
            odd += func(left + h * i)
    ans *= (2 * even + 4 * odd + func(left) + func(right))
    return ans


def f_2():
    func = lambda x: x*(my_k(x)**4 - T0**4)
    integral = simpson(func, 0, l, 41)
    return 4 * n_p * n_p * sigma * integral


def f_1():
    return F0 - alpha * (2400 - T0)


def find_abs_max_f(s):
    cur_max = -1e10
    for i in range(1, s):
        if (abs((f_1() ** i - f_2() ** i) / f_1() ** i) > cur_max):
            cur_max = abs((f_1() ** i - f_2() ** i) / f_1() ** i)
    if ((cur_max <= eps_2) and (cur_max != -1e10)):
        return False
    return True


if __name__ == "__main__":
    h = 1e-3
    N = 0.2
    eps_1 = 1e-2
    eps_2 = 2e-2
    n_p = 1.4
    l = 0.2
    T0 = 300
    sigma = 5.668 * 1e-12
    F0 = 100
    alpha = 0.05
    T_lambda_table = [
        [300, 500, 800, 1100, 2000, 2400],
        [1.36 * 1e-2, 1.63 * 1e-2, 1.81 * 1e-2, 1.98 * 1e-2, 2.5 * 1e-2, 2.74 * 1e-2]
    ]
    T_k_table = [
        [293, 1278, 1528, 1677, 2000, 2400], 
        [2 * 1e-2, 5 * 1e-2, 7.8 * 1e-2, 1 * 1e-1, 1.3 * 1e-1, 2 * 1e-1]
    ]
    cnt = 0
    y_n = [0]*200
    x = h
    n = 1
    # t = [0] * (n + 1)
    while ((cnt < 200) and (find_abs_max_y(y_n, cnt)) and (find_abs_max_f(cnt))):
        k0, M0, P0 = left()
        kN, MN, PN = right()
        eps = [0, -M0 / k0]
        eta = [0, P0 / k0]
        x = h
        n = 1
        while x + h < N:
            eps.append(C(x) / (B(x) - A(x) * eps[n]))
            eta.append((A(x) * eta[n] + D(x)) / (B(x) - A(x) * eps[n]))
            n += 1
            x += h
        t = [0] * (n + 1)
        t[n] = (PN - MN * eta[n]) / (kN + MN * eps[n])
        for i in range(n - 1, -1, -1):
            t[i] = (eps[i + 1] * t[i + 1] + eta[i + 1])
        y_n[cnt] = t[n]
        cnt +=1
        h = h / 2

    x = [i for i in np.arange(0, N, h)]
    plt.plot(x, t)
    plt.xlabel("x, cm")
    plt.ylabel("temperature, K")
    plt.grid()
    plt.show()
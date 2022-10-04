import numpy as np

from distribution import *
from visualize import *






def main():
    print("Равномерное распределение")
    n = int(input("Введите количество равномерных функций распределения: "))
    a = list(map(float, input(f"Введите a ({n} раз): ").split()))[:n]
    b = list(map(float, input(f"Введите b ({n} раз): ").split()))[:n]
    l = (b[-1] - a[0]) / 2
    x = np.arange(a[0] - l, b[-1] + l, 1e-3)

    f_res = [[func_uniform(current_x, aa, bb) for current_x in x] for aa, bb in zip(a, b)]
    cdf_res = [[density_uniform(current_x, aa, bb) for current_x in x] for aa, bb in zip(a, b)]
    create_graphs(x, f_res, cdf_res, "Равномерное распределение", a=a, b=b)

    print("#####################")

    print("Нормальное распределение")
    n = int(input("Введите количество нормальных функций распределения: "))
    mu = list(map(float, input(f"Введите mu ({n} раз): ").split()))[:n]
    sigma = list(map(float, input(f"Введите sigma ({n} раз): ").split()))[:n]

    f_res = [[func_normal(current_x, m, s) for current_x in x] for m, s in zip(mu, sigma)]
    cdf_res = [[density_normal(current_x, m, s) for current_x in x] for m, s in zip(mu, sigma)]
    create_graphs(x, f_res, cdf_res, "Нормальное распределение", mu=mu, sigma=sigma)


if __name__ == '__main__':
    main()

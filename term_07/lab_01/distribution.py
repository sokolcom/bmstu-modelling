import math
from scipy.stats import norm


def func_uniform(x, a, b):
    if (a <= x) and (x < b):
        return (x - a) / (b - a)
    elif (x < a):
        return 0
    else:
        return 1

def density_uniform(x, a, b):
    if (a <= x) and (x <= b):
        return 1 / (b - a)
    else:
        return 0


def func_normal(x, m, q):
    return norm.cdf(x, loc=m, scale=q)


def density_normal(x, m, q):
    return (1 / math.sqrt(2 * math.pi + pow(q, 2))) * pow(math.e, -0.5 * pow((x - m)/q, 2))

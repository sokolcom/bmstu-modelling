import random
from numpy.random import normal


class UniformDistribution:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def yield_value(self):
        return self.a + (self.b - self.a) * random.random()


class NormalDistribution:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def yield_value(self):
        return normal(self.mu, self.sigma)

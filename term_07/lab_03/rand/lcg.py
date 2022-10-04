# Linear congruential generator
class LCGRandom:
    def __init__(self):
        self.current = 10
        self.m = 2. ** 31
        self.a = 1594525
        self.c = 1123504223

    def generate(self, low=0, high=100):
        self.current = (self.a * self.current + self.c) % self.m
        result = int(low + self.current % (high - low))
        return result

from itertools import islice
from os.path import join, abspath, curdir

from .lcg import LCGRandom


COUNT = 10000


def rand_table():
    numbers = set()
    with open(join(abspath(curdir), "rand/integers.txt"), "r") as file: 
        line_num = 0
        lines = islice(file, line_num, None)
        for l in lines:
            numbers.update(set(l.split(" ")[1:-1]))
            line_num += 1
            if len(numbers) >= 3 * COUNT + 1:
                break
        numbers.remove("") 
        numbers = list(numbers)[:3*COUNT]

    one_digit = [int(i) % 10 for i in numbers[:COUNT]]
    two_digits = [int(i) % 90 + 10 for i in numbers[COUNT : COUNT * 2]]
    three_digits = [int(i) % 900 + 100 for i in numbers[COUNT * 2 : 3 * COUNT]]
    return one_digit, two_digits, three_digits


def rand_algorithmic():
    random = LCGRandom()
    one_digit = [random.generate(0, 10) for i in range(COUNT)]
    two_digits = [random.generate(10, 100) for i in range(COUNT)]
    three_digits = [random.generate(100, 1000) for i in range(COUNT)]
    return  one_digit, two_digits, three_digits

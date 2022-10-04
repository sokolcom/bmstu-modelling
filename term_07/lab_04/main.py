from apparatus.event_model import event_model
from apparatus.step_model import step_model
from apparatus.distribution import *


def main():
    a, b = 1, 11
    generator = UniformDistribution(a, b)

    mu, sigma = 6, 0.2
    handler = NormalDistribution(mu, sigma)

    total_tasks = int(input("Number of tasks: "))
    repeat_percentage = int(input("Repeat percentage: "))
    step = 0.01

    print("Max queue length:")
    print('\tStep model:\t', step_model(generator, handler, total_tasks, repeat_percentage, step))
    print('\tEvent model:\t', event_model(generator, handler, total_tasks, repeat_percentage))


if __name__ == '__main__':
    main()

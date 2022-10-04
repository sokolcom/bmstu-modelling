from prettytable import PrettyTable
import numpy as np

from methods import *


def welcome():
    print("\
        #############################\n\
        ##### MODELLING LAB #01 #####\n\
        #############################\n"
    )
    print("\
        \r{ u'(x) = x^2 + u^2(x)\n\
        \r{ u(0) = 0\n"
    )


def enter_data():
    start = float(input("Enter START of the range:\t"))
    stop = float(input("Enter STOP of the range:\t"))
    step = float(input("Enter STEP in the range:\t"))
    return (start, stop, step)


if __name__ == "__main__":
    # print(0.1234 ** 12 / 19845 + 2 * 0.1234 ** 8 / 693)
    # print((11 * 0.1234 ** 12 + 630 * 0.1234 ** 8) / 218295)
    # print((0.1234 ** 12 + 21) / 21)
    welcome()
    start, stop, step = enter_data()

    # print(np.arange(0, 1 + 0.1, 0.1))
    # print(int((stop - start) / step) + 1)
    # print(np.linspace(start, stop, int((stop - start) / step) + 1, dtype='float32'))

    output_table = PrettyTable()
    # output_table.add_column("X", [round(i, 5) for i in np.arange(start, stop + step, step)], align='l')
    # output_table.add_column("Picard (1st approx.)", calculate(picard_1, start, stop, step)[1], align='l')
    # output_table.add_column("Picard (2nd approx.)", calculate(picard_2, start, stop, step)[1], align='l')
    # output_table.add_column("Picard (3rd approx.)", calculate(picard_3, start, stop, step)[1], align='l')
    # output_table.add_column("Picard (4th approx.)", calculate(picard_4, start, stop, step)[1], align='l')
    # output_table.add_column("Euler (explicit)", calculate(euler_method)[1], align='l')
    # output_table.add_column("Runge-Kutta (2nd order)", calculate(runge_kutta_method, start, stop, step)[1], align='l')

    a = calculate(runge_kutta_method, start, stop, step)[1]
    b = calculate(runge_kutta_method, start, stop, step)[1]
    print("Math's done!")
    print(len(a), len(b))
    print(a[-1], b[-1])


    with open("output.txt", "w") as f:
        f.write(f"{a} \n\n\n\n {b}")
    
    if len([round(i, 5) for i in np.arange(start, stop + step, step)]) > 100:
        print("Table is too large!\nCheck output.txt for the result")
    else:
        print(output_table)

    
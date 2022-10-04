from prettytable import PrettyTable

from rand.generator import rand_table, rand_algorithmic
from rand.utils import calc_chi


def main():
    numbers = [i for i in range(10)]
    table_tbl = PrettyTable()
    one_tbl, two_tbl, three_tbl = rand_table()

    table_tbl.add_column("№", numbers)
    table_tbl.add_column('1 разряд', one_tbl[:10])
    table_tbl.add_column('2 разряд', two_tbl[:10])
    table_tbl.add_column('3 разряд', three_tbl[:10])
        
    one_alg, two_alg, three_alg = rand_algorithmic()
    one_alg, two_alg, three_alg = rand_algorithmic()
    table_tbl.add_column('1 разряд', one_alg[:10])
    table_tbl.add_column('2 разряд', two_alg[:10])
    table_tbl.add_column('3 разряд', three_alg[:10])
    
    table_tbl.add_row([
        'Коэффициент Хи-квадрат',
        calc_chi(one_tbl, 10000, 0 , 10),
        calc_chi(two_tbl, 10000,10, 100),
        calc_chi(three_tbl, 10000, 100, 1000),
        calc_chi(one_alg, 10000, 0 , 10),
        calc_chi(two_alg, 10000, 10, 100),
        calc_chi(three_alg, 10000, 100, 1000)
    ])

    print("\t\t\t\t--Табличный метод--\t\t\t\t\t\t\t--Алгоритмический метод--")
    print(table_tbl)
    

if __name__ == '__main__':
    main() 

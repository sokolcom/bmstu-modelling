
def calc_chi(arr, n, start, end): 
    tab = [0 for i in range(start + end)]
    for i in range(n):
        tab[arr[i]] += 1
    s = 0
    for i in tab:
        s += i * i

    return s * (end - start) / n - n

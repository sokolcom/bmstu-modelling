import math
import pprint

tableI = (
    [0.5, 6400, 0.4],
    [1.0, 6790, 0.55],
    [5.0, 7150, 1.7],
    [10.0, 7270, 3],
    [50.0, 8010, 11],
    [200.0, 9185, 32],
    [400.0, 10010, 40],
    [800.0, 11140, 41],
    [1200.0, 12010, 39])


def linInterpol(I, tbl, index=1):
        if I <= tbl[0][0]:
                return tbl[0][index]
        elif I > tbl[len(tbl)-1][0]:
                return tbl[len(tbl)-1][index]
        else:
                for i in range(len(tbl)-1):
                        if tbl[i][0] < I <= tbl[i+1][0]:
                                return tbl[i][index] + \
        (tbl[i+1][index] - tbl[i][index])/(tbl[i+1][0] - tbl[i][0])*(I - tbl[i][0])

tableSigm = (
    [4000,  0.031],
    [5000, 0.27],
    [6000, 2.05],
    [7000, 6.06],
    [8000, 12],
    [9000, 19.9],
    [10000, 29.6],
    [11000, 41.1],
    [12000, 54.1],
    [13000, 67.7],
    [14000, 81.5])


def logInterpol(T, tbl, index=1):
    if T <= tbl[0][0]:
        return tbl[0][index]
    elif T > tbl[len(tbl)-1][0]:
        return tbl[len(tbl)-1][index]
    else:
        for i in range(len(tbl)-1):
                if tbl[i][0] < T <= tbl[i+1][0]:
                        return math.exp(math.log(tbl[i][index]) +\
(math.log(tbl[i+1][index]) - math.log(tbl[i][index]))*(T - tbl[i][0])/(tbl[i+1][0] - tbl[i][0]))


# calculating an integral by Simpson's method
def simpsonIntegr(a, b, func, stepcnt=41):
	if(stepcnt and stepcnt%2 == 1):
		step = (b-a)/(stepcnt-1)
		ret = func(a) + func(b)

		for i in range(1, stepcnt-1):
			a += step
			if i%2 == 1:
				ret += 4*func(a)
			else:
				ret += 2*func(a)

		return ret*step/3


def specialSimpson(I):
    R = 0.35

    zList = [r*1.0/40 for r in range(41)]
    # print(zList)
    res = logInterpol(getT(I,zList[0]), tableSigm)*zList[0] +\
     logInterpol(getT(I,zList[40]), tableSigm)*zList[40]

    for i in range(1, 40):
        if i%2 == 1:
            res += 4*logInterpol(getT(I,zList[i]), tableSigm)*zList[i]
        else:
            res += 2*logInterpol(getT(I,zList[i]), tableSigm)*zList[i]

    return (res*1.0/40)/3


def integrFunc(x):
	return x*(T0 + (Tw - T0)*x**n)


def getT(I, z):
    T_w = 2000
    T_0 = linInterpol(I,tableI, index=1)
    n = linInterpol(I, tableI, index=2)
    #print("T_0 =", T_0, "; n =", n)
    #print(I, z)
    #print(T_0, T_w , z, n)
    return T_0 + (T_w - T_0)*z**n


def getR(I):
    l_e = 12 #sm
    R = 0.35 #1sm
    #sigm = simpsonIntegr(0, 1, lambda z: z*(T_0 + (T_w - T_0)*z**n))
    #sigm
    return l_e/(2*math.pi*R*R*specialSimpson(I))


def dU(I):
#def dU(t, U_c, I):
    C_k = 150e-6
    return -I/C_k


def dI(I, U_c):
#def dI(t, U_c, I):
    R_k = 0.5
    L_k = 60e-6
    R_p = getR(I)
    return (U_c - I*(R_k + R_p))/L_k


def difRungeKutta(dt, I_n, U_n):
    m1 = dU(I_n)
    k1 = dI(I_n, U_n)

    m2 = dU(I_n + dt*k1/2)
    k2 = dI(I_n + dt*k1/2, U_n + dt*m1/2)

    m3 = dU(I_n + dt*k2/2)
    k3 = dI(I_n + dt*k2/2, U_n + dt*m2/2)

    m4 = dU(I_n + dt*k1/2)
    k4 = dI(I_n + dt*k3, U_n + dt*m3)

    U_n1 = U_n + dt*(m1 + 2*m2 + 2*m3 + m4)/6
    I_n1 = I_n + dt*(k1 + 2*k2 + 2*k3 + k4)/6

    return I_n1, U_n1


def printArr(arr):
    s = ""
    for i in arr:
        s+= str(i)+ " "
    print(s)

if __name__ == "__main__":
    t_n = 2e-4
    step_num = 2000
    dt = t_n/(step_num-1)
    print(step_num)

    I_0 = 0.5
    U_0 = 1500
    R = getR(I_0)

    data = [[0, I_0, U_0, R]]
    #!!!
    # print(data[0])
    printArr(data[0])
    for i in range(1, step_num):
        I, U = difRungeKutta(dt, data[i-1][1], data[i-1][2])
        #U, I = Runge_Kutta_IV_3var_1step(dI, dU, dt, data[i-1][2], data[i-1][1], dt)
        R = getR(I)
        data.append([dt*i, I, U, R])
        printArr(data[i])
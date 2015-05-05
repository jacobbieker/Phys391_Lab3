__author__ = 'Jacob'
#8.10
import numpy as np
import matplotlib.pyplot as pyplot
import math

x=[1,2,3]
y=[2,3,2]
un=[0.5,0.5,1]
no_w_w = [1,1,1]
no_w = [1, 1, 1, 1, 1]
x_pressure = [79, 82, 85, 88, 90]
y_temperature = [8, 17, 30, 37, 52]

#should satify y = y0 * e^ (-t/tau)
#Which is z = ln(y) = ln(y0) - t/tau
x_time = [10, 20, 30, 40, 50]
y_number = [409, 304, 260, 192, 170]

#Define sums

def sumwx(a,b,c): #x,y,uncertainty respectively
	return sum( [a[i]/(c[i]**2) for i in range(len(c))] )

def sumw(a,b,c):
	return sum( [1/(c[i]**2) for i in range(len(c))] )

def sumwy(a,b,c):
	return sum( [b[i]/(c[i]**2) for i in range(len(c))] )

def sumwx2(a,b,c):
	return sum( [a[i]**2/(c[i]**2) for i in range(len(c))] )

def sumwxy(a,b,c):
	return sum( [a[i]*b[i]/(c[i]**2) for i in range(len(c))] )

def delta(a,b,c): #referring to x, y, and uncertainties respectively
	return sumw(a,b,c) * sumwx2(a,b,c) - (sumwx(a,b,c))**2

#Equations for A and B
def A(a,b,c):
	return ( sumwx2(a,b,c)*sumwy(a,b,c) - sumwx(a,b,c)*sumwxy(a,b,c) ) / delta(a,b,c)

def B(a,b,c):
	return ( sumw(a,b,c)*sumwxy(a,b,c) - sumwx(a,b,c)*sumwy(a,b,c) ) / delta(a,b,c)

def sum_tabp(T, A, B, P):
    return sum( [(T[i] - A -B*P[i]) ** 2 for i in range(len(P))] )


def sigma_y(T, A, B, P):
    return (math.sqrt( (1/(5 - 2)) * sum_tabp(T, A, B, P)))


def sigma_a(sigma_y_val, sump2, delta):
    return sigma_y_val * math.sqrt(sump2/delta)

print A(x, y, un)
print B(x, y, un)

weighted = []
unweighted = []
for value in x:
    point = A(x,y,un) + B(x,y,un) * value
    weighted.append(point)
    un_point = A(x,y,no_w_w) + B(x,y,no_w_w) * value
    unweighted.append(un_point)

fig1 = pyplot.figure(1)

print  math.sqrt(sumwx2(x,y,un) / delta(x,y,un))
print math.sqrt(sumw(x,y,un) / delta(x,y,un))
weighted_plot = fig1.add_subplot(111)
unweighted_plot = fig1.add_subplot(111)
weighted_plot.plot(x, weighted)
unweighted_plot.plot(x, unweighted)
points_plot = fig1.add_subplot(111)
points_plot.errorbar(x, y, yerr=un, linestyle='None')
pyplot.ylim(0, 3.8)
pyplot.xlim(0.8, 3.5)
pyplot.show()


print ("Pressure and Temp")
print A(x_pressure, y_temperature, no_w)
print B(x_pressure, y_temperature, no_w)
A_expected = -273
A_calc = A(x_pressure, y_temperature, no_w)
B_calc = B(x_pressure, y_temperature, no_w)
simga_y_value = sigma_y(y_temperature, A_expected, B_calc, x_pressure)
simga_y1_value = sigma_y(y_temperature, A_calc, B_calc, x_pressure)
print ( "Sigma_T: " + str(simga_y_value))
print ( "Sigma_T1: " + str(simga_y1_value))
print sigma_a(simga_y_value, sumwx2(x_pressure, y_temperature, no_w), delta(x_pressure, y_temperature, no_w))

print ("Time And Number")
print A(x_time, y_number, no_w)
print B(x_time, y_number, no_w)
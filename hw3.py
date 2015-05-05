from __future__ import division
__author__ = 'Jacob'
import math
import numpy as np
import matplotlib.pyplot as pyplot

x = [1, 3, 5]
y = [6, 5, 1]

print np.polyfit(x,y,1)

x_1 = [1, 2, 3]
y_1 = [2, 3, 2]
y_1_err = [0.5, 0.5, 1]

x_pressure = [79, 82, 85, 88, 90]
y_temperature = [8, 17, 30, 37, 52]

#should satify y = y0 * e^ (-t/tau)
#Which is z = ln(y) = ln(y0) - t/tau
x_time = [10, 20, 30, 40, 50]
y_number = [409, 304, 260, 192, 170]


def values(x_vals, y_vals, x_err=[], y_err=[]):
    x_sq = []
    sum_y = 0
    sum_w_y = 0
    sum_x = 0
    sum_w_x = 0
    sum_xy = 0
    sum_w_xy = 0
    sum_x_sqr = 0
    sum_w_x_sqr = 0
    num_values = 0
    weight = []
    sigma_A = 0
    sigm_B = 0
    print len(y_err)
    if len(y_err) is not 0:
        for value in y_err:
            weight.append(1 / (value ** 2))

    for index, value in enumerate(x_vals):
        sum_x += value
        x_sq.append(value * value)
        sum_xy += (value + y_vals[index])
        sum_x_sqr += value * value
        num_values += 1
        sum_y += y_vals[index]
        print ("Number: " + str(num_values))
        print ("Sum X2: " + str(sum_x_sqr))
        print ("Sum XY: " + str(sum_xy))
        print ("X2: " + str(value * value))
        print ("Sum X: " + str(sum_x))
    delta = (num_values * sum_x_sqr - sum_x * sum_x)
    A = ((sum_x_sqr * sum_y) - (sum_x * sum_xy)) / delta
    B = ((num_values * sum_xy) - (sum_x * sum_y)) / delta
    weighted_A = ((sum_x_sqr * sum_y) - (sum_x * sum_xy)) / delta
    weighted_B = ((num_values * sum_xy) - (sum_x * sum_y)) / delta
    print [A, B]
    print [weighted_A, weighted_B]

values(x_1, y_1, y_err=y_1_err)
values(y_temperature, x_pressure)
values(x_pressure, y_temperature)
values(x_time, y_number)
from __future__ import division
__author__ = 'Jacob'
import numpy as np
import matplotlib.pyplot as pyplot
import math

bead_size = 3.2 #um
temp = 23.1 #C


'''
Calibrating the Scale per pixel
'''


def pythag(a,b):
    return math.sqrt((a ** 2) + (b ** 2))


calibration_file = 'calibration.txt'

cal_time = []
cal_x = []
cal_y = []

with open(calibration_file, 'r') as cal:
    cal.readline()
    cal.readline()
    for line in cal:
        line.strip()
        col = line.split()
        cal_time.append(col[0])
        cal_x.append(col[1])
        cal_y.append(col[2])

print cal_time
print cal_x
print cal_y

x_scale = pythag(.32, float(cal_x[1]) - float(cal_x[0]))

y_scale = pythag(0, float(cal_y[3]) - float(cal_y[2]))

print x_scale
print y_scale

scaled_x = x_scale/0.15 #scale of pixels per millimeter
scaled_y = y_scale/0.15 #scale of y axis pixel per millimeter

# End of calibration section
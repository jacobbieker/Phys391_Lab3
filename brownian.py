from __future__ import division
__author__ = 'Jacob'
import numpy as np
import matplotlib.pyplot as pyplot

bead_size = 3.2 #um
temp = 23.1 #C


'''
Calibrating the Scale per pixel
'''
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



# End of calibration section
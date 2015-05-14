from __future__ import division
__author__ = 'Jacob'
import numpy as np
import matplotlib.pyplot as pyplot
import math

bead_size = 3.2 #um
temp = 23.1 #C
time_array = []
TwoDdeltaT_array = []
d_var_array = []
delta_r_2_array = []
delta_r_2_error_array = []
#ERROR: size of one microbead for each calibration one diameter for the
#delta R^2 graph is sigma squared vs D deltaT
#Find error of slope
#Error for measured quantities in everything
#Actually estimate the error in calibration: a couple pixels from each edge, ie 3 or 4 pixels total and one microbead diameter 3.2 um for each X and Y
#Plotting 2DDeltaT in graph, because that equals 2 sigma
#Delta_r_2 - (Delta_r)^2 is not the same as before, since Delta_r is always positive
#Error found through SDOM except for DeltaK
'''
Basic functions to call later
'''


def power_error(power, frac_uncertainty):
    return power * frac_uncertainty


def frac_error(error, true_value):
    return error / abs(true_value)


def quad_error(b_error, v_error):
    return math.sqrt((b_error ** 2) + (v_error ** 2))


def standard_dev(set_of_values, avg_value):
    #Finds Standard Deviation for V
    diffsquared = 0
    sum_diffsquared = 0
    std_dev = 0
    for value in set_of_values:
        diffsquared = (value-avg_value)**2
        sum_diffsquared += diffsquared
        std_dev = (((sum_diffsquared)/(len(set_of_values) - 1))**(1/2))
    return std_dev


def correlation(setX_of_values, setY_of_values, x_avg, y_avg, x_err, y_err):
    sum_of_points = 0
    for index, value in enumerate(setX_of_values):
        point = (((value - x_avg) / x_err) * ((setY_of_values[index] - y_avg) / y_err))
        sum_of_points += point
    return (1 / (len(setX_of_values) - 1)) * sum_of_points

def kB(D, f, T):
    return (D * f) / T


def f(R):
    return 6 * math.pi * .001 * R


def D(delta_t, avg_axis_r):
    return avg_axis_r / (4 * delta_t)


def standard_dev_sd(number_of_measurements):
    return 1 / (math.sqrt(2 * (number_of_measurements - 1)))

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

y_scale = pythag(0, float(cal_y[1]) - float(cal_y[0]))

print x_scale
print y_scale

scaled_x = x_scale/0.00015 #scale of pixels per meter
scaled_y = y_scale/0.00015 #scale of y axis pixel per meter

error_in_x = (1 / scaled_x) * 4 #Finds the distance of 4 pixels in the X direction, the estimated error in X calibration
error_in_y = (1 / scaled_y) * 4 #Finds the distance of 4 pixels in the Y direction, the estimated error in Y calibration

print ("Error in X Cal: " + str(error_in_x))
print ("Error in Y Cal: " + str(error_in_y))


# End of calibration section

'''
Converting the pixel values in data to the calibrated data
'''

data_file = 'data.txt'

def boltzmann_constant(time_step):

    '''
    Data analysis for Delta x, y
    '''
    x_values = []
    y_values = []

    with open(data_file, 'r') as data:
        data.readline()
        for line in data:
            line.strip()
            col = line.split()
            x_values.append(float(col[1]))
            y_values.append(float(col[2]))

    cal_x_values = []
    cal_y_values = []

    for value in x_values:
        cal_x_values.append(value / scaled_x)

    for value in y_values:
        cal_y_values.append(value / scaled_y)


    delta_x_val = []
    delta_y_val = []
    for i in range(len(x_values)):
        if i > (int((time_step / 5)) - 1):
            delta_x_val.append(cal_x_values[i] - cal_x_values[i-int((time_step / 5))])
            delta_y_val.append(cal_y_values[i] - cal_y_values[i-int((time_step / 5))])

    print delta_x_val
    print delta_y_val

    pyplot.hist(delta_x_val)
    pyplot.title("X Coordinate Graph From A " + str(time_step) + " Second Time Step")
    pyplot.savefig("Histogram_delta_x_" + str(time_step) + ".png")
    pyplot.show()
    pyplot.close()
    pyplot.hist(delta_y_val)
    pyplot.title("Y Coordinate Graph From A " + str(time_step) + " Second Time Step")
    pyplot.savefig("Histogram_delta_y_" + str(time_step) + ".png")
    pyplot.show()
    pyplot.close()

    #Mean and standard deviation for deltaX and deltaY
    mean_delta_x = 0
    mean_delta_y = 0

    for value in delta_x_val:
        mean_delta_x += value
    mean_delta_x /= len(delta_x_val)

    for value in delta_y_val:
        mean_delta_y += value
    mean_delta_y /= len(delta_y_val)

    standard_dev_x = standard_dev(delta_x_val, mean_delta_x)
    standard_dev_y = standard_dev(delta_y_val, mean_delta_y)

    #Error in delta_x, delta_y from quadrature addition
    error_in_delta_x = quad_error(error_in_x, error_in_x)
    error_in_delta_y = quad_error(error_in_y, error_in_y)

    sd_x_sd = standard_dev_x * standard_dev_sd(len(delta_x_val))
    sd_y_sd = standard_dev_y * standard_dev_sd(len(delta_y_val))

    print ("Mean X: " + str(mean_delta_x) + " SD: " + str(standard_dev_x) + " SDOM: " + str(standard_dev_sd(len(delta_x_val))))
    print ("Mean Y: " + str(mean_delta_y) + " SD: " + str(standard_dev_y) + " SDOM: " + str(standard_dev_sd(len(delta_y_val))))

    #End Standard deviation and mean for deltaX and deltaY

    #Mean and standard deviation for deltaX^@ and deltaY^2
    mean_delta_x_2 = 0
    mean_delta_y_2 = 0

    delta_x_2_val = []
    delta_y_2_val = []

    for value in delta_x_val:
        delta_x_2_val.append((value ** 2))

    for value in delta_y_val:
        delta_y_2_val.append((value ** 2))


    for value in delta_x_2_val:
        mean_delta_x_2 += value
    mean_delta_x_2 /= len(delta_x_val)

    for value in delta_y_2_val:
        mean_delta_y_2 += value
    mean_delta_y_2 /= len(delta_y_val)

    standard_dev_x_2 = standard_dev(delta_x_2_val, mean_delta_x_2)
    standard_dev_y_2 = standard_dev(delta_y_2_val, mean_delta_y_2)

    sd_y_2_sd = standard_dev_y_2 * standard_dev_sd(len(delta_y_2_val))
    sd_x_2_sd = standard_dev_x_2 * standard_dev_sd(len(delta_x_2_val))

    sdsd_x2_from_x = (standard_dev_x / mean_delta_x) * 2
    sdsd_y2_from_y = (standard_dev_y / mean_delta_y) * 2

    #Error in delta_X^2 and delta_Y^2
    error_in_delta_x_2 = power_error(2, frac_error(error_in_delta_x, mean_delta_x))
    error_in_delta_y_2 = power_error(2, frac_error(error_in_delta_y, mean_delta_y))

    print ("Mean X^2: " + str(mean_delta_x_2) + " SD: " + str(standard_dev_x_2) + " SDOM: " + str(standard_dev_sd(len(delta_x_2_val))))
    print ("Mean Y^2: " + str(mean_delta_y_2) + " SD: " + str(standard_dev_y_2) + " SDOM: " + str(standard_dev_sd(len(delta_y_2_val))))

    '''
    End Delta X, y analysis
    '''

    '''
    Calculating D
    '''

    r_2 = []
    mean_delta_r_2 = 0

    for index, value in enumerate(cal_x_values):
        r_2.append(math.sqrt((value ** 2) + (cal_y_values[index] ** 2)))

    print r_2
    delta_r_2_val = []
    for i in range(len(r_2)):
        if i > 0:
            delta_r_2_val.append((r_2[i] - r_2[i-1]) ** 2)

    print delta_r_2_val
    for value in delta_r_2_val:
        mean_delta_r_2 += value
    mean_delta_r_2 /= len(delta_r_2_val)

    standard_dev_r_2 = standard_dev(delta_r_2_val, mean_delta_r_2)

    sd_r_2_sd = standard_dev_r_2 * standard_dev_sd(len(delta_r_2_val))

    print ("Mean R^2: " + str(mean_delta_r_2) + " SD: " + str(standard_dev_r_2) + " SDOM: " + str(sd_r_2_sd))

    error_in_r_2 = sd_x_2_sd + sd_y_2_sd
    delta_delta_r = math.sqrt((mean_delta_x_2 ** 2) + (mean_delta_y_2 ** 2))
    print ("Delta Delta R: " + str(delta_delta_r))
    print error_in_r_2
    delta_r_2_array.append(delta_delta_r)
    delta_r_2_error_array.append(error_in_r_2)

    d_var10 = D(time_step, mean_delta_r_2)
    d_var11 = D(time_step, mean_delta_r_2 + standard_dev_r_2) #Check to see if actual value in one standard deviation
    d_var9 = D(time_step, mean_delta_r_2 - standard_dev_r_2)

    kb_constant = kB(d_var10, f(.0000016), 296.25)
    kb_constant2 = kB(d_var11, f(.0000016), 296.25)
    kb_constant3 = kB(d_var9, f(.0000016), 296.25)
    print kb_constant
    print kb_constant2
    print kb_constant3
    print ("D: " + str(d_var10) + " D-Error: " + str(error_in_r_2 / (4 * int(time_step))) + " D-Frac: " + str((error_in_r_2 / (4 * int(time_step))) / d_var10))
    time_array.append(int(time_step))
    d_var_array.append(d_var10)
    print (math.erf(mean_delta_x))
    print (math.erf(mean_delta_y))
    print ("K " + str(kb_constant) + " KB Error: " + str((error_in_r_2 / (4 * int(time_step))) * (f(.0000016) / 296.25)))
    percent_correct = (kb_constant - (1.38e-13))/ (error_in_r_2 / (4 * int(time_step))) * (f(.0000016) / 296.25)
    print ("Prob K within K: " + str(percent_correct) + " " + str(math.erf(percent_correct)))
    print str(((1- math.erf(percent_correct)) / 2))

boltzmann_constant(5)
boltzmann_constant(10)
boltzmann_constant(15)
boltzmann_constant(20)
boltzmann_constant(25)

pyplot.errorbar(time_array, delta_r_2_array, yerr=delta_r_2_error_array)
pyplot.xlim(0, 30)
pyplot.savefig("R_Squared.png")
pyplot.show()

print delta_r_2_array
print delta_r_2_error_array
import numpy as np
from scipy.optimize import fmin
import matplotlib.pyplot as plt

pi = float(np.pi)
G = 6.67e-11
Ms = 2.78 * 1.9891e30
au = 149597870700
mJ = 1.9e27
wave0 = 656.281  # nm
c = 3e8

def read_file(filename):
    data = np.genfromtxt(filename, delimiter=',', comments='%')
    return data


data = read_file('doppler_data_1(1).csv')
where_is_nan = np.isnan(data)
data[where_is_nan] = 0
time1 = data[:, 0];lamba1 = data[:, 1]; flu1 = data[:, 2]
where_is_zero = np.argwhere(time1==0)
time1 = np.delete(time1, where_is_zero)
lamba1 = np.delete(lamba1, where_is_zero)
flu1 = np.delete(flu1, where_is_zero)
velocity1 = ((lamba1 / wave0) - 1) * c
print(lamba1)



plt.plot(time1, velocity1)
plt.show()

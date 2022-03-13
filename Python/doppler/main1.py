import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin

pi = float(np.pi)
G = 6.67e-11
Ms = 2.78 * 1.9891e30
au = 149597870700
mJ = 1.9e27
wave0 = 656.281  # nm
c = 3e8


def read_data1():
    with open('doppler_data_1(1).csv', 'r') as f:
        reader = csv.reader(f)
        list_read = list(reader)
        time = np.zeros(len(list_read) - 1)
        wavelen = np.zeros(len(list_read) - 1)
        uncertainty = np.zeros(len(list_read) - 1)
        for i in range(1, len(list_read)):
            a = list_read[i]
            if a[0] != 'nan':
                try:
                    time[i - 1] = float(a[0])
                    wavelen[i - 1] = float(a[1])
                    uncertainty[i - 1] = float(a[2])
                except ValueError:
                    continue
    u = np.argwhere(time == 0)
    time = np.delete(time, u)
    wavelen = np.delete(wavelen, u)
    wavelen[12] = (wavelen[11]+wavelen[13])/2
    uncertainty = np.delete(uncertainty, u)
    velocity = ((wavelen / wave0) - 1) * c
    delta_v = (uncertainty / wave0) * c
    return time, velocity, delta_v


def initialize(velocity, time):
    t1 = np.argwhere(np.absolute(velocity) <= 5)
    half = float(time[t1[1]] - time[t1[0]])
    ini_w = pi / half
    vma = max(velocity)
    vmi = min(velocity)
    ini_v = (vma - vmi) / 2
    return ini_v, ini_w


def optimize(ini_v, ini_w, velocity, time, delta_v):
    X2 = np.zeros(shape=[100, 100])
    PHI = np.zeros(shape=[100, 100])
    for i in range(100):
        for j in range(100):
            v = ini_v - i * 0.03
            w = ini_w + (j - 50) * 0.005
            t1 = np.argwhere(time[np.argwhere(np.absolute(velocity) < 4)] < 1)
            t = int(t1[0, 0])
            phi = pi - w * time[t]
            PHI[i, j] = phi
            vt = np.array(v * np.sin(w * time + phi))
            x_square = [((vt[i] - velocity[i]) / delta_v[i]) ** 2 for i in range(len(vt))]
            X2[i, j] = np.sum(x_square)
    chi_sqr = X2.min()
    locate = np.argwhere(X2 == chi_sqr)
    i = locate[0, 0]
    j = locate[0, 1]
    v = ini_v - i * 0.03
    w = ini_w + (j - 50) * 0.005
    phi = PHI[i, j]
    return v, w, chi_sqr, phi


def func(vw):
    v = vw[0]
    w = vw[1]
    x = 0
    for i in range(len(time)):
        vt = v * np.sin(w * time[i] + pi)
        x = x + ((vt - velocity[i]) / delta_v[i]) ** 2
    return x


def minim():
    fit_result = fmin(func, (ini_v, ini_w), full_output=True)
    [v, w] = fit_result[0]
    chi_sqr = fit_result[1]
    reduced_chi_sqr = chi_sqr/(len(time))
    return v, w, reduced_chi_sqr


def plot(phi):
    TIME = np.linspace(-1, 7, 80)
    # ini_vt = ini_v * np.sin(ini_w * TIME + pi)
    vt = v * np.sin(w * TIME + phi)
    vtime = v * np.sin(w * time + phi)
    plt.xlabel('time/year', fontsize=15)
    plt.ylabel('velocity/(m/s)', fontsize=15)
    # plt.plot(TIME, ini_vt, 'grey')
    plt.plot(TIME, vt, 'orange')
    plt.errorbar(time, velocity, delta_v, fmt='bo')
    # plt.scatter(time, velocity)
    plt.legend(['fitting result', 'Data point'])
    plt.savefig('data1.png')
    plt.show()
    return 0


def calculate(v, w):
    period = pi / w * 2 * 365 * 86400
    omega = 2 * pi / period
    radius = (G * Ms / (omega ** 2)) ** (1 / 3)
    reduced_radius = radius / au
    vP = (G * Ms / radius) ** 0.5
    mP = Ms * v / vP
    reduced_mp = mP / mJ
    return reduced_mp, reduced_radius, omega






time, velocity, delta_v = read_data1()
ini_v, ini_w = initialize(velocity, time)
# v, w, chi_sqr, phi = optimize(ini_v, ini_w, velocity, time, delta_v)
v, w, reduced_chi_sqr = minim()
phi = pi
reduced_mp, reduced_radius, omega = calculate(v, w)
OMEGA = omega*(10**8)
print('v0=%.4f(m/s)' % v, ' ', ' w=%.4fe-08(rad/s)' % OMEGA)
print("The planet's mass is %.4f Jovian mass" % reduced_mp)
print('Its orbital radius is %.4f AU' % reduced_radius)
print('with chi squared being %.3f' % reduced_chi_sqr)
plot(phi)


'''def optimize(ini_v, ini_w, velocity, time, delta_v):
    X2 = np.zeros(shape=[200, 200])
    PHI = np.zeros(shape=[200, 200])
    for i in range(200):
        for j in range(200):
            v = ini_v - i * 0.03
            w = ini_w + (j - 100) * 0.005
            t1 = np.argwhere(time[np.argwhere(np.absolute(velocity) < 0.5)] < 1)
            t = int(t1[0, 0])
            phi = pi - w * time[t]
            PHI[i, j] = phi
            vt = np.array(v * np.sin(w * time + phi))
            x_square = [((vt[i] - velocity[i]) / delta_v[i]) ** 2 for i in range(len(vt))]
            X2[i, j] = np.sum(x_square)
    chi_sqr = X2.min()
    locate = np.argwhere(X2 == chi_sqr)
    i = locate[0, 0]
    j = locate[0, 1]
    v = ini_v - i * 0.03
    w = ini_w + (j - 100) * 0.005
    phi = PHI[i, j]
    # reduced_chi = chi_sqr/(len(time)-2)
    reduced_chi = chi_sqr / Ndof
    return v, w, reduced_chi, phi'''

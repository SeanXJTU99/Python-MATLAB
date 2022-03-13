import csv
import numpy as np
import matplotlib.pyplot as plt

pi = float(np.pi)
G = 6.67e-11
Ms = 2.78 * 1.9891e30
au = 149597870700
mJ = 1.9e27
wave0 = 656.281  # nm
c = 3e8


def read_data2():
    with open('doppler_data_2(1).csv', 'r') as f:
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
    u = np.argwhere(uncertainty == 0)
    uncertainty[u] = np.mean(uncertainty)
    t = np.argwhere(time == 1.75)
    wavelen[t] = wavelen[t] - 100
    t = np.argwhere(time == 5.75)
    wavelen[t] = (wavelen[t + 1] + wavelen[t - 1]) / 2
    velocity = ((wavelen / wave0) - 1) * c
    delta_v = (uncertainty / wave0) * c
    return time, velocity, delta_v


def initialize(velocity, time):
    t1 = np.argwhere(np.absolute(velocity) <= 1)
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
            t1 = np.argwhere(time[np.argwhere(np.absolute(velocity) < 1)] < 1)
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


def plot(phi):
    TIME = np.linspace(-1, 7, 80)
    ini_vt = ini_v * np.sin(ini_w * TIME + pi)
    vt = v * np.sin(w * TIME + phi)
    plt.xlabel('time/year', fontsize=15)
    plt.ylabel('velocity/(m/s)', fontsize=15)
    plt.plot(TIME, ini_vt, 'grey')
    plt.plot(TIME, vt, 'orange')
    plt.scatter(time, velocity)
    plt.legend(['initial function', 'fitting result', 'raw data'])
    plt.savefig('data2.png')
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






time, velocity, delta_v = read_data2()
ini_v, ini_w = initialize(velocity, time)
v, w, chi_sqr, phi = optimize(ini_v, ini_w, velocity, time, delta_v)
reduced_mp, reduced_radius, omega = calculate(v, w)
OMEGA = omega*10**8
print('v0=%.4f(m/s)' % v, ' ', ' w=%.4fe-08(rad/s)' % OMEGA)
print("The planet's mass is %.4f Jovian mass" % reduced_mp)
print('Its orbital radius is %.4f AU' % reduced_radius)
print('with chi squared being %.3f' % chi_sqr)
plot(phi)

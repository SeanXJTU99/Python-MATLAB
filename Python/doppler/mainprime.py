from scipy.optimize import fmin
import numpy as np
import matplotlib.pyplot as plt

pi = float(np.pi)
G = 6.67e-11
Ms = 2.78 * 1.9891e30
au = 149597870700
mJ = 1.9e27
wave0 = 656.281  # nm
c = 3e8
Ndof = 36 * 2 - 2


def read_data():
    with open('doppler_data_1(1).csv', 'r') as f:
        reader = f.readlines()
        list_read = list(reader)
        time1 = np.zeros(len(list_read) - 1)
        wave_len = np.zeros(len(list_read) - 1)
        uncertainty = np.zeros(len(list_read) - 1)
        for i in range(1, len(list_read)):
            a = np.array(list_read[i].split(','))
            if a[0] != 'nan':
                try:
                    time1[i - 1] = float(a[0])
                    wave_len[i - 1] = float(a[1])
                    uncertainty[i - 1] = float(a[2])
                except ValueError:
                    continue
    u = np.argwhere(time1 == 0)
    time1 = np.delete(time1, u)
    wave_len = np.delete(wave_len, u)
    wave_len[12] = (wave_len[11] + wave_len[13]) / 2
    uncertainty = np.delete(uncertainty, u)
    velocity1 = ((wave_len / wave0) - 1) * c
    delta_v1 = (uncertainty / wave0) * c

    with open('doppler_data_2(1).csv', 'r') as f:
        reader = f.readlines()
        list_read = list(reader)
        time2 = np.zeros(len(list_read) - 1)
        wave_len = np.zeros(len(list_read) - 1)
        uncertainty = np.zeros(len(list_read) - 1)
        for i in range(1, len(list_read)):
            a = np.array(list_read[i].split(','))
            if a[0] != 'nan':
                try:
                    time2[i - 1] = float(a[0])
                    wave_len[i - 1] = float(a[1])
                    uncertainty[i - 1] = float(a[2])
                except ValueError:
                    continue
    u = np.argwhere(uncertainty == 0)
    uncertainty[u] = np.mean(uncertainty)
    t = np.argwhere(time2 == 1.75)
    wave_len[t] = wave_len[t] - 100
    t = np.argwhere(time2 == 5.75)
    wave_len[t] = (wave_len[t + 1] + wave_len[t - 1]) / 2
    velocity2 = ((wave_len / wave0) - 1) * c
    delta_v2 = (uncertainty / wave0) * c

    time = np.zeros(len(time1) + len(time2))
    velocity = np.zeros(len(time))
    delta_v = np.zeros(len(time))
    for i in range(len(time1)):
        time[i] = time1[i]
        velocity[i] = velocity1[i]
        delta_v[i] = delta_v1[i]
    for i in range(len(time2)):
        time[i + len(time1)] = time2[i]
        velocity[i + len(time1)] = velocity2[i]
        delta_v[i + len(time1)] = delta_v2[i]
    return time, velocity, delta_v


def initialize(velocity, time):
    t1 = np.argwhere(np.absolute(velocity) <= 0.5)

    half = float(time[t1[1]] - time[t1[0]])
    ini_w = pi / half
    vma = max(velocity)
    vmi = min(velocity)
    ini_v = (vma - vmi) / 2
    return ini_v, ini_w


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


def func(vw):
    v = vw[0]
    w = vw[1]
    x = 0
    for i in range(len(time)):
        vt = v * np.sin(w * time[i] + pi)
        x = x + ((vt - velocity[i]) / delta_v[i]) ** 2
    return x


def optimize():
    fit_result = fmin(func, (ini_v, ini_w), full_output=True)
    [v, w] = fit_result[0]
    chi_sqr = fit_result[1]
    reduced_chi_sqr = chi_sqr / (len(time) - 2)
    return v, w, reduced_chi_sqr


def flu(v, w, chi):
    dv = v / 20
    dw = w / 20
    min_v = v - dv
    min_w = w - dw
    max_v = v + dv
    max_w = w + dw
    V = np.linspace(min_v, max_v, 100)
    J = np.linspace(min_w, max_w, 100)
    RESULT = np.zeros(shape=[100, 100])
    for i in range(len(V)):
        v = V[i]
        for j in range(len(J)):
            w = J[j]
            x = 0
            for k in range(len(time)):
                vt = v * np.sin(w * time[k] + pi)
                x = x + ((vt - velocity[k]) / delta_v[k]) ** 2
            x = x / (len(time) - 2)
            # if x < 1 + (1 - chi):
                # print(V[i])
                # print(J[j]/(365*86400))
    return V, J


def plot(time, w):
    time = time * 365 * 86400
    w = w / (365 * 86400)
    TIME = np.linspace(-1 * 365 * 86400, 7 * 365 * 86400, 80)
    phi = pi
    vt = v * np.sin(w * TIME + phi)
    plt.title('The velocity of stars')
    plt.xlabel('time (s)', fontsize=15)
    plt.ylabel('velocity (m/s)', fontsize=15)
    plt.plot(TIME, vt, 'orange')
    plt.errorbar(time, velocity, delta_v, fmt='bo')
    plt.legend(['fitting result', 'Data point'])
    plt.savefig('velocity.png')
    # plt.show()
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


time, velocity, delta_v = read_data()
ini_v, ini_w = initialize(velocity, time)
# v, w, reduced_chi, phi = optimize(ini_v, ini_w, velocity, time, delta_v)
v, w, reduced_chi = optimize()
V, W = flu(v, w, reduced_chi)
print(V, W)
plot(time, w)
reduced_mp, reduced_radius, omega = calculate(v, w)
OMEGA = omega * (10 ** 8)
print('v0=%.4f(m/s)' % v, ' ', ' w=%.4fe-08(rad/s)' % OMEGA)
print("The planet's mass is %.4f Jovian mass" % reduced_mp)
print('Its orbital radius is %.4f AU' % reduced_radius)
print('with reduced_chi_square being %.3f' % reduced_chi)

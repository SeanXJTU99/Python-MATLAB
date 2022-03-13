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


def read_data():
    data = np.genfromtxt('doppler_data_1(1).csv', delimiter=',', comments='%')  # 读入文档原始数据

    for line in data:
        if line[2] == 0:
            line[2] = np.nan
    data = data[~np.isnan(data).any(axis=1)]                      # 删去无数据部分(文档中为‘nan’)

    # remove bad data
    time1 = data[:, 0]
    wave_len = data[:, 1]
    uncertainty = data[:, 2]                                      # 将数据分为三列，第一列时间，第二列波长，第三列涨落

    u = np.argwhere(time1 == 0)                                   # 若时间项为0 删去所在整行数据
    time1 = np.delete(time1, u)
    wave_len = np.delete(wave_len, u)
    uncertainty = np.delete(uncertainty, u)

    wave_len[12] = (wave_len[11]+wave_len[13])/2                   # 调整不正常数据点

    velocity1 = ((wave_len / wave0) - 1) * c                       # 换算为速度和速度涨落
    delta_v1 = (uncertainty / wave0) * c

    data = np.genfromtxt('doppler_data_2(1).csv', delimiter=',', comments='%')
    for line in data:
        if line[2] == 0:
            line[2] = np.nan
    data = data[~np.isnan(data).any(axis=1)]

    # bad data
    time2 = data[:, 0]
    wave_len = data[:, 1]
    uncertainty = data[:, 2]
    u = np.argwhere(uncertainty == 0)
    uncertainty[u] = np.mean(uncertainty)
    t = np.argwhere(time2 == 1.75)
    wave_len[t] = wave_len[t] - 100
    t = np.argwhere(time2 == 5.75)
    wave_len[t] = (wave_len[t + 1] + wave_len[t - 1]) / 2
    velocity2 = ((wave_len / wave0) - 1) * c
    delta_v2 = (uncertainty / wave0) * c

    # 构建列长度为data1，data2 之和的矩阵，用于数据合并
    y1 = np.zeros(len(time1) + len(time2))  # y1， 用于存储时间数据，目前为零矩阵
    y2 = np.zeros(len(y1))                  # y2， 速度
    y3 = np.zeros(len(y1))                  # y3， 涨落
    for i in range(len(time1)):
        y1[i] = time1[i]                    # 将data1的时间数据填入y1
        y2[i] = velocity1[i]                # data1的速度
        y3[i] = delta_v1[i]                 # data1的涨落
    for i in range(len(time2)):
        y1[i + len(time1)] = time2[i]          # data2
        y2[i + len(time1)] = velocity2[i]
        y3[i + len(time1)] = delta_v2[i]
    return y1, y2, y3


def initialize(x1, x2):
    t1 = np.argwhere(np.absolute(x1) <= 0.5)
    half = float(x2[t1[1]] - x2[t1[0]])   # x1 = velocity, x2 = time
    y2 = pi / half                 # ini_w
    vma = max(x1)
    vmi = min(x1)
    y1 = (vma - vmi) / 2           # ini_v
    return y1, y2


def func(vw):
    A = vw[0]    # v
    W = vw[1]    # w
    x = 0
    for i in range(len(time)):
        vt = A * np.sin(W * time[i] + pi)
        x = x + ((vt - velocity[i]) / delta_v[i]) ** 2
    return x


def optimize():
    fit_result = fmin(func, (ini_v, ini_w), full_output=True)
    [y1, y2] = fit_result[0]      # [v, w]
    chi_sqr = fit_result[1]
    y3 = chi_sqr/(len(time)-2)    # reduced_chi_sqr
    return y1, y2, y3, chi_sqr



def plot(x1, x2):
    x1 = x1 * 365 * 86400        # x1 = time
    x2 = x2 / (365 * 86400)      # x2 = w
    TIME = np.linspace(-1*365*86400, 7*365*86400, 80)
    phi = pi
    vt = v * np.sin(x2 * TIME + phi)
    plt.title('The velocity of stars')
    plt.xlabel('time (s)', fontsize=15)
    plt.ylabel('velocity (m/s)', fontsize=15)
    plt.plot(TIME, vt, 'orange')
    plt.errorbar(x1, velocity, delta_v, fmt='bo')
    plt.legend(['fitting result', 'Data point'])
    plt.savefig('velocity.png')
    plt.show()
    return 0


def calculate(x1, x2):
    period = pi / x2 * 2 * 365 * 86400      # x1 = v, x2 = w
    y3 = 2 * pi / period                    # omega
    radius = (G * Ms / (y3 ** 2)) ** (1 / 3)
    y2 = radius / au               # reduced_radius
    vP = (G * Ms / radius) ** 0.5
    mP = Ms * x1 / vP
    y1 = mP / mJ                   # reduced_mp
    return y1, y2, y3


def contour_plot(t, vlct, delta, v0, w0):
    v_array = np.linspace(v0 - 0.02 * v0, v0 + 0.02 * v0, 100)
    w_array = np.linspace(w0 - 0.01 * w0, w0 + 0.01 * w0, 100)
    vw = np.vstack((v_array, w_array))
    plt.figure()
    v_array = vw[0, :]
    w_array = vw[1, :] / (365*86400)
    w0 = w0 / (365*86400)
    times = t * 365 * 86400

    # mesh grids
    X = np.empty((0, len(v_array)))
    for _ in w_array:
        X = np.vstack((X, v_array))
    Y = np.empty((0, len(w_array)))
    for _ in v_array:
        Y = np.vstack((Y, w_array))
    Y = np.transpose(Y)

    plt.title(r'contour of $\chi^2_{red}$  against parameters')
    plt.xlabel('velocity (m/s)')
    plt.ylabel('omega (rad/s)')

    # calculate chi_squared by different parameters
    Z = np.zeros([len(v_array), len(w_array)])
    for i in range(len(v_array)):
        for j in range(len(w_array)):
            v = v_array[i]
            w = w_array[j]
            vt = v * np.sin(w * times + pi)
            Z[i, j] = (np.sum(((vt - vlct) / delta) ** 2))

    # plot contour
    CONTOUR_PLOT = plt.contour(X, Y, Z, 15)
    plt.clabel(CONTOUR_PLOT, inline=1, fontsize=10)
    plt.scatter(v0, w0)
    plt.legend(('minimal',))
    plt.savefig('contour.png')
    plt.show()
    return 0



time, velocity, delta_v = read_data()
ini_v, ini_w = initialize(velocity, time)
v, w, reduced_chi, chi_sqr = optimize()
plot(time, w)
contour_plot(time, velocity, delta_v, v, w)
reduced_mp, reduced_radius, omega = calculate(v, w)
OMEGA = omega*(10**8)
print('v0=%.4f(m/s)' % v, ' ', ' w=%.4fe-08(rad/s)' % OMEGA)
print("The planet's mass is %.4f Jovian mass" % reduced_mp)
print('Its orbital radius is %.4f AU' % reduced_radius)
print(r'with reduced_chi_square being %.3f' % reduced_chi)

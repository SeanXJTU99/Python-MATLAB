from scipy.optimize import fmin
import numpy as np
import matplotlib.pyplot as plt

# Constants

PI = float(np.pi)

G = 6.67e-11 # Gravitational Constant

MS = 2.78 * 1.9891e30 # Mass of Star

AU = 149597870700 # Artronomical Unit

MJ = 1.9e27 # Mass of Jovian

WAVE_0 = 656.281  # nm

C = 3e8 # Light of Speed/ms^-1

# Function definitions

def read_data():
    """
    Reads in date file, skipping non-numeric values,get the data of time,
    velocity and uncertainty of velocity.
    Args:
        doppler_data_1.csv
        doppler_data_2.csv
    Returns:
        y1[floats]
        y2[floats]
        y3[floats]
    """
    data = np.genfromtxt('doppler_data_1(1).csv', delimiter=',', comments='%')
    for line in data:
        if line[2] == 0:
            line[2] = np.nan
    data = data[~np.isnan(data).any(axis=1)]

    # remove bad data
    time1 = data[:, 0]
    wave_len = data[:, 1]
    uncertainty = data[:, 2]
    u = np.argwhere(time1 == 0)
    time1 = np.delete(time1, u)
    wave_len = np.delete(wave_len, u)
    uncertainty = np.delete(uncertainty, u)
    wave_len[12] = (wave_len[11]+wave_len[13])/2
    velocity1 = ((wave_len / WAVE_0) - 1) * C
    delta_v1 = (uncertainty / WAVE_0) * C

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
    velocity2 = ((wave_len / WAVE_0) - 1) * C
    delta_v2 = (uncertainty / WAVE_0) * C

    TIME = np.zeros(len(time1) + len(time2))  # time
    VELOCITY = np.zeros(len(TIME))                  # velocity
    DELTA_V = np.zeros(len(TIME))                  # delta_v
    for i in range(len(time1)):
        TIME[i] = time1[i]
        VELOCITY[i] = velocity1[i]
        DELTA_V[i] = delta_v1[i]
    for i in range(len(time2)):
        TIME[i + len(time1)] = time2[i]
        VELOCITY[i + len(time1)] = velocity2[i]
        DELTA_V[i + len(time1)] = delta_v2[i]
    return TIME, VELOCITY, DELTA_V


def initialize(VELOCITY, TIME):
    """
    Find the initial velocity and initial omega.
    Parameters:
        VELOCITY : float
        TIME : float
    Returns:
        y1[float]
        y2[float]
    """
    T1 = np.argwhere(np.absolute(VELOCITY) <= 0.5)
    HALF = float(TIME[T1[1]] - TIME[T1[0]])   # x1 = velocity, x2 = time
    INI_W = PI / HALF                 # ini_w
    VMA = max(VELOCITY)
    VMI = min(VELOCITY)
    INI_V = (VMA - VMI) / 2           # ini_v
    return INI_V, INI_W


def func(VW):
    V = VW[0]    # v
    W = VW[1]    # w
    X = 0
    for i in range(len(TIME)):
        VT = V * np.sin(W * TIME[i] + PI)
        X = X + ((VT - VELOCITY[i]) / DELTA_V[i]) ** 2
    return X


def optimize(INI_V, INI_W):
    FIT_RESULT = fmin(func, (INI_V, INI_W), full_output=True)
    [V, W] = FIT_RESULT[0]      # [v, w]
    CHI_SQR = FIT_RESULT[1]
    REDUCED_CHI = CHI_SQR/(len(TIME)-2)    # reduced_chi_sqr
    return V, W, REDUCED_CHI, CHI_SQR



def plot(TIME, W):
    TIME = TIME * 365 * 86400        # x1 = time
    W = W / (365 * 86400)      # x2 = w
    TIME_PRIME = np.linspace(-1*365*86400, 7*365*86400, 80)
    PHI = PI
    vt = V * np.sin(W * TIME_PRIME + PHI)
    plt.title('The velocity of stars')
    plt.xlabel('time (s)', fontsize=15)
    plt.ylabel('velocity (m/s)', fontsize=15)
    plt.plot(TIME_PRIME, vt, 'orange')
    plt.errorbar(TIME, VELOCITY, DELTA_V, fmt='bo')
    plt.legend(['fitting result', 'Data point'])
    plt.savefig('velocity.png')
    plt.show()
    return 0


def result(V, W):
    PERIOD = PI / W * 2 * 365 * 86400      # x1 = v, x2 = w
    OMEGA = 2 * PI / PERIOD                    # omega
    RADIUS = (G * MS / (OMEGA ** 2)) ** (1 / 3)
    REDUCED_RADIUS = RADIUS / AU               # reduced_radius
    vP = (G * MS / RADIUS) ** 0.5
    mP = MS * V / vP
    REDUCED_MP = mP / MJ                   # reduced_mp
    return REDUCED_MP, REDUCED_RADIUS, OMEGA


def contour_plot(T, VLCT, DELTA, V0, W0):
    V_ARRAY = np.linspace(V0 - 0.02 * V0, V0 + 0.02 * V0, 100)
    W_ARRAY = np.linspace(W0 - 0.01 * W0, W0 + 0.01 * W0, 100)
    VW = np.vstack((V_ARRAY, W_ARRAY))
    plt.figure()
    V_ARRAY = VW[0, :]
    W_ARRAY = VW[1, :] / (365*86400)
    W0 = W0 / (365*86400)
    TIMES = T * 365 * 86400

    # mesh grids
    X = np.empty((0, len(V_ARRAY)))
    for _ in W_ARRAY:
        X = np.vstack((X, V_ARRAY))
    Y = np.empty((0, len(W_ARRAY)))
    for _ in V_ARRAY:
        Y = np.vstack((Y, W_ARRAY))
    Y = np.transpose(Y)

    plt.title(r'contour of $\chi^2$ against parameters')
    plt.xlabel('velocity (m/s)')
    plt.ylabel('omega (rad/s)')

    # calculate chi_squared by different parameters
    Z = np.zeros([len(V_ARRAY), len(W_ARRAY)])
    for i in range(len(V_ARRAY)):
        for j in range(len(W_ARRAY)):
            V = V_ARRAY[i]
            W = W_ARRAY[j]
            VT = V * np.sin(W * TIMES + PI)
            Z[i, j] = (np.sum(((VT - VLCT) / DELTA) ** 2))

    # plot contour
    CONTOUR_PLOT = plt.contour(X, Y, Z, 15)
    plt.clabel(CONTOUR_PLOT, inline=1, fontsize=10)
    plt.scatter(V0, W0)
    plt.legend(('minimal',))
    plt.savefig('contour.png')
    plt.show()
    return 0



TIME, VELOCITY, DELTA_V = read_data()
INI_V, INI_W = initialize(VELOCITY, TIME)
V, W, REDUCED_CHI, CHI_SQR = optimize(INI_V, INI_W)
plot(TIME, W)
contour_plot(TIME, VELOCITY, DELTA_V, V, W)
REDUCED_MP, REDUCED_RADIUS, OMEGA = result(V, W)
OMEGA_PRIME = OMEGA*(10**8)
print('v0=%.4f(m/s)' % V, ' ', ' w=%.4fe-08(rad/s)' % OMEGA_PRIME)
print("The planet's mass is %.4f Jovian mass" % REDUCED_MP)
print('Its orbital radius is %.4f AU' % REDUCED_RADIUS)
print(r'with reduced_chi_square being %.3f' % REDUCED_CHI)

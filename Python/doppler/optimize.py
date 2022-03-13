import numpy as np

pi: float = float(np.pi)
GDNS = np.zeros(shape=[100, 100])
X2 = np.zeros(shape=[100, 100])


def optimize(ini_v, ini_w, velocity, time, deltav):
    for i in range(100):
        for j in range(100):
            v = ini_v - i * 0.03
            w = ini_w + (j - 50) * 0.005
            # t = np.argwhere(np.absolute(velocity) < 0.2)
            # phi = float(pi - w * time[t])
            phi = pi
            vt = np.array(v * np.sin(w * time + phi))
            # if i % 10 == 0 and j % 10 == 0:
            #   plt.plot(vt)
            good = [(vt[i] - velocity[i]) ** 2 for i in range(len(vt))]
            goodness = np.sum(good)
            GDNS[i, j] = goodness
            xsquared = [((vt[i] - velocity[i]) / deltav[i]) ** 2 for i in range(len(vt))]
            x2 = np.sum(xsquared)
            X2[i, j] = x2
    # plt.show()
    '''ax = plt.axes(projection='3d')
    x = np.linspace(1, 100, 100, dtype=int)
    y = np.linspace(1, 100, 100, dtype=int)
    X, Y = np.meshgrid(x, y)
    # print(X)
    Z = GDNS[X-1, Y-1]
    # print(Z)
    ax.scatter3D(X, Y, Z)
    plt.show()'''
    goodness = GDNS.min()
    x2 = X2.min()

    # locate = np.argwhere(GDNS == goodness)
    locate = np.argwhere(X2 == x2)
    i = locate[0, 0]
    # print(i)
    j = locate[0, 1]
    v = ini_v - i * 0.03
    w = ini_w + (j - 50) * 0.005
    # t = np.argwhere(np.absolute(velocity) < 0.2)
    # phi = pi - w * time[t]
    # phi = pi
    # vt = v * np.sin(w * time + phi)
    return v, w, x2


'''for repeat in range(19):
        vi, wi = optimize.optimize(ini_v, ini_w, velocity, time, deltav)
        v = v+vi
        w = w+wi
    v = v/20
    w = w/20'''
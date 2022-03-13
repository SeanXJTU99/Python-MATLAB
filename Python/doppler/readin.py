import numpy as np
import csv


def read_data():
    with open('doppler_data_2(1).csv', 'r') as f:
        reader = csv.reader(f)
        # for i in reader:
        #    print(i[1])
        liread = list(reader)
        time = np.zeros(len(liread) - 1)
        wavelen = np.zeros(len(liread) - 1)
        uncertainty = np.zeros(len(liread) - 1)
        for i in range(1, len(liread)):
            a = liread[i]
            a0 = float(a[0])
            a1 = float(a[1])
            a2 = float(a[2])
            time[i - 1] = a0
            wavelen[i - 1] = a1
            uncertainty[i - 1] = a2
        # print(time)
        # print(wavelen)
    time = np.array(time)
    wavelen = np.array(wavelen)
    uncertainty = np.array(uncertainty)
    u = np.argwhere(uncertainty == 0)
    uncertainty[u] = np.mean(uncertainty)
    t = np.argwhere(time == 1.75)
    wavelen[t] = wavelen[t] - 100
    # plt.plot(time, wavelen)
    t = np.argwhere(time == 5.75)
    wavelen[t] = (wavelen[t + 1] + wavelen[t - 1]) / 2
    # plt.plot(time,wavelen)
    # plt.show()
    velocity = ((wavelen / 656.281) - 1) * 3e8
    deltav = (uncertainty / 656.281) * 3e8
    # print(deltav)
    # plt.scatter(time, velocity)
    # plt.show()
    return time, wavelen, velocity, deltav

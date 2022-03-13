import datanrp5
import numpy as np
import random
import matplotlib.pyplot as plt

lor = datanrp5.data1           # list of requirements
woc = datanrp5.data3           # weight of clients
wor = datanrp5.data2           # weight of requirements
value = datanrp5.value         # satisfaction of requirements
cost = np.zeros(shape=len(lor), dtype='int')
for i in range(len(lor)):
    cost[i] = wor[lor[i]-1, 0]   # cost of requirements
score = np.matmul(value, woc)  # overall value of requirements
N = len(cost)                  # number of requirements
G = 20                         # member in a group
T = 10000                        # times
minx = 0
maxx = 1


def ranfunc(vector):
    y = (np.matmul(cost, vector)/sum(cost))/(np.matmul(score, vector)/sum(score))  # optimize y = minimize y
    return y


p = [round(minx + (maxx - minx) * random.random()) for i in range(N)]

if __name__ == '__main__':
    t = 0
    p = [round(minx + (maxx - minx) * random.random()) for i in range(N)]
    yp = ranfunc(p)
    result = p
    while t <= T:
        q = [round(minx + (maxx - minx) * random.random()) for i in range(N)]
        yq = ranfunc(q)
        if yq < yp:
            result = q
        if t % 1000 == 0:
            X = np.matmul(cost, result)
            Y = np.matmul(score, result)
            plt.xlabel('cost', fontsize=15)
            plt.ylabel('score', fontsize=15)
            plt.scatter(X, Y)
            plt.show()
        t += 1
    np.array(result)
    print(result)

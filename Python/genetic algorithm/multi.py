import datanrp4
import numpy as np
import random
import math
import matplotlib.pyplot as plt

lor = datanrp4.data1           # list of requirements
woc = datanrp4.data3           # weight of clients
wor = datanrp4.data2           # weight of requirements
value = datanrp4.value         # satisfaction of requirements
cost = np.zeros(shape=[len(lor)], dtype='int')
for i in range(len(lor)):
    cost[i] = wor[lor[i]-1, 0]   # cost of requirements
score = np.matmul(value, woc)  # overall value of requirements
N = len(cost)                  # number of requirements
G = 20                         # member in a group
T = 500                         # times
minx = 0
maxx = 1
x = [round(minx+(maxx-minx)*random.random())for i in range(N)]   # By approximation, we got 0-1 vector x, also
x = np.transpose(x)                                              # the solution


def mulfunc1(vector):
    y = np.matmul(cost, vector)/sum(cost)       # normalized fitness function of cost
    return y


def mulfunc2(vector):
    y = np.matmul(score, vector)/sum(score)     # normalized fitness function of score(satisfaction)
    y = 1/y                                     # transform maximize to minimize
    return y


def dominator(f1p, f2p, f1q, f2q):      # dominating condition
    if f1p < f1q:                       # function1(p)<function1(q)
        if f2p <= f2q:                  # function2(p)<=function2(q)
            return True                 # p dominates q
        else:
            return False
    elif f1p == f1q:
        if f2p < f2q:
            return True
        else:
            return False
    else:
        return False


def nsga2(vector1, vector2):
    global Q
    S = [[] for i in range(G)]
    F = [[]]
    n = np.zeros(G)
    rank = np.zeros(G)
    for i in range(G):
        S[i] = []
        n[i] = 0
        for j in range(G):
            if dominator(vector1[i], vector2[i], vector1[j], vector2[j]):    # p dominates q
                if j not in S[i]:
                    S[i].append(j)
            elif dominator(vector1[j], vector2[j], vector1[i], vector2[i]):  # q dominates p
                n[i] += 1
        if n[i] == 0:                   # no solution dominates p
            rank[i] = 0
            if i not in F[0]:
                F[0].append(i)
    f = 0
    while F[f] != []:
        Q = []
        for p in F[f]:
            for q in S[p]:
                n[q] = n[q]-1
                if n[q] == 0:
                    rank[q] = f+1
                    if q not in Q:
                        Q.append(q)
        F.append(Q)
        f += 1
    del F[len(F)-1]
    return F


def seque(list1, values):                       # sort a list with sequence
    result = []
    index = 0
    while len(result) != len(list1):
        for i in range(len(values)):
            if values[i] == min(values):
                index = i
        if index in list1:
            result.append(index)
        values[index] = math.inf
    return result


def crowd(vector1, vector2, F):
    cuboid = [0 for i in range(0,len(F))]
    seq1 = seque(F, vector1[:])                     # looking for adjacent solution
    seq2 = seque(F, vector2[:])
    cuboid[0] = cuboid[len(F) - 1] =3*10**8          # first & last will be discarded
    for k in range(1,len(F)-1):
        cuboid[k] = cuboid[k]+(vector1[seq1[k+1]] - vector1[seq1[k-1]])/(max(vector1)-min(vector1))+(vector1[seq2[k+1]] - vector2[seq2[k-1]])/(max(vector2)-min(vector2))
    return cuboid


c = 0.5
def crossover(x1, x2):
    u = random.random()
    if u < 0.5:
        beta = (2*u)**(1/(c+1))
    else:
        beta = (0.5*1/(1-u))**(1/(c+1))
    y1 = 0.5 * ((1 + beta) * x1 + (1 - beta) * x2)
    y2 = 0.5 * ((1 - beta) * x1 + (1 + beta) * x2)
    for i in range(len(x1)):
        y1[i] = int(round(y1[i]))
        y2[i] = int(round(y2[i]))
    return y1, y2


def mutation(x):
    u = random.random()
    if u < 0.1:
        y = [round(minx+(maxx-minx)*random.random())for i in range(N)]
    else:
        y = x
    return y


def specie_orig(numofvariable, numofgroup):
    group = np.zeros(shape=[numofvariable, numofgroup], dtype='int')                 # generate a blank group
    for j in range(G):
        p = [round(minx + (maxx - minx) * random.random()) for i in range(N)]        # random solution
        group[:, j] = p
    return group


def index_of(f, F):
    for i in range(0, len(F)):
        if F[i] == f:
            return i
    return -1


t = 0                           # time = 0
P = specie_orig(N, G)           # initial generation
while t <= T:
    vectors1 = [mulfunc1(P[:, i]) for i in range(G)]     # group member's fitness for two aims respectively
    vectors2 = [mulfunc2(P[:, i]) for i in range(G)]
    F = nsga2(vectors1, vectors2)                        # NSGA2
    if t%50 == 0:                                        # every 50 times print a result
        print(t)
        X = [np.matmul(cost, P[:, i]) for i in range(G)]
        Y = [np.matmul(score, P[:, i]) for i in range(G)]
        plt.xlabel('cost', fontsize=15)
        plt.ylabel('score', fontsize=15)
        plt.scatter(X, Y)
        plt.show()

    crdis = []                                           # crowd distance
    for i in range(0, len(F)):
        crdis.append(crowd(vectors1[:], vectors2[:], F[i][:]))

    SP = P                                     # offspring
    while SP.shape[1] < 2*G:                   # crossover and mutation
        x1 = random.randint(0, G-1)
        x2 = random.randint(0, G-1)
        x3 = random.randint(0, G - 1)
        y3 = mutation(x3)
        Y = np.zeros(shape=[N, 3], dtype='int')
        Y[:, 0], Y[:, 1] = crossover(P[:, x1], P[:, x2])
        Y[:, 2] = mutation(P[:, x3])
        SP = np.hstack([SP, Y])                # combination of ancestor & offspring

    vectors11 = [mulfunc1(SP[:, i]) for i in range(2*G)]
    vectors22 = [mulfunc2(SP[:, i]) for i in range(2*G)]
    F2 = nsga2(vectors11, vectors22)           # NSGA2 again

    crdis2 = []                                # crowd distance again
    for i in range(0, len(F2)):
        crdis2.append(crowd(vectors11[:], vectors22[:], F2[i][:]))

    Q = []                                     # new generation
    for i in range(len(F2)):
        F21 = [index_of(F2[i][j], F2[i])for j in range(len(F2[i]))]
        F22 = seque(F21[:], crdis2[i][:])
        F = [F2[i][F22[j]]for j in range(len(F2[i]))]
        F.reverse()                            # get members into new generation till it is full of population
        for value in F:
            Q.append(value)
            if len(Q) == G:
                break
        if len(Q) == G:
            break
    for i in Q:
        P[:, i] = SP[:, i]      # new generation produced

    t += 1




import datanrp2
import numpy as np
import random
import matplotlib.pyplot as plt

lor = datanrp2.data1           # list of requirements
woc = datanrp2.data3           # weight of clients
wor = datanrp2.data2           # weight of requirements
value = datanrp2.value         # satisfaction of requirements
cost = np.zeros(shape=len(lor), dtype='int')
for i in range(len(lor)):
    cost[i] = wor[lor[i]-1, 0]   # cost of requirements
score = np.matmul(value, woc)  # overall value of requirements
N = len(cost)                  # number of requirements
G = 100                         # member in a group
T = 500                        # times
minx = 0
maxx = 1


def sigfunc(vector):
    y = (np.matmul(cost, vector)/sum(cost))+(np.matmul(score, vector)/sum(score))  # optimize y = minimize y
    return y


def select(P, fitness):
    newfit = []
    totalfit = sum(fitness)
    for i in range(len(fitness)):
        newfit.append(fitness[i]/totalfit)

    newfit = np.cumsum(newfit)
    ms = []
    poplen = P.shape[1]
    for i in range(poplen):
        ms.append(random.random())
    fitin = 0
    newin = 0
    newP = P
    while newin < poplen:
        if ms[newin] < newfit[fitin]:
            newP[newin] = P[fitin]
            newin += 1
        else:
            fitin += 1
        P = newP
    return


c = 0.05


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
    if (max(y1) != 1) | (min(y1) != 0):
        y1 = [round(minx+(maxx-minx)*random.random())for i in range(N)]
    if (max(y2) != 1) | (min(y2) != 0):
        y2 = [round(minx+(maxx-minx)*random.random())for i in range(N)]
    return y1, y2


def mutation(x):
    u = random.random()
    if u < 0.1:
        y = [round(minx+(maxx-minx)*random.random())for i in range(N)]
    else:
        y = x
    return y


def specie_orig(numofvariable, numofgroup):
    group = np.zeros(shape=[numofvariable, numofgroup], dtype='int')                 # generate a group randomly
    for j in range(G):
        p = [round(minx + (maxx - minx) * random.random()) for i in range(N)]
        group[:, j] = p
    return group


def best(P, fitness):
    px = P.shape[1]
    bestindividual = []
    bestfitness = fitness[0]
    for i in range(1, px):
        if(fitness[i] < bestfitness):
            bestfitness = fitness[i]
            bestindividual = P[:, i]
    return bestindividual, bestfitness



if __name__ == '__main__':
    t = 0                           # time = 0
    P = specie_orig(N, G)           # initial generation
    results = [[]]
    while t < T:
        fitness = [sigfunc(P[:, i]) for i in range(G)]
        best_individual, best_fitness = best(P, fitness)     # best individual
        results.append(best_individual)
        select(P, fitness)                                   # select
        x1 = random.randint(0, G - 1)
        x2 = random.randint(0, G - 1)
        x3 = random.randint(0, G - 1)
        Y = np.zeros(shape=[N, 2], dtype='int')
        Y[:, 0], Y[:, 1] = crossover(P[:, x1], P[:, x2])     # crossover
        P[:, x1], P[:, x2] = Y[:, 0], Y[:, 1]
        Y[:, 0] = mutation(P[:, x3])                         # mutation
        P[:, x3] = Y[:, 0]
        if t % 50 == 0:
            X = [np.matmul(cost, P[:, i])for i in range(G)]
            Y = [np.matmul(score, P[:, i])for i in range(G)]
            plt.xlabel('cost', fontsize=15)
            plt.ylabel('score', fontsize=15)
            plt.scatter(X, Y)
            plt.show()

        t += 1

    results = results[1:]
    for i in range(len(results)):
        print(results[i])


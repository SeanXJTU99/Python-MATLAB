import numpy as np


data1 = np.loadtxt('nrp101.txt', dtype='int')  # sequence of requirements
data1 = np.array(data1)
data11 = data1[:, 0]
data12 = data1[:, 1]
data1 = np.r_[data11, data12]                  # combine requirements A & B, we take them the same

data2 = np.loadtxt('nrp102.txt', dtype='int')  # cost of requirements
data2 = np.array(data2)

# weight of level
a = np.zeros(shape=[data2.shape[0]], dtype='int')   # recording level of requirements
for i in range(20):
    a[i] = 3
for i in range(20, 60):
    a[i] = 2
for i in range(60, 140):
    a[i] = 1
data2 = np.stack((data2, a))
data2 = np.transpose(data2)              # transpose for convenience of later calculation


with open('nrp103.txt', 'r') as file3:
    lines = file3.readlines()
    data3 = np.zeros(shape=[len(lines)], dtype='int')
    i = 0
    for line in lines:
        d = np.array(line.rsplit(), dtype='int')
        s3 = d[0]                            # we take profit as clients' weights for company
        data3[i] = round(s3)                 # initial weight of clients
        i += 1

data3 = data3/sum(data3)                     # ensure sum of weights is one
data3 = np.transpose(data3)                  # weight of clients


# value or satisfaction of requirements
value = np.zeros(shape=[len(data1), (data3.shape[0])])
with open('nrp103.txt', 'r') as file3:
    lines = file3.readlines()
    i = 0
    for line in lines:                   # for each client
        d = np.array(line.rsplit(), dtype='int')  # check the requirement he want
        for j in range(len(data1)):      # looking for corresponding requirement
            for s in range(len(d[2:])):  # only when client want the requirement, its value for the client is not zero
                if data1[j] == d[s]:
                    value[j, i] = data2[d[s], 1]
        i += 1
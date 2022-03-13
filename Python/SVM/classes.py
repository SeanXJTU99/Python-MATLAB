import numpy as np
from matplotlib import pyplot as plt


# We try to generate 2 statistics with  different means and fluctuation
# from this 2 gaussion data we randomly select datasets
def classes():
    np.random.seed(4711)  # for repeatability
    c1 = np.random.multivariate_normal(
        [10, 0], [[3, 1], [1, 4]], size=[100, ])
    # l1 = np.zeros(100)
    # l2 = np.ones(100)
    c2 = np.random.multivariate_normal(
        [0, 10], [[3, 1], [1, 4]], size=[100, ])
    # noise
    np.random.seed(1)
    noiselx = np.random.normal(0, 2, 100)
    noisely = np.random.normal(0, 8, 100)
    noise2 = np.random.normal(0, 8, 100)
    c1[:, 0] += noiselx
    c1[:, 1] += noisely
    c2[:, 1] += noise2
    Fig = plt.figure(figsize=(20, 15))
    ax = Fig.add_subplot(111)
    ax.set_xlabel('x', fontsize=30)
    ax.set_ylabel('y', fontsize=30)
    Fig.suptitle('classes', fontsize=30)
    # labels = np.concatenate((l1, l2), )
    X = np.concatenate((c1, c2), )
    pp1 = ax.scatter(c1[:, 0], c1[:, 1], cmap='prism', s=50, color='r')
    pp2 = ax.scatter(c2[:, 0], c2[:, 1], cmap='prism', s=50, color='g')
    ax.legend((pp1, pp2), ('class1', 'class2'), fontsize=35)
    Fig.savefig('classes.png')
    return Fig, X

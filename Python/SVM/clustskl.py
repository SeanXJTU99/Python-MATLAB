from scipy.cluster.hierarchy import fcluster as fc
from scipy.cluster.hierarchy import linkage as lnk
from sklearn import mixture as mit
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from matplotlib import pyplot as plt


def clust4(fig, X):
    fig.clf()  # reset plt
    fig, ((axis1, axis2), (axis3, axis4)) = plt.subplots(2, 2, sharex='col', sharey='row')

    # k-means
    km = KMeans(n_clusters=2)
    km.fit(X)
    pre_km = km.labels_
    plt.scatter(X[:, 0], X[:, 1], c=pre_km, cmap='prism')  # plot points with cluster dependent colors
    axis1.scatter(X[:, 0], X[:, 1], c=pre_km, cmap='prism')
    axis1.set_ylabel('y', fontsize=40)
    axis1.set_title('k-means', fontsize=20)

    # mean-shift
    ms = MeanShift(bandwidth=7)
    ms.fit(X)
    pred_ms = ms.labels_
    axis2.scatter(X[:, 0], X[:, 1], c=pred_ms, cmap='prism')
    axis2.set_title('mean-shift', fontsize=20)

    # gaussion mixture
    g = mit.GaussianMixture(n_components=2)
    g.fit(X)
    pred_g = g.predict(X)
    axis3.scatter(X[:, 0], X[:, 1], c=pred_g, cmap='prism')
    axis3.set_xlabel('x', fontsize=40)
    axis3.set_ylabel('y', fontsize=40)
    axis3.set_title('gaussion mixture', fontsize=20)

    # hierarchical

    Z = lnk(X, 'ward')
    max_d = 110
    pred_h = fc(Z, max_d, criterion='distance')
    axis4.scatter(X[:, 0], X[:, 1], c=pred_h, cmap='prism')
    axis4.set_xlabel('x', fontsize=40)
    axis4.set_title('hierarchical ward', fontsize=20)

    # generate the linkage matrix
    fig.set_size_inches(18.5, 10.5)
    fig.savefig('comp_clustering.png', dpi=100)
    return Z

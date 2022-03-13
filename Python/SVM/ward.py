from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt


def ward(Z):
    fig = plt.figure(figsize=(20, 15))
    plt.title('hierarchical clustering dendrogram', fontsize=30)
    plt.xlabel('data point index (or cluster index)', fontsize=30)
    plt.ylabel('distance (ward)', fontsize=30)
    dendrogram(
        Z,
        truncate_mode='lastp',  # show only the last p merged clusters
        p=12,
        leaf_rotation=90.,
        leaf_font_size=12,
        show_contracted=True,
    )
    return fig.savefig('dendrogram.png')

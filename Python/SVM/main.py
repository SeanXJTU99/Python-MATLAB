import classes
import clustskl
import ward

if __name__ == '__main__':
    fig, x = classes.classes()
    ward.ward(clustskl.clust4(fig, x))

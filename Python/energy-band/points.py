import numpy as np
import matplotlib.pyplot as plt

reload = 0
N = 15
H = 7.62  # ai*eV
pi = np.pi
A = 5.43  # ai
V0 = 0
V3 = 0
V8 = 0
V11 = 0

if reload == 1:
    V3 = -3.04768
    V8 = 0.74831
    V11 = 0.97961

node = np.array([[0, 0, 0], [2, 0, 0], [-2, 0, 0], [0, 2, 0], [0, -2, 0], [0, 0, 2], [0, 0, -2]])
n1 = np.array([[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1], [-1, 1, 1], [1, -1, 1], [1, 1, -1], [1, 1, 1]])
n2 = np.array([[2, 2, 0], [2, 0, 2], [0, 2, 2], [-2, 2, 0], [-2, 0, 2], [0, -2, 2], [2, -2, 0], [2, 0, -2], [0, 2, -2],
               [-2, -2, 0], [-2, 0, -2], [0, -2, -2]])
n3 = np.array([[3, 1, 1], [1, 3, 1], [1, 1, 3], [-3, 1, 1], [1, -3, 1], [1, 1, -3], [3, -1, 1], [-1, 3, 1], [-1, 1, 3],
               [3, 1, -1], [1, 3, -1], [1, -1, 3], [3, -1, -1], [-1, 3, -1], [-1, -1, 3], [-3, -1, 1], [-1, -3, 1],
               [-1, 1, -3], [-3, 1, -1], [1, -3, -1], [1, -1, -3], [-3, -1, -1], [-1, -3, -1], [-1, -1, -3]])

if N == 15:
    n = np.row_stack((node, n1))
elif N == 27:
    n = np.row_stack((node, n1, n2))
else:
    n = np.row_stack((node, n1, n2, n3))
g = (2 * pi / A) * n


# print(g)


def mat(k, g, Vg):
    MATRIX = np.zeros(shape=[N, N])
    for i in range(0, N):
        MATRIX[i, i] = sum((k + g[i]) ** 2)
    MATRIX = MATRIX * H/2
    MATRIX = MATRIX + Vg
    return MATRIX


def vmat(n):
    Vg = np.zeros(shape=[N, N])
    for i in range(0, N):
        for j in range(0, N):
            n_prime = n[i] - n[j]
            n_squ = sum(n_prime ** 2)
            S = np.cos(sum(n_prime) * pi / 4)
            if n_squ == 3:
                V = V3
            elif n_squ == 8:
                V = V8
            elif n_squ == 11:
                V = V11
            else:
                V = V0
            Vg[i, j] = S * V
    return Vg


energy = np.zeros(shape=[4, N])
Vg = vmat(n)
k = np.array([[0.5, 0.5, 0.5],
              [0, 0, 0],
              [1, 0, 0],
              [0.75, 0.75, 0]])
for i in range(0,4):
    M = mat(k[i, :], g, Vg)
    energy[i, :] = np.linalg.eigvalsh(M)

print(energy)
plt.plot(energy)
plt.xticks([])
plt.text(0, -4, r'$\Gamma$')
plt.text(1, -4, r'L')
plt.text(2, -4, r'X')
plt.text(3, -4, r'K')
plt.show()
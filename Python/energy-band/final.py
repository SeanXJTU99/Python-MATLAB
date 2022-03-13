import numpy as np
import matplotlib.pyplot as plt

reload = 1
N = 15
H = 7.62/2  # ai*eV
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

node = np.array(
    [[0, 0, 0], [-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1], [-1, 1, 1], [1, -1, 1], [1, 1, -1], [1, 1, 1]])
n1 = np.array([[2, 0, 0], [-2, 0, 0], [0, 2, 0], [0, -2, 0], [0, 0, 2], [0, 0, -2]])
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
            Vg[i, j] = S * V/2
    return Vg


energy = np.zeros(shape=[100, N])
Vg = vmat(n)
for i in range(0, 100):
    kk = (i / 100) * (2 * pi / A)
    k = np.array([1, 0, 0]) * kk
    M = mat(k, g, Vg)
    a = np.linalg.eigvalsh(M)
    energy[i, :] = a-5

k = np.linspace(0, 1, 100)
plt.plot(k, energy, 'k')
up = energy[:, 5]
down = energy[:, 4]
# print(down)
minim = np.argmin(up)
gap = round(min(up),2)
print('at direction of [1,0,0], k=', minim/100, ', the conduction band minimum occurs and the band gap is', gap, 'eV')

for i in range(0, 100):
    kk = (i / 100) * (2 * pi / A) * 0.5
    k = np.array([1, 1, 1]) * kk
    M = mat(k, g, Vg)
    a = np.linalg.eigvalsh(M)
    energy[i, :] = a-5

Lp = (3 * 0.5 ** 2) ** 0.5
k = np.linspace(0, -Lp, 100)
plt.ylim(-13,10)
plt.plot(k, energy, 'k')
GAMMA = np.linspace(-13, 10, 100)
gamma = np.zeros(GAMMA.shape)
xxxx = np.ones(GAMMA.shape)
L = -xxxx * Lp
plt.plot(gamma, GAMMA, 'k')
plt.xticks([])
plt.ylabel('energy')
plt.xlim(-Lp, 1)
plt.text(0, -14, r'$\Gamma$')
plt.text(-Lp, -14, r'L')
plt.text(1, -14, r'X')
plt.text(0.375,0.2,'fermi energy level')
level = np.linspace(-0.9, 1,100)
LEVEL = np.ones(level.shape)
plt.plot(level, LEVEL,'.', markersize=3)
plt.show()

'''k = np.array([1, 1, 1]) * (2 * pi / A) * 0.5
band = np.zeros(shape=[1, 3])
n = np.row_stack((node, n1))
N = 15
g = (2 * pi / A) * n
Vg = vmat(n)
M = mat(k, g, Vg)
a = np.linalg.eigvalsh(M)
band[0, 0] = a[4] - a[3]
n = np.row_stack((node, n1, n2))
N = 27
g = (2 * pi / A) * n
Vg = vmat(n)
M = mat(k, g, Vg)
a = np.linalg.eigvalsh(M)
band[0, 1] = a[4] - a[3]
n = np.row_stack((node, n1, n2, n3))
N = 51
g = (2 * pi / A) * n
Vg = vmat(n)
M = mat(k, g, Vg)
a = np.linalg.eigvalsh(M)
band[0, 2] = a[4] - a[3]
print(band)'''


band = np.zeros(shape=[1, 3])
n = np.row_stack((node, n1))
N = 15
energy = np.zeros(shape=[100, N])
g = (2 * pi / A) * n
Vg = vmat(n)
for i in range(0, 100):
    kk = (i / 100) * (2 * pi / A)
    k = np.array([1, 0, 0]) * kk
    M = mat(k, g, Vg)
    a = np.linalg.eigvalsh(M)
    energy[i, :] = a-10
band[0, 0] = energy[18,4]-energy[0, 3]
n = np.row_stack((node, n1, n2))
N = 27
energy = np.zeros(shape=[100, N])
g = (2 * pi / A) * n
Vg = vmat(n)
for i in range(0, 100):
    kk = (i / 100) * (2 * pi / A)
    k = np.array([1, 0, 0]) * kk
    M = mat(k, g, Vg)
    a = np.linalg.eigvalsh(M)
    energy[i, :] = a-10
band[0, 1] = energy[18,4]-energy[0, 3]
n = np.row_stack((node, n1, n2, n3))
N = 51
energy = np.zeros(shape=[100, N])
g = (2 * pi / A) * n
Vg = vmat(n)
for i in range(0, 100):
    kk = (i / 100) * (2 * pi / A)
    k = np.array([1, 0, 0]) * kk
    M = mat(k, g, Vg)
    a = np.linalg.eigvalsh(M)
    energy[i, :] = a-10
band[0, 2] = energy[18,4]-energy[0, 3]
print(band)

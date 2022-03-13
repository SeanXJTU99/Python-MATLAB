#  the equation we solve is
# (A phi_x )_x + (B phi_y )_y = 0
# with Dirichlet BC

#  the disrete system is
#      A_xp * (phi[i+1,j] - phi[i,j]) - A_xm * (phi[i,j] - phi[i-1,j])
#     + B_yp*(phi[i,j+1] - phi[i,j]) - B_ym * (phi[i,j] - phi[i,j-1]) = 0
#
#
#   the coefficients of the operator can be described by a 5-point stencil
#   as shown below
#
#                              B_yp
#
#       A_xm            -(A_xp+A_xm+B_yp+B_ym)              A_xp
#
#                              B_ym
#
#   A = A(x,y), B = B(x,y) and 
#    for the full potential equation A + B = rho  and then 
#    B_yp correspond to the value of B at     [x,y + 1/2 * h]
#    B_ym                             B at [x,y -1/2 * h]
#    A_xp                             A at [x+1/2 * h, y]
#    A_xm                           A at [x-1/2 * h,y]
#
#  by appropriately defining A,B we can run several models.
#   A = B = 1     the poisson equation
#   A = 1 - M*M , B = 1     the small disturbance equation
#   A = B = rho where rho = rho(u*u+v*v)
#        where u = D/Dx Phi,     v = D/Dy phi   (see lecture )
#
#   In this code I set A = B = 1
#   and you have to change it to the correct
#   formula as required by the HW
#

import numpy as np
import matplotlib.pyplot as plt
M=0.3
a=1-M*M


def BC_F(x):
    pi = np.pi
    beta = 0.05

    if x < 1 or x > 2:
        return 0.0
    else:
        return beta * np.cos(pi * (x - 1))


def error(phi):
    newphi = phi.copy()
    Nx = newphi.shape[0]
    Ny = newphi.shape[1]
    err = 0.0
    for i in range(1, Nx - 1):
        for j in range(1, Ny - 1):
            A_xp = a
            A_xm = a
            B_yp = 1
            B_ym = 1
            C0 = (A_xp + A_xm + B_yp + B_ym)
            eq = - C0 * newphi[i, j] + (B_yp * newphi[i, j + 1] + B_ym * newphi[i, j - 1] +
                                        A_xp * newphi[i + 1, j] + A_xm * newphi[i - 1, j])
            err += abs(eq)

    return err / (Nx * Ny)


def velocity_vec(phi):
    U = np.zeros((phi.shape[0] - 2, phi.shape[1] - 2))
    V = np.zeros((phi.shape[0] - 2, phi.shape[1] - 2))

    hx = 1 / phi.shape[0]
    hy = 1 / phi.shape[1]

    for i in range(1, phi.shape[0] - 1):
        for j in range(1, phi.shape[1] - 1):
            U[i - 1, j - 1] = 0.5 * (phi[i + 1, j] - phi[i - 1, j]) / hx
            V[i - 1, j - 1] = 0.5 * (phi[i, j + 1] - phi[i, j - 1]) / hy

    return U, V


def BCS(x):
    S = np.sqrt((x - 1) ** 2 + 1)  # S(x) = √{[(x - 1)^2] + 1}
    return S


def SOR(phi):
    h = 3.0 / phi.shape[0]
    newphi = phi.copy()
    sor = 1.7  # sor = 12 is Gauss-eidel relation
    for i in range(1, newphi.shape[0] - 1):
        for j in range(1, newphi.shape[1] - 1):
            A_xp = a
            A_xm = a
            B_yp = 1
            B_ym = 1
            C0 = (A_xp + A_xm + B_yp + B_ym)
            dp = -newphi[i, j] + (B_yp * newphi[i, j + 1] + B_ym * newphi[i, j - 1] +
                                  A_xp * newphi[i + 1, j] + A_xm * newphi[i - 1, j]) / C0

            newphi[i, j] += sor * dp
        # Here after this double loop we need to implement the BC at j = 0 which is
        # Neumann BC
        # the equation at j = 0, for i=1,...,N-1 is given in the lecture notes.
        # You need to add this part to the code.
    j = 0
    for i in range(1, newphi.shape[0] - 1):
        A_xp = a
        A_xm = a
        B_yp = 1
        B_ym = 1
        C0 = (A_xp + A_xm + B_yp + B_ym)

        dp = -newphi[i, j] + (2 * B_yp * newphi[i, j + 1] +
                              A_xp * newphi[i + 1, j] + A_xm * newphi[i - 1, j]
                              - 2 * h * BC_F(i * h)) / C0

        newphi[i, j] += sor * dp

    return newphi


N = 32
phi = np.zeros((3 * N, N))
U_inf = 1
h = 1 / N

#  x = i * h
# y = j * h

for i in range(3 * N):
    for j in range(N):
        phi[i, j] = U_inf * i * h
        x[i, 0] = i * h
        y[j, 0] = j * h

for iter in range(100):
    phi = SOR(phi)
    if iter % 100 == 0:
        print(iter, error(phi))  # need to see this error going to zero

#  plot streamlines of the solution
#

plt.plot(phi)
plt.show()

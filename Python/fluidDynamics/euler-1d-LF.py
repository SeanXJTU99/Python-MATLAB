
import matplotlib.pyplot as plt
import numpy as np


# a program to simulate the Euler eq 1D, see assignment no 3.
#
#  U_t + F_x = 0

#  U = (rho, m, e)
#  F = (m,m*m/rho + p, m(e + p)) 

#   U(n+1,j) = 1/2 *( U(n,j+1) + U(n,j-1)) + dt/(2*dx) (F(n,j+1) - F(n,j-1))/(2*dx)


def FU(U):
    rho = U[0]
    m = U[1]
    e = U[2]
    gamma = 1.4
    if abs(rho) == 0:
        print("U=",U)
        print("rho = 0 ...     exitting...")
        exit()
    p = (gamma -1) * (e - 0.5*m*m/rho)
    F = np.zeros(3)
    F[0] = m
    F[1] = m*m/rho + p 
    F[2] = m*(e+p)
    return F


T = 30.0
N = 64  # change this to have a finer discretization
dx = 1 / N
alpha = 0.3
dt = alpha * dx
gamma= 1.4

#BC
M = 0.3 
p_in = 1
p_out = 0.001* p_in
rho_in = 1
c2= gamma*p_in / rho_in
c = np.sqrt(c2)
u_in = c * M
e_in = 1/(gamma-1)*p_in + 0.5 * rho_in * u_in * u_in
                  
print( "RHO", rho_in,"\n U", u_in, "\n P_in", p_in, "\n P_out", p_out, "\n e ", e_in, "\n c ", c, "\n M ", u_in / c )

                  
# Numerical BC
# u_in is extrapolated
# rho_out, u_out extrapolated

U_prev = np.zeros((N,3))
F = np.zeros((N,3))
U = np.zeros((N,3))

t = 0.0
fig = plt.figure()
u = np.zeros(N)
for i in range(N):
    u[i] =u_in
    


# fix BC for initial condition

for i in range(N):
    U_prev[i,0] = rho_in
    U_prev[i,1] = rho_in * u_in
    U_prev[i,2] = 1./(gamma-1)*p_in + 0.5*rho_in*u_in*u_in
    

plt.plot(U_prev[:,0]) 
k = 0
while t < T:
    for i in range(1,N-1):
        FUp = FU(U_prev[i+1,:])
        FUm = FU(U_prev[i-1,:])
                
        U[i,:] = 0.5*(U_prev[i+1,:]+U_prev[i-1,:]) + dt/(2*dx)*(FUp - FUm)

    #  INFLOW BC.
    #   p,rho from BC and we extrapolate others. 
    U[0,0] = rho_in
    u_in = U[1,1] / U[1,0]  # u = m / rho 
    U[0,1] = rho_in * u_in
    U[0,2] = 1./(gamma -1) * p_in + 0.5 *rho_in * u_in * u_in # e_in = 1/(gamma -1)*p_in + 0.5*rho_in * u_in *u_in

    # OUTFLOW BC
    #b specift p_out fro mBC and extrapolate others, u, rho
    rho_out = U[N-2,0]    # extrapolate rho
    U[N-1,0] = rho_out
    u_out = U[N-2,1] / U[N-2,0]   # extrapolate u_out 
    U[N-1,1] = U[N-1,1] * u_out
    U[N-1,2] = 1./(gamma -1) * p_out + 0.5 *rho_out * u_out * u_out

    for i in range(N):
        #p[i] = (gamma-1)*(U[i,2] - 0.5* U[i,1]*U[i,1]/U[i,0])
        u[i] = U_prev[i,1] / U_prev[i,0]
                          
    if k % 500 == 0:
        plt.plot(U[:,0])  # plot rho
    

        
    for j in range(N):
        U_prev[j,:] = U[j,:]
            
    t = t + dt
    k = k + 1


    
plt.show()
plt.figure()
plt.plot(U[:,0])
plt.show()




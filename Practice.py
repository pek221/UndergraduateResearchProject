from scipy.integrate import odeint
import numpy
import matplotlib.pyplot as plt
import pygame


# Model
def SIR_model(N, t, beta, upsilonR, upsilonD):
    S,I,R,D = N

    dS_dt = -beta*S*I
    dI_dt = beta*S*I - (upsilonR+upsilonD)*I
    dR_dt = upsilonR * I
    dD_dt = upsilonD*I
    return([dS_dt, dI_dt, dR_dt, dD_dt])

# Initial Conditions
S0 = 0.9
I0 = 0.1
R0 = 0.0
D0 = 0.0
N = [S0,I0,R0,D0]
beta = 0.35         #Infection rate
upsilonR = 0.085    #Recovery rate
upsilonD = 0.015    #Death rate

# Time vector
t = numpy.linspace(0, 100, 100000)

solution = odeint(SIR_model, N, t, args=(beta, upsilonR, upsilonD))
solution = numpy.array(solution)

# Plot Results
plt.figure(figsize=[6, 4])
plt.plot(t, solution[:, 0], label="Susceptible(t)")
plt.plot(t, solution[:, 1], label="Infective(t)")
plt.plot(t, solution[:, 2], label="Recovered(t)")
plt.plot(t, solution[:, 3], label="Dead(t)")
plt.grid()
plt.legend()
plt.xlabel("Time (Days)")
plt.ylabel("Proportions")
plt.title("SIR Model")
plt.show()

from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from sympy.abc import xi, w, n, s
from scipy import signal
from matplotlib.patches import Rectangle
import math

def orderOfMagnitude(number):
    return math.floor(math.log(number, 10))

def butterworth(Gp, Ga, wc, wa):
    F2 = Lambda(w, 1/(1 + (xi*(w/wc)**n)**2))
    eq = Eq(F2(wc), Gp**2)
    xiCalc = solve(eq, xi)[1]
    G = F2.subs(xi, xiCalc)
    eq2 = Eq(G(wa), Ga**2)
    nCalc = solve(eq2, n)[0]
    nRound = np.ceil(nCalc)
    FS = F2.subs(((xi, xiCalc), (n, nRound)))
    FS = FS(s/I)
    aver = np.array(Poly(fraction(FS)[1]).all_coeffs(), dtype=float)
    tf1 = signal.tf2zpk(np.array(1.0, dtype=float), aver)
    a = plt.scatter(np.real(tf1[1]), np.imag(tf1[1]), marker='x', color='r')
    #plt.axis([-1.6, 1.6, -1.1, 1.1])
    plt.show()

    useful_poles = [p for p in tf1[1] if np.real(p) < 0]
    tf2 = signal.ZerosPolesGain([], useful_poles, np.cumprod(useful_poles)[-1])

    plt.scatter(np.real(tf2.poles), np.imag(tf2.poles), marker='x', color='g')
    #plt.axis([-1.6, 1.6, -1.1, 1.1])
    plt.show()

    wp, m, p = signal.bode(tf2, np.linspace(0, wa+10**orderOfMagnitude(wa), 100+10**orderOfMagnitude(wa)))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
    ax.add_patch(Rectangle((0, 1), wc, -(1 - Gp), facecolor='green', alpha=0.2))
    ax.add_patch(Rectangle((wa, 0), 10**orderOfMagnitude(wa), Ga, facecolor='red', alpha=0.2))
    plt.xlim([0, wa+10**orderOfMagnitude(wa)])
    plt.ylim([0, 1.5])
    plt.show()










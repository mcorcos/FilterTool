from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from sympy.abc import xi, w, n, s
from scipy import signal
from matplotlib.patches import Rectangle
import math

def _orderOfMagnitude(number):
    return math.floor(math.log(number, 10))

def _chevyPol(n, wc):
    if n == 0:
        return 1
    elif n == 1:
        return w/wc
    else:
        return 2*(w/wc)*_chevyPol(n-1, wc) - _chevyPol(n-2, wc)

def butterworth(Gp, Ga, wc, wa):
    F2 = Lambda(w, 1/(1 + (xi*(w/wc)**n)**2))
    eq = Eq(F2(wc), Gp**2)
    xiCalc = solve(eq, xi)[1]
    G = F2.subs(xi, xiCalc)
    eq2 = Eq(G(wa), Ga**2)
    nCalc = solve(eq2, n)[0]
    nRound = np.ceil(nCalc)
    print(nRound)
    FS = F2.subs(((xi, xiCalc), (n, nRound)))
    FS = FS(s/I)
    print(FS)

    aver = np.array(Poly(fraction(FS)[1]).all_coeffs(), dtype=float)
    tf1 = signal.tf2zpk(np.array(1.0, dtype=float), aver)
    plt.scatter(np.real(tf1[1]), np.imag(tf1[1]), marker='x', color='r')
    #plt.axis([-1.6, 1.6, -1.1, 1.1])
    plt.show()

    useful_poles = [p for p in tf1[1] if np.real(p) < 0]
    tf2 = signal.ZerosPolesGain([], useful_poles, np.cumprod(useful_poles)[-1])

    plt.scatter(np.real(tf2.poles), np.imag(tf2.poles), marker='x', color='r')
    #plt.axis([-1.6, 1.6, -1.1, 1.1])
    plt.show()

    wp, m, p = signal.bode(tf2, np.linspace(0, wa+10**_orderOfMagnitude(wa), 100+10**_orderOfMagnitude(wa)))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
    ax.add_patch(Rectangle((0, 1), wc, -(1 - Gp), facecolor='green', alpha=0.2))
    ax.add_patch(Rectangle((wa, 0), 10**_orderOfMagnitude(wa), Ga, facecolor='red', alpha=0.2))
    plt.xlim([0, wa+10**_orderOfMagnitude(wa)])
    plt.ylim([0, 1.5])
    plt.show()


def chevyshevI(Gp, Ga, wc, wa):
    p = symbols("p")

    G = 1 / (1 + (xi * p) ** 2)

    G = Lambda(p, G)

    eq = Eq(G(1), Gp ** 2)

    sol_xi = solve(eq)[1]
    Fs = G.subs(xi, sol_xi)

    F2 = Lambda(w, Fs(_chevyPol(1, wc)))

    orden = 1
    while F2(wa) > Ga ** 2:
        orden = orden+1
        F2 = Lambda(w, Fs(_chevyPol(orden, wc)))

    F3 = F2(s / I)
    print(orden)


    aver = np.array(Poly(fraction(F3)[1]).all_coeffs(), dtype=float)

    tf1 = signal.tf2zpk(np.array(1.0, dtype=float), aver)

    a = plt.scatter(np.real(tf1[1]), np.imag(tf1[1]), marker='x', color='r')
    print(type(a))
    plt.axis([-3.2, 3.2, -2.2, 2.2])
    plt.show()

    useful_poles = [p for p in tf1[1] if np.real(p) < 0]

    if orden % 2:
        tf2 = signal.ZerosPolesGain([], useful_poles, np.cumprod(useful_poles)[-1] * (
            1))  # Magic number?? Cómo es que a veces va Gp y otras no...
    else:
        tf2 = signal.ZerosPolesGain([], useful_poles, np.cumprod(useful_poles)[-1] * (
            Gp))  # Magic number?? Cómo es que a veces va Gp y otras no...

    print(tf2.gain)

    plt.scatter(np.real(tf2.poles), np.imag(tf2.poles), marker='x', color='r')
    #plt.axis([-3.2, 3.2, -2.2, 2.2])
    plt.show()

    wp, m, p = signal.bode(tf2, np.linspace(0, wa+10**_orderOfMagnitude(wa), 1000+10**_orderOfMagnitude(wa)))

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
    ax.add_patch(Rectangle((0, 1), wc, -(1 - Gp), facecolor='green', alpha=0.2))
    ax.add_patch(Rectangle((wa, 0), 10 ** _orderOfMagnitude(wa), Ga, facecolor='red', alpha=0.2))
    plt.xlim([0, wa + 10 ** _orderOfMagnitude(wa)])
    plt.ylim([0, 1.5])
    plt.show()






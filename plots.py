import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import math
from scipy import signal

def _orderOfMagnitude(number):
    return math.floor(math.log(number, 10))

def plotTemplate(F, Gp, Ga, wa):
    wp, m, p = signal.bode(F, np.linspace(0, (wa) + 10 ** _orderOfMagnitude(wa), 1000 + 10 ** _orderOfMagnitude(wa)))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
    ax.add_patch(Rectangle((0, 1), 1, -(1 - Gp), facecolor='green', alpha=0.2))
    ax.add_patch(Rectangle((wa, 0), 10 ** _orderOfMagnitude(wa), Ga, facecolor='red', alpha=0.2))
    plt.xlim([0, wa + 1 + 10 ** _orderOfMagnitude(wa)])
    plt.ylim([0, 1.1])
    plt.show()

def plotLowPass(F, Gp, Ga, wc, wa):
    wp, m, p = signal.bode(F, np.linspace(0, (wa) + 10 ** _orderOfMagnitude(wa), 1000 + 10 ** _orderOfMagnitude(wa)))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
    ax.add_patch(Rectangle((0, 1), wc, -(1 - Gp), facecolor='green', alpha=0.2))
    ax.add_patch(Rectangle((wa, 0), 10 ** _orderOfMagnitude(wa), Ga, facecolor='red', alpha=0.2))
    plt.xlim([0, wa + 1 + 10 ** _orderOfMagnitude(wa)])
    plt.ylim([0, 1.1])
    plt.show()

def plotHighPass(F, Gp, Ga, wc, wa):
    wp, m, p = signal.bode(F, np.linspace(0, (wc) + 10 ** _orderOfMagnitude(wc), 1000 + 10 ** _orderOfMagnitude(wc)))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
    ax.add_patch(Rectangle((0, 0), wa, Ga, facecolor='red', alpha=0.2))
    ax.add_patch(Rectangle((wc, 1), 10 ** _orderOfMagnitude(wc), -(1-Gp), facecolor='green', alpha=0.2))
    plt.xlim([0, wc + 1 + 10 ** _orderOfMagnitude(wc)])
    plt.ylim([0, 1.1])
    plt.show()

def plotPolesZeroes(z, p):
    plt.scatter(np.real(p), np.imag(p), marker='x', color='r')
    #plt.axis([-1.6, 1.6, -1.1, 1.1])
    plt.show()


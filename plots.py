import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import math
from scipy import signal
from utility import *

def plotTemplate(F, Gp, Ga, wa):
    wp, m, p = signal.bode(F, np.linspace(0, (wa) + 10 ** orderOfMagnitude(wa), 1000 + 10 ** orderOfMagnitude(wa)))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
    ax.add_patch(Rectangle((0, 1), 1, -(1 - Gp), facecolor='green', alpha=0.2))
    ax.add_patch(Rectangle((wa, 0), 10 ** orderOfMagnitude(wa), Ga, facecolor='red', alpha=0.2))
    #plt.xlim([0, wa + 1 + 10 ** _orderOfMagnitude(wa)])
    plt.ylim([0, 1.1])
    plt.show()

def plotLowPass(F, Gp, Ga, wc, wa):
    wp, m, p = signal.bode(F, np.linspace(0, (wa) + 10 ** orderOfMagnitude(wa), 1000 + 10 ** orderOfMagnitude(wa)))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
    ax.add_patch(Rectangle((0, 1), wc, -(1 - Gp), facecolor='green', alpha=0.2))
    ax.add_patch(Rectangle((wa, 0), 10 ** orderOfMagnitude(wa), Ga, facecolor='red', alpha=0.2))
    plt.xlim([0, wa + 1 + 10 ** orderOfMagnitude(wa)])
    plt.ylim([0, 1.1])
    plt.show()

def plotHighPass(F, Gp, Ga, wc, wa):
    wp, m, p = signal.bode(F, np.linspace(0, (wc) + 10 ** orderOfMagnitude(wc), 1000 + 10 ** orderOfMagnitude(wc)))
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
    ax.add_patch(Rectangle((0, 0), wa, Ga, facecolor='red', alpha=0.2))
    ax.add_patch(Rectangle((wc, 1), 10 ** orderOfMagnitude(wc), -(1-Gp), facecolor='green', alpha=0.2))
    #plt.xlim([0, wc + 1 + 10 ** _orderOfMagnitude(wc)])
    plt.ylim([0, 1.1])
    plt.show()

def plotBandPass(F, Gp, Ga, wcmin, wcmax, wamin, wamax, gain='veces'):
    wp, m, p = signal.bode(F, np.linspace(0, (wamax) + 10 ** orderOfMagnitude(wamax), 1000 + 10 ** orderOfMagnitude(wamax)))
    fig, ax = plt.subplots(figsize=(10, 8))
    if gain == 'veces':
        ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
        ax.add_patch(Rectangle((0, 0), wamin, Ga, facecolor='red', alpha=0.2))
        ax.add_patch(Rectangle((wamax, 0), 10 ** orderOfMagnitude(wamax), Ga, facecolor='red', alpha=0.2))
        ax.add_patch(Rectangle((wcmin, 1), wcmax, -(1 - Gp), facecolor='green', alpha=0.2))
    elif gain == 'dB':
        ax.semilogx(wp, m, label='Algún polinomio')
        #ax.add_patch(Rectangle((0, 0), wamin, Ga, facecolor='red', alpha=0.2))
        #ax.add_patch(Rectangle((wamax, 0), 10 ** orderOfMagnitude(wamax), Ga, facecolor='red', alpha=0.2))
        #ax.add_patch(Rectangle((wcmin, 1), wcmax, -(1 - Gp), facecolor='green', alpha=0.2))
    #plt.xlim([0, wc + 1 + 10 ** _orderOfMagnitude(wc)])
    #plt.ylim([0, 1.1])
    plt.show()

def plotBandReject(F, Gp, Ga, wcmin, wcmax, wamin, wamax, gain='veces'):
    wp, m, p = signal.bode(F, np.linspace(0, (wcmax) + 10 ** orderOfMagnitude(wcmax), 1000 + 10 ** orderOfMagnitude(wcmax)))
    fig, ax = plt.subplots(figsize=(10, 8))
    if gain == 'veces':
        ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
        ax.add_patch(Rectangle((0, 1), wcmin, -(1 - Gp), facecolor='green', alpha=0.2))
        ax.add_patch(Rectangle((wamin, 0), wamax, Ga, facecolor='red', alpha=0.2))
        ax.add_patch(Rectangle((wcmax, 1), 10 ** orderOfMagnitude(wcmax), -(1 - Gp), facecolor='green', alpha=0.2))
    elif gain == 'dB':
        ax.semilogx(wp, m, label='Algún polinomio')
        #ax.add_patch(Rectangle((0, 0), wamin, Ga, facecolor='red', alpha=0.2))
        #ax.add_patch(Rectangle((wamax, 0), 10 ** orderOfMagnitude(wamax), Ga, facecolor='red', alpha=0.2))
        #ax.add_patch(Rectangle((wcmin, 1), wcmax, -(1 - Gp), facecolor='green', alpha=0.2))
    #plt.xlim([0, wc + 1 + 10 ** _orderOfMagnitude(wc)])
    #plt.ylim([0, 1.1])
    plt.show()

def plotPolesZeroes(z, p):
    plt.scatter(np.real(p), np.imag(p), marker='x', color='r')
    #plt.axis([-1.6, 1.6, -1.1, 1.1])
    plt.show()


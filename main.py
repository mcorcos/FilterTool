
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def dB(G):
    return 20*np.log10(G)

if __name__ == '__main__':
    wc = 1
    wa = 1.5
    Gp = 0.96
    Ga = 0.01
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk')
    Gp = 0.96 ** 2
    Ga = 0.01 ** 2
    a = plt.scatter(np.real(p), np.imag(p), marker='x', color='r')
    plt.axis([-1.6, 1.6, -1.1, 1.1])
    plt.show()
    w, m, p = signal.bode(signal.zpk2tf(z, p, k), n=1000)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(w, 10 ** (m / 20))
    ax.add_patch(Rectangle((0, 1), 1, -(1 - Gp ** 0.5), facecolor='green', alpha=0.2))
    ax.add_patch(Rectangle((wa, 0), 1, Ga ** 0.5, facecolor='red', alpha=0.2))
    plt.xlim([0, 2])
    plt.ylim([0, 1])
    plt.show()



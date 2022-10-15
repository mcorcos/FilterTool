from scipy import signal
import numpy as np

def dB(G):
    return 20*np.log10(G)

def butterNormalized(wa, Gp, Ga):
    N, wp = signal.buttord(1, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk')
    return z, p, k

def butterLowPass(wc, wa, Gp, Ga):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk')
    return z, p, k

def butterHighPass(wc, wa, Gp, Ga):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk', btype='highpass')
    return z, p, k

"""
def butterLowPass(wc, wa, Gp, Ga):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk')
    return z, p, k

def butterLowPass(wc, wa, Gp, Ga):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk')
    return z, p, k
"""


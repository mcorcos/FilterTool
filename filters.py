from scipy import signal
import numpy as np
from utility import *



def butterNormalized(wa, Gp, Ga, n=0):
    N, wp = signal.buttord(1, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    print(N)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk')
    return z, p, k

def butterLowPass(wc, wa, Gp, Ga, n=0):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.butter(N, wp, analog=True, output='zpk')
    return z, p, k, N

def chevyINormalized(wa, Gp, Ga, n=0):
    N, wp = signal.cheb1ord(1, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    print(N)
    z, p, k = signal.cheby1(N, -dB(Gp), wp, analog=True, output='zpk')
    return z, p, k

def chevyILowPass(wc, wa, Gp, Ga, n=0):
    N, wp = signal.cheb1ord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.cheby1(N, -dB(Gp), wp, analog=True, output='zpk')
    return z, p, k, N

def butterHighPass(wc, wa, Gp, Ga):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk', btype='highpass')
    return z, p, k

def butterBandPass(wc, wa, Gp, Ga):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk', btype='bandpass')
    return z, p, k

def butterBandReject(wc, wa, Gp, Ga):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk', btype='bandstop')
    return z, p, k



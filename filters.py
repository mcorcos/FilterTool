from scipy import signal
import numpy as np
from utility import *



def butterNormalized(wa, Gp, Ga, n=0):
    N, wp = signal.buttord(1, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.butter(N, wp, analog=True, output='zpk')
    return z, p, k

def butter(wc, wa, Gp, Ga, fType, n=0):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.butter(N, wp, analog=True, output='zpk', btype=fType)
    return z, p, k, N

def chevyINormalized(wa, Gp, Ga, n=0):
    N, wp = signal.cheb1ord(1, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.cheby1(N, -dB(Gp), wp, analog=True, output='zpk')
    return z, p, k

def chevyI(wc, wa, Gp, Ga, fType, n=0):
    N, wp = signal.cheb1ord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.cheby1(N, -dB(Gp), wp, analog=True, output='zpk', btype=fType)
    return z, p, k, N

def chevyIINormalized(wa, Gp, Ga, n=0):
    N, wp = signal.cheb2ord(1, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.cheby2(N, -dB(Ga), wp, analog=True, output='zpk')
    return z, p, k

def chevyII(wc, wa, Gp, Ga, fType, n=0):
    N, wp = signal.cheb2ord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.cheby2(N, -dB(Ga), wp, analog=True, output='zpk', btype=fType)
    return z, p, k, N

def cauerNormalized(wa, Gp, Ga, n=0):
    N, wp = signal.ellipord(1, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.ellip(N, -dB(Gp), -dB(Ga), wp, analog=True, output='zpk')
    return z, p, k

def cauer(wc, wa, Gp, Ga, fType, n=0):
    N, wp = signal.ellipord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.ellip(N, -dB(Gp), -dB(Ga), wp, analog=True, output='zpk', btype=fType)
    return z, p, k, N


def butterBandPass(wc, wa, Gp, Ga):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk', btype='bandpass')
    return z, p, k

def butterBandReject(wc, wa, Gp, Ga):
    N, wp = signal.buttord(wc, wa, -dB(Gp), -dB(Ga), analog=True)
    z, p, k = signal.butter(N, wp, analog=True, output='zpk', btype='bandstop')
    return z, p, k



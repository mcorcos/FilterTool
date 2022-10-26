from scipy import signal
import numpy as np
from utility import *


def findIndex(m, Ga):
    for i in range(len(m)):
        if m[i] < dB(Ga):
            return i

def butterNormalized(wa, Gp, Ga, n=0):
    N, wp = signal.buttord(1, wa, -dB(Gp), -dB(Ga), analog=True)
    if n != 0:
        N = n
    z, p, k = signal.butter(N, wp, analog=True, output='zpk')
    return z, p, k, N

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
    return z, p, k, N

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
    return z, p, k, N

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
    return z, p, k, N

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

def denormLp(z, p, k, Ga, wan, wc, denorm):
    w, m, f = signal.bode(signal.zpk2tf(z, p, k), n=3000)
    ind = findIndex(m, Ga)
    dist = wan - w[ind]
    c = (wan / (wan - dist*denorm))
    z, p, k = signal.lp2lp_zpk(z, p, k, c)
    z, p, k = signal.lp2lp_zpk(z, p, k, wc)
    return z, p, k

def denormhp(z, p, k, Ga, wan, wc, denorm):
    w, m, f = signal.bode(signal.zpk2tf(z, p, k), n=3000)
    ind = findIndex(m, Ga)
    dist = wan - w[ind]
    c = (wan / (wan - dist*denorm))
    z, p, k = signal.lp2lp_zpk(z, p, k, c)
    z, p, k = signal.lp2hp_zpk(z, p, k, wc)
    return z, p, k

def denormBp(z, p, k, Ga, wan, wc, B, denorm):
    w, m, f = signal.bode(signal.zpk2tf(z, p, k), n=3000)
    ind = findIndex(m, Ga)
    dist = wan - w[ind]
    c = (wan / (wan - dist*denorm))
    z, p, k = signal.lp2lp_zpk(z, p, k, c)
    z, p, k = signal.lp2bp_zpk(z, p, k, wc, B)
    return z, p, k

def denormBr(z, p, k, Ga, wan, wc, B, denorm):
    w, m, f = signal.bode(signal.zpk2tf(z, p, k), n=3000)
    ind = findIndex(m, Ga)
    dist = wan - w[ind]
    c = (wan / (wan - dist*denorm))
    z, p, k = signal.lp2lp_zpk(z, p, k, c)
    z, p, k = signal.lp2bs_zpk(z, p, k, wc, B)
    return z, p, k


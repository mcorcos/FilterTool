import numpy as np
import math

def dB(G):
    return 20*np.log10(G)

def orderOfMagnitude(number):
    return math.floor(math.log(number, 10))

def anti_dB(G):
    return 10**(G/20)
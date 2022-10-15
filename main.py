from filters import *
from plots import *

if __name__ == '__main__':
    wc = 1
    wa = 1.5
    Gp = 0.96
    Ga = 0.01
    z, p, k = butterNormalized(wa, Gp, Ga)
    plotPolesZeroes(z, p)
    plotTemplate(signal.zpk2tf(z, p, k), Gp, Ga, wc, wa)





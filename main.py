from filters import *
from plots import *

if __name__ == '__main__':
    wc = 1500
    wa = 1000
    Gp = 0.96
    Ga = 0.01
    zn, pn, kn = butterNormalized(wc/wa, Gp, Ga)
    #plotPolesZeroes(zn, pn)
    plotTemplate(signal.zpk2tf(zn, pn, kn), Gp, Ga, wc/wa)
    z, p, k = butterHighPass(wc, wa, Gp, Ga)
    #plotPolesZeroes(z, p)
    plotHighPass(signal.zpk2tf(z, p, k), Gp, Ga, wc, wa)






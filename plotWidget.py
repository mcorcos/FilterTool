from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import scipy.signal as signal
from utility import *

class plotWidget():

    def __init__(self, parent=None):

        self.plotList = []
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot()
        plt.tight_layout()
        self.navToolBar = NavigationToolbar(self.canvas, parent=parent)
        self.colorMap = plt.rcParams['axes.prop_cycle'].by_key()['color']
        self.colorIndex = 0
        self.scatterPoles = []
        self.scatterZeroes = []

    def patchLowPass(self, Gp, Ga, wc, wa):
        self.ax.add_patch(Rectangle((0, 1), wc, -(1 - Gp), facecolor='green', alpha=0.2))
        self.ax.add_patch(Rectangle((wa, 0), 10 ** orderOfMagnitude(wa), Ga, facecolor='red', alpha=0.2))
        self.canvas.show()

    def patchHighPass(self, Gp, Ga, wc, wa):
        self.ax.add_patch(Rectangle((wc, 1),10 ** orderOfMagnitude(wc) , -(1 - Gp), facecolor='green', alpha=0.2))
        self.ax.add_patch(Rectangle((0, 0), wa, Ga, facecolor='red', alpha=0.2))
        self.canvas.show()

    def patchLowPassBode(self, Gp, Ga, wc, wa):
        self.ax.add_patch(Rectangle((0, dB(1)), wc, dB(Gp), facecolor='green', alpha=0.2))
        self.ax.add_patch(Rectangle((wa, dB(Ga)), 10 ** orderOfMagnitude(wa), -20, facecolor='red', alpha=0.2))
        self.canvas.show()

    def patchLowPassAt(self,  Gp, Ga, wc, wa):
        self.ax.add_patch(Rectangle((0, -dB(Gp)), wc, 300, facecolor='green', alpha=0.2))
        self.ax.add_patch(Rectangle((wa, 0), 10 ** (orderOfMagnitude(wa)+1), -dB(Ga), facecolor='red', alpha=0.2))
        self.canvas.show()

    def patchHighPassAt(self, Gp, Ga, wc, wa):
        self.ax.add_patch(Rectangle((wc, -dB(Gp)), 10 ** (orderOfMagnitude(wc) + 1), 300, facecolor='green', alpha=0.2))
        self.ax.add_patch(Rectangle((0, 0), wa, -dB(Ga), facecolor='red', alpha=0.2))
        self.canvas.show()

    def plotTemplate(self, F, Gp, Ga, wa, labeltxt):
        wp, m, p = signal.bode(F, np.linspace(0, (wa) + 10 ** orderOfMagnitude(wa), 1000 + 10 ** orderOfMagnitude(wa)))
        self.ax.plot(wp, 10 ** (m / 20), label=labeltxt)
        self.ax.grid()
        self.ax.legend()
        self.canvas.draw()


    def plotVeces(self, F, Gp, Ga, wc, wa, labeltxt):
        wm = max(wa, wc)
        wp, m, p = signal.bode(F, np.linspace(0, (wm) + 10 ** orderOfMagnitude(wm), 1000 + 10 ** orderOfMagnitude(wm)))
        fig, ax = plt.subplots()
        self.ax.plot(wp, 10 ** (m / 20), label=labeltxt)
        self.ax.grid()
        self.ax.legend()
        self.canvas.show()

    def plotVecesBand(self, F, Gp, Ga, wc, wa, labeltxt):
        wm = max(wa[0], wc[0], wa[1], wc[0])
        wn = min(wa[0], wc[0], wa[1], wc[0])
        wp, m, p = signal.bode(F, np.linspace(wn - 10 ** orderOfMagnitude(wn), (wm) + 10 ** orderOfMagnitude(wm), 1000 + 10 ** orderOfMagnitude(wm)))
        fig, ax = plt.subplots()
        self.ax.plot(wp, 10 ** (m / 20), label=labeltxt)
        self.ax.grid()
        self.ax.legend()
        self.canvas.show()

    def plotBode(self, F, Gp, Ga, wc, wa, labeltxt):
        wm = max(wa, wc)
        wn = min(wa, wc)
        wp, m, p = signal.bode(F, np.logspace(orderOfMagnitude(wn) - 1, 1 + orderOfMagnitude(wm), 1000 + 10 ** orderOfMagnitude(wm)))
        self.ax.semilogx(wp, m, label=labeltxt)
        self.ax.grid('log')
        self.ax.legend()
        self.canvas.show()

    def plotBodeBand(self, F, Gp, Ga, wc, wa, labeltxt):
        wm = max(wa[0], wa[1], wc[0], wc[1])
        wn = min(wa[0], wa[1], wc[0], wc[1])
        wp, m, p = signal.bode(F, np.logspace(orderOfMagnitude(wn) - 1, 1 + orderOfMagnitude(wm), 1000 + 10 ** orderOfMagnitude(wm)))
        self.ax.semilogx(wp, m, label=labeltxt)
        self.ax.grid('log')
        self.ax.legend()
        self.canvas.show()

    def plotAt(self, F, wc, wa, labeltxt):
        wm = max(wa, wc)
        wn = min(wa, wc)
        wp, m, p = signal.bode(F, np.logspace(orderOfMagnitude(wn) - 1, 1 + orderOfMagnitude(wm), 1000 + 10 ** orderOfMagnitude(wm)))
        self.ax.semilogx(wp, -m, label=labeltxt)
        self.ax.grid('log')
        self.ax.legend()
        self.canvas.show()

    def plotAtBand(self, F, wc, wa, labeltxt):
        wm = max(wa[0], wa[1], wc[0], wc[1])
        wn = min(wa[0], wa[1], wc[0], wc[1])
        wp, m, p = signal.bode(F, np.logspace(orderOfMagnitude(wn) - 1, 1 + orderOfMagnitude(wm), 1000 + 10 ** orderOfMagnitude(wm)))
        self.ax.semilogx(wp, -m, label=labeltxt)
        self.ax.grid('log')
        self.ax.legend()
        self.canvas.show()


    def plotFase(self, F, wc, wa, labeltxt):
        wm = max(wa, wc)
        wn = min(wa, wc)
        wp, m, p = signal.bode(F, np.logspace(orderOfMagnitude(wn) - 1, 1 + orderOfMagnitude(wm),
                                              1000 + 10 ** orderOfMagnitude(wm)))
        self.ax.semilogx(wp, p, label=labeltxt)
        self.ax.grid('log')
        self.ax.legend()
        self.canvas.show()

    def plotFaseBand(self, F, wc, wa, labeltxt):
        wm = max(wa[0], wa[1], wc[0], wc[1])
        wn = min(wa[0], wa[1], wc[0], wc[1])
        wp, m, p = signal.bode(F, np.logspace(orderOfMagnitude(wn) - 1, 1 + orderOfMagnitude(wm),
                                              1000 + 10 ** orderOfMagnitude(wm)))
        self.ax.semilogx(wp, p, label=labeltxt)
        self.ax.grid('log')
        self.ax.legend()
        self.canvas.show()


    def plotStepResp(self, F, labeltxt):
        t, y = signal.step(F, N=1000)
        self.ax.plot(t, y, label=labeltxt)
        self.ax.grid()
        self.ax.legend()
        self.canvas.show()

    def plotBandPass(self, F, Gp, Ga, wcmin, wcmax, wamin, wamax, gain='veces'):
        wp, m, p = signal.bode(F, np.linspace(0, (wamax) + 10 ** orderOfMagnitude(wamax),
                                              1000 + 10 ** orderOfMagnitude(wamax)))
        fig, ax = plt.subplots(figsize=(10, 8))
        if gain == 'veces':
            ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
            ax.add_patch(Rectangle((0, 0), wamin, Ga, facecolor='red', alpha=0.2))
            ax.add_patch(Rectangle((wamax, 0), 10 ** orderOfMagnitude(wamax), Ga, facecolor='red', alpha=0.2))
            ax.add_patch(Rectangle((wcmin, 1), wcmax, -(1 - Gp), facecolor='green', alpha=0.2))
        elif gain == 'dB':
            ax.semilogx(wp, m, label='Algún polinomio')
            # ax.add_patch(Rectangle((0, 0), wamin, Ga, facecolor='red', alpha=0.2))
            # ax.add_patch(Rectangle((wamax, 0), 10 ** orderOfMagnitude(wamax), Ga, facecolor='red', alpha=0.2))
            # ax.add_patch(Rectangle((wcmin, 1), wcmax, -(1 - Gp), facecolor='green', alpha=0.2))
        # plt.xlim([0, wc + 1 + 10 ** _orderOfMagnitude(wc)])
        # plt.ylim([0, 1.1])
        plt.show()



    def plotBandReject(self, F, Gp, Ga, wcmin, wcmax, wamin, wamax, gain='veces'):
        wp, m, p = signal.bode(F, np.linspace(0, (wcmax) + 10 ** orderOfMagnitude(wcmax),
                                              1000 + 10 ** orderOfMagnitude(wcmax)))
        fig, ax = plt.subplots(figsize=(10, 8))
        if gain == 'veces':
            ax.plot(wp, 10 ** (m / 20), label='Algún polinomio')
            ax.add_patch(Rectangle((0, 1), wcmin, -(1 - Gp), facecolor='green', alpha=0.2))
            ax.add_patch(Rectangle((wamin, 0), wamax, Ga, facecolor='red', alpha=0.2))
            ax.add_patch(Rectangle((wcmax, 1), 10 ** orderOfMagnitude(wcmax), -(1 - Gp), facecolor='green', alpha=0.2))
        elif gain == 'dB':
            ax.semilogx(wp, m, label='Algún polinomio')
            # ax.add_patch(Rectangle((0, 0), wamin, Ga, facecolor='red', alpha=0.2))
            # ax.add_patch(Rectangle((wamax, 0), 10 ** orderOfMagnitude(wamax), Ga, facecolor='red', alpha=0.2))
            # ax.add_patch(Rectangle((wcmin, 1), wcmax, -(1 - Gp), facecolor='green', alpha=0.2))
        # plt.xlim([0, wc + 1 + 10 ** _orderOfMagnitude(wc)])
        # plt.ylim([0, 1.1])
        plt.show()

    def plotPolesZeroes(self, z, p, labeltxt):
        self.scatterPoles.append(self.ax.scatter(np.real(p), np.imag(p), marker='x', color=self.colorMap[self.colorIndex], label=labeltxt + ' (polos)'))
        self.scatterZeroes.append(self.ax.scatter(np.real(z), np.imag(z), marker='o', color=self.colorMap[self.colorIndex], label=labeltxt + ' (ceros)'))
        self.ax.set_aspect('equal')
        self.ax.set_box_aspect(1)
        self.ax.grid()
        self.colorIndex = self.colorIndex + 1
        self.ax.legend()
        self.canvas.show()

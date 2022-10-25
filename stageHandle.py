from plotWidget import plotWidget
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget
import math
from scipy.signal import zpk2tf, ZerosPolesGain, tf2zpk
import numpy as np
from utility import *

class StageHandle:
    def __init__(self, page, comboBoxes, filterCombo, stageCheckbox, gainBox):
        self.graphs = [plotWidget(), plotWidget(), plotWidget()]
        self.transferFunctions = []
        self.data = []
        self.stages = []
        self.stagesF = []
        self.graphNum = 0
        self.comboBoxes = comboBoxes
        self.filterCombo = filterCombo
        self.page = page
        self.stageCheckbox = stageCheckbox
        self.gainBox = gainBox

        i = 2
        for layout in page.findChild(QStackedWidget).findChildren(QVBoxLayout):
            layout.addWidget(self.graphs[i].navToolBar)
            layout.addWidget(self.graphs[i].canvas)
            i = i - 1

    def numOfStages(self, index):
        for combos in self.comboBoxes:
            combos.clear()
            combos.addItem('--')
        stages = math.ceil(len(self.transferFunctions[index-1][1])/2)
        self.stages = [None]*stages
        self.stagesF = [None]*stages
        for i in range(stages):
            self.comboBoxes[0].addItem('Etapa ' + str(i+1))
        self.graphs[0].ax.clear()
        self.graphs[0].plotSelectedPZ(self.transferFunctions[index-1][0], self.transferFunctions[index-1][1],
                                       self.transferFunctions[index-1][3])
        F = zpk2tf(self.transferFunctions[index - 1][0], self.transferFunctions[index - 1][1],
                   self.transferFunctions[index - 1][2])
        self.graphs[1].ax.clear()
        if self.data[index - 1][7] == 'highpass' or self.data[index - 1][7] == 'lowpass':
            self.graphs[1].plotBode(F, self.data[index - 1][1], self.data[index - 1][3],
                                    self.data[index - 1][0], self.data[index - 1][2], self.transferFunctions[index-1][3])
        else:
            self.graphs[1].plotBodeBand(F, self.data[index - 1][1], self.data[index - 1][3],
                                        self.data[index - 1][0], self.data[index - 1][2], self.transferFunctions[index-1][3])
        for poles in self.transferFunctions[index - 1][1]:
            self.comboBoxes[1].addItem("{:g}".format(poles))
            self.comboBoxes[2].addItem("{:g}".format(poles))

        for zeroes in self.transferFunctions[index - 1][0]:
            self.comboBoxes[3].addItem("{:g}".format(zeroes))
            self.comboBoxes[4].addItem("{:g}".format(zeroes))

    def deleteStage(self):
        self.stages[self.comboBoxes[0].currentIndex() - 1] = None
        self.stagesF[self.comboBoxes[0].currentIndex() - 1] = None
        for i in range(1, len(self.comboBoxes)):
            self.comboBoxes[i].setCurrentIndex(0)

    def saveSelection(self):
        index = self.filterCombo.currentIndex() - 1
        index0 = self.comboBoxes[0].currentIndex() - 1
        index1 = self.comboBoxes[1].currentIndex() - 1
        index2 = self.comboBoxes[2].currentIndex() - 1
        index3 = self.comboBoxes[3].currentIndex() - 1
        index4 = self.comboBoxes[4].currentIndex() - 1
        check = self.stageCheckbox.checkState()
        if index1 >= 0:
            P1 = self.transferFunctions[index][1][index1]
        else:
            P1 = None
        if index2 >= 0:
            P2 = self.transferFunctions[index][1][index2]
        else:
            P2 = None
        if index3 >= 0:
            Z1 = self.transferFunctions[index][0][index3]
        else:
            Z1 = None
        if index4 >= 0:
            Z2 = self.transferFunctions[index][0][index4]
        else:
            Z2 = None
        if P2 is None and Z2 is None and Z1 is None:
            self.stages[index0] = [[[], [P1], P1, 0], [index1+1, index2+1, index3+1, index4+1, index0+1, check]]
        elif P2 is None and Z2 is None:
            if Z1:
                G = P1/Z1
            else:
                G = P1
            self.stages[index0] = [[[Z1], [P1], G, 0], [index1+1, index2+1, index3+1, index4+1, index0+1, check]]
        elif Z2 is None:
            if Z1:
                G = (P1*P2)/Z1
            else:
                G = P1*P2
            self.stages[index0] = [[[Z1], [P1, P2], G, 0], [index1+1, index2+1, index3+1, index4+1, index0+1, check]]
        elif Z2 is None and Z1 is None:
            self.stages[index0] = [[[], [P1, P2], P1*P2, 0], [index1+1, index2+1, index3+1, index4+1, index0+1, check]]
        else:
            if Z1 and not Z2:
                G = (P1*P2)/Z1
            elif Z2 and not Z1:
                G = (P1*P2)/Z2
            elif not Z1 and not Z2:
                G = P1 * P2
            else:
                G = (P1 * P2) / (Z2 * Z1)
            self.stages[index0] = [[[Z1, Z2], [P1, P2], G, 0], [index1+1, index2+1, index3+1, index4+1, index0+1, check]]
        self.graphs[0].plotSelectedP(P1)
        self.graphs[0].plotSelectedP(P2)
        self.graphs[0].plotSelectedZ(Z1)
        self.graphs[0].plotSelectedZ(Z2)

    def solveQ(self):
        for i in range(len(self.stages)):
            Z = self.stages[i][0][0]
            if not Z or Z[0] is None:
                Z = []
            P = self.stages[i][0][1]
            if not P or P[0] is None:
                P = []
            k = self.stages[i][0][2]
            F = zpk2tf(Z, P, k)
            G = 1/F[1][-1]
            for j in range(len(F[1])):
                F[1][j] = F[1][j]/F[1][-1]
            G = G*F[0][-1]
            for j in range(len(F[0])):
                F[0][j] = F[0][j]/F[0][-1]
            if len(F[0]) == 2:
                wcz = 1/F[0][0]
                Qz = 0
            elif len(F[0]) == 3:
                wcz = 1/math.sqrt(F[0][0])
                Qz = 1/(wcz*F[0][1])
            else:
                wcz = None
                Qz = None
            if len(F[1]) == 2:
                wcp = 1/F[1][0]
                Qp = 0
            if len(F[1]) == 3:
                wcp = 1/math.sqrt(F[1][0])
                Qp = 1/(wcp*F[1][1])
            self.stagesF[i] = [F, G, wcz, Qz, wcp, Qp]
            self.stages[i][0][3] = Qp

    def solveGain(self):
        Qt = 0
        index = self.filterCombo.currentIndex() - 1
        k = self.transferFunctions[index][2]
        print(k)
        arr = []
        for stage in self.stages:
            Qt = Qt + stage[0][3]
            print(stage[0][2])
            k = k/stage[0][2]
        i = 0
        print(k)
        for stage in self.stages:
            arr.append([stage[0][3]/Qt, i])
            i = i + 1
        arr.sort()
        print(np.real(k))
        k = dB(np.real(k))
        for i in range(len(self.stages)):
            if i < len(self.stages) - 1:
                k = k/2
                print(k)
            self.stages[arr[i][1]][0][2] = anti_dB(k)*self.stages[arr[i][1]][0][2]


    def plotCascade(self):
        poles = []
        zeros = []
        gain = 0
        for stage in self.stages:
            if stage[1][5]:
                for i in range(len(stage[0][1])):
                    poles.append(stage[0][1][i])
                if not stage[0][0] or stage[0][0][0] is None:
                    zeros = []
                else:
                    for i in range(len(stage[0][0])):
                        zeros.append(stage[0][0][i])
                gain += dB(stage[0][2])
        gain = anti_dB(gain)
        F = zpk2tf(zeros, poles, gain)
        self.graphs[2].plotBodeAlt(F)


    def showSelection(self, index):
        if index-1 >= 0 and self.stages[index-1]:
            for i in range(1, len(self.comboBoxes)):
                self.comboBoxes[i].setCurrentIndex(self.stages[index-1][1][i-1])
            self.stageCheckbox.setChecked(self.stages[index-1][1][5])
            self.gainBox.setText(str(dB(self.stages[index-1][0][2])))

    def placeConjugatePole1(self, index):
        if index-1 >= 0:
            indexFil = self.filterCombo.currentIndex() - 1
            P1 = self.transferFunctions[indexFil][1][index - 1]
            for i in range(len(self.transferFunctions[indexFil][1])):
                p = self.transferFunctions[indexFil][1][i]
                if np.real(p) == np.real(P1) and np.imag(p) == -np.imag(P1) and np.imag(p):
                    self.comboBoxes[2].setCurrentIndex(i+1)

    def placeConjugatePole2(self, index):
        if index-1 >= 0:
            indexFil = self.filterCombo.currentIndex() - 1
            P1 = self.transferFunctions[indexFil][1][index - 1]
            for i in range(len(self.transferFunctions[indexFil][1])):
                p = self.transferFunctions[indexFil][1][i]
                if np.real(p) == np.real(P1) and np.imag(p) == -np.imag(P1) and np.imag(p):
                    self.comboBoxes[1].setCurrentIndex(i+1)

    def placeConjugateZero1(self, index):
        if index-1 >= 0:
            indexFil = self.filterCombo.currentIndex() - 1
            P1 = self.transferFunctions[indexFil][0][index - 1]
            for i in range(len(self.transferFunctions[indexFil][0])):
                p = self.transferFunctions[indexFil][0][i]
                if np.real(p) == np.real(P1) and np.imag(p) == -np.imag(P1) and np.imag(p):
                    self.comboBoxes[4].setCurrentIndex(i+1)

    def placeConjugateZero2(self, index):
        if index-1 >= 0:
            indexFil = self.filterCombo.currentIndex() - 1
            P1 = self.transferFunctions[indexFil][0][index - 1]
            for i in range(len(self.transferFunctions[indexFil][0])):
                p = self.transferFunctions[indexFil][0][i]
                if np.real(p) == np.real(P1) and np.imag(p) == -np.imag(P1) and np.imag(p):
                    self.comboBoxes[3].setCurrentIndex(i+1)

from plotWidget import plotWidget
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget
import math
from scipy.signal import zpk2tf, ZerosPolesGain, tf2zpk
import numpy as np

class StageHandle:
    def __init__(self, page, comboBoxes, filterCombo):
        self.graphs = [plotWidget(), plotWidget(), plotWidget()]
        self.transferFunctions = []
        self.data = []
        self.stages = []
        self.graphNum = 0
        self.comboBoxes = comboBoxes
        self.filterCombo = filterCombo
        self.page = page

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
        for i in range(stages):
            self.comboBoxes[0].addItem('Etapa ' + str(i+1))
        self.graphs[0].ax.clear()
        self.graphs[0].plotSelectedPZ(self.transferFunctions[index-1][0], self.transferFunctions[index-1][1],
                                       self.transferFunctions[index-1][3])
        F = zpk2tf(self.transferFunctions[index - 1][0], self.transferFunctions[index - 1][1],
                   self.transferFunctions[index - 1][2])
        self.graphs[1].ax.clear()
        self.graphs[1].plotBode(F, self.data[index - 1][1], self.data[index - 1][3],
                                self.data[index - 1][0], self.data[index - 1][2], self.transferFunctions[index-1][3])

        for poles in self.transferFunctions[index - 1][1]:
            self.comboBoxes[1].addItem("{:g}".format(poles))
            self.comboBoxes[2].addItem("{:g}".format(poles))

        for zeroes in self.transferFunctions[index - 1][0]:
            self.comboBoxes[3].addItem("{:g}".format(zeroes))
            self.comboBoxes[4].addItem("{:g}".format(zeroes))

    def deleteStage(self):
        self.stages[self.comboBoxes[0].currentIndex() - 1] = None
        for i in range(1, len(self.comboBoxes)):
            self.comboBoxes[i].setCurrentIndex(0)

    def saveSelection(self):
        index = self.filterCombo.currentIndex() - 1
        index0 = self.comboBoxes[0].currentIndex() - 1
        index1 = self.comboBoxes[1].currentIndex() - 1
        index2 = self.comboBoxes[2].currentIndex() - 1
        index3 = self.comboBoxes[3].currentIndex() - 1
        index4 = self.comboBoxes[4].currentIndex() - 1
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
        if not P2 and not Z2 and not Z1:
            self.stages[index0] = [[[], [P1], 1, 0], [index1+1, index2+1, index3+1, index4+1, index0+1]]
        elif not P2 and not Z2:
            self.stages[index0] = [[[Z1], [P1], 1, 0], [index1+1, index2+1, index3+1, index4+1, index0+1]]
        elif not Z2:
            self.stages[index0] = [[[Z1], [P1, P2], 1, 0], [index1+1, index2+1, index3+1, index4+1, index0+1]]
        elif not Z2 and not Z1:
            self.stages[index0] = [[[], [P1, P2], 1, 0], [index1+1, index2+1, index3+1, index4+1, index0+1]]
        else:
            self.stages[index0] = [[[Z1, Z2], [P1, P2], 1, 0], [index1+1, index2+1, index3+1, index4+1, index0+1]]
        self.graphs[0].plotSelectedP(P1)
        self.graphs[0].plotSelectedP(P2)
        self.graphs[0].plotSelectedZ(Z1)
        self.graphs[0].plotSelectedZ(Z2)

    def solveQ(self):
        print(len(self.stages))
        for i in range(len(self.stages)):
            Z = self.stages[i][0][0]
            print(Z)
            if not Z or Z[0] is None:
                print('la concha de tu madre')
                Z = []
            print(Z)
            P = self.stages[i][0][1]
            if not P or P[0] is None:
                P = []
            print(P)
            k = self.stages[i][0][2]
            F = zpk2tf(Z, P, k)
            print(F)


    def showSelection(self, index):
        if index-1 >= 0 and self.stages[index-1]:
            for i in range(1, len(self.comboBoxes)):
                self.comboBoxes[i].setCurrentIndex(self.stages[index-1][1][i-1])

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

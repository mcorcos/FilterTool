from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout
from filters import *
from scipy.signal import zpk2tf
from plots import plots
import numpy as np
import matplotlib.pyplot as mpl
from stageHandle import StageHandle

class iniciar:
    def __init__(self):
        # init
        app = QtWidgets.QApplication([])
        self.ventana = uic.loadUi("GUI.ui")
        self.ventana.show()

        self.lowPass = plots('lowPass')
        self.createCanvas(self.lowPass)
        self.lowPassPage = 0
        self.lowPassData = []

        self.highPass = plots('highPass')
        self.createCanvas(self.highPass)
        self.highPassPage = 0
        self.highPassData = []

        self.bandPass = plots('bandPass')
        self.createCanvas(self.bandPass)
        self.bandPassPage = 0
        self.bandPassData = []

        self.bandReject = plots('bandReject')
        self.createCanvas(self.bandReject)
        self.bandRejectPage = 0
        self.bandRejectData = []

        self.comboBoxes = [self.ventana.stageCombo, self.ventana.p1Combo, self.ventana.p2Combo,
                           self.ventana.z1Combo, self.ventana.z2Combo]
        self.stageHandle = StageHandle(self.ventana.stageTab, self.comboBoxes,  self.ventana.filterCombo,
                                       self.ventana.plotCheck, self.ventana.gain)

        self.rightButtons = QtWidgets.QButtonGroup()
        self.rightButtons.addButton(self.ventana.RightLowPass, 0)
        self.rightButtons.addButton(self.ventana.RightHighPass, 1)
        self.rightButtons.addButton(self.ventana.RightBandPass, 2)
        self.rightButtons.addButton(self.ventana.RightBandReject, 3)
        self.rightButtons.addButton(self.ventana.rightStages, 4)

        self.leftButtons = QtWidgets.QButtonGroup()
        self.leftButtons.addButton(self.ventana.LeftLowPass, 0)
        self.leftButtons.addButton(self.ventana.LeftHighPass, 1)
        self.leftButtons.addButton(self.ventana.LeftBandPass, 2)
        self.leftButtons.addButton(self.ventana.LeftBandReject, 3)
        self.leftButtons.addButton(self.ventana.leftStages, 4)

        self.rightButtons.buttonClicked.connect(self.nextPage)
        self.leftButtons.buttonClicked.connect(self.prevPage)

        self.plotButtons = QtWidgets.QButtonGroup()
        self.plotButtons.addButton(self.ventana.LowPassBtn, 0)
        self.plotButtons.addButton(self.ventana.HighPassBtn, 1)
        self.plotButtons.addButton(self.ventana.BandPassBtn, 2)
        self.plotButtons.addButton(self.ventana.BandRejectBtn, 3)

        self.plotButtons.buttonClicked.connect(self.getDataLowHigh)
        self.plotButtons.buttonClicked.connect(self.template)
        self.plotButtons.buttonClicked.connect(self.plotAll)

        self.deleteButtons = QtWidgets.QButtonGroup()
        self.deleteButtons.addButton(self.ventana.lowPassElim, 0)
        self.deleteButtons.addButton(self.ventana.highPassElim, 1)
        self.deleteButtons.addButton(self.ventana.bandPassElim, 2)
        self.deleteButtons.addButton(self.ventana.bandRejectElim, 3)

        self.deleteButtons.buttonClicked.connect(self.deleteAll)

        self.newButtons = QtWidgets.QButtonGroup()
        self.newButtons.addButton(self.ventana.newLowPass, 0)
        self.newButtons.addButton(self.ventana.newHighPass, 1)
        self.newButtons.addButton(self.ventana.newBandPass, 2)
        self.newButtons.addButton(self.ventana.newBandReject, 3)

        self.newButtons.buttonClicked.connect(self.getDataLowHigh)
        self.newButtons.buttonClicked.connect(self.plotAll)

        self.ventana.lowPassList.currentIndexChanged.connect(self.showDataLP)
        self.ventana.highPassList.currentIndexChanged.connect(self.showDataHP)
        self.ventana.bandPassList.currentIndexChanged.connect(self.showDataBP)
        self.ventana.bandRejectList.currentIndexChanged.connect(self.showDataBR)

        self.ventana.filterCombo.currentIndexChanged.connect(self.stageHandle.numOfStages)
        self.ventana.clrStageButton.clicked.connect(self.stageHandle.deleteStage)
        self.ventana.selectButton.clicked.connect(self.stageHandle.saveSelection)
        self.ventana.stageCombo.currentIndexChanged.connect(self.stageHandle.showSelection)
        self.ventana.p1Combo.currentIndexChanged.connect(self.stageHandle.placeConjugatePole1)
        self.ventana.p2Combo.currentIndexChanged.connect(self.stageHandle.placeConjugatePole2)
        self.ventana.z1Combo.currentIndexChanged.connect(self.stageHandle.placeConjugateZero1)
        self.ventana.z2Combo.currentIndexChanged.connect(self.stageHandle.placeConjugateZero2)
        self.ventana.splitButton.clicked.connect(self.stageHandle.solveQ)
        self.ventana.splitButton.clicked.connect(self.stageHandle.solveGain)
        self.ventana.splitButton.clicked.connect(self.stageHandle.plotCascade)


        app.exec()


    def createCanvas(self, plot):
        i = 7
        if plot.type == 'lowPass':
            for layout in self.ventana.LowPassStack.findChildren(QVBoxLayout):
                layout.addWidget(plot.array[i].navToolBar)
                layout.addWidget(plot.array[i].canvas)
                i = i - 1
        if plot.type == 'highPass':
            for layout in self.ventana.HighPassStack.findChildren(QVBoxLayout):
                layout.addWidget(plot.array[i].navToolBar)
                layout.addWidget(plot.array[i].canvas)
                i = i - 1
        if plot.type == 'bandPass':
            for layout in self.ventana.BandPassStack.findChildren(QVBoxLayout):
                layout.addWidget(plot.array[i].navToolBar)
                layout.addWidget(plot.array[i].canvas)
                i = i - 1
        if plot.type == 'bandReject':
            for layout in self.ventana.BandRejectStack.findChildren(QVBoxLayout):
                layout.addWidget(plot.array[i].navToolBar)
                layout.addWidget(plot.array[i].canvas)
                i = i - 1


    def nextPage(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            self.lowPassPage = self.lowPassPage + 1
            self.ventana.LowPassStack.setCurrentIndex(self.lowPassPage)
        if index == 1:
            self.highPassPage = self.highPassPage + 1
            self.ventana.HighPassStack.setCurrentIndex(self.highPassPage)
        if index == 2:
            self.bandPassPage = self.bandPassPage + 1
            self.ventana.BandPassStack.setCurrentIndex(self.bandPassPage)
        if index == 3:
            self.bandRejectPage = self.bandRejectPage + 1
            self.ventana.BandRejectStack.setCurrentIndex(self.bandRejectPage)
        if index == 4:
            self.stageHandle.graphNum = self.stageHandle.graphNum + 1
            self.ventana.stageStack.setCurrentIndex(self.stageHandle.graphNum)


    def prevPage(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            self.lowPassPage = self.lowPassPage - 1
            self.ventana.LowPassStack.setCurrentIndex(self.highPassPage)
        if index == 1:
            self.highPassPage = self.highPassPage - 1
            self.ventana.HighPassStack.setCurrentIndex(self.highPassPage)
        if index == 2:
            self.bandPassPage = self.bandPassPage - 1
            self.ventana.BandPassStack.setCurrentIndex(self.bandPassPage)
        if index == 3:
            self.bandRejectPage = self.bandRejectPage - 1
            self.ventana.BandRejectStack.setCurrentIndex(self.bandRejectPage)
        if index == 4:
            self.stageHandle.graphNum = self.stageHandle.graphNum - 1
            self.ventana.stageStack.setCurrentIndex(self.stageHandle.graphNum)

    def plotAll(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            self.plotLowPass()
            self.ventana.lowPassList.addItem(self.ventana.LowPassLabel.text())
        elif index == 1:
            self.plotHighPass()
            self.ventana.highPassList.addItem(self.ventana.HighPassLabel.text())
        elif index == 2:
            self.plotBandPass()

        elif index == 3:
            self.plotBandReject()
            self.ventana.bandRejectList.addItem(self.ventana.BandRejectLabel.text())


    def deleteAll(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            for i in range(len(self.lowPass.array)):
                if i != 7:
                    self.lowPass.array[i].ax.lines.pop(self.ventana.lowPassList.currentIndex() - 1)
                else:
                    self.lowPass.array[i].scatterPoles[self.ventana.lowPassList.currentIndex() - 1].remove()
                    self.lowPass.array[i].scatterPoles.pop(self.ventana.lowPassList.currentIndex() - 1)
                    self.lowPass.array[i].scatterZeroes[self.ventana.lowPassList.currentIndex() - 1].remove()
                    self.lowPass.array[i].scatterZeroes.pop(self.ventana.lowPassList.currentIndex() - 1)
                self.lowPass.array[i].ax.legend()
            self.lowPassData.pop(self.ventana.lowPassList.currentIndex() - 1)
            self.ventana.lowPassList.removeItem(self.ventana.lowPassList.currentIndex())
        elif index == 1:
            for i in range(len(self.highPass.array)):
                if i != 7:
                    self.highPass.array[i].ax.lines.pop(self.ventana.highPassList.currentIndex() - 1)
                else:
                    self.highPass.array[i].scatterPoles[self.ventana.highPassList.currentIndex() - 1].remove()
                    self.highPass.array[i].scatterPoles.pop(self.ventana.highPassList.currentIndex() - 1)
                    self.highPass.array[i].scatterZeroes[self.ventana.highPassList.currentIndex() - 1].remove()
                    self.highPass.array[i].scatterZeroes.pop(self.ventana.highPassList.currentIndex() - 1)
                self.highPass.array[i].ax.legend()
            self.highPassData.pop(self.ventana.highPassList.currentIndex() - 1)
            self.ventana.highPassList.removeItem(self.ventana.highPassList.currentIndex())
        elif index == 2:
            for i in range(len(self.bandPass.array)):
                if i != 7:
                    self.bandPass.array[i].ax.lines.pop(self.ventana.bandPassList.currentIndex() - 1)
                else:
                    self.bandPass.array[i].scatterPoles[self.ventana.bandPassList.currentIndex() - 1].remove()
                    self.bandPass.array[i].scatterPoles.pop(self.ventana.bandPassList.currentIndex() - 1)
                    self.bandPass.array[i].scatterZeroes[self.ventana.bandPassList.currentIndex() - 1].remove()
                    self.bandPass.array[i].scatterZeroes.pop(self.ventana.bandPassList.currentIndex() - 1)
                self.bandPass.array[i].ax.legend()
            self.bandPassData.pop(self.ventana.bandPassList.currentIndex() - 1)
            self.ventana.bandPassList.removeItem(self.ventana.bandPassList.currentIndex())
        elif index == 3:
            for i in range(len(self.bandReject.array)):
                if i != 7:
                    self.bandReject.array[i].ax.lines.pop(self.ventana.bandRejectList.currentIndex() - 1)
                else:
                    self.bandReject.array[i].scatterPoles[self.ventana.bandRejectList.currentIndex() - 1].remove()
                    self.bandReject.array[i].scatterPoles.pop(self.ventana.bandRejectList.currentIndex() - 1)
                    self.bandReject.array[i].scatterZeroes[self.ventana.bandRejectList.currentIndex() - 1].remove()
                    self.bandReject.array[i].scatterZeroes.pop(self.ventana.bandRejectList.currentIndex() - 1)
                self.bandReject.array[i].ax.legend()
            self.bandRejectData.pop(self.ventana.bandRejectList.currentIndex() - 1)
            self.ventana.bandRejectList.removeItem(self.ventana.bandRejectList.currentIndex())



    def showDataLP(self, index):
        if index != 0:
            Wp, Gp, Wa, Ga, N, label, fIndex = self.lowPassData[index - 1]
            self.ventana.LowPassWp.setText(str(Wp))
            self.ventana.LowPassWa.setText(str(Wa))
            self.ventana.LowPassGp.setText(str(Gp))
            self.ventana.LowPassGa.setText(str(Ga))
            self.ventana.LowPassN.setText(str(N))
            self.ventana.LowPassLabel.setText(label)
            self.ventana.LowPassCombo.setCurrentIndex(fIndex)


    def showDataHP(self, index):
        if index != 0:
            Wp, Gp, Wa, Ga, N, label, fIndex = self.highPassData[index - 1]
            self.ventana.HighPassWp.setText(str(Wp))
            self.ventana.HighPassWa.setText(str(Wa))
            self.ventana.HighPassGp.setText(str(Gp))
            self.ventana.HighPassGa.setText(str(Ga))
            self.ventana.HighPassN.setText(str(N))
            self.ventana.HighPassLabel.setText(label)
            self.ventana.HighPassCombo.setCurrentIndex(fIndex)

    def showDataBP(self, index):
        if index != 0:
            wcN, wcP, Gp, waN, waP, Ga, N, label, fIndex = self.bandPassData[index - 1]
            Wp = [wcN, wcP]
            Wa = [waN, waP]
            self.ventana.BandPassBp.setText(str(Wp))
            self.ventana.BandPassBa.setText(str(Wa))
            self.ventana.BandPassGp.setText(str(Gp))
            self.ventana.BandPassGa.setText(str(Ga))
            self.ventana.BandPassN.setText(str(N))
            self.ventana.BandPassLabel.setText(label)
            self.ventana.BandPassCombo.setCurrentIndex(fIndex)

    def showDataBR(self, index):
        if index != 0:
            wcN, wcP, Gp, waN, waP, Ga, N, label, fIndex = self.bandRejectData[index - 1]
            Wp = [wcN, wcP]
            Wa = [waN, waP]
            self.ventana.BandRejectBp.setText(str(Wp))
            self.ventana.BandRejectBa.setText(str(Wa))
            self.ventana.BandRejectGp.setText(str(Gp))
            self.ventana.BandRejectGa.setText(str(Ga))
            self.ventana.BandRejectN.setText(str(N))
            self.ventana.BandRejectLabel.setText(label)
            self.ventana.BandRejectCombo.setCurrentIndex(fIndex)


    def getDataLowHigh(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            Wp = float(self.ventana.LowPassWp.text())
            Gp = anti_dB(float(self.ventana.LowPassGp.text()))
            Wa = float(self.ventana.LowPassWa.text())
            Ga = anti_dB(float(self.ventana.LowPassGa.text()))
            N = self.ventana.LowPassN.text()
            label = self.ventana.LowPassLabel.text()
            fIndex = self.ventana.LowPassCombo.currentIndex()
            if not N:
                N = 0
            N = int(N)
            self.lowPassData.append([Wp, Gp, Wa, Ga, N, label, fIndex])
        elif index == 1:
            Wp = float(self.ventana.HighPassWp.text())
            Gp = anti_dB(float(self.ventana.HighPassGp.text()))
            Wa = float(self.ventana.HighPassWa.text())
            Ga = anti_dB(float(self.ventana.HighPassGa.text()))
            N = self.ventana.HighPassN.text()
            label = self.ventana.HighPassLabel.text()
            fIndex = self.ventana.HighPassCombo.currentIndex()
            if not N:
                N = 0
            N = int(N)
            self.highPassData.append([Wp, Gp, Wa, Ga, N, label, fIndex])
        elif index == 2:
            if not self.ventana.passCheck.isChecked():
                Wc = self.ventana.BandPassBp.text().split(', ')
                wcP = float(Wc[1])
                wcN = float(Wc[0])
                Wa = self.ventana.BandPassBa.text().split(', ')
                waP = float(Wa[1])
                waN = float(Wa[0])
            elif self.ventana.passCheck.isChecked():
                Wo = float(self.ventana.BandPassWo.text())
                Bp = float(self.ventana.BandPassBp.text())
                Ba = float(self.ventana.BandPassBa.text())
                wcP = Wo+Bp/2
                wcN = Wo-Bp/2
                waP = Wo+Ba/2
                waN = Wo-Ba/2
            Gp = anti_dB(float(self.ventana.BandPassGp.text()))
            Ga = anti_dB(float(self.ventana.BandPassGa.text()))
            N = self.ventana.BandPassN.text()
            label = self.ventana.BandPassLabel.text()
            fIndex = self.ventana.BandPassCombo.currentIndex()
            if not N:
                N = 0
            N = int(N)
            self.bandPassData.append([wcN, wcP, Gp, waN, waP, Ga, N, label, fIndex])
            if wcN/waN < waP/wcP:
                waP = wcN*wcP/waN
            elif wcN/waN >= waP/wcP:
                waN = wcN*wcP/waP
            label = label + ' (simetrica)'
            self.bandPassData.append([wcN, wcP, Gp, waN, waP, Ga, N, label, fIndex])

        elif index == 3:
            if not self.ventana.rejectCheck.isChecked():
                Wc = self.ventana.BandRejectBp.text().split(', ')
                wcP = float(Wc[1])
                wcN = float(Wc[0])
                Wa = self.ventana.BandRejectBa.text().split(', ')
                waP = float(Wa[1])
                waN = float(Wa[0])
            elif self.ventana.rejectCheck.isChecked():
                Wo = float(self.ventana.BandRejectWo.text())
                Bp = float(self.ventana.BandRejectBp.text())
                Ba = float(self.ventana.BandRejectBa.text())
                wcP = Wo + Bp / 2
                wcN = Wo - Bp / 2
                waP = Wo + Ba / 2
                waN = Wo - Ba / 2
            Gp = anti_dB(float(self.ventana.BandRejectGp.text()))
            Ga = anti_dB(float(self.ventana.BandRejectGa.text()))
            N = self.ventana.BandRejectN.text()
            label = self.ventana.BandRejectLabel.text()
            fIndex = self.ventana.BandRejectCombo.currentIndex()
            if not N:
                N = 0
            N = int(N)
            self.bandRejectData.append([wcN, wcP, Gp, waN, waP, Ga, N, label, fIndex])
            if wcN/waN < waP/wcP:
                wcP = waN*waP/wcN
            elif wcN/waN >= waP/wcP:
                wcN = waN*waP/wcP
            label = label + ' (simetrica)'
            self.bandRejectData.append([wcN, wcP, Gp, waN, waP, Ga, N, label, fIndex])

    def template(self):
        if self.ventana.filterTabs.currentIndex() == 0:
            Wp, Gp, Wa, Ga, Nin, label, fIndex = self.lowPassData[-1]
            for i in range(len(self.lowPass.array)):
                [p.remove() for p in reversed(self.lowPass.array[i].ax.patches)]
            Wan = Wa / Wp
            self.lowPass.array[0].patchLowPass(Gp, Ga, 1, Wan)
            self.lowPass.array[1].patchLowPass(Gp, Ga, Wp, Wa)
            self.lowPass.array[2].patchLowPassBode(Gp, Ga, Wp, Wa)
            self.lowPass.array[3].patchLowPassAt(Gp, Ga, Wp, Wa)
        if self.ventana.filterTabs.currentIndex() == 1:
            Wp, Gp, Wa, Ga, Nin, label, fIndex = self.highPassData[-1]
            for i in range(len(self.highPass.array)):
                [p.remove() for p in reversed(self.highPass.array[i].ax.patches)]
            Wan = Wp / Wa
            self.highPass.array[0].patchLowPass(Gp, Ga, 1, Wan)
            self.highPass.array[1].patchHighPass(Gp, Ga, Wp, Wa)
            self.highPass.array[3].patchHighPassAt(Gp, Ga, Wp, Wa)

    def plotLowPass(self):
        Wp, Gp, Wa, Ga, Nin, label, fIndex = self.lowPassData[-1]
        Wan = Wa/Wp
        if self.ventana.LowPassCombo.currentIndex() == 0:
            zn, pn, kn = butterNormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = butter(Wp, Wa, Gp, Ga, 'lowpass', Nin)
        elif self.ventana.LowPassCombo.currentIndex() == 1:
            zn, pn, kn = chevyINormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = chevyI(Wp, Wa, Gp, Ga, 'lowpass', Nin)
        elif self.ventana.LowPassCombo.currentIndex() == 2:
            zn, pn, kn = chevyIINormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = chevyII(Wp, Wa, Gp, Ga, 'lowpass', Nin)
        elif self.ventana.LowPassCombo.currentIndex() == 3:
            zn, pn, kn = cauerNormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = cauer(Wp, Wa, Gp, Ga, 'lowpass', Nin)
        F = zpk2tf(z, p, k)
        self.lowPass.array[0].plotTemplate(zpk2tf(zn, pn, kn), Gp, Ga, Wan, label)
        self.lowPass.array[1].plotVeces(F, Gp, Ga, Wp, Wa, label)
        self.lowPass.array[2].plotBode(F, Gp, Ga, Wp, Wa, label)
        self.lowPass.array[3].plotAt(F, Wp, Wa, label)
        self.lowPass.array[4].plotFase(F, Wp, Wa, label)
        self.lowPass.array[5].plotAt(F, Wp, Wa, label)
        self.lowPass.array[6].plotStepResp(F, label)
        self.lowPass.array[7].plotPolesZeroes(z, p, label)
        self.ventana.LowPassN.setText(str(N))
        self.lowPassData.pop(-1)
        self.lowPassData.append([Wp, Gp, Wa, Ga, N, label, fIndex])
        self.stageHandle.transferFunctions.append([z, p, k, label])
        self.stageHandle.data.append([Wp, Gp, Wa, Ga, N, label, fIndex, 'lowpass'])
        self.ventana.filterCombo.addItem(label)

        #self.printSos(z, p, k)

    def plotHighPass(self):
        Wp, Gp, Wa, Ga, Nin, label, fIndex = self.highPassData[-1]
        Wan = Wp / Wa
        if self.ventana.HighPassCombo.currentIndex() == 0:
            zn, pn, kn = butterNormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = butter(Wp, Wa, Gp, Ga, 'highpass', Nin)
        elif self.ventana.HighPassCombo.currentIndex() == 1:
            zn, pn, kn = chevyINormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = chevyI(Wp, Wa, Gp, Ga, 'highpass', Nin)
        elif self.ventana.HighPassCombo.currentIndex() == 2:
            zn, pn, kn = chevyIINormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = chevyII(Wp, Wa, Gp, Ga, 'highpass', Nin)
        elif self.ventana.HighPassCombo.currentIndex() == 3:
            zn, pn, kn = cauerNormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = cauer(Wp, Wa, Gp, Ga, 'highpass', Nin)
        F = zpk2tf(z, p, k)
        self.highPass.array[0].plotTemplate(zpk2tf(zn, pn, kn), Gp, Ga, Wan, label)
        self.highPass.array[1].plotVeces(F, Gp, Ga, Wp, Wa, label)
        self.highPass.array[2].plotBode(F, Gp, Ga, Wp, Wa, label)
        self.highPass.array[3].plotAt(F, Wp, Wa, label)
        self.highPass.array[4].plotFase(F, Wp, Wa, label)
        self.highPass.array[5].plotAt(F, Wp, Wa, label)
        self.highPass.array[6].plotStepResp(F, label)
        self.highPass.array[7].plotPolesZeroes(z, p, label)
        self.ventana.HighPassN.setText(str(N))
        self.highPassData.pop(-1)
        self.highPassData.append([Wp, Gp, Wa, Ga, N, label, fIndex])
        self.stageHandle.transferFunctions.append([z, p, k, label])
        self.stageHandle.data.append([Wp, Gp, Wa, Ga, N, label, fIndex, 'highpass'])
        self.ventana.filterCombo.addItem(label)

    def plotBandPass(self):
        for i in reversed(range(1, 3)):
            wcN, wcP, Gp, waN, waP, Ga, Nin, label, fIndex = self.bandPassData[-i]
            Wan = (waP-waN) / (wcP-wcN)
            Wp = [wcN, wcP]
            Wa = [waN, waP]
            if self.ventana.BandPassCombo.currentIndex() == 0:
                zn, pn, kn = butterNormalized(Wan, Gp, Ga, Nin)
                z, p, k, N = butter(Wp, Wa, Gp, Ga, 'bandpass', Nin)
            elif self.ventana.BandPassCombo.currentIndex() == 1:
                zn, pn, kn = chevyINormalized(Wan, Gp, Ga, Nin)
                z, p, k, N = chevyI(Wp, Wa, Gp, Ga, 'bandpass', Nin)
            elif self.ventana.BandPassCombo.currentIndex() == 2:
                zn, pn, kn = chevyIINormalized(Wan, Gp, Ga, Nin)
                z, p, k, N = chevyII(Wp, Wa, Gp, Ga, 'bandpass', Nin)
            elif self.ventana.BandPassCombo.currentIndex() == 3:
                zn, pn, kn = cauerNormalized(Wan, Gp, Ga, Nin)
                z, p, k, N = cauer(Wp, Wa, Gp, Ga, 'bandpass', Nin)
            F = zpk2tf(z, p, k)
            self.bandPass.array[0].plotTemplate(zpk2tf(zn, pn, kn), Gp, Ga, Wan, label)
            self.bandPass.array[1].plotVecesBand(F, Gp, Ga, Wp, Wa, label)
            self.bandPass.array[2].plotBodeBand(F, Gp, Ga, Wp, Wa, label)
            self.bandPass.array[3].plotAtBand(F, Wp, Wa, label)
            self.bandPass.array[4].plotFaseBand(F, Wp, Wa, label)
            self.bandPass.array[5].plotAtBand(F, Wp, Wa, label)
            self.bandPass.array[6].plotStepResp(F, label)
            self.bandPass.array[7].plotPolesZeroes(z, p, label)
            self.ventana.BandPassN.setText(str(N))
            self.bandPassData.pop(-i)
            self.bandPassData.insert(-i+1, [wcN, wcP, Gp, waN, waP, Ga, N, label, fIndex])
            self.stageHandle.transferFunctions.append([z, p, k, label])
            self.stageHandle.data.append([Wp, Gp, Wa, Ga, N, label, fIndex, 'bandpass'])
            self.ventana.filterCombo.addItem(label)
            self.ventana.bandPassList.addItem(label)

    def plotBandReject(self):
        for i in reversed(range(1, 3)):
            wcN, wcP, Gp, waN, waP, Ga, Nin, label, fIndex = self.bandRejectData[-i]
            print([wcN, wcP, Gp, waN, waP, Ga, Nin, label, fIndex])
            Wan = (wcP-wcN) / (waP-waN)
            print(Wan)
            Wp = [wcN, wcP]
            Wa = [waN, waP]
            if self.ventana.BandRejectCombo.currentIndex() == 0:
                zn, pn, kn = butterNormalized(Wan, Gp, Ga, Nin)
                z, p, k, N = butter(Wp, Wa, Gp, Ga, 'bandstop', Nin)
            elif self.ventana.BandRejectCombo.currentIndex() == 1:
                zn, pn, kn = chevyINormalized(Wan, Gp, Ga, Nin)
                z, p, k, N = chevyI(Wp, Wa, Gp, Ga, 'bandstop', Nin)
            elif self.ventana.BandRejectCombo.currentIndex() == 2:
                zn, pn, kn = chevyIINormalized(Wan, Gp, Ga, Nin)
                z, p, k, N = chevyII(Wp, Wa, Gp, Ga, 'bandstop', Nin)
            elif self.ventana.BandRejectCombo.currentIndex() == 3:
                zn, pn, kn = cauerNormalized(Wan, Gp, Ga, Nin)
                z, p, k, N = cauer(Wp, Wa, Gp, Ga, 'bandstop', Nin)
            F = zpk2tf(z, p, k)
            self.bandReject.array[0].plotTemplate(zpk2tf(zn, pn, kn), Gp, Ga, Wan, label)
            self.bandReject.array[1].plotVecesBand(F, Gp, Ga, Wp, Wa, label)
            self.bandReject.array[2].plotBodeBand(F, Gp, Ga, Wp, Wa, label)
            self.bandReject.array[3].plotAtBand(F, Wp, Wa, label)
            self.bandReject.array[4].plotFaseBand(F, Wp, Wa, label)
            self.bandReject.array[5].plotAtBand(F, Wp, Wa, label)
            self.bandReject.array[6].plotStepResp(F, label)
            self.bandReject.array[7].plotPolesZeroes(z, p, label)
            self.ventana.BandRejectN.setText(str(N))
            self.bandRejectData.pop(-i)
            self.bandRejectData.insert(-i + 1, [wcN, wcP, Gp, waN, waP, Ga, N, label, fIndex])
            self.stageHandle.transferFunctions.append([z, p, k, label])
            self.stageHandle.data.append([Wp, Gp, Wa, Ga, N, label, fIndex, 'bandreject'])
            self.ventana.filterCombo.addItem(label)
            self.ventana.bandRejectList.addItem(label)

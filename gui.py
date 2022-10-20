from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout
from filters import *
from scipy.signal import zpk2tf
from plotWidget import plotWidget
from plots import plots

class iniciar:
    def __init__(self):
        # init
        app = QtWidgets.QApplication([])
        self.ventana = uic.loadUi("GUI.ui")
        self.ventana.show()

        self.lowPass = plots()
        self.createCanvas(self.lowPass)
        self.lowPassPage = 0
        self.lowPassData = []

        self.ventana.RightLowPass.clicked.connect(self.nextPage)
        self.ventana.LeftLowPass.clicked.connect(self.prevPage)

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

        self.deleteButtons.buttonClicked.connect(self.deleteAll)

        self.newButtons = QtWidgets.QButtonGroup()
        self.newButtons.addButton(self.ventana.newLowPass, 0)

        self.newButtons.buttonClicked.connect(self.getDataLowHigh)
        self.newButtons.buttonClicked.connect(self.plotAll)

        self.ventana.lowPassList.currentIndexChanged.connect(self.showData)

        app.exec()

    def createCanvas(self, plot):
        if plot.type == 'lowPass':
            i = 7
            for layout in self.ventana.LowPassStack.findChildren(QVBoxLayout):
                layout.addWidget(plot.array[i].navToolBar)
                layout.addWidget(plot.array[i].canvas)
                i = i - 1


    def nextPage(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            self.lowPassPage = self.lowPassPage + 1
            self.ventana.LowPassStack.setCurrentIndex(self.lowPassPage)

    def prevPage(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            self.lowPassPage = self.lowPassPage - 1
            self.ventana.LowPassStack.setCurrentIndex(self.lowPassPage)

    def plotAll(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            self.plotLowPass()
            self.ventana.lowPassList.addItem(self.ventana.LowPassLabel.text())
        elif index == 1:
            self.plotHighPass()

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
            self.lowPassData.pop(self.ventana.lowPassList.currentIndex() - 1)
            self.ventana.lowPassList.removeItem(self.ventana.lowPassList.currentIndex())

    def showData(self, index):
        if index != 0:
            Wp, Gp, Wa, Ga, N, label, fIndex = self.lowPassData[index - 1]
            self.ventana.LowPassWp.setText(str(Wp))
            self.ventana.LowPassWa.setText(str(Wa))
            self.ventana.LowPassGp.setText(str(Gp))
            self.ventana.LowPassGa.setText(str(Ga))
            self.ventana.LowPassN.setText(str(N))
            self.ventana.LowPassLabel.setText(label)
            self.ventana.LowPassCombo.setCurrentIndex(fIndex)

    def getDataLowHigh(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            Wp = float(self.ventana.LowPassWp.text())
            Gp = float(self.ventana.LowPassGp.text())
            Wa = float(self.ventana.LowPassWa.text())
            Ga = float(self.ventana.LowPassGa.text())
            N = self.ventana.LowPassN.text()
            label = self.ventana.LowPassLabel.text()
            fIndex = self.ventana.LowPassCombo.currentIndex()
            if not N:
                N = 0
            N = int(N)
        elif index == 1:
            Wp = float(self.ventana.HighPassWp.text())
            Gp = float(self.ventana.HighPassGp.text())
            Wa = float(self.ventana.HighPassWa.text())
            Ga = float(self.ventana.HighPassGa.text())
        self.lowPassData.append([Wp, Gp, Wa, Ga, N, label, fIndex])

    def template(self):
        Wp, Gp, Wa, Ga, Nin, label, fIndex = self.lowPassData[-1]
        if self.ventana.filterTabs.currentIndex() == 0:
            [p.remove() for p in reversed(self.lowPass.array[0].ax.patches)]
            Wan = Wa / Wp
            self.lowPass.array[0].patchLowPass(Gp, Ga, 1, Wan)
            self.lowPass.array[1].patchLowPass(Gp, Ga, Wp, Wa)
            self.lowPass.array[2].patchLowPassBode(Gp, Ga, Wp, Wa)
            self.lowPass.array[3].patchLowPassAt(Gp, Ga, Wp, Wa)

    def plotLowPass(self):
        Wp, Gp, Wa, Ga, Nin, label, fIndex = self.lowPassData[-1]
        Wan = Wa/Wp
        if self.ventana.LowPassCombo.currentIndex() == 0:
            zn, pn, kn = butterNormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = butterLowPass(Wp, Wa, Gp, Ga, Nin)
        elif self.ventana.LowPassCombo.currentIndex() == 1:
            zn, pn, kn = chevyINormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = chevyILowPass(Wp, Wa, Gp, Ga, Nin)
        elif self.ventana.LowPassCombo.currentIndex() == 2:
            zn, pn, kn = chevyIINormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = chevyIILowPass(Wp, Wa, Gp, Ga, Nin)
        elif self.ventana.LowPassCombo.currentIndex() == 3:
            zn, pn, kn = cauerNormalized(Wan, Gp, Ga, Nin)
            z, p, k, N = cauerLowPass(Wp, Wa, Gp, Ga, Nin)
        F = zpk2tf(z, p, k)
        self.lowPass.array[0].plotTemplate(zpk2tf(zn, pn, kn), Gp, Ga, Wan, label)
        self.lowPass.array[1].plotLowPass(F, Gp, Ga, Wp, Wa, label)
        self.lowPass.array[2].plotLowPassBode(F, Gp, Ga, Wp, Wa, label)
        self.lowPass.array[3].plotLowPassAt(F, Wp, Wa, label)
        self.lowPass.array[4].plotLowPassAt(F, Wp, Wa, label)
        self.lowPass.array[5].plotLowPassAt(F, Wp, Wa, label)
        self.lowPass.array[6].plotLowPassAt(F, Wp, Wa, label)
        self.lowPass.array[7].plotPolesZeroes(z, p, label)
        self.ventana.LowPassN.setText(str(N))
        self.lowPassData.pop(-1)
        self.lowPassData.append([Wp, Gp, Wa, Ga, N, label, fIndex])

    def plotHighPass(self):
        Wp, Gp, Wa, Ga = self.getDataLowHigh(1)
        print(Wp, Gp, Wa, Ga)
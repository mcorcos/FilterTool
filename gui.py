from PyQt5 import QtWidgets, uic
from filters import *
from plots import *
from scipy.signal import zpk2tf
from plotWidget import plotWidget
from PyQt5.QtGui import QKeySequence

class iniciar:
    def __init__(self):
        # init
        app = QtWidgets.QApplication([])
        self.ventana = uic.loadUi("GUI.ui")
        self.ventana.show()

        self.TemplateLowPass = plotWidget()
        self.BodeVecesLowPass = plotWidget()
        self.BodeLowPass = plotWidget()
        self.FaseLowPass = plotWidget()
        self.EscalonLowPass = plotWidget()
        self.PZLowPass = plotWidget()


        self.ventana.hola.addWidget(self.TemplateLowPass.navToolBar)
        self.ventana.hola.addWidget(self.TemplateLowPass.canvas)
        self.ventana.BodeVecesLowPass.addWidget(self.BodeVecesLowPass.navToolBar)
        self.ventana.BodeVecesLowPass.addWidget(self.BodeVecesLowPass.canvas)
        self.ventana.BodeLowPass.addWidget(self.BodeLowPass.navToolBar)
        self.ventana.BodeLowPass.addWidget(self.BodeLowPass.canvas)
        self.ventana.FaseLowPass.addWidget(self.FaseLowPass.navToolBar)
        self.ventana.FaseLowPass.addWidget(self.FaseLowPass.canvas)
        self.ventana.EscalonLowPass.addWidget(self.EscalonLowPass.navToolBar)
        self.ventana.EscalonLowPass.addWidget(self.EscalonLowPass.canvas)
        self.ventana.PZLowPass.addWidget(self.PZLowPass.navToolBar)
        self.ventana.PZLowPass.addWidget(self.PZLowPass.canvas)

        self.lowPassPage = 0

        self.ventana.RightLowPass.clicked.connect(self.nextPage)
        self.ventana.LeftLowPass.clicked.connect(self.prevPage)

        self.plotButtons = QtWidgets.QButtonGroup()
        self.plotButtons.addButton(self.ventana.LowPassBtn, 0)
        self.plotButtons.addButton(self.ventana.HighPassBtn, 1)
        self.plotButtons.addButton(self.ventana.BandPassBtn, 2)
        self.plotButtons.addButton(self.ventana.BandRejectBtn, 3)

        self.plotButtons.buttonClicked.connect(self.plotAll)

        app.exec()

    def nextPage(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            self.lowPassPage = self.lowPassPage + 1
            print(self.lowPassPage)
            self.ventana.stackedWidget.setCurrentIndex(self.lowPassPage)

    def prevPage(self):
        index = self.ventana.filterTabs.currentIndex()
        print(index)
        if index == 0:
            self.lowPassPage = self.lowPassPage - 1
            self.ventana.stackedWidget.setCurrentIndex(self.lowPassPage)

    def plotAll(self):
        index = self.ventana.filterTabs.currentIndex()
        if index == 0:
            self.plotLowPass()
        elif index == 1:
            self.plotHighPass()

    def getDataLowHigh(self, index):
        if index == 0:
            Wp = float(self.ventana.LowPassWp.text())
            Gp = float(self.ventana.LowPassGp.text())
            Wa = float(self.ventana.LowPassWa.text())
            Ga = float(self.ventana.LowPassGa.text())
        elif index == 1:
            Wp = float(self.ventana.HighPassWp.text())
            Gp = float(self.ventana.HighPassGp.text())
            Wa = float(self.ventana.HighPassWa.text())
            Ga = float(self.ventana.HighPassGa.text())
        return Wp, Gp, Wa, Ga


    def plotLowPass(self):
        Wp, Gp, Wa, Ga = self.getDataLowHigh(0)
        Wan = Wa/Wp
        if self.ventana.LowPassCombo.currentIndex() == 0:
            zn, pn, kn = butterNormalized(Wan, Gp, Ga)
            self.TemplateLowPass.plotTemplate(zpk2tf(zn, pn, kn), Gp, Ga, Wan)
            z, p, k = butterLowPass(Wp, Wa, Gp, Ga)
            self.BodeVecesLowPass.plotLowPass(zpk2tf(z, p, k), Gp, Ga, Wp, Wa)
            self.BodeLowPass.plotLowPassBode(zpk2tf(z, p, k), Gp, Ga, Wp, Wa)
            self.PZLowPass.plotPolesZeroes(z, p)



    def plotHighPass(self):
        Wp, Gp, Wa, Ga = self.getDataLowHigh(1)
        print(Wp, Gp, Wa, Ga)
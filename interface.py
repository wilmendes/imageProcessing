
from PyQt4.QtGui import * 
import sys, os
import numpy as np
from PIL import Image
from PIL import ImageQt
# import time

import img as ImgManipulator

def npToPix(npImg):
    pImg = Image.fromarray(npImg.astype(np.uint8))
    qtImg = ImageQt.ImageQt(pImg)

    return QPixmap.fromImage(qtImg)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(0, 0, 1000, 800)

        self.drawStatusBar()

        self.imgContainer = QLabel(self)
        self.imgContainer.setGeometry(0, 0,1000, 800)

        self.createMenu()

        self.move(1, 1)
        self.show()

    def getDouble(self):
        num, ok = QInputDialog.getDouble(self, "integer input dualog", "enter a number")

        if ok:
            return num
        else:
            return None

    def openHistogram(self):

        dialog = QDialog()
        dialog.setGeometry(0, 0, 256, 256)
        hist = ImgManipulator.hist_draw(self.currentImage)

        pix = npToPix(hist)

        imgContainer = QLabel(dialog)
        imgContainer.setGeometry(0, 0, 256, 256)

        imgContainer.setPixmap(pix)

        dialog.move(1, 1)
        dialog.exec_()

    def createMenu(self):
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)

        fileMenu = mainMenu.addMenu('File')
        statMenu = mainMenu.addMenu('Statistcs')
        transformationMenu = mainMenu.addMenu('Transformation')

        histButton = QAction(QIcon(''), 'Histogram', self)
        histButton.triggered.connect(self.openHistogram)

        openButton = QAction(QIcon(''), "Open Image", self)
        openButton.triggered.connect(self.onOpenImageClick)

        translateButton = QAction(QIcon(''), "Translate", self)
        translateButton.triggered.connect(self.onTranslate)

        scaleButton = QAction(QIcon(''), "Scale", self)
        scaleButton.triggered.connect(self.onScale)

        fileMenu.addAction(openButton)
        statMenu.addAction(histButton)
        transformationMenu.addAction(translateButton)
        transformationMenu.addAction(scaleButton)

    def onOpenImageClick(self):
        fName = QFileDialog.getOpenFileName(None, 'Open file', 'd:\\', "Image files (*.jpg *.gif *.png)")

        img = Image.open(str(fName))
        self.currentImage = np.asarray(img.convert("L"))

        self.imgContainer.setPixmap(QPixmap(npToPix(self.currentImage)))
        self.updateStatusBar()

    def onTranslate(self):
        newImg = ImgManipulator.translate(self.currentImage, [20,25,1])
        self.imgContainer.setPixmap(QPixmap(npToPix(newImg)))

    def onScale(self):
        factor = self.getDouble()
        if(factor <> None):
            newImg = ImgManipulator.scale(self.currentImage, factor)
            print(factor)
            self.imgContainer.setPixmap(QPixmap(npToPix(newImg)))


    def updateStatusBar(self):
        self.modeLbl.setText("Mode: " + str(ImgManipulator.mode(self.currentImage)[0]))
        self.varianceLbl.setText("Variance: " + str(ImgManipulator.variance(self.currentImage)))
        self.avgLbl.setText("Average: " + str(ImgManipulator.avg(self.currentImage)))
        self.medianLbl.setText("Median: " + str(ImgManipulator.median(self.currentImage)))

    def drawStatusBar(self):
        sb = self.statusBar()

        self.modeLbl = QLabel()
        sb.addWidget(self.modeLbl)

        self.avgLbl = QLabel()
        sb.addWidget(self.avgLbl)

        self.varianceLbl = QLabel()
        sb.addWidget(self.varianceLbl)

        self.medianLbl = QLabel()
        sb.addWidget(self.medianLbl)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

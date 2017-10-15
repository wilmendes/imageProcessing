
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

    def setImage(self, image):
        self.currentImage = image
        self.imgContainer.setPixmap(QPixmap(npToPix(self.currentImage)))

    def initUi(self):
        self.setGeometry(0, 0, 1000, 800)

        self.drawStatusBar()

        self.imgContainer = QLabel(self)
        self.imgContainer.setGeometry(0, 0,1000, 800)

        self.createMenu()

        self.move(1, 1)
        self.show()

    def getDouble(self):
        num, ok = QInputDialog.getDouble(self, "integer input dialog", "enter a number")

        if ok:
            return num
        else:
            return None

    def getInt(self):
        num, ok = QInputDialog.getInt(self, "integer input dialog", "enter a number")

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

        #Creating Menus
        fileMenu = mainMenu.addMenu('File')
        statMenu = mainMenu.addMenu('Statistcs')
        transformationMenu = mainMenu.addMenu('Transformation')
        filterMenu = mainMenu.addMenu('Filter')

        lowPassSubMenu = filterMenu.addMenu('Low Pass')
        highPassSubMenu = filterMenu.addMenu('High Pass')


        #Creating Buttons
        histButton = QAction('Histogram', self)
        histButton.triggered.connect(self.openHistogram)

        openButton = QAction("Open Image", self)
        openButton.triggered.connect(self.onOpenImageClick)

        scaleButton = QAction("Scale", self)
        scaleButton.triggered.connect(self.onScale)

        rotateButton = QAction("Rotate", self)
        rotateButton.triggered.connect(self.onRotate)

        gaussianButton = QAction("Gaussian", self)
        gaussianButton.triggered.connect(self.onGaussianPress)

        medianButton = QAction("Median", self)
        medianButton.triggered.connect(self.onMedianPress)

        prewittButton = QAction("Prewitt", self)
        prewittButton.triggered.connect(self.onPrewittPress)

        #Connectiong them

        fileMenu.addAction(openButton)
        statMenu.addAction(histButton)
        transformationMenu.addAction(scaleButton)
        transformationMenu.addAction(rotateButton)
        lowPassSubMenu.addAction(gaussianButton)
        lowPassSubMenu.addAction(medianButton)
        highPassSubMenu.addAction(prewittButton)

    def onOpenImageClick(self):
        fName = QFileDialog.getOpenFileName(None, 'Open file', 'd:\\', "Image files (*.jpg *.gif *.png)")

        img = Image.open(str(fName))
        img = np.asarray(img.convert("L"))

        self.setImage(img)


        self.updateStatusBar()

    def onScale(self):
        factor = self.getDouble()
        if(factor <> None):
            newImg = ImgManipulator.scale(self.currentImage, factor)
            self.setImage(newImg)

    def onRotate(self):
        angle = self.getInt()
        if(angle <> None):
            newImg = ImgManipulator.rotate(self.currentImage, angle)
            self.setImage(newImg)

    def onGaussianPress(self):
        mask = np.matrix([[1,2,1],[2,4,2],[1,2,1]])
        def cb(mat):
            mult = np.multiply(mask, mat)
            return np.sum(mult)/16
        img = ImgManipulator.convolution(self.currentImage, cb)
        self.setImage(img)

    def onMedianPress(self):
        def cb(mat):
            median = ImgManipulator.median(mat)
            return median
        img = ImgManipulator.convolution(self.currentImage, cb)
        self.setImage(img)

    def onPrewittPress(self):
        maskX = np.matrix([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]).astype(float)
        maskY = np.matrix([[1, 1, 1], [0, 0, 0], [-1, -1, -1]]).astype(float)

        def cb(mat):
            mult = np.multiply(maskY, mat)
            return np.sum(mult) / 16

        img = ImgManipulator.convolution(self.currentImage, cb)
        self.setImage(img)

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

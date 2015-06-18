# -*- encoding: utf-8 -*-

__author__ = 'gaspardzul'
#! /usr/bin/env python

from PyQt4 import QtCore

from app.functions import *
from app.config import *


class workerThread(QtCore.QThread):

    def __init__(self,parent,config):
        QtCore.QThread.__init__(self,parent)
        self.conf=config
        self.ui = parent


    def run(self):
        qa = int(self.conf.quality)
        dir_i=str(self.conf.dir_input)
        dir_o=str(self.conf.dir_output)
        count =0
        for file_image in glob.glob(unicode('{0}/*.jpg'. format(dir_i))) + glob.glob(unicode('{0}/*.png'. format(dir_i))) + glob.glob(unicode('{0}/*.jpeg'. format(dir_i))) + glob.glob(unicode('{0}/*.JPG'. format(dir_i))):
            compressImg(file_image, dir_o, qa)
            count=count+1
            self.emit(QtCore.SIGNAL("update(PyQt_PyObject)"), count)
        self.emit(QtCore.SIGNAL("alert(PyQt_PyObject)"), 'se comprimieron {0} imagenes con exito'.format(count))



class MainUI(QtGui.QMainWindow):



    def openDirI(self):
        dirI = QtGui.QFileDialog.getExistingDirectory(None, 'Select a input folder:', '', QtGui.QFileDialog.ShowDirsOnly)
        if dirI:
            config.dir_input=dirI
            self.txtDirI.setText(dirI)

    def openDirO(self):
        dirO = QtGui.QFileDialog.getExistingDirectory(None, 'Select a output folder:', '', QtGui.QFileDialog.ShowDirsOnly)
        if dirO:
            config.dir_output=str(dirO)
            self.txtDirO.setText(dirO)



    def slideQA(self):
        config.quality=self.slideQuality.value()
        self.statusBar.showMessage('www.damfara.org | Quality:{0}%'.format(config.quality));

    def progressWorker(self):
        self.progressBar.setValue(0)
        self.progressBar.setMaximum=config.imagenes_en_directorio
        return


# comprime imagenes
    def compressImg(self,file_image):
        img = Image.open(file_image,)
        dir, extensionFile = os.path.splitext(file_image)
        nameFile = dir.split('/')
        nameFile = nameFile[len(nameFile)-1]
        img.save((config.dir_output+"/{0}{1}{2}" . format(nameFile, "_compressed", extensionFile)), quality=config.quality) #########:D
        print 'success:'+config.dir_output


    def compress(self):
        directorio_entrada = config.dir_input
        config.imagenes_en_directorio=0

        if self.txtDirI.text()=='':
            msg = QMessageBox.critical(self,'Error','Es necesario seleccionar una ruta de entrada')
            return
        elif  self.txtDirO.text()=='':
            msg = QMessageBox.critical(self,'Error','Es necesario seleccionar una ruta de salida')
            return
        quality = self.slideQuality.value()

        #obtenermos cuantos elementos tipo imagen tenemos en el directorio seleccionado
        for file_image in glob.glob(unicode('{0}/*.jpg'. format(directorio_entrada))) + glob.glob(unicode('{0}/*.png'. format(directorio_entrada))) + glob.glob(unicode('{0}/*.jpeg'. format(directorio_entrada))) + glob.glob(unicode('{0}/*.JPG'. format(directorio_entrada))):
            config.imagenes_en_directorio += 1

        if config.imagenes_en_directorio>0:
            # msg = QMessageBox.information(self,'Error','existen {0}'.format(self.imagenes_en_directorio))
            self.progressBar.setMinimum(0)
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(config.imagenes_en_directorio)
            self.t= workerThread(self, config) #thread que sirve para comprimir
            QtCore.QObject.connect(self.t, QtCore.SIGNAL("update(PyQt_PyObject)"), self.update) #le decimos al thread que podrá accede a la funcion update desde su funcion run
            QtCore.QObject.connect(self.t, QtCore.SIGNAL("alert(PyQt_PyObject)"), self.alert) #le decimos al thread que podrá acceder a la funcion alert desde su funcion run
            self.t.start()
            # self.t=threading.Thread(target=self.progressWorker)
            # self.t.start()
        else:
            msg = QMessageBox.critical(self, 'Error', 'No existen imagenes en esta ruta, por favor seleccione nuevamente')

    def update(self,val):
        print val
        self.progressBar.setValue(val)

    def alert(self,text):
        QMessageBox.information(self,'Aviso',text)
        self.progressBar.setValue(0)


    def buildUI(self):

        self.setMinimumSize(QtCore.QSize(530, 316))
        self.setMaximumSize(QtCore.QSize(530, 316))
        self.setAnimated(True)
        self.setObjectName('window')
        self.centralWidget = QtGui.QWidget(self)
        self.gridLayout_2 = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.progressBar = QtGui.QProgressBar(self.centralWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 2, 0, 1, 1)

        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.txtDirO = QtGui.QLineEdit(self.centralWidget)
        self.txtDirO.setObjectName("txtDirO")
        self.gridLayout.addWidget(self.txtDirO, 2, 0, 1, 1)
        self.txtDirI = QtGui.QLineEdit(self.centralWidget)
        self.txtDirI.setObjectName("txtDirI")
        self.gridLayout.addWidget(self.txtDirI, 1, 0, 1, 1)
        self.btnDirI = QtGui.QPushButton(self.centralWidget)
        self.btnDirI.setObjectName("btnDirI")
        self.gridLayout.addWidget(self.btnDirI, 1, 1, 1, 1)
        self.btnDirO = QtGui.QPushButton(self.centralWidget)
        self.btnDirO.setObjectName("btnDirO")
        self.gridLayout.addWidget(self.btnDirO, 2, 1, 1, 1)
        self.slideQuality = QtGui.QSlider(self.centralWidget)
        self.slideQuality.setOrientation(QtCore.Qt.Horizontal)
        self.slideQuality.setObjectName("slideQuality")
        self.gridLayout.addWidget(self.slideQuality, 3, 0, 1, 1)
        self.btnCompress = QtGui.QPushButton(self.centralWidget)
        self.btnCompress.setObjectName("btnCompress")
        self.gridLayout.addWidget(self.btnCompress, 3, 1, 1, 1)
        self.lblImagen = QtGui.QLabel(self.centralWidget)
        self.lblImagen.setObjectName("lblPortada")
        self.gridLayout.addWidget(self.lblImagen, 0, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 500, 25))
        self.menuBar.setObjectName("menuBar")
        self.menuArchivo = QtGui.QMenu(self.menuBar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        self.actionSalir = QtGui.QAction(self)
        self.actionSalir.setObjectName("actionSalir")
        self.actionSalir_2 = QtGui.QAction(self)
        self.actionSalir_2.setObjectName("actionSalir_2")
        self.menuArchivo.addAction(self.actionSalir)
        self.menuArchivo.addAction(self.actionSalir_2)
        self.menuBar.addAction(self.menuArchivo.menuAction())
        self.txtDirI.setFocus()
        with open("style/damfara.css") as f:
            self.setStyleSheet(f.read())

    def actionsUI(self):
        ###### Events elements
        self.btnDirI.clicked.connect(self.openDirI)
        self.btnDirO.clicked.connect(self.openDirO)

        self.btnCompress.clicked.connect(self.compress)
        self.slideQuality.sliderMoved.connect(self.slideQA)




    def run(self):
        self.buildUI()
        self.setText()
        self.actionsUI()
        centerUI(self)
        self.show()



    def setText(self):
        self.setWindowTitle("Damfara")
        self.txtDirO.setPlaceholderText( "Directorio de salida")
        self.txtDirI.setPlaceholderText("Directorio de entrada")
        self.btnDirI.setText("...")
        self.btnDirO.setText("...")
        pixmap = QPixmap('resources/damfara.png')
        self.lblImagen.setPixmap(pixmap)
        self.btnCompress.setText("Comprimir")
        self.menuArchivo.setTitle("Archivo")
        self.actionSalir.setText("Acerca de")
        self.actionSalir_2.setText("Salir")
        self.slideQuality.setMaximum(100)
        self.slideQuality.setMinimum(0)
        self.slideQuality.setValue(50)
        self.statusBar.showMessage('www.damfara.org | Quality:50%');




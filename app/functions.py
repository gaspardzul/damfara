__author__ = 'gaspardzul'
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtGui import *
import os, sys, glob
import threading
from PIL import Image


def centerUI(uiForm):
    qr = uiForm.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    uiForm.move(qr.topLeft())


# recibe como parametro la imagen con directorio completo, directorio de salida y la calidad
def compressImg(file_image,dirO,quality):
    img = Image.open(file_image)
    dir, extensionFile = os.path.splitext(file_image)
    nameFile = dir.split('/')
    nameFile = nameFile[len(nameFile)-1]
    #img.save((dirO+"/{0}{1}{2}" . format(nameFile, "_compressed", extensionFile)), quality=quality) #########:D
    file_path = os.path.join("%s" % dirO, "%s_compressed%s" % (nameFile, extensionFile))
    img.save(file_path, quality=quality) #########:D





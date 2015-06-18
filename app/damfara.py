# -*- coding: utf-8 -*-

__author__ = 'gaspardzul'

from Tkinter import *
import tkMessageBox
import ttk
from tkFileDialog import *
from PIL import Image
import os, glob
import  threading


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width =  width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    if win.attributes('-alpha') == 0:
        win.attributes('-alpha', 1.0)
    win.deiconify()

def click_btnDirI():
    dir_files = askdirectory()
    dirI.set(unicode(dir_files))

def click_btnDirO():
    dir_files = askdirectory()
    dirO.set(unicode(dir_files))


def event_scale(val):
    qualityScale = val
    print qualityScale


def click_btnComprimir():
     global dirOutput, dir_
     dirOutput = dirO.get()
     dir_= dirI.get()
     if dir_=="":
         tkMessageBox.showwarning("Error","Debes seleccionar una ruta de entrada")
         return
     elif dirOutput == "":
         tkMessageBox.showwarning("Error","Debes seleccionar una ruta de salida")
         return


     global i_fil
     i_fil= 0

     #obtenemos cuantos elemento imagen tenemos
     dir_=unicode(dir_)
     for fil in glob.glob(unicode('{0}/*.jpg'. format(dir_))) + glob.glob(unicode('{0}/*.png'. format(dir_))) + glob.glob(unicode('{0}/*.jpeg'. format(dir_))) + glob.glob(unicode('{0}/*.JPG'. format(dir_))):
         i_fil+=1

     if(i_fil>0):
        th= threading.Thread(target=progressWorker)
        t= threading.Thread(target=worker)
        th.start()
        t.start()
     else:
        tkMessageBox.showwarning("Error","No existen imagenes en la ruta seleccionada")

def progressWorker():
    progressBar["value"] = 0
    progressBar["maximum"] = i_fil
    return


def worker():
    ifile = 0

    for fil in glob.glob('{0}/*.jpg'. format(dir_)) + glob.glob('{0}/*.png'. format(dir_)) + glob.glob('{0}/*.jpeg'. format(dir_)) + glob.glob('{0}/*.JPG'. format(dir_)):
        img = Image.open(fil)
        print "comprimiendo : {0}" . format(fil)
        dir, extensionFile = os.path.splitext(fil)
        nameFile = dir.split('/')
        nameFile = nameFile[len(nameFile)-1]
        ifile +=1
        progressBar["value"] = ifile
        img.save((dirOutput+"/{0}{1}{2}" . format(nameFile, "_compressed", extensionFile)), quality=qualityScale)
    progressBar.stop()
    tkMessageBox.showinfo("Information", "{0} files compressed" .format(ifile))
    return


def makeWindow():
    global dirI, dirO, qualityScale
    qualityScale = 0

    win = Tk()

    frame1 = Frame(win,borderwidth=3,height=50, width=60)
    frame1.grid(row=0,columnspan=2,ipady=10)

    lbl1 = Label(frame1,text="Seleccionar directorio de entrada:")
    lbl1.grid(row=0,column=0,sticky=W)

    btnDirI = Button(frame1,text="...",command=click_btnDirI)
    btnDirI.grid(row=0,column=2)

    dirI = StringVar()
    txtDirI = Entry(frame1,textvariable = dirI, width=30)
    txtDirI.grid(row=0,column=1)

    lbl2 = Label(frame1,text="Seleccionar directorio de salida:")
    lbl2.grid(row=1,column=0,sticky=W)

    btnDirO = Button(frame1,text="...",command=click_btnDirO)
    btnDirO.grid(row=1,column=2)

    dirO = StringVar()
    txtDirO = Entry(frame1,textvariable = dirO, width=30)
    txtDirO.grid(row=1,column=1)


    lbl3 = Label(frame1,text="Seleccionar calidad de la imagen:")
    lbl3.grid(row=2,column=0,sticky=W)

    lbl3 = Label(frame1,text="%")
    lbl3.grid(row=2,column=2,sticky=W+E+N+S)


    #herramienta de selección de calidad
    scale = Scale(frame1,from_=0,to=100,orient=HORIZONTAL,command=event_scale,length=250)
    scale.set(100)
    scale.grid(row=2,column=1,columnspan=1,sticky=W)

    frame2 = Frame(win,borderwidth=0,relief=SOLID,height=50, width=50)
    frame2.grid(row=1,columnspan=2,padx=5, pady=5)

    btnComprimir = Button(frame2,text="Comprimir",command=click_btnComprimir,width=10)
    btnComprimir.grid(row=0,columnspan=2,sticky=W+E+N+S)

    frame3 = Frame(win, borderwidth=0,height=50, width=50)
    frame3.grid(row=2, column=0, columnspan=4)

    global progressBar
    progressBar = ttk.Progressbar(frame3,orient=HORIZONTAL, length=500, mode='determinate')
    progressBar.grid(row=1,column=0, columnspan=2)
    return win

global win
win= makeWindow()
win.geometry("515x200")
win.title("Damfara")
center(win)

win.mainloop()

from tkinter import *
from tkinter import filedialog as FileDialog
from io import open
import sys

def arch_nuevo():
    global ruta
    mensaje.set("Nuevo fichero")
    ruta = ""
    texto.delete(1.0, "end")
    root.title("GoQ - Editor")

def abrir_arch():
    global ruta
    mensaje.set("Abrir fichero")
    ruta = FileDialog.askopenfilename(
    initialdir='.', 
    filetypes=(("Ficheros python", "*.py"),),
    title="Abrir un fichero python")
    

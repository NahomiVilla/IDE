from tkinter import *
from tkinter import filedialog as FileDialog
from io import open
import sys

def nuevo():
    global ruta
    mensaje.set("Nuevo fichero")
    ruta = ""
    texto.delete(1.0, "end")
    root.title("GoQ - Editor")



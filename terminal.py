import tkinter as tk
from tkinter import ttk
import sys

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Scroll al final del texto

    def flush(self):
        pass
frame_output1 = None 
output_text=None
color=None
colorforeg=None
def configurar_redireccion(ventana,colorbg,colorfg):
    # Función para mostrar el widget Text con efecto de despliegue
    global color,colorforeg
    color=colorbg
    colorforeg=colorfg
    def toggle():
        global frame_output1,color,colorforeg,output_text

        if frame_output1 is None:
            frame_output1 = tk.Frame(ventana, bg=colorbg)
            frame_output1.lift()
            frame_output1.place(relx=0.495, rely=1.0, relwidth=0.985, relheight=0.35,anchor='s')

            output_text = tk.Text(frame_output1, wrap="word", bg=colorbg, fg=colorforeg)
            output_text.pack(side='bottom', fill='both',expand=True)
            
            # Redirigir stdout y stderr a la salida en el widget Text
            redirector = RedirectText(output_text)
            sys.stdout = redirector
            sys.stderr = redirector
        
    def toggle2():
        global frame_output1
        if frame_output1 is None:
            toggle()
        else:
            frame_output1.destroy()
            frame_output1 = None




    return toggle2, toggle

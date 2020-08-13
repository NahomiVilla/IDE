import tkinter
from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk # para combox

window = Tk()

vert=10
hor=10

#Titulo
window.title("Programando board arduino con Python")

#Tamaño de la ventana
window.geometry('700x550')

def click_abrir():    
    print("A")

def click_guardar():    
    print("G")

def click_run():    
    print("R")
    
def click_open_port():
    print(baudios.get())

def click_close_port():
    print("Cerrar ojos")


#etiquetas
Label(window, text="Baudios").place(x= 320, y = vert+5)


#Botones 
#Boton abrir
btn_abir = Button(window, text="A", command=click_abrir).place(x=hor,y=vert)
#Boton guardar
btn_guardar = Button(window, text="G", command=click_guardar).place(x=hor+40,y=vert)
#Boton run
btn_run = Button(window, text="R", command=click_run).place(x=hor+80,y=vert)


#Boton abrir puerto
btn_open_port = Button(window, text="O", command=click_open_port).place(x=hor+480,y=vert)

#Boton cerrar puerto
btn_close_port = Button(window, text="C", command=click_close_port).place(x=hor+520,y=vert)




#------Baudios de comunicación serial
baudios = ttk.Combobox(window, width = 7,
                            values=[
                                    "2400", 
                                    "4800",
                                    "9600",
                                    "14400",
                                    "19200",
                                    "28800",
                                    "38400",
                                    "115200"])

baudios.place(x=hor+380,y=vert+5)
baudios.current(1)



# Cajas de textos

# Creating scrolled text  
# area widget 
edit = scrolledtext.ScrolledText(window,  
                                      wrap = WORD,  
                                      width = 40,  
                                      height = 50,  
                                      font = ("Times New Roman", 
                                              12)) 
  
caja_msj = scrolledtext.ScrolledText(window,  
                                      wrap = WORD,  
                                      width = 40,  
                                      height = 50,  
                                      font = ("Times New Roman", 
                                              12)) 



edit.place(rely = 0.1,relwidth=0.6, anchor = NW)
edit.config(bd=0, padx=6, pady=4, font=("Consolas",12))


caja_msj.place(relx = 1,rely = 0.1,relwidth=0.4,anchor = NE)
caja_msj.config(bd=0, padx=6, pady=4, font=("Consolas",12))


window.mainloop()


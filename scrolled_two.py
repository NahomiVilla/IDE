# Python program demonstrating 
# ScrolledText widget in tkinter 
  
from tkinter import *
from tkinter import ttk 
from tkinter import scrolledtext 
  
# Creating tkinter main window 
window = Tk() 
window.title("ScrolledText Widget") 
  
def click_abrir():    
    #Label(window,text="Boton abrir").place(x=100,y=150)
    print("A")

def click_guardar():    
    #Label(window,text="Boton guardar").place(x=100,y=150)
    print("G")

def click_run():    
    #Label(window,text="Boton run").place(x=100,y=150)
    print("R")


#Botones 
#Boton abrir
btn_abir = Button(window, text="A", command=click_abrir).grid(column = 0,row=0)
#Boton guardar
btn_guardar = Button(window, text="G", command=click_guardar).grid(column = 1,row=0)
#Boton run
btn_run = Button(window, text="R", command=click_run).grid(column = 2,row=0)


# Creating scrolled text  
# area widget 
text_area = scrolledtext.ScrolledText(window,  
                                      wrap = WORD,  
                                      width = 40,  
                                      height = 25,  
                                      font = ("Times New Roman", 
                                              12)) 
  
text_area_2 = scrolledtext.ScrolledText(window,  
                                      wrap = WORD,  
                                      width = 40,  
                                      height = 5,  
                                      font = ("Times New Roman", 
                                              12)) 

text_area.grid(column = 0, pady = 10, padx = 5)   
text_area_2.grid(column = 0, pady = 10, padx = 5) 

# Placing cursor in the text area 
text_area.focus() 
window.mainloop() 

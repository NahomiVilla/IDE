# Python program demonstrating 
# ScrolledText widget in tkinter 
  
from tkinter import *
from tkinter import ttk 
from tkinter import scrolledtext 
  
# Creating tkinter main window 
window = Tk() 
window.title("ScrolledText Widget") 
  
# Title Label 
Label(window,  
          text = "ScrolledText Widget Example", 
          font = ("Times New Roman", 15),  
          background = 'green',  
          foreground = "white").grid(column = 0, 
                                     row = 0) 
  
# Creating scrolled text  
# area widget 
text_area = scrolledtext.ScrolledText(window,  
                                      wrap = WORD,  
                                      width = 40,  
                                      height = 10,  
                                      font = ("Times New Roman", 
                                              12)) 
  
text_area_2 = scrolledtext.ScrolledText(window,  
                                      wrap = WORD,  
                                      width = 40,  
                                      height = 5,  
                                      font = ("Times New Roman", 
                                              12)) 

text_area.grid(column = 0, pady = 10, padx = 10) 
  
text_area_2.grid(column = 0, pady = 10, padx = 10) 

# Placing cursor in the text area 
text_area.focus() 
window.mainloop() 

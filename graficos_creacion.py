from tkinter import messagebox
import matplotlib.pyplot as plt
from collections import deque
import numpy as np
plt.style.use('ggplot')


def create_plots(num_plots, graph_type):
    if num_plots < 1 or num_plots > 6:
        messagebox.showerror("Error", "El número de gráficos debe estar entre 1 y 6")
        return None,None,None
    print('crenado plots')
    # Determinar el número de columnas
    if num_plots==1:
        num_cols=1
    elif num_plots%2:
        num_cols=2
    else:
        num_cols=3
    print('se determinaron columnas')
    # Determinar el número de filas
    
    num_rows = max((num_plots + num_cols - 1) // num_cols, 1)
    print('se determinaron filas')
    plt.ion()
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(8, 4 * num_rows))
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    #convertir axs en un array bidimensional
    axs=np.atleast_2d(axs)
    x = np.linspace(0, 10, 100)  # Eje x inicial
    y = deque([0]*100, maxlen=100)
    print('se convirtieron bidmensionales')
    for i in range(num_rows):
        for j in range(num_cols):
            idx = i * num_cols + j
            if idx < num_plots:
                if graph_type == "Barras":
                    line=axs[i,j].barh(x,y)
                elif graph_type == "Torta":
                    line=axs[i,j].pie(x,y, autopct='%1.1f%%')
                elif graph_type == "Frecuencia":
                    line, =axs[i,j].plot(x,y)
                    print('se crea grafico frecuencia')
                    #axs[i,j].set_yscale('log')
                elif graph_type == "Columnas":
                    line=axs[i,j].bar(x,y)
                elif graph_type == "Lineas":
                    line, =axs[i,j].plot(x,y, marker='o')
                return axs,line,y
            else:
                axs[i, j].axis('off')  # Desactivar ejes para los subplots no utilizados
            

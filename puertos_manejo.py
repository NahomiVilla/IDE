import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import messagebox
from graficos_creacion import create_plots
import matplotlib.pyplot as plt
import platform

global ser
puerto=None
baudios=None
cantidad=1
tipo='Frecuencia'
conexion=False
#evento_conexion_exitosa = tk.Event()
def detectar_arduinos():
    global puertos, arduinos_conectados
    #capturar los puertos com
    system = platform.system()
    if system == 'Windows'or system=='Linux':
        puertos = serial.tools.list_ports.comports()
    arduinos_conectados = []
    for puerto in puertos:
        arduinos_conectados.append(puerto.device)
    #time.sleep(3)
    return arduinos_conectados
def recibir_datos(port, baud, ax, line, lista):
    try:
        global ser
        with serial.Serial(port, baud, timeout=1) as ser:            
            while not finish:
                if ser.isOpen():
                    rcv = ser.readline()
                    if rcv:
                        data = rcv.decode().strip()  # Elimina los caracteres de nueva línea
                        try:
                            num = float(data)
                            crear_graph(ax, line, lista, num)
                        except ValueError:
                            print("Error: No se pudo convertir '{}' a float".format(data))
                    else:
                        desconectar()
                else:
                    break  # Salir del bucle si el puerto no está abierto
    except serial.SerialException as e:
        messagebox.showerror('Puerto',f'Error al abrir el puerto serial. Intente nuevamente\n Error:',e)


def crear_graph(a,linea,lista,dato):
    global cantidad
    lista.append(dato)
    print(lista)
    linea.set_ydata(lista)
    plt.draw()
    plt.pause(0.001)
def click_conectar(port,baudis=9600,graph='lineas',canti=1,callback=None):
    global baudios,puerto,cantidad,tipo,conexion
    puerto=port
    baudios=baudis
    cantidad=canti
    tipo=graph
    if len(port) :
        if len(baudis) and baudis.isdigit():
            print('iniciando proceso')
            conexion=True
            ax,line,datos_y=create_plots(cantidad,tipo)
            if ax==None and line==None and datos_y==None:
                desconectar()
                print('error')
            recibir_datos(puerto,baudios,ax,line,datos_y)
        else:
            messagebox.showerror('Baudios','Invalido')
    else:
        messagebox.showerror('Puerto','Invalido')

def desconectar():
    global conexion
    ser.close()
    plt.close()
    print("Puerto Cerrado")
    conexion=False
# Ejemplo de uso
finish = False


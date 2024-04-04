import serial.tools.list_ports
import time
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



#funcion recibe datos del arduino
def recibir_datos(port,baud,ax,line,lista):
    try:
        global ser,num
        ser=serial.Serial(port, int(baud))
        time.sleep(1)
        while not finish:
            if ser.isOpen():
                rcv = ser.readline()
                if rcv != b'\r\n': 
                    data=rcv.decode()
                    num = float(data)
                    crear_graph(ax,line,lista,num)
    except:
        #messagebox.showinfo(message="No abierto", title="Puerto")
        print('excepcion')
def crear_graph(a,linea,lista,dato):
    global cantidad
    lista.append(dato)
    print(lista)
    linea.set_ydata(lista)
    plt.draw()
    plt.pause(0.001)


#Función conexion
#iniciar
def click_conectar(port,baudis=9600,graph='lineas',canti=1):
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
            recibir_datos(puerto,baudios,ax,line,datos_y)
        else:
            messagebox.showerror('Baudios','Invalido')
    else:
        messagebox.showerror('Puerto','Invalido')


def desconectar():
    global conexion
    ser.close()
    print("Puerto Cerrado")
    conexion=False


finish=False




import serial.tools.list_ports
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
def establecer_conexion(port, baud):
    try:
        global ser,conexion
        ser = serial.Serial(port, baud, timeout=1)           
        if ser.isOpen():
            conexion=True
            messagebox.showinfo('Conexión','Conexión establecida')
        else:
            conexion=False  
    except serial.SerialException as e:
        messagebox.showerror('Puerto','Error al abrir el puerto serial. Intente nuevamente')

def datos ( ax, line, lista,boton=None,img=None,color=None,fun=None):
    global ser ,conexion
    if conexion==True:
        try: 
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
                        boton.configure(image=img,command=fun,bg=color)
                        messagebox.showerror('Datos','No se estan recibiendo datos, no se puede graficar. Conexión cerrada')
                        break
                else:
                    print('no')
                    conexion=False
                    break
        except serial.SerialException as e:
            messagebox.showerror('Datos', 'Error al leer datos del puerto serial: {}'.format(e))
            conexion = False
    else:
        plt.close()
        messagebox.showerror('Conexión','Establezca conexión antes de mostrar graficos')

def crear_graph(a,linea,lista,dato):
    global cantidad
    lista.append(dato)
    print(lista)
    linea.set_ydata(lista)
    plt.draw()
    plt.pause(0.001)
def click_conectar(port='Frecuencia',baudis=9600):
    global baudios,puerto,cantidad,tipo,conexion
    puerto=port
    baudios=baudis
    if len(port) :
        if len(baudis) and baudis.isdigit():
            print('iniciando proceso')
            establecer_conexion(puerto,baudios)
        else:
            messagebox.showerror('Baudios','Invalido')
    else:
        messagebox.showerror('Puerto','Invalido')
def funcion(graph='Lineas',canti=1,boton=None,img=None,color=None,fun=None):
    cantidad=canti
    tipo=graph
    ax,line,datos_y=create_plots(cantidad,tipo)
    if ax==None and line==None and datos_y==None:
        desconectar()
        boton.configure(image=img,command=fun,bg=color)
        print('error')
    datos(ax,line,datos_y,boton,img,color,fun)
def desconectar():
    global conexion
    ser.close()
    plt.close()
    print("Puerto Cerrado")
    conexion=False
# Ejemplo de uso
finish = False


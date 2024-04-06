import tkinter as tk
from tkinter import*
from NumberedScrolledText import NumberedScrolledText
from tkinter.filedialog import asksaveasfilename,askopenfilename
from tkinter import messagebox
from colorizador import TemaManager as tm
from terminal import configurar_redireccion
from puertos_manejo import click_conectar,detectar_arduinos,desconectar

import puertos_manejo
import json
from Info import *


archivo_actual=None
frame_output=None
conexion_exitosa=False
img2=None
tema=None
fuente=None
siz=None
temas={}
color='black'
colorfg='white'
ultima_posicion = "1.0"


def seleccion_graficos(grafi='Frecuencia', cant=1):
    global selec_graph, selec_cant, menu_graficos, graficos, graf_menu
    menu_graficos.delete(0, "end")
    graf_menu.delete(0,"end")
    for idx1,item1 in enumerate(range(1,7)):
        if cant== item1:
            item1="\u2713 " + str(item1)
        graf_menu.add_command(label=item1,command=lambda graf=grafi, i=cant:seleccion_graficos(graf,i))
    for idx, item in enumerate(tipos_graficos):
        if grafi == item:  # Aquí usamos selec_graph en lugar de opcion
            # Agrega un visto a la opción seleccionada
            item = "\u2713 " + item  
        menu_graficos.add_cascade(label=item,menu=graf_menu)
    selec_graph = grafi
    selec_cant = cant  
    
     
def marcado(opcion,lista,menu):
    global seleccion_baudio
    menu.delete(0, "end")
    for idx, item in enumerate(lista):
        if opcion == item:
            # Agrega un visto a la opción seleccionada
            item = "\u2713 " + item
            seleccion_baudio.set(opcion)
        menu.add_command(label=item, command=lambda opt=item: marcado(opt,baudios,menu_baudios))

def marcado_ard(opcion1,lista1,menu1):
    global seleccion_arduino
    menu1.delete(0, "end")
    for idx, item in enumerate(lista1):
        if opcion1 == item:
            # Agrega un visto a la opción seleccionada
            item = "\u2713 " + item
            seleccion_arduino.set(opcion1)
        menu1.add_command(label=item, command=lambda opt=item: marcado(opt,arduinos,menu_puertos))

def click_conexion():
    global img2,conexion_exitosa,usb_boton,selec_graph,selec_cant
    #cambio_imagen()
    if puertos_manejo.conexion!=True:
        if selec_graph=='' and selec_cant=='':
            selec_graph='Frecuencia'
            selec_cant=1
            seleccion_graficos(selec_graph,selec_cant)
        usb_boton.configure(image=usb_image2,command=funcion_desconectar,bg=color)
        click_conectar(seleccion_arduino.get(),seleccion_baudio.get(),selec_graph,selec_cant)
        if puertos_manejo.conexion!=True:
            usb_boton.configure(image=usb_image,bg=color,borderwidth=0,command=click_conexion)
            messagebox.showerror('Puerto','Conecte una tarjeta arduino o seleccione el puerto y tipo de grafico ')     
    else:
        usb_boton.configure(image=usb_image2,command=funcion_desconectar,bg=color)
        messagebox.showerror('conexion','ya hay una conexion existente')
      
def funcion_desconectar():
    global usb_boton,usb_image
    desconectar()
    usb_boton.configure(image=usb_image,bg=color,borderwidth=0,command=click_conexion)
def open_file():
    path = askopenfilename(filetypes=[('Archivos Python','*.py')])
    with open(path, 'r') as file:
        contenido = file.read()
        area_texto.text_area.delete('1.0', 'end')  
        area_texto.text_area.insert('1.0', contenido)  
    archivos_abiertos.append(path)
    agregar_archivo(path)
# Función para guardar el contenido del archivo
def guardar_contenido():
    global archivo_actual
    if archivo_actual is None:
        messagebox.showwarning("Pycode Warning", "No hay archivo abierto para guardar.")
        return
    
    contenido = area_texto.text_area.get('1.0', 'end-1c')
    if not contenido.strip():
        messagebox.showwarning("Pycode Warning", "No hay contenido para guardar.")
        return

    with open(archivo_actual, 'w') as file:
        file.write(contenido)
# Función para manejar el evento de modificación del área de texto
def guardar_al_modificar(event):
    global archivo_actual
    if archivo_actual:
        guardar_contenido()
# Función para manejar el clic en un archivo
def clic_archivo(nombre_archivo):
    global archivo_actual
    print("Archivo seleccionado:", nombre_archivo)
    archivo_actual = nombre_archivo
    # Lógica para abrir una sección de escritura de texto
    with open(nombre_archivo, 'r') as file:
        contenido = file.read()
        area_texto.text_area.delete('1.0', 'end') 
        area_texto.text_area.insert('1.0', contenido)
# Función para agregar un archivo a la barra de archivos abiertos
def agregar_archivo(nombre_archivo):
    frame_boton_archivos = tk.Frame(barra_archivos_frame, bg='black')  
    frame_boton_archivos.pack(side='left', padx=5, pady=5)
    signos=['/','//','\\']
    for signo in signos:
        if signo in nombre_archivo:
            nombre=nombre_archivo.split(signo)
    boton_archivo = tk.Button(frame_boton_archivos, text=nombre[-1], bg='black', fg='white', borderwidth=0,
                              activebackground='gray', activeforeground='white',
                              command=lambda nombre=nombre_archivo: clic_archivo(nombre))
    boton_archivo.pack(side='left', padx=5, pady=5)
    boton_cerrar = tk.Button(frame_boton_archivos, text='x', bg='black', fg='white', activebackground='gray',
                             activeforeground='white', bd=0,
                             command=lambda frame=frame_boton_archivos, nombre=nombre_archivo: cerrar_archivo(frame,
                                                                                                               nombre_archivo))
    boton_cerrar.pack(side='right')
    archivos_abiertos.append(archivo_actual)
#funcion para cerrar archivo
def cerrar_archivo(frame, nombre_archivo):
    global archivo_actual
    guardar_contenido()
    frame.destroy()
    archivos_abiertos.remove(nombre_archivo)
    if archivos_abiertos:
        siguiente_archivo = archivos_abiertos[0]
        clic_archivo(siguiente_archivo)
    else:
        archivo_actual = None
        area_texto.text_area.delete('1.0', 'end')
#funcion para guardar como
def guardar_como():
    global archivo_actual

    contenido = area_texto.text_area.get('1.0', 'end-1c')
    if not contenido.strip():
        messagebox.showwarning("Pycode Warning", "No hay contenido para guardar.")
        return

    path = asksaveasfilename(filetypes=[('Archivos Python', '*.py')], defaultextension='.py')
    if not path:
        return

    with open(path, 'w') as file:
        file.write(contenido)

    archivo_actual = path
    agregar_archivo(archivo_actual)
#funcion para guardar archivo
def guardar():
    global archivo_actual
    if not archivo_actual:
        messagebox.showwarning("Pycode Warning", 'Por favor, abre o guarda un archivo antes de guardar')
        return

    guardar_contenido()
#funcion para correr programa
def run():
    global archivo_actual, frame_output
    while click_conexion:
        if not archivo_actual:
            messagebox.showwarning("Pycode Warning", 'Por favor, abre un archivo antes de ejecutar')
            return
        
        if frame_output is None:
            _,toggle_output = configurar_redireccion(ventana,color,colorfg)
            toggle_output()

        try:
            with open(archivo_actual, 'r') as file:
                code = file.read()
                local_vars = {}
                exec(code, globals(), local_vars)
                output = local_vars.get('__output__', '')
                
                if frame_output:
                    output_text_widget = frame_output.winfo_children()[0]
                    output_text_widget.insert(tk.END, output)
        except Exception as e:
            messagebox.showerror("Error de ejecución", str(e))
    else:
        messagebox.showerror("Debe realizar conexion antes de ejecutar codigo", str(e))
#funcion para mostrar terminal
def mostrar_terminal():
    global frame_output
    if frame_output is None:
        delete,_ = configurar_redireccion(area_texto,color,colorfg)
        delete()
        frame_output=None      
#funcion para crear archivo nuevo
def crear_archivo_nuevo():
    # Abrir el explorador de archivos para guardar el nuevo archivo con la extensión .py
    path = asksaveasfilename(filetypes=[('Archivos Python', '*.py')], defaultextension='.py')
    if not path:
        return  # Salir si se cancela la operación

    # Crear un nuevo archivo y guardarlo con el nombre especificado
    with open(path, 'w') as file:
        pass  # No es necesario escribir nada en el archivo por ahora

    # Mostrar el archivo nuevo en la barra de archivos
    agregar_archivo(path)
#ventana de configuracion
def configuracion():
    global fuente,siz,tema,temas,modo,color
    ventana_configuracion=tk.Toplevel(ventana)
    ventana_configuracion.configure(background=color)
    ventana_configuracion.minsize(300,300)
    ventana_configuracion.maxsize(300,300)
    ventana_configuracion.resizable(False, False)
    ventana_configuracion.title('Configuraciones')
    
    fuentes=['Courier Normal','Fixedsys Normal','Courier New','Agency FB']
    tamaños=[8,10,12,14,16,18,20]
    temas={'Predeterminado':coli.predeterminado,'Blue':coli.tema_1,'Pink':coli.tema_3,'Sun':coli.tema_2}
    modos=['Light','Dark']
    
    frame_fuentes=tk.Frame(ventana_configuracion,bg='black')
    frame_fuentes.pack(side='top',fill='x')
    frame_tamaño=tk.Frame(ventana_configuracion,bg='black')
    frame_tamaño.pack(side='top',fill='x')
    frame_tema=tk.Frame(ventana_configuracion,bg='black')
    frame_tema.pack(side='top',fill='x')
    frame_modo=tk.Frame(ventana_configuracion,bg='black')
    frame_modo.pack(side='top',fill='x')
    
    label_fuente = tk.Label(frame_fuentes, text="Font",font=('Arial',12),bg=color,fg=colorfg)
    label_fuente.pack(side=tk.LEFT)
    label_tamaño = tk.Label(frame_tamaño, text="Size",bg=color,fg=colorfg,font=('Arial',12))
    label_tamaño.pack(side=tk.LEFT)
    label_tema = tk.Label(frame_tema, text="Theme",bg=color,fg=colorfg,font=('Arial',12))
    label_tema.pack(side=tk.LEFT)
    label_modo = tk.Label(frame_modo, text="Mode",bg=color,fg=colorfg,font=('Arial',12))
    label_modo.pack(side=tk.LEFT)
    
    #fuente=tk.StringVar()
    fuente.set(fuentes[1])
    #siz=tk.IntVar()
    siz.set(tamaños[2])
    #tema=tk.StringVar()
    tema.set(list(temas.keys())[0])
    #modo=tk.StringVar()
    modo.set(modos[1])
    
    menu_fuentes=tk.OptionMenu(frame_fuentes,fuente,*fuentes,command=lambda x:seleccion(fuente,x))
    menu_fuentes.pack()
    menu_tamaño=tk.OptionMenu(frame_tamaño,siz,*tamaños,command=lambda x:seleccion(siz,x))
    menu_tamaño.pack()
    menu_temas=tk.OptionMenu(frame_tema,tema,*temas.keys(),command=lambda x: seleccion(tema,x))
    menu_temas.pack()
    menu_modo=tk.OptionMenu(frame_modo,modo,*modos,command= lambda x:seleccion(modo,x))
    menu_modo.pack()
    boton_aplicar=tk.Button(ventana_configuracion,text='Aplicar',command=aplicar,bg=color,fg=colorfg)
    boton_aplicar.pack(side='bottom')
#funcion de seleccion de opciones en la ventana configuracion
def seleccion(variable,opcion):
    variable.set(opcion)
#funcion de aplicacion de temas para letras
def aplicar_tema(tema,fondo):
    global temas
    #tema_seleccionado=tema
    funcion=temas.get(tema.get())
    if funcion:
        funcion(fondo)
#guardar configuraciion aplicada para el siguiente inicio de la app
def guardar_configuracion():
    configuracion_dic={
        'fuente':fuente.get(),
        'tamaño':siz.get(),
        'tema': tema.get(),
        'modo': modo.get()} 
    with open('configuracion.json','w')as archivo_config:
        json.dump(configuracion_dic,archivo_config)   
#carga de configuracion guardada
def cargar_configuracion():
    global configuracion_dic
    try:
        with open('configuracion.json','r')as archivo_config:
            configuracion_dic=json.load(archivo_config)
            fuente.set(configuracion_dic['fuente'])
            siz.set(configuracion_dic['tamaño'])
            tema.set(configuracion_dic['tema'])
            modo.set(configuracion_dic['modo'])
            aplicar()
    except FileNotFoundError:
        pass    
#aplicar configuracion aplicada
def aplicar():
    global tema,siz,fuente,modo,color,colorfg
    area_texto.text_area.config(font=(fuente.get(),siz.get()))
    if modo.get() != 'Dark':
        color='white'
        colorfg='black'
        aplicar_tema(tema,color)
        boton_terminal.configure(image=icono_terminal_black,background=color)
        area_texto.text_area.configure(bg=color,fg=colorfg,insertbackground=colorfg,selectbackground=colorfg,selectforeground=color)
        area_texto.line_numbers.configure(background=color,foreground=colorfg,insertbackground=colorfg,selectbackground=colorfg,selectforeground=color)
        menu_frame.configure(bg=color)
        archivo.configure(bg=color,fg=colorfg)
        graficos.configure(bg=color,fg=colorfg)
        puertos.configure(bg=color,fg=colorfg)
        guardar_boton.configure(bg=color,fg=colorfg)
        run_boton.configure(bg=color)
        frame_info.configure(bg=color)
    else:
        color='black'
        colorfg='white'
        aplicar_tema(tema,color)
        boton_terminal.configure(image=icono_terminal,background=color)
        area_texto.text_area.configure(bg=color,fg=colorfg,insertbackground=colorfg,selectbackground=colorfg,selectforeground=color)
        area_texto.line_numbers.configure(background=color,foreground=colorfg,insertbackground=colorfg,selectbackground=colorfg,selectforeground=color)
        menu_frame.configure(bg=color)
        archivo.configure(bg=color,fg=colorfg)
        graficos.configure(bg=color,fg=colorfg)
        puertos.configure(bg=color,fg=colorfg)
        guardar_boton.configure(bg=color,fg=colorfg)
        run_boton.configure(bg=color)
        frame_info.configure(bg=color)
    guardar_configuracion()
def mostrar_menu(event):
    editar_menu.post(event.x_root, event.y_root)
def copiar_texto():
    area_texto.text_area.clipboard_clear()
    area_texto.text_area.clipboard_append(area_texto.text_area.selection_get())

def pegar_texto():
    area_texto.text_area.insert(tk.INSERT, area_texto.text_area.clipboard_get())
def cortar_texto():
    copiar_texto()
    area_texto.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
def seleccionar_todo():
    area_texto.text_area.tag_add(tk.SEL, "1.0", tk.END)
def actualizar_puertos(menu_puertos):
    global ventana
    # Limpiar el menú de puertos
    menu_puertos.delete(0, tk.END)
    # Obtener la lista de puertos disponibles
    arduinos = detectar_arduinos()
    for arduino in arduinos:
        menu_puertos.add_command(label=arduino, command=lambda ard=arduino: marcado_ard(ard, arduinos, menu_puertos))
    # Obtener la opción seleccionada actualmente
    opcion_seleccionada = seleccion_arduino.get()
    if opcion_seleccionada in arduinos:
        # Si la opción seleccionada todavía está en la lista de arduinos disponibles,
        # marcarla nuevamente después de actualizar el menú
        marcado_ard(opcion_seleccionada, arduinos, menu_puertos)

    ventana.after(1000, lambda: actualizar_puertos(menu_puertos))
def creadores():
    ventana_info_creadores=tk.Toplevel(ventana)
    ventana_info_creadores.configure(background=color)
    ventana_info_creadores.minsize(400,400)
    ventana_info_creadores.maxsize(850,850)
    #ventana_info_creadores.resizable(False,False)
    ventana_info_creadores.title('Creadores')
    
    #logo
    logo=tk.PhotoImage(file='logo.png')
    logo_label=tk.Label(ventana_info_creadores,image=logo)
    logo_label.pack(pady=10)
    
    #label descripcion
    descripcion=tk.Label(ventana_info_creadores,text="""
        IDE Personalizada para Análisis de Datos en Tiempo Real con Arduino.\n
Esta aplicación desarrollada en Python proporciona un entorno completo para la 
edición, visualización y análisis de datos procedentes de dispositivos Arduino.
Características incluyen: 
Conexión directa con Arduino, Visualización dinámica de datos, Configuración flexible,
Personalización del tema, Edición, Ejecución de código Python

CREADORES:
    José Luis Laica Cornejo
    Contacto: jose.laica@gmail.com
    
    Nahomi Solange Villa Garzón
    Contacto: nahomyvillag2@gmail.com""",font=('Arial',10),bg=color,fg=colorfg)
    descripcion.pack(pady=10)

####################################PROGRAMA PRINCIPAL##########################################
# Crear la ventana
ventana = tk.Tk()

selec_graph=''
selec_cant=''
arduinos=[]
fuente=tk.StringVar()
siz=tk.IntVar()
tema=tk.StringVar()
modo=tk.StringVar()
seleccion_baudio = tk.StringVar()
seleccion_arduino = tk.StringVar()

configuracion_dic = {
    'fuente': fuente.get(),
    'tamaño': siz.get(),
    'tema': tema.get(),
    'modo': modo.get()
}
modo.set(configuracion_dic.get('modo','Dark'))
fuente.set(configuracion_dic.get('fuente','Fixedsys Normal'))
siz.set(configuracion_dic.get('tamaño',12))
tema.set(configuracion_dic.get('tema','Predeterminado'))

########################## AREA BARRA DE MENU #############################################3
#frame para menu
menu_frame=tk.Frame(ventana,bg=color)
menu_frame.pack(side='top',fill='x')

# Crear la barra de menú
barra_menu = tk.Menu(ventana, bg=color, fg=color, activebackground=color, activeforeground="gray52")
ventana.config(menu=barra_menu)

#menu button dentro del frame
archivo=tk.Menubutton(menu_frame,text='Archivo',
                      bg=color,
                      fg=colorfg,
                      activebackground=color,
                      activeforeground='gray52')
guardar_boton=tk.Button(menu_frame,text='Guardar',
                      bg=color,
                      fg=colorfg,
                      activebackground=color,
                      activeforeground='gray52',
                      borderwidth=0,
                      command=guardar
                      )
graficos=tk.Menubutton(menu_frame,text='Graficos',
                      bg=color,
                      fg=colorfg,
                      activebackground=color,
                      activeforeground='gray52')
puertos=tk.Menubutton(menu_frame,text='Puertos',
                      bg=color,
                      fg=colorfg,
                      activebackground=color,
                      activeforeground='gray52')
baudi=tk.Menubutton(menu_frame,text='Baudios',
                    bg=color,
                    fg=colorfg,
                    activebackground=color,
                    activeforeground='gray52')

#menu desplegable
menu_archivo=tk.Menu(archivo,tearoff=0)

menu_graficos=tk.Menu(graficos,tearoff=0)
menu_puertos=tk.Menu(puertos,tearoff=0)
menu_baudios=tk.Menu(baudi,tearoff=0)

#agregar opciones
menu_archivo.add_command(label='abrir',
                         command=open_file)
menu_archivo.add_command(label='nuevo archivo',
                         command=crear_archivo_nuevo)
menu_archivo.add_command(label='guardar como',
                         command=guardar_como)
menu_archivo.add_command(label='Configuración',command=configuracion)

#submenu informacion
info_menu=tk.Menu(menu_archivo,tearoff=0)
info_menu.add_command(label='Creadores',command=creadores)
info_menu.add_command(label='Guia de uso')

menu_archivo.add_cascade(label='Información',menu=info_menu)

#edicion
opciones_edicion={"Copiar":copiar_texto,"Pegar":pegar_texto,"Cortar":cortar_texto,"Seleccionar":seleccionar_todo}
editar_menu=tk.Menu(menu_archivo,tearoff=0)
for opcion,funcion in opciones_edicion.items():
    editar_menu.add_command(label=opcion,command=funcion)
menu_archivo.add_cascade(label="Editar",menu=editar_menu)
#tipo de graficos
tipos_graficos=['Barras','Torta','Columnas','Frecuencia','Lineas']
for graf in tipos_graficos:
    graf_menu=tk.Menu(menu_graficos,tearoff=0)
    for i in range(1,7):
        graf_menu.add_command(label=i,command=lambda graf=graf, i=i:seleccion_graficos(graf,i))
    menu_graficos.add_cascade(label=graf,menu=graf_menu)

#baudios
baudios=[
    "2400", 
    "4800",
    "9600",
    "14400",
    "19200",
    "28800",
    "38400",
    "115200"]
for baudio in baudios:
    menu_baudios.add_command(label=baudio,command=lambda bd=baudio: marcado(bd,baudios,menu_baudios))
#arduinos
actualizar_puertos(menu_puertos)

#asignacion 
archivo.config(menu=menu_archivo)
archivo.pack(side='left')
graficos.config(menu=menu_graficos)
graficos.pack(side='left')
puertos.config(menu=menu_puertos)
puertos.pack(side='left')
guardar_boton.pack(side='left')
baudi.config(menu=menu_baudios)
baudi.pack(side='left')

######################## BOTONES ########################################
#botones con iconos

#botón ejecutar
run_image=PhotoImage(file='iconos/run.png')
run_boton=tk.Button(menu_frame,image=run_image,bg=color,borderwidth=0,command=run)
run_boton.pack(side='right')

# Cargar imagen para el botón de conexion
img='iconos/USB_red.png'
img2='iconos/USB_green.png'
usb_image=PhotoImage(file=img)
usb_image2=PhotoImage(file=img2)
usb_boton=tk.Button(menu_frame,image=usb_image,bg=color,borderwidth=0,command=click_conexion)
usb_boton.pack(side='right')

##botón terminal
icono_terminal=PhotoImage(file='iconos/terminal.png')
icono_terminal_black=PhotoImage(file='iconos/teminal_negro.png')
boton_terminal=tk.Button(menu_frame,image=icono_terminal,bg=color,borderwidth=0,command=mostrar_terminal)
boton_terminal.pack(side='right')

############################ AREA ARCHIVOS ##############################################3
# Frame para la barra de archivos abiertos
barra_archivos_frame = tk.Frame(ventana, bg=color)
barra_archivos_frame.pack(side='top', fill='x')

#listas para manejo de archivos
archivos_abiertos = []
botones_archivos = []
frames_archivos=[]
# Crear un mensaje para mostrar cuando no hay archivos abiertos
mensaje_frame = tk.Frame(ventana, bg='white')
mensaje_label = tk.Label(mensaje_frame, text='No hay archivos abiertos', bg='white')
mensaje_label.pack(expand=True)
frame_info=tk.Frame(ventana,bg=color)
frame_info.pack(side='bottom',fill='x')
# Etiqueta para mostrar la posición
etiqueta_posicion = tk.Label(frame_info, text="Línea: 1, Columna: 0",bg=color,fg=colorfg)
etiqueta_posicion.pack(side='left', padx=5, pady=5,fill='x')

etiqueta_info=tk.Label(frame_info,text='Port: --    Baudio: --',bg=color,fg=colorfg)
etiqueta_info.pack(side='right',padx=5,pady=5,fill='x')
################################ TEXTO (ENTRADA Y SALIDA) #####################################################
# Área de texto con desplazamiento
area_texto = NumberedScrolledText(ventana)
area_texto.pack(side='top', fill='both', expand=True)
position_info = PositionInfo(area_texto.text_area, etiqueta_posicion,etiqueta_info,seleccion_arduino,seleccion_baudio)
# Manejar el evento de modificación del área de texto
area_texto.text_area.bind('<KeyRelease>', guardar_al_modificar)
area_texto.text_area.bind("<Button-3>", mostrar_menu)
#colores al texto
coli=tm(area_texto)
cargar_configuracion()
#evento_conexion_exitosa.add_observer(manejar_evento_conexion_exitosa)
# Ejecutar la ventana
ventana.mainloop()
puertos_manejo.finish=True

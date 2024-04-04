import tkinter as tk
class PositionInfo:
    def __init__(self, text_area, etiqueta_posicion, etiqueta_info, seleccion_arduino, seleccion_baudio):
        self.text_area = text_area
        self.etiqueta_posicion = etiqueta_posicion
        self.etiqueta_info = etiqueta_info

        self.ultima_posicion = "1.0"
        self.seleccion_arduino = seleccion_arduino
        self.seleccion_baudio = seleccion_baudio

        # Manejar el evento de cambio de posición
        self.text_area.bind('<KeyRelease>', self.mostrar_posicion)
        self.text_area.bind('<Motion>', self.actualizar_posicion)

    def mostrar_posicion(self, event=None):
        nueva_posicion = self.text_area.index(tk.INSERT)
        
        # Solo actualiza la posición si ha cambiado
        if nueva_posicion != self.ultima_posicion:
            self.ultima_posicion = nueva_posicion
            linea, columna = nueva_posicion.split('.')
            self.etiqueta_posicion.config(text=f'Línea: {linea}, Columna: {columna}')
        if self.seleccion_arduino.get() != '' :
            self.etiqueta_info.configure(text='Port: {}    Baudio: --'.format(self.seleccion_arduino.get()))
        elif self.seleccion_baudio.get() != '':
            self.etiqueta_info.configure(text='Port: --    Baudio: {}'.format( self.seleccion_baudio.get()))
        elif self.seleccion_arduino.get() != ''  and self.seleccion_baudio.get() != '':
            self.etiqueta_info.configure(text='Port: {}    Baudio: {}'.format(self.seleccion_arduino.get(), self.seleccion_baudio.get()))
    def actualizar_posicion(self, event):
        self.etiqueta_posicion.after(50, self.mostrar_posicion)  # 50 ms de retraso

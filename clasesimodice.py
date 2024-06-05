from tkinter import *
import tkinter as tk
import random
from tkinter import messagebox
from gestor import GestorJugadores
from clasejugador import Jugador
import datetime

class simondice:
    __ventana: object
    __dialogo = None

    def __init__(self, ventana):
        self.__ventana = ventana
        self.__ventana.title("Py -SimonGame")
        self.color = ["#ff0000", "#00ff00", "#0000ff", "#ffff00"]
        self.secuencia = []
        self.secuencia_user = []
        self.secuencia_user_active = False
        self.botonverde = self.create_button(self.color[0], 0)
        self.botonrojo = self.create_button(self.color[1], 1)
        self.botonamarrillo = self.create_button(self.color[2], 2)
        self.botonazul = self.create_button(self.color[3], 3)
        self.ventana_nuevo_usuario()

        # Posiciona los botones en la ventana
        self.botonverde.grid(row=0, column=0)
        self.botonrojo.grid(row=0, column=1)
        self.botonamarrillo.grid(row=1, column=0)
        self.botonazul.grid(row=1, column=1)

    def create_button(self, color, index):
        canvas = tk.Canvas(self.__ventana, bg=color, width=100, height=100, relief="raised")
        canvas.bind("<Button-1>", lambda event, c=color: self.on_button_click(event, canvas, c))
        return canvas

    def iniciar_juego(self):
        self.secuencia = []
        self.secuencia_user = []
        self.secuencia_user_active = False
        self.agregar_color_juego()

    def agregar_color_juego(self):
        self.secuencia.append(random.choice(self.color))
        self.mostrar_secuencia()

    def mostrar_secuencia(self):
        if self.dificultad == "Principiante":
            delay = 1000  # Milisegundos
        elif self.dificultad == "Intermedio":
            delay = 700
        elif self.dificultad == "Avanzado":
            delay = 500

        for i, color in enumerate(self.secuencia):
            self.__ventana.after(delay * i, lambda color=color: self.cambiar_color_botones(color))
            self.__ventana.after(delay * i + delay // 2, self.restaurar_color_botones)
        self.__ventana.after(delay * len(self.secuencia), self.activar_botones)

    def cambiar_color_botones(self, color):
        if color == self.color[0]:
            self.botonverde.config(bg="#ffffff")
        elif color == self.color[1]:
            self.botonrojo.config(bg="#ffffff")
        elif color == self.color[2]:
            self.botonamarrillo.config(bg="#ffffff")
        elif color == self.color[3]:
            self.botonazul.config(bg="#ffffff")

    def restaurar_color_botones(self):
        self.botonverde.config(bg=self.color[0])
        self.botonrojo.config(bg=self.color[1])
        self.botonamarrillo.config(bg=self.color[2])
        self.botonazul.config(bg=self.color[3])

    def ventana_nuevo_usuario(self):
        self.__dialogo = tk.Toplevel()
        self.__dialogo.geometry('300x200')
        self.__dialogo.resizable(0, 0)
        tk.Label(self.__dialogo, text="Nombre de Usuario:").pack()
        self.nombre_entrada = tk.Entry(self.__dialogo)
        self.nombre_entrada.pack()

        tk.Label(self.__dialogo, text="Selecciona la Dificultad:").pack()
        self.dificultad_var = tk.StringVar(value="Principiante")
        dificultades = ["Principiante", "Intermedio", "Avanzado"]
        for dificultad in dificultades:
            tk.Radiobutton(self.__dialogo, text=dificultad, variable=self.dificultad_var, value=dificultad).pack()

        self.boton_confirmar = tk.Button(self.__dialogo, text='Confirmar', command=self.guardar_nombre_usuario)
        self.boton_confirmar.pack()

    def guardar_nombre_usuario(self):
        nombre_usuario = self.nombre_entrada.get()
        dificultad = self.dificultad_var.get()
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        nuevo_jugador = Jugador(nombre_usuario, fecha_actual, hora_actual, 0, dificultad)
        gestor_jugadores = GestorJugadores("pysimonpuntajes.json")
        gestor_jugadores.guardar_jugador(nuevo_jugador)
        self.__dialogo.destroy()
        self.dificultad = dificultad
        self.nombre_usuario = nombre_usuario
        self.iniciar_juego()

    def on_button_click(self, event, canvas, color):
        if not self.secuencia_user_active:
            return
        canvas.config(bg="#ffffff")
        self.__ventana.after(500, lambda: canvas.config(bg=color))
        self.secuencia_user.append(color)
        if self.secuencia[:len(self.secuencia_user)] == self.secuencia_user:
            if len(self.secuencia) == len(self.secuencia_user):
                messagebox.showinfo("¡Bien hecho!", "Has completado la secuencia. Tu puntuación es: " + str(len(self.secuencia)))
                self.actualizar_puntuacion(len(self.secuencia))
                self.secuencia_user = []
                self.desactivar_botones()
                self.agregar_color_juego()
        else:
            messagebox.showinfo("¡Oh no!", "Has perdido. Tu puntuación final es: " + str(len(self.secuencia) - 1))
            self.actualizar_puntuacion(len(self.secuencia) - 1)
            self.__ventana.quit()

    def actualizar_puntuacion(self, puntaje):
        gestor_jugadores = GestorJugadores("pysimonpuntajes.json")
        for jugador in gestor_jugadores.jugadores:
            if jugador.get_nombre() == self.nombre_usuario:
                jugador._Jugador__puntaje = puntaje
                gestor_jugadores.guardar_jugadores()
                break

    def desactivar_botones(self):
        self.botonverde.unbind("<Button-1>")
        self.botonrojo.unbind("<Button-1>")
        self.botonamarrillo.unbind("<Button-1>")
        self.botonazul.unbind("<Button-1>")
        self.secuencia_user_active = False

    def activar_botones(self):
        self.botonverde.bind("<Button-1>", lambda event: self.on_button_click(event, self.botonverde, self.color[0]))
        self.botonrojo.bind("<Button-1>", lambda event: self.on_button_click(event, self.botonrojo, self.color[1]))
        self.botonamarrillo.bind("<Button-1>", lambda event: self.on_button_click(event, self.botonamarrillo, self.color[2]))
        self.botonazul.bind("<Button-1>", lambda event: self.on_button_click(event, self.botonazul, self.color[3]))
        self.secuencia_user_active = True



if __name__ == '__main__':
    ventana = tk.Tk()
    juego = simondice(ventana)
    ventana.mainloop()

import tkinter as tk
import random
from tkinter import messagebox, Menu
from gestor import GestorJugadores
from clasejugador import Jugador
import datetime

class SimonDice:
    def __init__(self, ventana):
        self.__ventana = ventana
        self.__ventana.title("Py-SimonGame")
        self.__ventana.geometry("300x350")  # Ventana más chica

        self.color = ["#ff0000", "#00ff00", "#0000ff", "#ffff00"]
        self.secuencia = []
        self.secuencia_user = []
        self.secuencia_user_active = False
        self.gestor_jugadores = GestorJugadores("pysimonpuntajes.json")
        
        self.nombre_usuario = ""
        self.puntaje = 0

        self.label_info = tk.Label(self.__ventana, text="Nombre: -- | Puntaje: 0", font=("Arial", 12))
        self.label_info.pack(pady=10)

        self.frame_botones = tk.Frame(self.__ventana)
        self.frame_botones.pack(expand=True, fill="both")
        
        self.botonverde = self.create_button(self.color[0])
        self.botonrojo = self.create_button(self.color[1])
        self.botonazul = self.create_button(self.color[2])
        self.botonamarillo = self.create_button(self.color[3])
        
        self.botonverde.grid(row=0, column=0, sticky="nsew")
        self.botonrojo.grid(row=0, column=1, sticky="nsew")
        self.botonazul.grid(row=1, column=0, sticky="nsew")
        self.botonamarillo.grid(row=1, column=1, sticky="nsew")
        
        self.frame_botones.grid_rowconfigure(0, weight=1)
        self.frame_botones.grid_rowconfigure(1, weight=1)
        self.frame_botones.grid_columnconfigure(0, weight=1)
        self.frame_botones.grid_columnconfigure(1, weight=1)
        
        self.mostrar_dialogo_usuario()
        self.crear_menu()

    def create_button(self, color):
        canvas = tk.Canvas(self.frame_botones, bg=color, width=100, height=100, relief="raised")
        canvas.bind("<Button-1>", lambda event, c=color: self.on_button_click(event, canvas, c))
        return canvas

    def iniciar_juego(self):
        self.secuencia = []
        self.secuencia_user = []
        self.secuencia_user_active = False
        self.puntaje = 0
        self.actualizar_info()
        self.agregar_color_juego()

    def agregar_color_juego(self):
        self.secuencia.append(random.choice(self.color))
        self.mostrar_secuencia()

    def mostrar_secuencia(self):
        delay = 1000  # Milisegundos por defecto para mostrar la secuencia
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
            self.botonazul.config(bg="#ffffff")
        elif color == self.color[3]:
            self.botonamarillo.config(bg="#ffffff")

    def restaurar_color_botones(self):
        self.botonverde.config(bg=self.color[0])
        self.botonrojo.config(bg=self.color[1])
        self.botonazul.config(bg=self.color[2])
        self.botonamarillo.config(bg=self.color[3])

    def on_button_click(self, event, canvas, color):
        if not self.secuencia_user_active:
            return
        canvas.config(bg="#ffffff")
        self.__ventana.after(500, lambda: canvas.config(bg=color))
        self.secuencia_user.append(color)
        if self.secuencia[:len(self.secuencia_user)] == self.secuencia_user:
            if len(self.secuencia) == len(self.secuencia_user):
                self.puntaje += 1
                self.actualizar_info()
                self.secuencia_user = []
                self.desactivar_botones()
                self.agregar_color_juego()
        else:
            messagebox.showinfo("GAME OVER", f"Has perdido. Tu puntuación final es: {self.puntaje}")
            self.guardar_puntaje_final()
            self.reset_juego()

    def guardar_puntaje_final(self):
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        nuevo_jugador = Jugador(self.nombre_usuario, fecha_actual, hora_actual, self.puntaje)
        self.gestor_jugadores.guardar_jugador(nuevo_jugador)

    def desactivar_botones(self):
        self.botonverde.unbind("<Button-1>")
        self.botonrojo.unbind("<Button-1>")
        self.botonazul.unbind("<Button-1>")
        self.botonamarillo.unbind("<Button-1>")
        self.secuencia_user_active = False

    def activar_botones(self):
        self.botonverde.bind("<Button-1>", lambda event: self.on_button_click(event, self.botonverde, self.color[0]))
        self.botonrojo.bind("<Button-1>", lambda event: self.on_button_click(event, self.botonrojo, self.color[1]))
        self.botonazul.bind("<Button-1>", lambda event: self.on_button_click(event, self.botonazul, self.color[2]))
        self.botonamarillo.bind("<Button-1>", lambda event: self.on_button_click(event, self.botonamarillo, self.color[3]))
        self.secuencia_user_active = True

    def mostrar_dialogo_usuario(self):
        self.__dialogo = tk.Toplevel(self.__ventana)
        self.__dialogo.geometry('300x200')
        self.__dialogo.resizable(0, 0)
        tk.Label(self.__dialogo, text="Nombre de Usuario:").pack()
        self.nombre_entrada = tk.Entry(self.__dialogo)
        self.nombre_entrada.pack()
        self.boton_confirmar = tk.Button(self.__dialogo, text='Confirmar', command=self.guardar_nombre_usuario)
        self.boton_confirmar.pack()

    def guardar_nombre_usuario(self):
        self.nombre_usuario = self.nombre_entrada.get()
        self.__dialogo.destroy()
        self.iniciar_juego()

    def reset_juego(self):
        self.secuencia = []
        self.secuencia_user = []
        self.secuencia_user_active = False
        self.puntaje = 0
        self.iniciar_juego()

    def actualizar_info(self):
        self.label_info.config(text=f"Nombre: {self.nombre_usuario} | Puntaje: {self.puntaje}")

    def crear_menu(self):
        menubar = Menu(self.__ventana)
        self.__ventana.config(menu=menubar)
        opciones_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones", menu=opciones_menu)
        opciones_menu.add_command(label="Ver puntajes", command=self.ver_puntajes)
        opciones_menu.add_separator()
        opciones_menu.add_command(label="Salir", command=self.__ventana.quit)

    def ver_puntajes(self):
        self.gestor_jugadores.ver_puntajes()

if __name__ == '__main__':
    ventana = tk.Tk()
    juego = SimonDice(ventana)
    ventana.mainloop()

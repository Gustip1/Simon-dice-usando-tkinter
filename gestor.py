from clasejugador import Jugador
import json
from tkinter import messagebox
class GestorJugadores:
    def __init__(self, archivo):
        self.archivo = archivo #ruta del archivo json
        self.jugadores = self.cargar_jugadores() 

    def cargar_jugadores(self):
        try:
            with open(self.archivo, 'r') as file:
                data = json.load(file)
                return [Jugador.from_dict(jugador) for jugador in data]
        except FileNotFoundError:
            return []


    def guardar_jugador(self, jugador):
        self.jugadores.append(jugador)
        self.guardar_jugadores()

    def guardar_jugadores(self):
        with open(self.archivo, 'w') as file:
            json.dump([jugador.to_dict() for jugador in self.jugadores], file, indent=4)



    def ver_puntajes(self):
        self.jugadores.sort(reverse=True)
        puntajes = "\n".join([f"Nombre: {jugador.get_nombre()}, Puntaje: {jugador.get_puntaje()}, Fecha: {jugador.get_fecha()},Hora: {jugador.get_hora()} Nivel: {jugador.get_nivel()}" for jugador in self.jugadores])
        messagebox.showinfo("Puntajes", puntajes)

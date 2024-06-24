class Jugador:
    def __init__(self, nombre, fecha, hora, puntaje):
        self.__nombre = nombre
        self.__fecha = fecha
        self.__hora = hora
        self.__puntaje = puntaje
    
    def get_nombre(self):
        return self.__nombre
    
    def get_fecha(self):
        return self.__fecha
    
    def get_hora(self):
        return self.__hora
    
    def get_puntaje(self):
        return self.__puntaje
    
    def __gt__(self, other):
        return self.__puntaje > other.__puntaje

    def to_dict(self):
        return {
            "nombre": self.__nombre,
            "fecha": self.__fecha,
            "hora": self.__hora,
            "puntaje": self.__puntaje
        }

    @staticmethod
    def from_dict(data):
        try:
            return Jugador(
                data["nombre"],
                data["fecha"],
                data["hora"],
                data["puntaje"]
            )
        except KeyError as e:
            print(f"Error: Falta la clave {e} en los datos del jugador: {data}")
            raise

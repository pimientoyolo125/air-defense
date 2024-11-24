from ..entidad import Entidad
import configuracion

class Intruso(Entidad):
    def __init__(self, dir_imagen, velocidad, punto_inicial):
        
        super().__init__(dir_imagen, punto_inicial.x, punto_inicial.y)
        self.velocidad = velocidad
        self.punto_inicial = punto_inicial

    def dijkstra(self):
        
        # Inicializar variables
        cola = [()]
        distancias = {}
        camino = {}
from ..entidad import Entidad
import configuracion

class Intruso(Entidad):
    def __init__(self, dir_imagen, velocidad, punto_inicial, punto_final):
        
        super().__init__(dir_imagen, punto_inicial.x, punto_inicial.y)
        self.velocidad = velocidad
        self.punto_inicial = punto_inicial
        self.punto_final = punto_final

    def set_punto_inicial(self, punto_inicial):
        self.punto_inicial = punto_inicial
        self.x = punto_inicial.x
        self.y = punto_inicial.y

    def dijkstra(self, puntos):
        
        # Inicializar variables
        distancias = {punto: float('inf') for punto in puntos}
        distancias[self.punto_inicial] = 0
        visitados = set()
        camino = {}
        pendientes = [self.punto_inicial]

        # Recorrer los puntos
        while pendientes:
            # Seleccionar el punto con la menor distancia acumulada
            punto_actual = min(pendientes, key=lambda p: distancias[p])
            pendientes.remove(punto_actual)
            visitados.add(punto_actual)

            # Si llegamos al punto final, salimos del bucle
            if punto_actual == self.punto_final:
                break

            # Relajación de vecinos
            for vecino in punto_actual.vecinos:
                if vecino in visitados:
                    continue  # Saltar puntos ya visitados
                nuevo_costo = distancias[punto_actual] + vecino.peso
                if nuevo_costo < distancias[vecino]:
                    distancias[vecino] = nuevo_costo
                    camino[vecino] = punto_actual
                    if vecino not in pendientes:
                        pendientes.append(vecino)

        # Reconstruir el camino desde el punto final
        ruta = []
        punto = self.punto_final
        while punto != self.punto_inicial:
            ruta.append(punto)
            punto = camino.get(punto, None)  # Obtener el nodo previo
            if punto is None:
                raise ValueError("No se pudo encontrar un camino al destino.")
        ruta.append(self.punto_inicial)
        return ruta[::-1] 
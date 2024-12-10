from .defensa import Defensa
import configuracion
import random

class S1(Defensa):
    def __init__(self, x, y):

        super().__init__(
            configuracion.DIR_S1,
            x, 
            y,
            alcance=30,
            peso_minimo=0.1,
            peso_maximo=0.8,
            dano_maximo=160,
            dano_minimo=16
        )
    
    def mover_defensa(self, avion,probabilidad, distancia):
        if random.random() < probabilidad:
            x_avion = avion.x
            y_avion = avion.y
            x_actual = self.x
            y_actual = self.y
            co = y_avion - y_actual
            ca = x_avion - x_actual
            h = (co**2 + ca**2)**0.5
            if h <= distancia:
                self.x = x_avion
                self.y = y_avion
            else:
                direccion_x = ca/h
                direccion_y = co/h
                mover_x = int(direccion_x * distancia)
                mover_y = int(direccion_y * distancia)
                self.x += mover_x
                self.y += mover_y
            
import pygame
import configuracion
from ..entidad import Entidad

class Defensa(Entidad):
    def __init__(self, dir_imagen, x, y, alcance, peso_minimo, peso_maximo, dano_minimo, dano_maximo):

        super().__init__(dir_imagen, x, y)
        self.alcance = alcance
        self.peso_minimo = peso_minimo
        self.peso_maximo = peso_maximo
        self.dano_minimo = dano_minimo
        self.dano_maximo = dano_maximo

    def dibujar(self, pantalla):
        
        super().dibujar(pantalla)
        
        # Dibujar el alcance
        pygame.draw.circle(pantalla, configuracion.ROJO, (self.x, self.y), self.alcance, 1)
        
    
        



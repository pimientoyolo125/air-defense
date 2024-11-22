import pygame
import configuracion

class Defensa:
    def __init__(self, dir_imagen, x, y):

        self.imagen = pygame.image.load(dir_imagen)
        self.imagen = pygame.transform.scale(self.imagen, (configuracion.ANCHO_OBJETO, configuracion.ALTO_OBJETO))

        self.x = x
        self.y = y

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def mover(self, x, y):
        self.x = x
        self.y = y

    def tomar_rectangulo(self):
        return pygame.Rect(self.x, self.y, configuracion.ANCHO_OBJETO, configuracion.ALTO_OBJETO)

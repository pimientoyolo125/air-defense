import pygame

class Punto():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.peso = 0
        self.radio = 2
        self.vecinos = []

    def set_peso(self, peso):
        self.peso = peso
        if self.peso < 0:
            self.peso = 0
        elif self.peso > 100:
            self.peso = 100

    def calcular_color(self):
        verde = int(255 - self.peso * 2.55)
        rojo = int(self.peso * 2.55)
        azul = 0
        return (rojo, verde, azul,100)

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.calcular_color(), (self.x, self.y), self.radio)

    def agregar_vecino(self, vecino):
        self.vecinos.append(vecino)
        
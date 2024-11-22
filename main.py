import pygame
import configuracion
import sys
import random
from entidades.defensas.s400 import S400
from entidades.intrusos.a10 import A10
from punto import Punto

pygame.init()

# Configuración de la pantalla
pantalla = pygame.display.set_mode((configuracion.ANCHO, configuracion.ALTO))
pygame.display.set_caption(configuracion.TITULO)

#Imagen de fondo
fondo = pygame.image.load(configuracion.DIR_FONDO)
fondo = pygame.transform.scale(fondo, (configuracion.ANCHO, configuracion.ALTO))

#Reloj
reloj = pygame.time.Clock()

################################### DEFENSAS ###################################
numero_defensas_s400 = 20

# Lista de defensas
defensas = []

# Crear ubicaciones aleatorias para las defensas
for i in range(numero_defensas_s400):
    x = random.randint(configuracion.ZONA_SEGURA, configuracion.ANCHO - configuracion.ANCHO_OBJETO)
    y = random.randint(configuracion.ALTO_OBJETO//2, configuracion.ALTO - configuracion.ALTO_OBJETO)

    defensas.append(S400(x, y))

################################### INTRUSO ###################################
intruso = None

# Crear ubicación aleatoria para el
x = random.randint(configuracion.ANCHO_OBJETO//2, configuracion.ZONA_SEGURA)
y = random.randint(configuracion.ALTO_OBJETO//2, configuracion.ALTO - configuracion.ALTO_OBJETO)

intruso = A10(x, y)


################################### ENTIDADES ##################################
entidades = []
entidades.extend(defensas)
entidades.append(intruso)


################################### PUNTO ######################################
puntos = []

# Crear cuadricula de puntos
for x in range(0, configuracion.ANCHO, configuracion.SEPARACION_PUNTOS):
    for y in range(0, configuracion.ALTO, configuracion.SEPARACION_PUNTOS):
        puntos.append(Punto(x, y))

################################### FUNCIONES ##################################
#Calculo de pesos de cada punto
def calcular_pesos():
    for punto in puntos:
        punto.set_peso(0)

        for defensa in defensas:
            distancia = ((punto.x - defensa.x)**2 + (punto.y - defensa.y)**2)**0.5
            if distancia < defensa.alcance:
                peso = defensa.peso_maximo - distancia * (defensa.peso_maximo - defensa.peso_minimo)/defensa.alcance
                punto.set_peso(punto.peso + peso)

calcular_pesos()


################################### BUCLE PRINCIPAL ############################


# Bucle principal
ejecutando = True
while ejecutando:

    # Eventos
    for evento in pygame.event.get():

        # Salir del juego
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Dibujando
    pantalla.blit(fondo, (0, 0))

    # Dibujar todos los puntos
    for punto in puntos:
        punto.dibujar(pantalla)

    # Dibujar todas las entidades
    for entidad in entidades:
        entidad.dibujar(pantalla)

    # Refresco de pantalla
    pygame.display.flip()
    reloj.tick(configuracion.FPS)
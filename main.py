import pygame
import configuracion
import sys
import random
from defensas.s400 import S400

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
numero_defensas_s400 = 5

# Lista de defensas
defensas = []

# Crear ubicaciones aleatorias para las defensas
for i in range(numero_defensas_s400):
    x = random.randint(200, configuracion.ANCHO - configuracion.ANCHO_OBJETO)
    y = random.randint(0, configuracion.ALTO - configuracion.ALTO_OBJETO)

    defensas.append(S400(x, y))


# Bucle principal
ejecutando = True
while ejecutando:

    # Eventos
    for evento in pygame.event.get():

        # Salir del juego
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Dibujado
    pantalla.blit(fondo, (0, 0))

    # Dibujar defensas
    for defensa in defensas:
        defensa.dibujar(pantalla)

    # Refresco de pantalla
    pygame.display.flip()
    reloj.tick(configuracion.FPS)
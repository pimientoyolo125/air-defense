import pygame
import configuracion
import sys

pygame.init()

# Configuración de la pantalla
pantalla = pygame.display.set_mode((configuracion.ANCHO, configuracion.ALTO))
pygame.display.set_caption(configuracion.TITULO)

#Imagen de fondo
fondo = pygame.image.load(configuracion.DIR_FONDO)
fondo = pygame.transform.scale(fondo, (configuracion.ANCHO, configuracion.ALTO))

#Reloj
reloj = pygame.time.Clock()

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

    # Refresco de pantalla
    pygame.display.flip()
    reloj.tick(configuracion.FPS)
import pygame
import configuracion
import sys
import random
from entidades.defensas.s400 import S400
from entidades.intrusos.a10 import A10
from entidades.objetivo import Objetivo
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

################################### PUNTO ######################################
puntos = []

# Crear cuadricula de puntos
for x in range(configuracion.SEPARACION_PUNTOS, configuracion.ANCHO, configuracion.SEPARACION_PUNTOS):
    for y in range(configuracion.SEPARACION_PUNTOS, configuracion.ALTO, configuracion.SEPARACION_PUNTOS):
        puntos.append(Punto(x, y))

################################### FUNCIONES ##################################
def buscar_punto_mas_cercano(x, y):
    punto_mas_cercano = None
    distancia_minima = 1000000

    for punto in puntos:
        distancia = ((x - punto.x)**2 + (y - punto.y)**2)**0.5

        if distancia < distancia_minima:
            punto_mas_cercano = punto
            distancia_minima = distancia

    return punto_mas_cercano
    

#Calculo de pesos de cada punto
def calcular_pesos(defensas):
    for punto in puntos:
        punto.set_peso(0)

        for defensa in defensas:
            distancia = ((punto.x - defensa.x)**2 + (punto.y - defensa.y)**2)**0.5
            if distancia < defensa.alcance:
                peso = defensa.peso_maximo - distancia * (defensa.peso_maximo - defensa.peso_minimo)/defensa.alcance
                punto.set_peso(punto.peso + peso)



#Conectar puntos
def conectar_puntos():
    for punto in puntos:

        longitud = len(puntos)
        indice = puntos.index(punto)
        limite_inferior = max(0, indice - configuracion.ALTO//configuracion.SEPARACION_PUNTOS-1)
        limite_superior = min(longitud, indice + configuracion.ANCHO//configuracion.SEPARACION_PUNTOS+1)

        for vecino in puntos[limite_inferior:limite_superior]:
            
            if vecino != punto:
                distancia = ((punto.x - vecino.x)**2 + (punto.y - vecino.y)**2)**0.5

                if distancia < configuracion.SEPARACION_PUNTOS * 1.5:
                    punto.agregar_vecino(vecino)

conectar_puntos()

def dibujar_ruta(ruta):
    for i in range(1, len(ruta)):
        pygame.draw.line(pantalla, configuracion.COLOR_RUTA, (ruta[i-1].x, ruta[i-1].y), (ruta[i].x, ruta[i].y), 2)

################################### DEFENSAS ###################################
numero_defensas_s400 = 20

# Lista de defensas
defensas = []

# Crear ubicaciones aleatorias para las defensas
for i in range(numero_defensas_s400):
    x = random.randint(configuracion.ZONA_SEGURA, configuracion.ANCHO - configuracion.ANCHO_OBJETO)
    y = random.randint(configuracion.ALTO_OBJETO//2, configuracion.ALTO - configuracion.ALTO_OBJETO)

    defensas.append(S400(x, y))

calcular_pesos(defensas)

################################## OBJECTIVO ##################################
punto_final = buscar_punto_mas_cercano(configuracion.OBJETIVO[0], configuracion.OBJETIVO[1])

objetivo = Objetivo(punto_final)


################################### INTRUSO ###################################
intruso = None

# Crear ubicación aleatoria para el
x = random.randint(configuracion.ANCHO_OBJETO//2, configuracion.ZONA_SEGURA)
y = random.randint(configuracion.ALTO_OBJETO//2, configuracion.ALTO - configuracion.ALTO_OBJETO)

punto_inicial = buscar_punto_mas_cercano(x, y)

intruso = A10(punto_inicial, punto_final)

# Calcular ruta
ruta = intruso.dijkstra(puntos)


################################### ENTIDADES ##################################
entidades = []
entidades.extend(defensas)
entidades.append(intruso)



################################### BUCLE PRINCIPAL ############################

i_ruta = 0


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

    # Dibujar ruta
    dibujar_ruta(ruta)

    # Dibujar todos los puntos
    for punto in puntos:
        punto.dibujar(pantalla)

    # Dibujar todas las entidades
    for entidad in entidades:
        entidad.dibujar(pantalla)

    # Dibujar objetivo
    objetivo.dibujar(pantalla)

    if(i_ruta < len(ruta)):
        intruso.mover(ruta[i_ruta].x, ruta[i_ruta].y)
        i_ruta += 1
        if i_ruta == len(ruta):
            print("Intruso llego al objetivo")

    # Refresco de pantalla
    pygame.display.flip()
    reloj.tick(configuracion.FPS)
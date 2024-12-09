import pygame
import configuracion
import random
from entidades.defensas.s400 import S400
from entidades.defensas.s1 import S1
from entidades.defensas.pac3 import PAC3
from entidades.defensas.ironDome import IronDome
from entidades.intrusos.a10 import A10
from entidades.intrusos.f15 import F15
from entidades.objetivo import Objetivo
from punto import Punto
import pandas as pd


columnas = ["avion", "daño recibido", "cantidad de impactos", "cantidad disparos", "derribado", "objetivo", "cantidad de saltos"]

df = pd.DataFrame(columns=columnas)

df.to_csv("simulacion_grilla.csv", index=False)

numero_simulaciones = 1000

def agregar_fila(nueva_fila):
    global df
    nueva_fila = pd.DataFrame([nueva_fila])
    df = pd.concat([df, nueva_fila], ignore_index=True)
    df.to_csv("simulacion_grilla.csv", index=False)
    

pygame.init()

cantidad_llegadas = 0
cantidad_derribados = 0

for i_simulacion in range(numero_simulaciones):

    list_intrusos = ["A10", "F15"]

    select_intruso = random.choice(list_intrusos)


    ################################### VARIABLES DE CONTROL ##################################

    i_ruta = 0
    intruso_derribado = False
    intruso_llego = False
    cantidad_disparons = 0
    cantidad_impactos = 0
    dano_total = 0
    ejecutando = True


    ###############################################################################3

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
    def generar_grilla_defensas(defensas):

        # Barajar defensas
        random.shuffle(defensas)

        alto_minimo = int(configuracion.ALTO*0.1)
        ancho_minimo = int(configuracion.ANCHO*0.1)

        separacion_alto = (configuracion.ALTO-2*alto_minimo)//3
        separacion_ancho = (configuracion.ANCHO-2*ancho_minimo-configuracion.ZONA_SEGURA)//4

        #generar grilla de defensas
        for i in range(5):
            for j in range(4):
                x = ancho_minimo + i*separacion_ancho + configuracion.ZONA_SEGURA
                y = alto_minimo + j*separacion_alto
                defensas[i*4+j].set_posicion(x, y)

        return defensas

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
                    peso_real = 1 - (1-punto.peso)*(1-peso)
                    punto.set_peso(peso_real)



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

    def intruso_dano(intruso, defensa, distancia):
        global dano_total
        dano = defensa.dano_maximo - distancia * (defensa.dano_maximo - defensa.dano_minimo)/defensa.alcance
        dano_total += dano
        intruso.hacer_dano(dano)

    def impacto(intruso, defensas):
        global cantidad_disparons
        global cantidad_impactos
        global intruso_derribado
        for defensa in defensas:
            distancia = ((intruso.x - defensa.x)**2 + (intruso.y - defensa.y)**2)**0.5
            if distancia <= defensa.alcance:
                peso = intruso.punto_inicial.peso
                cantidad_disparons += 1
                if random.random() < peso:
                    cantidad_impactos += 1
                    intruso_dano(intruso, defensa, distancia)
                    if intruso.derribado:
                        intruso_derribado = True
                        return False
                    break
        return True

    def print_resultados():

        global intruso_derribado
        global intruso_llego
        global i_ruta
        global cantidad_disparons
        global cantidad_impactos
        global dano_total
        global select_intruso
        global cantidad_derribados
        global cantidad_llegadas

        if intruso_llego:
            intruso_derribado = False
            cantidad_llegadas += 1
        else:
            cantidad_derribados += 1

        nueva_fila = {
            "avion": select_intruso,
            "daño recibido": dano_total,
            "cantidad de impactos": cantidad_impactos,
            "cantidad disparos": cantidad_disparons,
            "derribado": intruso_derribado,
            "objetivo": intruso_llego,
            "cantidad de saltos": i_ruta
        }

        agregar_fila(nueva_fila)

        print("\n\n-----------------------------------------------------------------")
        print("Simulacion: ", i_simulacion+1)
        print("Cantidad de llegadas: ", cantidad_llegadas)
        print("Cantidad de derribados: ", cantidad_derribados)
        print()
        print("Resultados:")
        print("Intruso: ", select_intruso)
        print("Cantidad de disparos: ", cantidad_disparons)
        print("Cantidad de impactos: ", cantidad_impactos)
        print("Daño total: ", dano_total)
        print("Intruso derribado: ", intruso_derribado)
        print("Intruso llego al objetivo: ", intruso_llego)
        print("Cantidad de saltos: ", i_ruta)
        print("-----------------------------------------------------------------")

    ################################### DEFENSAS ###################################
    numero_defensas_s400 = 5
    numero_defensas_pac3 = 5
    numero_defensas_s1 = 5
    numero_defensas_iron_dome = 5

    # Lista de defensas
    defensas = []

    # Crear ubicaciones aleatorias para las defensas
    for i in range(numero_defensas_s400):
        x = random.randint(configuracion.ZONA_SEGURA, configuracion.ANCHO - configuracion.ANCHO_OBJETO)
        y = random.randint(configuracion.ALTO_OBJETO//2, configuracion.ALTO - configuracion.ALTO_OBJETO)

        defensas.append(S400(x, y))

    for i in range(numero_defensas_pac3):
        x = random.randint(configuracion.ZONA_SEGURA, configuracion.ANCHO - configuracion.ANCHO_OBJETO)
        y = random.randint(configuracion.ALTO_OBJETO//2, configuracion.ALTO - configuracion.ALTO_OBJETO)

        defensas.append(PAC3(x, y))

    for i in range(numero_defensas_s1):
        x = random.randint(configuracion.ZONA_SEGURA, configuracion.ANCHO - configuracion.ANCHO_OBJETO)
        y = random.randint(configuracion.ALTO_OBJETO//2, configuracion.ALTO - configuracion.ALTO_OBJETO)

        defensas.append(S1(x, y))

    for i in range(numero_defensas_iron_dome):
        x = random.randint(configuracion.ZONA_SEGURA, configuracion.ANCHO - configuracion.ANCHO_OBJETO)
        y = random.randint(configuracion.ALTO_OBJETO//2, configuracion.ALTO - configuracion.ALTO_OBJETO)

        defensas.append(IronDome(x, y))

    defensas = generar_grilla_defensas(defensas)

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

    if select_intruso == "A10":
        intruso = A10(punto_inicial, punto_final)
    elif select_intruso == "F15":
        intruso = F15(punto_inicial, punto_final)

    # Calcular ruta
    ruta = intruso.dijkstra(puntos)


    ################################### ENTIDADES ##################################
    entidades = []
    entidades.extend(defensas)
    entidades.append(intruso)



    ################################### BUCLE PRINCIPAL ############################


    show_results = False
    distancia_siguiente = 1

    # Bucle principal
    while ejecutando:

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
            # Impacto
            ejecutando = impacto(intruso, defensas)
            if not ejecutando:
                intruso.derribado = True
                intruso.intruso_inmune()
                print_resultados()
                show_results = True

            # Calcular si salta de punto
            elif distancia_siguiente <= 0:
                # Mover intruso
                distancia_siguiente = 1
                intruso.set_punto_inicial(ruta[i_ruta])
                i_ruta += 1
                if i_ruta == len(ruta):
                    intruso_llego = True
                    intruso.derribado = False
                    intruso.intruso_inmune()
                    print_resultados()
                    show_results = True
                    ejecutando = False
            else:
                distancia_siguiente -= intruso.velocidad/3000



        if intruso_derribado:
            if(not print_resultados):
                print_resultados()
                show_results = True
                ejecutando = False

        

        


        # Refresco de pantalla
        pygame.display.flip()
        #reloj.tick(configuracion.FPS)

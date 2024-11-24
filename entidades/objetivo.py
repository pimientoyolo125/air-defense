from .entidad import Entidad
import configuracion

class Objetivo(Entidad):
    def __init__(self):

        super().__init__(
            configuracion.DIR_OBJETIVO, 
            configuracion.OBJETIVO[0],
            configuracion.OBJETIVO[1]
            )
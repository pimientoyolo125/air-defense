from .entidad import Entidad
import configuracion

class Objetivo(Entidad):
    def __init__(self, punto_final):

        super().__init__(
            configuracion.DIR_OBJETIVO, 
            punto_final.x,
            punto_final.y
            )
        
        self.punto_final = punto_final
from .intruso import Intruso
import configuracion

class A10(Intruso):
    def __init__(self,punto_inicial):
        super().__init__(
            configuracion.DIR_A10, 
            velocidad=1,
            punto_inicial=punto_inicial)
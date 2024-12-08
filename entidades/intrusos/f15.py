from .intruso import Intruso
import configuracion

class F15(Intruso):
    def __init__(self,punto_inicial, punto_final):
        super().__init__(
            configuracion.DIR_F15, 
            velocidad=3017,
            punto_inicial=punto_inicial,
            punto_final=punto_final,
            salud=60
            )
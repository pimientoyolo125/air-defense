from .intruso import Intruso
import configuracion

class A10(Intruso):
    def __init__(self, x, y):
        super().__init__(
            configuracion.DIR_A10, 
            x, 
            y, 
            velocidad=1)
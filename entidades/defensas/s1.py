from .defensa import Defensa
import configuracion

class S1(Defensa):
    def __init__(self, x, y):

        super().__init__(
            configuracion.DIR_S1,
            x, 
            y,
            alcance=30,
            peso_minimo=0.1,
            peso_maximo=0.8,
            dano_maximo=160,
            dano_minimo=16
        )
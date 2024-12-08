from .defensa import Defensa
import configuracion

class IronDome(Defensa):
    def __init__(self, x, y):

        super().__init__(
            configuracion.DIR_IRON_DOME,
            x, 
            y,
            alcance=70,
            peso_minimo=0.1,
            peso_maximo=0.9,
            dano_maximo=490,
            dano_minimo=49
        )
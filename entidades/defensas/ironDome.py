from .defensa import Defensa
import configuracion

class IronDome(Defensa):
    def __init__(self, x, y):

        super().__init__(
            configuracion.DIR_IRON_DOME,
            x, 
            y,
            alcance=100,
            peso_minimo=0.1,
            peso_maximo=0.9,
            dano_maximo=240,
            dano_minimo=24
        )
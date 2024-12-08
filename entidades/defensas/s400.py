from .defensa import Defensa
import configuracion

class S400(Defensa):
    def __init__(self, x, y):

        super().__init__(
            configuracion.DIR_S400,
            x, 
            y,
            alcance=120,
            peso_minimo=0.1,
            peso_maximo=0.9,
            dano_maximo=900,
            dano_minimo=90
        )
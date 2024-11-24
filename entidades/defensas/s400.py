from .defensa import Defensa
import configuracion

class S400(Defensa):
    def __init__(self, x, y):

        super().__init__(
            configuracion.DIR_S400,
            x, 
            y,
            alcance=100,
            peso_minimo=10,
            peso_maximo=70,
            dano_maximo=50,
            dano_minimo=10
        )
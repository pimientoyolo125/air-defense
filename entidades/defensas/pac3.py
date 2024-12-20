from .defensa import Defensa
import configuracion

class PAC3(Defensa):
    def __init__(self, x, y):

        super().__init__(
            configuracion.DIR_PAC3,
            x, 
            y,
            alcance=80,
            peso_minimo=0.1,
            peso_maximo=0.8,
            dano_maximo=510,
            dano_minimo=51
        )
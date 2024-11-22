from .defensa import Defensa
import configuracion

class S400(Defensa):
    def __init__(self, x, y):

        super().__init__(configuracion.DIR_S400,x, y)

    def disparar(self):
        pass
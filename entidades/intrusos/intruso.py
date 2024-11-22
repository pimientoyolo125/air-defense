from ..entidad import Entidad

class Intruso(Entidad):
    def __init__(self, dir_imagen, x, y, velocidad):
        
        super().__init__(dir_imagen, x, y)
        self.velocidad = velocidad
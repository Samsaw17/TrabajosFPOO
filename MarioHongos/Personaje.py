class Personaje:
    def __init__(self, id, nombre, x, y, estado="Vivo"):
        self.id         = id
        self.nombre     = nombre
        self.posicionX  = x
        self.posicionY  = y
        self.estado     = estado

    def mover(self, dx=0, dy=0):
        self.posicionX += dx
        self.posicionY += dy

class Enemigo(Personaje):
    def __init__(self, id, nombre, x=0, y=0, velocidad=2):
        super().__init__(id, nombre, x, y)
        self.direccion = "izquierda"
        self.velocidad = velocidad
        self.vivo = True
        self.image_key = "goomba"

    def mover_automatico(self):
        if not self.vivo:
            return
        if self.direccion == "izquierda":
            self.posicionX -= self.velocidad
        else:
            self.posicionX += self.velocidad

        # Cambiar dirección si toca los bordes
        if self.posicionX <= 10:
            self.direccion = "derecha"
        elif self.posicionX >= 740:
            self.direccion = "izquierda"

    def aplastar(self):
        self.vivo = False
        self.image_key = "goombaMuerto"


class Jugador(Personaje):
    def __init__(self, id, nombre, x=0, y=0):
        super().__init__(id, nombre, x, y)
        self.vidas   = 3
        self.monedas = 0
        self.puntos  = 0
        self.tiempo  = 300
        self.dispara = False
        self.tamano = 'pequeño'
        self.direccion = "derecha"
        self.saltando = False 
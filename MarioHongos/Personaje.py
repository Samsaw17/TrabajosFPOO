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
        self.direccion = "izquierda"  # Siempre se mueve hacia la izquierda
        self.velocidad = velocidad
        self.vivo = True
        self.image_key = "goomba"

    def mover_automatico(self):
        if not self.vivo:
            return
            
        # Movimiento constante hacia la izquierda
        self.posicionX -= self.velocidad
        
        # Reaparece por la derecha si sale completamente por la izquierda
        if self.posicionX <= -40:
            self.posicionX = 800

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
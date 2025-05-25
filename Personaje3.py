import random
import time

class Personaje:
    def __init__(self, id, nombre, x, y, estado="Vivo"):
        self.id = id
        self.nombre = nombre
        self.posicionX = x
        self.posicionY = y
        self.estado = estado

    def mover(self, dx=0, dy=0):
        self.posicionX += dx
        self.posicionY += dy


class Enemigo(Personaje):
    def __init__(self, vida, id, x=0, y=0):
        super().__init__(id, f"Goomba{id}", x, y)
        self.vida = vida
        self.direccion = "izquierda"
        self.velocidad = 2
        self.vivo = True
        self.image_key = "goomba"

    def mover_automatico(self, game_width):
        if not self.vivo:
            return
            
        self.posicionX -= self.velocidad
        
        if self.posicionX < -50:
            self.respawn(game_width)

    def respawn(self, game_width):
        self.posicionX = random.randint(game_width + 40, game_width + 200)
        self.posicionY = 346
        self.vivo = True
        self.image_key = "goomba"

    def aplastar(self):
        self.vivo = False
        self.image_key = "goombaMuerto"


class Jugador(Personaje):
    def __init__(self, id, nombre, x=0, y=0):
        super().__init__(id, nombre, x, y)
        self.vidas = 3
        self.monedas = 0
        self.puntos = 0
        self.tiempo = 300
        self.tamano = 'pequeño'
        self.direccion = "derecha"
        self.saltando = False
        self.image_key = "inicial"
import random

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


class Koopa(Enemigo):
    def __init__(self, vida, id, x=None, y=0):
        # Alternar posición inicial basada en ID
        if id % 2 == 1: 
            x = 0
            direccion_caida = "derecha"
            image_key = "KoopaDerecha"
        else:
            x = 750
            direccion_caida = "izquierda"
            image_key = "Koopa"
        
        super().__init__(vida, id, x, y)
        self.direccion_caida = direccion_caida
        self.image_key = image_key
        self.velocidad_caida = 8
        self.caido = False
        self.velocidad = 2 if self.direccion_caida == "derecha" else -2
        self.posicionY = -50 
        
    def mover_automatico(self, game_width):
        if not self.vivo:
            return
            
        if not self.caido:
            self.posicionY += self.velocidad_caida
            if self.posicionY >= 346:
                self.posicionY = 346
                self.caido = True
        else:
            self.posicionX += self.velocidad
            
            if (self.direccion_caida == "izquierda" and self.posicionX < -50) or \
                (self.direccion_caida == "derecha" and self.posicionX > game_width + 50):
                self.respawn(game_width)
                
    def respawn(self, game_width):
        self.vivo = True
        self.caido = False
        
        # Alternar posición de respawn
        if self.direccion_caida == "izquierda":
            self.posicionX = game_width + 50
        else:
            self.posicionX = -50
            
        self.posicionY = -50


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
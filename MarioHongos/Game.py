import pygame
import random
import time
from Personaje import Jugador, Enemigo

# Constantes del juego
PASO_X = 10
JUMP_HEIGHT = 100
JUMP_STEPS = 10
ASSETS_DIR = "assets/images/"
WIDTH, HEIGHT = 800, 477
GROUND_Y = 333 

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Juego de Mario")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.imgs = {}
        self.load_images()

        self.players = []
        self.font = pygame.font.SysFont("Arial", 20)

        # Jugador principal
        p1 = Jugador(1, "Jugador1", 200, GROUND_Y)
        self.add_player(p1, "inicial")

        # Enemigos
        self.enemigos = []
        goomba = Enemigo(100, "Goomba1", x=600, y=346)
        self.enemigos.append(goomba)

        # Ítems
        self.hongoRojo = self.spawn_item("hongoRojo")
        self.hongoVerde = self.spawn_item("hongoVerde")

        self.enemigos_aplastados = {}

    def load_images(self):
        def load_img(name, size):
            return pygame.transform.scale(pygame.image.load(ASSETS_DIR + name), size)

        self.imgs["fondo"] = pygame.image.load(ASSETS_DIR + "FondoMundo.png")

        self.imgs["inicial"] = load_img("1.png", (50, 50))
        self.imgs["inicialGrande"] = load_img("1.png", (60, 60))
        self.imgs["inicialI"] = load_img("1i.png", (50, 50))
        self.imgs["inicialGrandeI"] = load_img("1i.png", (60, 60))
        self.imgs["izquierda"] = load_img("2i.png", (50, 50))
        self.imgs["izquierdaGrande"] = load_img("2i.png", (60, 60))
        self.imgs["derecha"] = load_img("2.png", (50, 50))
        self.imgs["derechaGrande"] = load_img("2.png", (60, 60))
        self.imgs["agachado"] = load_img("4.png", (50, 50))
        self.imgs["agachadoGrande"] = load_img("4.png", (60, 60))
        self.imgs["agachadoI"] = load_img("4i.png", (50, 50))
        self.imgs["agachadoGrandeI"] = load_img("4i.png", (60, 60))
        self.imgs["saltando"] = load_img("5.png", (50, 50))
        self.imgs["saltandoGrande"] = load_img("5.png", (60, 60))
        self.imgs["saltandoI"] = load_img("5i.png", (50, 50))
        self.imgs["saltandoGrandeI"] = load_img("5i.png", (60, 60))
        self.imgs["hongoRojo"] = load_img("hongoRojo.png", (40, 40))
        self.imgs["hongoVerde"] = load_img("hongoVerde.png", (40, 40))
        self.imgs["goomba"] = load_img("goombas.png", (40, 40))
        self.imgs["goombaMuerto"] = load_img("goombas_muerte.png", (40, 30))

    def spawn_item(self, key):
        x = random.randint(0, WIDTH - 40)
        y = 350
        return {"img": self.imgs[key], "pos": [x, y]}

    def add_player(self, jugador, img_key):
        jugador.image_key = img_key
        self.players.append(jugador)

    def update_stats(self, jugador):
        y = 10
        for attr in ("posicionX", "posicionY", "vidas", "monedas", "puntos", "tiempo"):
            texto = f"{attr}: {getattr(jugador, attr)}"
            texto_img = self.font.render(texto, True, (0, 0, 0))
            self.screen.blit(texto_img, (10, y))
            y += 20

    def draw(self):
        self.screen.blit(self.imgs["fondo"], (0, 0))

        if self.hongoRojo:
            self.screen.blit(self.hongoRojo["img"], self.hongoRojo["pos"])
        if self.hongoVerde:
            self.screen.blit(self.hongoVerde["img"], self.hongoVerde["pos"])

        current_time = time.time()
        for enemigo in self.enemigos:
            if not enemigo.vivo and enemigo.id in self.enemigos_aplastados:
                if current_time - self.enemigos_aplastados[enemigo.id] > 5:
                    continue
            img = self.imgs[enemigo.image_key]
            self.screen.blit(img, (enemigo.posicionX, enemigo.posicionY))

        for jugador in self.players:
            img = self.imgs[jugador.image_key]
            self.screen.blit(img, (jugador.posicionX, jugador.posicionY))
            self.update_stats(jugador)

        pygame.display.flip()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        jugador = self.players[0]

        limite_derecho = 800 - (60 if jugador.tamano == "grande" else 50)
        if keys[pygame.K_RIGHT] and jugador.posicionX + PASO_X <= limite_derecho:
            jugador.direccion = "derecha"
            jugador.image_key = "derechaGrande" if jugador.tamano == 'grande' else "derecha"
            jugador.mover(dx=PASO_X)

        if keys[pygame.K_LEFT] and jugador.posicionX - PASO_X >= 0:
            jugador.direccion = "izquierda"
            jugador.image_key = "izquierdaGrande" if jugador.tamano == 'grande' else "izquierda"
            jugador.mover(dx=-PASO_X)

        elif keys[pygame.K_DOWN]:
            if jugador.tamano == 'grande':
                jugador.image_key = "agachadoGrande" if jugador.direccion == "derecha" else "agachadoGrandeI"
            else:
                jugador.image_key = "agachado" if jugador.direccion == "derecha" else "agachadoI"

        elif keys[pygame.K_UP] and not jugador.saltando:
            self.saltar(jugador)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                jugador = self.players[0]
                if event.key in (pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT) and not jugador.saltando:
                    if jugador.tamano == 'grande':
                        jugador.image_key = "inicialGrande" if jugador.direccion == "derecha" else "inicialGrandeI"
                    else:
                        jugador.image_key = "inicial" if jugador.direccion == "derecha" else "inicialI"

    def saltar(self, jugador):
        if not hasattr(jugador, 'pasos_salto'):
            jugador.pasos_salto = 0
            jugador.saltando = True
            paso = JUMP_HEIGHT // JUMP_STEPS
            direccion = jugador.direccion

            if jugador.tamano == "grande":
                jugador.image_key = "saltandoGrande" if direccion == "derecha" else "saltandoGrandeI"
            else:
                jugador.image_key = "saltando" if direccion == "derecha" else "saltandoI"

        if jugador.pasos_salto < JUMP_STEPS * 2:
            if jugador.pasos_salto < JUMP_STEPS:
                jugador.mover(dy=-(JUMP_HEIGHT // JUMP_STEPS))  # Subida
            else:
                jugador.mover(dy=(JUMP_HEIGHT // JUMP_STEPS))  # Bajada
            
            jugador.pasos_salto += 1
        else:
            jugador.saltando = False
            del jugador.pasos_salto
            jugador.posicionY = GROUND_Y
            if jugador.tamano == "grande":
                jugador.image_key = "inicialGrande" if jugador.direccion == "derecha" else "inicialGrandeI"
            else:
                jugador.image_key = "inicial" if jugador.direccion == "derecha" else "inicialI"

    def check_collisions(self, jugador):
        jugador_height = 60 if jugador.tamano == "grande" else 50
        jugador_rect = pygame.Rect(jugador.posicionX, jugador.posicionY, 50, jugador_height)

        if self.hongoRojo:
            hongo_rect = pygame.Rect(*self.hongoRojo["pos"], 40, 40)
            if jugador_rect.colliderect(hongo_rect):
                self.hongoRojo = None
                self.crecer_personaje(jugador)

        if self.hongoVerde:
            hongo_rect = pygame.Rect(*self.hongoVerde["pos"], 40, 40)
            if jugador_rect.colliderect(hongo_rect):
                self.hongoVerde = None
                jugador.vidas += 1

        current_time = time.time()
        self.enemigos = [e for e in self.enemigos if e.id not in self.enemigos_aplastados or current_time - self.enemigos_aplastados[e.id] <= 5]

        for enemigo in self.enemigos:
            if not enemigo.vivo:
                continue

            enemigo_rect = pygame.Rect(enemigo.posicionX, enemigo.posicionY, 40, 40)

            if jugador_rect.colliderect(enemigo_rect):
                if jugador_rect.bottom <= enemigo_rect.top + 10 and jugador.saltando:
                    enemigo.aplastar()
                    jugador.puntos += 100
                    self.enemigos_aplastados[enemigo.id] = current_time

    def crecer_personaje(self, jugador):
        jugador.tamano = 'grande'
        if jugador.direccion == "derecha":
            jugador.image_key = "inicialGrande"
        else:
            jugador.image_key = "inicialGrandeI"

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.handle_input()

            # Mover enemigos independientemente del estado del jugador
            for enemigo in self.enemigos:
                if enemigo.vivo:
                    enemigo.mover_automatico()

            # Actualizar salto si está ocurriendo
            if hasattr(self.players[0], 'pasos_salto'):
                self.saltar(self.players[0])

            self.check_collisions(self.players[0])
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
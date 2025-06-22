import pygame
import random
import time
import math
from Personaje import Jugador, Enemigo, Koopa
from Sound import Sound

# Constantes
PASO_X = 10
JUMP_HEIGHT = 100
JUMP_STEPS = 10
ASSETS_DIR = "assets/images/"
WIDTH, HEIGHT = 800, 477
GROUND_Y = 333
GAME_OVER_FONT_SIZE = 72
MENU_FONT_SIZE = 36
MAX_MONEDAS = 10
TIEMPO_REAPARICION_ESTRELLA = 10

class Moneda:
    def __init__(self, x, y):
        self.posicionX = x
        self.posicionY = y
        self.activa = True
        self.image_key = "moneda"
        self.ancho = 30
        self.alto = 30

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Juego de Mario")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.sound = Sound()
        self.running = True
        self.game_over = False
        self.victory = False
        self.ultimo_segundo = pygame.time.get_ticks() // 1000
        self.imgs = {}
        self.load_images()
        self.players = []
        self.font = pygame.font.SysFont("Arial", 20)
        self.game_over_font = pygame.font.SysFont("Arial", GAME_OVER_FONT_SIZE, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", MENU_FONT_SIZE)

        # Jugador principal
        p1 = Jugador(1, "Jugador1", 200, GROUND_Y)
        self.add_player(p1, "inicial")

        # Sistema de enemigos
        self.enemigos = []
        self.koopas = []
        self.enemigos_aplastados = {}
        self.goomba_id_counter = 1

        # Control de spawneo
        self.goombas_por_oleada = 2
        self.koopas_por_oleada = 1
        self.goombas_eliminados_total = 0
        self.koopas_eliminados_total = 0
        self.max_goombas_total = 10
        self.max_koopas_total = 5

        # Sistema de monedas
        self.monedas = []
        self.spawn_monedas(10)

        # Crear primera oleada de enemigos
        self.spawn_oleada_goombas()
        self.spawn_oleada_koopas()

        # Ítems
        self.hongoRojo = self.spawn_item("hongoRojo", 300, 350)
        self.hongoVerde = self.spawn_item("hongoVerde", 600, 350)
        
        # Sistema de estrella
        self.estrella = None
        self.tiempo_espera_estrella = random.randint(10, 20)
        self.ultimo_tiempo_estrella = time.time()
        self.tiempo_animacion_estrella = 0
        self.frame_estrella = 0

    def spawn_oleada_goombas(self):
        if self.goombas_eliminados_total >= self.max_goombas_total:
            return
        
        goombas_restantes = self.max_goombas_total - self.goombas_eliminados_total
        goombas_a_crear = min(self.goombas_por_oleada, goombas_restantes)
        
        base_x = WIDTH + 100
        separacion = 150
        
        for i in range(goombas_a_crear):
            x = base_x + (i * separacion)
            y = 346
            goomba = Enemigo(100, self.goomba_id_counter, x, y)
            self.enemigos.append(goomba)
            self.goomba_id_counter += 1

    def spawn_oleada_koopas(self):
        if self.koopas_eliminados_total >= self.max_koopas_total:
            return
            
        koopas_restantes = self.max_koopas_total - self.koopas_eliminados_total
        koopas_a_crear = min(self.koopas_por_oleada, koopas_restantes)
        
        for _ in range(koopas_a_crear):
            koopa = Koopa(100, self.goomba_id_counter)
            if koopa.direccion_caida == "izquierda":
                koopa.posicionX = 750 
            else:
                koopa.posicionX = random.randint(50, 150)
            koopa.posicionY = random.randint(-300, -100)
            self.koopas.append(koopa)
            self.goomba_id_counter += 1

    def verificar_oleada_completada(self):
        if all(not goomba.vivo for goomba in self.enemigos):
            if self.goombas_eliminados_total >= self.max_goombas_total:
                if self.koopas_eliminados_total >= self.max_koopas_total:
                    self.victory = True
                else:
                    self.spawn_oleada_koopas()
            else:
                self.spawn_oleada_goombas()
        
        if all(not koopa.vivo for koopa in self.koopas):
            if self.koopas_eliminados_total < self.max_koopas_total:
                self.spawn_oleada_koopas()

    def limpiar_enemigos_muertos(self):
        current_time = time.time()
        enemigos_a_eliminar = []
        koopas_a_eliminar = []
        
        for enemigo in self.enemigos:
            if not enemigo.vivo and enemigo.id in self.enemigos_aplastados:
                if current_time - self.enemigos_aplastados[enemigo.id] > 1.5:
                    enemigos_a_eliminar.append(enemigo)
                    del self.enemigos_aplastados[enemigo.id]
        
        for koopa in self.koopas:
            if not koopa.vivo and koopa.id in self.enemigos_aplastados:
                if current_time - self.enemigos_aplastados[koopa.id] > 1.5:
                    koopas_a_eliminar.append(koopa)
                    del self.enemigos_aplastados[koopa.id]
        
        for enemigo in enemigos_a_eliminar:
            self.enemigos.remove(enemigo)
        
        for koopa in koopas_a_eliminar:
            self.koopas.remove(koopa)

    def spawn_monedas(self, cantidad):
        min_altura = GROUND_Y - JUMP_HEIGHT + 30
        for _ in range(cantidad):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(min_altura, GROUND_Y - 40)
            self.monedas.append(Moneda(x, y))

    def check_monedas(self):
        if not any(moneda.activa for moneda in self.monedas):
            self.spawn_monedas(10)

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
        self.imgs["moneda"] = load_img("moneda.png", (30, 30))
        self.imgs["estrella"] = load_img("estrella.png", (90, 40))
        self.imgs["Koopa"] = load_img("Koopa.png", (45, 45))
        self.imgs["KoopaDerecha"] = load_img("KoopaDerecha.png", (45, 45))
        self.imgs["KoopaMuerte"] = load_img("KoopaMuerte.png", (45, 30))

    def spawn_item(self, key, x=None, y=None):
        x = x if x is not None else random.randint(0, WIDTH - 40)
        y = y if y is not None else 350
        return {
            "img": self.imgs[key],
            "pos": [x, y],
            "visible": True,
            "ultimo_recogido": 0,
            "tiempo_reaparicion": 15
        }

    def add_player(self, jugador, img_key):
        jugador.image_key = img_key
        self.players.append(jugador)

    def actualizar_estrella(self):
        tiempo_actual = time.time()
        
        if self.estrella is None:
            if tiempo_actual - self.ultimo_tiempo_estrella > self.tiempo_espera_estrella:
                x = random.randint(100, WIDTH - 100)
                y = 350
                self.estrella = {
                    "img": self.imgs["estrella"],
                    "pos": [x, y],
                    "visible": True,
                    "activa": True
                }
                self.ultimo_tiempo_estrella = tiempo_actual
        else:
            self.tiempo_animacion_estrella += 1
            if self.tiempo_animacion_estrella >= 10:
                self.tiempo_animacion_estrella = 0
                self.frame_estrella = (self.frame_estrella + 1) % 8
                
            offset_y = math.sin(self.frame_estrella * 0.25 * math.pi) * 5
            self.estrella["pos"][1] = 350 + offset_y

    def aplicar_efecto_estrella(self, jugador):
        if hasattr(jugador, 'estrella_activa') and jugador.estrella_activa:
            tiempo_actual = time.time()
            
            if tiempo_actual > jugador.invulnerable_until:
                jugador.estrella_activa = False
                return True
            
            return int(tiempo_actual * 8) % 2 == 0
        
        return True

    def update_stats(self, jugador):
        y = 10
        goombas_vivos = len([e for e in self.enemigos if e.vivo])
        koopas_vivos = len([k for k in self.koopas if k.vivo])
        goombas_restantes = self.max_goombas_total - self.goombas_eliminados_total
        koopas_restantes = self.max_koopas_total - self.koopas_eliminados_total
        
        inmunidad = "No"
        if hasattr(jugador, 'estrella_activa') and jugador.estrella_activa:
            tiempo_restante = max(0, jugador.invulnerable_until - time.time())
            inmunidad = f"Sí ({tiempo_restante:.1f}s)"
        elif hasattr(jugador, 'invulnerable_until') and time.time() < jugador.invulnerable_until:
            tiempo_restante = max(0, jugador.invulnerable_until - time.time())
            inmunidad = f"Parpadeo ({tiempo_restante:.1f}s)"
        
        stats = [
            ("posicionX", jugador.posicionX),
            ("posicionY", jugador.posicionY),
            ("vidas", jugador.vidas),
            ("monedas", jugador.monedas),
            ("puntos", jugador.puntos),
            ("Inmunidad", inmunidad),
            ("Goombas vivos", goombas_vivos),
            ("Koopas vivos", koopas_vivos),
            ("Goombas eliminados", f"{self.goombas_eliminados_total}/{self.max_goombas_total}"),
            ("Koopas eliminados", f"{self.koopas_eliminados_total}/{self.max_koopas_total}"),
            ("Enemigos restantes", goombas_restantes + koopas_restantes)
        ]
        
        for attr, value in stats:
            color = (255, 0, 0) if attr == "Enemigos restantes" and (goombas_restantes + koopas_restantes) == 0 else (0, 0, 0)
            if attr == "Inmunidad" and inmunidad.startswith("Sí"):
                color = (255, 215, 0)
            elif attr == "Inmunidad" and inmunidad.startswith("Parpadeo"):
                color = (255, 165, 0)
            texto_img = self.font.render(f"{attr}: {value}", True, color)
            self.screen.blit(texto_img, (10, y))
            y += 20

    def verificar_reaparicion_hongos(self, tiempo_actual):
        if not self.hongoRojo["visible"] and self.hongoRojo["ultimo_recogido"] > 0:
            tiempo_transcurrido = tiempo_actual - self.hongoRojo["ultimo_recogido"]
            if tiempo_transcurrido >= self.hongoRojo["tiempo_reaparicion"]:
                self.hongoRojo["visible"] = True
                self.hongoRojo["ultimo_recogido"] = 0
        
        if not self.hongoVerde["visible"] and self.hongoVerde["ultimo_recogido"] > 0:
            tiempo_transcurrido = tiempo_actual - self.hongoVerde["ultimo_recogido"]
            if tiempo_transcurrido >= self.hongoVerde["tiempo_reaparicion"]:
                self.hongoVerde["visible"] = True
                self.hongoVerde["ultimo_recogido"] = 0

    def draw(self):
        self.screen.blit(self.imgs["fondo"], (0, 0))
        
        tiempo_actual = pygame.time.get_ticks() // 1000
        self.verificar_reaparicion_hongos(tiempo_actual)
        
        for moneda in self.monedas:
            if moneda.activa:
                self.screen.blit(self.imgs[moneda.image_key], (moneda.posicionX, moneda.posicionY))
        
        if self.hongoRojo["visible"]:
            self.screen.blit(self.hongoRojo["img"], self.hongoRojo["pos"])
        if self.hongoVerde["visible"]:
            self.screen.blit(self.hongoVerde["img"], self.hongoVerde["pos"])
        
        if self.estrella and self.estrella["activa"]:
            self.screen.blit(self.estrella["img"], self.estrella["pos"])

        for enemigo in self.enemigos:
            img = self.imgs["goombaMuerto"] if not enemigo.vivo else self.imgs[enemigo.image_key]
            if -100 <= enemigo.posicionX <= WIDTH + 100:
                self.screen.blit(img, (enemigo.posicionX, enemigo.posicionY))

        for koopa in self.koopas:
            img = self.imgs["KoopaMuerte"] if not koopa.vivo else self.imgs[koopa.image_key]
            if -100 <= koopa.posicionX <= WIDTH + 100:
                self.screen.blit(img, (koopa.posicionX, koopa.posicionY))

        for jugador in self.players:
            # Primero verificar inmunidad por estrella
            if hasattr(jugador, 'estrella_activa') and jugador.estrella_activa:
                if self.aplicar_efecto_estrella(jugador):
                    img = self.imgs[jugador.image_key]
                    self.screen.blit(img, (jugador.posicionX, jugador.posicionY))
            # Luego verificar inmunidad por parpadeo (al perder vida)
            elif hasattr(jugador, 'invulnerable_until'):
                current_time = time.time()
                if current_time < jugador.invulnerable_until:
                    # Parpadeo: visible solo en frames pares (cada 0.1 segundos)
                    if int(current_time * 10) % 2 == 0:
                        img = self.imgs[jugador.image_key]
                        self.screen.blit(img, (jugador.posicionX, jugador.posicionY))
                else:
                    # Eliminar el atributo cuando termina la invulnerabilidad
                    del jugador.invulnerable_until
                    img = self.imgs[jugador.image_key]
                    self.screen.blit(img, (jugador.posicionX, jugador.posicionY))
            else:
                # Dibujar normalmente si no está invulnerable
                img = self.imgs[jugador.image_key]
                self.screen.blit(img, (jugador.posicionX, jugador.posicionY))
            
            self.update_stats(jugador)

        pygame.display.flip()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        jugador = self.players[0]
        limite_derecho = WIDTH - (60 if jugador.tamano == "grande" else 50)
        
        if keys[pygame.K_RIGHT] and jugador.posicionX + PASO_X <= limite_derecho:
            jugador.direccion = "derecha"
            if not jugador.saltando:
                jugador.image_key = "derechaGrande" if jugador.tamano == 'grande' else "derecha"
            jugador.mover(dx=PASO_X)
        
        if keys[pygame.K_LEFT] and jugador.posicionX - PASO_X >= 0:
            jugador.direccion = "izquierda"
            if not jugador.saltando:
                jugador.image_key = "izquierdaGrande" if jugador.tamano == 'grande' else "izquierda"
            jugador.mover(dx=-PASO_X)
        
        if keys[pygame.K_DOWN] and not jugador.saltando and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            if jugador.tamano == 'grande':
                jugador.image_key = "agachadoGrande" if jugador.direccion == "derecha" else "agachadoGrandeI"
            else:
                jugador.image_key = "agachado" if jugador.direccion == "derecha" else "agachadoI"
        
        if keys[pygame.K_UP] and not jugador.saltando:
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
        direccion = jugador.direccion
        
        if jugador.tamano == "grande":
            jugador.image_key = "saltandoGrande" if direccion == "derecha" else "saltandoGrandeI"
        else:
            jugador.image_key = "saltando" if direccion == "derecha" else "saltandoI"
        
        if jugador.pasos_salto < JUMP_STEPS * 2:
            if jugador.pasos_salto < JUMP_STEPS:
                jugador.mover(dy=-(JUMP_HEIGHT // JUMP_STEPS))
            else:
                jugador.mover(dy=(JUMP_HEIGHT // JUMP_STEPS))
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
        
        current_time = time.time()
        
        # Si el jugador tiene inmunidad por estrella
        if hasattr(jugador, 'estrella_activa') and jugador.estrella_activa:
            # Matar enemigos al contacto
            for enemigo in self.enemigos + self.koopas:
                if enemigo.vivo:
                    enemigo_rect = pygame.Rect(enemigo.posicionX, enemigo.posicionY, 40, 40)
                    if jugador_rect.colliderect(enemigo_rect):
                        enemigo.aplastar()
                        jugador.puntos += 200
                        self.enemigos_aplastados[enemigo.id] = current_time
                        if enemigo in self.enemigos:
                            self.goombas_eliminados_total += 1
                        else:
                            self.koopas_eliminados_total += 1
            # Permitir recolectar otros ítems normalmente
            pass
        # Si el jugador está en modo invulnerable (parpadeo), no procesar colisiones con enemigos
        elif hasattr(jugador, 'invulnerable_until') and current_time < jugador.invulnerable_until:
            pass  # Permitir recolectar ítems pero no recibir daño
        else:
            # Colisión con enemigos (solo si no está invulnerable)
            for enemigo in self.enemigos + self.koopas:
                if not enemigo.vivo:
                    continue
                
                enemigo_rect = pygame.Rect(enemigo.posicionX, enemigo.posicionY, 40, 40)
                
                if jugador_rect.colliderect(enemigo_rect):
                    if jugador_rect.bottom <= enemigo_rect.top + 10 and jugador.saltando:
                        enemigo.aplastar()
                        jugador.puntos += 100
                        self.enemigos_aplastados[enemigo.id] = current_time
                        if enemigo in self.enemigos:
                            self.goombas_eliminados_total += 1
                        else:
                            self.koopas_eliminados_total += 1
                        
                        if (self.goombas_eliminados_total >= self.max_goombas_total and 
                            self.koopas_eliminados_total >= self.max_koopas_total):
                            self.victory = True
                    else:
                        if jugador.tamano == "grande":
                            jugador.tamano = 'pequeño'
                            jugador.image_key = "inicial" if jugador.direccion == "derecha" else "inicialI"
                            # No activar invulnerabilidad al cambiar de grande a pequeño
                        else:
                            jugador.vidas -= 1
                            if jugador.vidas <= 0:
                                self.sound.play('muerte')
                                self.game_over = True
                            
                            # Activar invulnerabilidad por 2 segundos solo al perder una vida
                            jugador.invulnerable_until = current_time + 2.0
                        
                        # Empujar al jugador lejos del enemigo (en ambos casos)
                        if jugador.posicionX < enemigo.posicionX:
                            jugador.posicionX = max(0, jugador.posicionX - 50)
                        else:
                            jugador.posicionX = min(WIDTH - 50, jugador.posicionX + 50)
        
        # Colisión con monedas (siempre activa)
        for moneda in self.monedas:
            if moneda.activa:
                moneda_rect = pygame.Rect(moneda.posicionX, moneda.posicionY, moneda.ancho, moneda.alto)
                if jugador_rect.colliderect(moneda_rect):
                    moneda.activa = False
                    jugador.monedas += 1
                    jugador.puntos += 50
                    self.sound.play('moneda')
        
        if jugador.monedas >= MAX_MONEDAS:
            jugador.vidas += 1
            jugador.monedas = 0
        
        # Colisión con hongos (siempre activa)
        tiempo_actual = pygame.time.get_ticks() // 1000
        
        if self.hongoRojo["visible"]:
            hongo_rect = pygame.Rect(*self.hongoRojo["pos"], 40, 40)
            if jugador_rect.colliderect(hongo_rect):
                self.hongoRojo["visible"] = False
                self.hongoRojo["ultimo_recogido"] = tiempo_actual
                self.crecer_personaje(jugador)
        
        if self.hongoVerde["visible"]:
            hongo_rect = pygame.Rect(*self.hongoVerde["pos"], 40, 40)
            if jugador_rect.colliderect(hongo_rect):
                self.hongoVerde["visible"] = False
                self.hongoVerde["ultimo_recogido"] = tiempo_actual
                jugador.vidas += 1
        
        # Colisión con estrella (siempre activa)
        if self.estrella and self.estrella["activa"]:
            estrella_rect = pygame.Rect(self.estrella["pos"][0], self.estrella["pos"][1], 40, 40)
            if jugador_rect.colliderect(estrella_rect):
                self.estrella["activa"] = False
                self.estrella = None
                jugador.invulnerable_until = time.time() + 8.0  # 8 segundos de inmunidad
                jugador.estrella_activa = True
                jugador.puntos += 200
                self.ultimo_tiempo_estrella = time.time()
                self.tiempo_espera_estrella = random.randint(10, 20)

    def crecer_personaje(self, jugador):
        jugador.tamano = 'grande'
        jugador.image_key = "inicialGrande" if jugador.direccion == "derecha" else "inicialGrandeI"

    def show_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        game_over_text = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        instruction_text = self.menu_font.render("Presiona ENTER para reiniciar", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False
            self.clock.tick(60)

    def show_victory_screen(self):
        self.screen.fill((0, 0, 0))
        victory_text = self.game_over_font.render("¡GANASTE!", True, (0, 255, 0))
        victory_rect = victory_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        self.screen.blit(victory_text, victory_rect)
        
        jugador = self.players[0]
        score_text = self.menu_font.render(f"Puntuación: {jugador.puntos}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        instruction_text = self.menu_font.render("Presiona ENTER para reiniciar", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False
            self.clock.tick(60)

    def reset_game(self):
        self.players = []
        p1 = Jugador(1, "Jugador1", 200, GROUND_Y)
        self.add_player(p1, "inicial")
        self.enemigos = []
        self.koopas = []
        self.enemigos_aplastados = {}
        self.goomba_id_counter = 1
        self.goombas_eliminados_total = 0
        self.koopas_eliminados_total = 0
        
        self.monedas = []
        self.spawn_monedas(10)
        self.spawn_oleada_goombas()
        self.spawn_oleada_koopas()
        
        self.hongoRojo = self.spawn_item("hongoRojo", 300, 350)
        self.hongoVerde = self.spawn_item("hongoVerde", 600, 350)
        
        self.estrella = None
        self.tiempo_espera_estrella = random.randint(10, 20)
        self.ultimo_tiempo_estrella = time.time()
        self.tiempo_animacion_estrella = 0
        self.frame_estrella = 0
        
        self.game_over = False
        self.victory = False

    def run(self):
        while self.running:
            if self.game_over:
                if self.show_game_over_screen():
                    self.reset_game()
                else:
                    self.running = False
                    break
            elif self.victory:
                if self.show_victory_screen():
                    self.reset_game()
                else:
                    self.running = False
                    break
            
            self.clock.tick(60)
            self.handle_events()
            self.handle_input()
            
            for enemigo in self.enemigos:
                if enemigo.vivo:
                    enemigo.mover_automatico(WIDTH)
            
            for koopa in self.koopas:
                if koopa.vivo:
                    koopa.mover_automatico(WIDTH)
            
            if hasattr(self.players[0], 'pasos_salto'):
                self.saltar(self.players[0])
            
            self.verificar_oleada_completada()
            self.limpiar_enemigos_muertos()
            self.actualizar_estrella()
            self.check_collisions(self.players[0])
            self.check_monedas()
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
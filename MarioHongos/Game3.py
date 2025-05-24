import pygame 
import random
import time
from Personaje3 import Jugador, Enemigo

# Constantes
PASO_X = 10
JUMP_HEIGHT = 100
JUMP_STEPS = 10
ASSETS_DIR = "assets/images/"
WIDTH, HEIGHT = 800, 477
GROUND_Y = 333
GAME_OVER_FONT_SIZE = 72
MENU_FONT_SIZE = 36
MAX_MONEDAS = 10  # Máximo de monedas para obtener una vida
TIEMPO_INICIAL = 60  # Tiempo inicial en segundos para la cuenta regresiva

class Moneda:
    def __init__(self, x, y):
        self.posicionX = x
        self.posicionY = y
        self.activa = True
        self.image_key = "moneda"
        self.ancho = 30
        self.alto = 30
        self.tiempo_animacion = 0
        self.frame_actual = 0
    
    def animar(self):
        # Simple animación para hacer que las monedas giren (simulación)
        self.tiempo_animacion += 1
        if self.tiempo_animacion >= 10:  # Cada 10 frames
            self.tiempo_animacion = 0
            self.frame_actual = (self.frame_actual + 1) % 4  # 4 frames de animación

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Juego de Mario")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.victory = False  # Variable para controlar la victoria
        self.tiempo_restante = TIEMPO_INICIAL
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
        self.enemigos_aplastados = {}
        self.goomba_id_counter = 1
        
        # Control de spawneo
        self.goombas_por_oleada = 2
        self.goombas_eliminados_total = 0
        self.max_goombas_total = 10
        
        # Sistema de monedas
        self.monedas = []
        self.spawn_monedas(5)  # Generamos 5 monedas iniciales
        
        # Crear primera oleada de Goombas
        self.spawn_oleada_goombas()

        # Ítems
        self.hongoRojo = self.spawn_item("hongoRojo")
        self.hongoVerde = self.spawn_item("hongoVerde")

    def spawn_oleada_goombas(self):
        if self.goombas_eliminados_total >= self.max_goombas_total:
            return
        
        goombas_restantes = self.max_goombas_total - self.goombas_eliminados_total
        goombas_a_crear = min(self.goombas_por_oleada, goombas_restantes)
        
        for _ in range(goombas_a_crear):
            x = random.randint(WIDTH + 40, WIDTH + 200)
            y = 346
            goomba = Enemigo(100, self.goomba_id_counter, x, y)
            self.enemigos.append(goomba)
            self.goomba_id_counter += 1

    def verificar_oleada_completada(self):
        if all(not goomba.vivo for goomba in self.enemigos):
            if self.goombas_eliminados_total >= self.max_goombas_total:
                # Si ya eliminamos todos los goombas permitidos, victoria
                self.victory = True
            else:
                self.spawn_oleada_goombas()

    def limpiar_enemigos_muertos(self):
        current_time = time.time()
        enemigos_a_eliminar = []
        
        for enemigo in self.enemigos:
            if not enemigo.vivo and enemigo.id in self.enemigos_aplastados:
                if current_time - self.enemigos_aplastados[enemigo.id] > 1.5:
                    enemigos_a_eliminar.append(enemigo)
                    del self.enemigos_aplastados[enemigo.id]
        
        for enemigo in enemigos_a_eliminar:
            self.enemigos.remove(enemigo)

    def spawn_monedas(self, cantidad):
        # Generar monedas en posiciones aleatorias pero alcanzables con un salto
        # Considerando que JUMP_HEIGHT es 100 y el GROUND_Y es 333
        # Las monedas deben estar a una altura máxima de GROUND_Y - JUMP_HEIGHT
        min_altura = GROUND_Y - JUMP_HEIGHT + 30  # Ajuste para que sea alcanzable
        
        for _ in range(cantidad):
            x = random.randint(100, WIDTH - 100)
            # Alturas alcanzables durante el salto
            y = random.randint(min_altura, GROUND_Y - 40)
            self.monedas.append(Moneda(x, y))
    
    def check_monedas(self):
        # Verificar si todas las monedas han sido recogidas
        if not any(moneda.activa for moneda in self.monedas):
            self.spawn_monedas(5)  # Generar nuevas monedas

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
        # Cargar imagen de la moneda
        self.imgs["moneda"] = load_img("moneda.png", (30, 30))

    def spawn_item(self, key):
        x = random.randint(0, WIDTH - 40)
        y = 350
        return {"img": self.imgs[key], "pos": [x, y]}

    def add_player(self, jugador, img_key):
        jugador.image_key = img_key
        self.players.append(jugador)

    def update_stats(self, jugador):
        y = 10
        goombas_vivos = len([e for e in self.enemigos if e.vivo])
        goombas_restantes = self.max_goombas_total - self.goombas_eliminados_total
        
        stats = [
            ("posicionX", jugador.posicionX),
            ("posicionY", jugador.posicionY),
            ("vidas", jugador.vidas),
            ("monedas", jugador.monedas),
            ("puntos", jugador.puntos),
            ("tiempo", jugador.tiempo),
            ("Goombas vivos", goombas_vivos),
            ("Goombas eliminados", f"{self.goombas_eliminados_total}/{self.max_goombas_total}"),
            ("Goombas restantes", goombas_restantes)
        ]
        
        for attr, value in stats:
            # Color rojo para los goombas restantes cuando sean 0
            color = (255, 0, 0) if attr == "Goombas restantes" and goombas_restantes == 0 else (0, 0, 0)
            texto_img = self.font.render(f"{attr}: {value}", True, color)
            self.screen.blit(texto_img, (10, y))
            y += 20

    def draw(self):
        self.screen.blit(self.imgs["fondo"], (0, 0))

        # Dibujar monedas activas
        for moneda in self.monedas:
            if moneda.activa:
                moneda.animar()  # Animar la moneda
                self.screen.blit(self.imgs[moneda.image_key], (moneda.posicionX, moneda.posicionY))

        if self.hongoRojo:
            self.screen.blit(self.hongoRojo["img"], self.hongoRojo["pos"])
        if self.hongoVerde:
            self.screen.blit(self.hongoVerde["img"], self.hongoVerde["pos"])

        for enemigo in self.enemigos:
            img = self.imgs["goombaMuerto"] if not enemigo.vivo else self.imgs[enemigo.image_key]
            if -100 <= enemigo.posicionX <= WIDTH + 100:
                self.screen.blit(img, (enemigo.posicionX, enemigo.posicionY))

        for jugador in self.players:
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

        # Colisión con monedas
        for moneda in self.monedas:
            if moneda.activa:
                moneda_rect = pygame.Rect(moneda.posicionX, moneda.posicionY, moneda.ancho, moneda.alto)
                if jugador_rect.colliderect(moneda_rect):
                    moneda.activa = False
                    jugador.monedas += 1
                    jugador.puntos += 50  # Añadir puntos por recoger moneda
                    
                    # Sistema de vida por monedas
                    if jugador.monedas >= MAX_MONEDAS:
                        jugador.vidas += 1
                        jugador.monedas = 0
                        # Efecto de sonido o visual aquí (opcional)

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

        if hasattr(jugador, 'invulnerable_until') and current_time < jugador.invulnerable_until:
            return

        for enemigo in self.enemigos:
            if not enemigo.vivo:
                continue

            enemigo_rect = pygame.Rect(enemigo.posicionX, enemigo.posicionY, 40, 40)

            if jugador_rect.colliderect(enemigo_rect):
                if jugador_rect.bottom <= enemigo_rect.top + 10 and jugador.saltando:
                    enemigo.aplastar()
                    jugador.puntos += 100
                    self.enemigos_aplastados[enemigo.id] = current_time
                    self.goombas_eliminados_total += 1
                    
                    # Verificar si hemos eliminado todos los goombas
                    if self.goombas_eliminados_total >= self.max_goombas_total:
                        # Victoria al eliminar todos los goombas
                        self.victory = True
                else:
                    if jugador.tamano == "grande":
                        jugador.tamano = 'pequeño'
                        jugador.image_key = "inicial" if jugador.direccion == "derecha" else "inicialI"
                    else:
                        jugador.vidas -= 1
                        if jugador.vidas <= 0:
                            self.game_over = True
                    
                    jugador.invulnerable_until = current_time + 1.0
                    
                    if jugador.posicionX < enemigo.posicionX:
                        jugador.posicionX = max(0, jugador.posicionX - 50)
                    else:
                        jugador.posicionX = min(WIDTH - 50, jugador.posicionX + 50)

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
        
        # Mostrar puntuación final
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

    def update_timer(self):
        current_second = pygame.time.get_ticks() // 1000
        if current_second > self.ultimo_segundo:
            self.ultimo_segundo = current_second
            if self.tiempo_restante > 0:
                self.tiempo_restante -= 1
                
            # Si el tiempo llega a 0, el jugador gana
            if self.tiempo_restante <= 0:
                self.victory = True

    def reset_game(self):
        self.players = []
        p1 = Jugador(1, "Jugador1", 200, GROUND_Y)
        self.add_player(p1, "inicial")
        
        self.enemigos = []
        self.enemigos_aplastados = {}
        self.goomba_id_counter = 1
        self.goombas_eliminados_total = 0
        
        # Reiniciar sistema de monedas
        self.monedas = []
        self.spawn_monedas(5)
        
        self.spawn_oleada_goombas()
        
        self.hongoRojo = self.spawn_item("hongoRojo")
        self.hongoVerde = self.spawn_item("hongoVerde")
        
        # Reiniciar el temporizador
        self.tiempo_restante = TIEMPO_INICIAL
        self.ultimo_segundo = pygame.time.get_ticks() // 1000
        
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
            self.update_timer()  # Mantener la actualización del temporizador por si deseas usar cuenta regresiva también

            for enemigo in self.enemigos:
                if enemigo.vivo:
                    enemigo.mover_automatico(WIDTH)

            if hasattr(self.players[0], 'pasos_salto'):
                self.saltar(self.players[0])

            self.verificar_oleada_completada()
            self.limpiar_enemigos_muertos()
            self.check_collisions(self.players[0])
            self.check_monedas()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()


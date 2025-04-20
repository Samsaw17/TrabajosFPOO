# Clase base
class Juego:
    def __init__(self, nombre, posicion):
        self.nombre = nombre
        self.posicion = posicion  # Tupla (x, y)

    def mover(self, nueva_posicion):
        self.posicion = nueva_posicion


# Clase Poder
class Poder:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def __str__(self):
        return f"{self.nombre}: {self.descripcion}"


# Clase Jugador
class Jugador(Juego):
    def __init__(self, nombre, posicion, vida):
        super().__init__(nombre, posicion)
        self.vida = vida
        self.poderes = []

    def agregar_poder(self, poder):
        self.poderes.append(poder)

    def __str__(self):
        poderes_str = '\n'.join(f" - {p}" for p in self.poderes)
        return (f"Jugador: {self.nombre}\n"
                f"Posición: {self.posicion}\n"
                f"Vida: {self.vida}\n"
                f"Poderes:\n{poderes_str}")


# Clase Enemigo
class Enemigo(Juego):
    def __init__(self, nombre, posicion, tipo):
        super().__init__(nombre, posicion)
        self.tipo = tipo

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) en posición {self.posicion}"


# Programa principal
def main():
    print("=== SUPER MARIO BROS ===")

    # Crear jugador en (0, 0)
    mario = Jugador("Mario", (0, 0), 3)
    print("\nJugador creado en posición inicial:", mario.posicion)

    # Crear enemigos
    enemigos = [
        Enemigo("Goomba 1", (5, 0), "Goomba"),
        Enemigo("Koopa 1", (7, 2), "Koopa Troopa"),
        Enemigo("Piraña", (4, 3), "Planta Piraña")
    ]
    print(f"\nSe han creado {len(enemigos)} enemigos.")

    # Crear nuevos poderes
    poder1 = Poder("Estrella", "inmunidad temporal")
    poder2 = Poder("Flor de fuego", "permite lanzar bolas de fuego")

    # Asignar poderes al jugador
    mario.agregar_poder(poder1)
    mario.agregar_poder(poder2)
    print("\nPoderes asignados al jugador.")

    # Mover al jugador
    mario.mover((3, 1))
    print(f"\nEl jugador se ha movido a {mario.posicion}.")

    # Mostrar información
    print("\n=== ESTADO ACTUAL DEL JUEGO ===")
    print("\nJUGADOR:")
    print(mario)

    print("\nENEMIGOS:")
    for enemigo in enemigos:
        print(enemigo)


# Ejecutar el programa
main()

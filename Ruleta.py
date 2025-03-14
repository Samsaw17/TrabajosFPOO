import random

# Bienvenida y reglas básicas
print("¡Bienvenido a la Ruleta de Apuestas!")
print("Comienzas con 100 coins.")
print("Opciones de apuesta: Número (1-36), Sección (1-12, 13-24, 25-36) o Color (rojo/negro).")

# Variables del jugador
saldo = 100
apuestas_realizadas = []
ganancias = []
victorias = 0
derrotas = 0

def mostrar_menu():
    print("\n¿Qué te gustaría hacer?")
    print("1. Realizar una apuesta")
    print("2. Consultar saldo disponible")
    print("3. Ver cantidades apostadas")
    print("4. Ver cantidades ganadas")
    print("5. Ver promedio de éxito")
    print("6. Salir")
    return int(input("Selecciona una opción: "))

while True:
    opcion = mostrar_menu()  
    
    if opcion == 1: # Menu de juego
        print("\nTipos de apuesta disponibles:")
        print("1. Número específico (1-36)")
        print("2. Sección (1-12, 13-24, 25-36)")
        print("3. Color (rojo o negro)")
        
        tipo_apuesta = int(input("Selecciona el tipo de apuesta: "))
        cantidad = int(input("¿Cuánto deseas apostar? "))
        
        if cantidad > saldo:
            print("No tienes suficiente saldo para esta apuesta.")
            continue
        
        saldo -= cantidad
        resultado = random.randint(1, 36)
        color_resultado = "rojo" if resultado % 2 == 0 else "negro"  
        if tipo_apuesta == 1:  # Número
            numero = int(input("Elige un número entre 1 y 36: "))
            if numero == resultado:
                ganancias.append(cantidad * 20)
                saldo += cantidad * 20
                print(f"¡Ganaste! El número ganador fue {resultado}, que es {color_resultado}")
                victorias += 1
            else:
                print(f"Perdiste. El número ganador fue {resultado}, que es {color_resultado}")
                derrotas += 1
        elif tipo_apuesta == 2: # Seccion
            print("Elige una sección:")
            print("1. 1-12")
            print("2. 13-24")
            print("3. 25-36")
            seccion = int(input("Selecciona una sección: "))
            if  (seccion == 1 and resultado in range(1, 13)) or \
                (seccion == 2 and resultado in range(13, 25)) or \
                (seccion == 3 and resultado in range(25, 37)):
                ganancias.append(cantidad * 5)
                saldo += cantidad * 5
                print(f"¡Ganaste! El número ganador fue {resultado}, que es {color_resultado}")
                victorias += 1
            else:
                print(f"Perdiste. El número ganador fue {resultado}, que es {color_resultado}")
                derrotas += 1
        elif tipo_apuesta == 3:  # Color
            color = input("Elige un color (rojo o negro): ").lower()
            if color == color_resultado:
                ganancias.append(cantidad * 2)
                saldo += cantidad * 2
                print(f"¡Ganaste! El número ganador fue {resultado} ({color_resultado}).")
                victorias += 1
            else:
                print(f"Perdiste. El número ganador fue {resultado} ({color_resultado}).")
                derrotas += 1
        
        apuestas_realizadas.append(cantidad)
    
    elif opcion == 2:
        print(f"\nSaldo disponible: {saldo} coins.")
    
    elif opcion == 3:
        print(f"\nCantidades apostadas: {apuestas_realizadas}")
    
    elif opcion == 4:
        print(f"\nCantidades ganadas: {ganancias}")
    
    elif opcion == 5:
        if derrotas > 0:
            promedio_exito = victorias / derrotas
            print(f"\nPromedio de éxito: {promedio_exito:.2f}")
        else:
            print("\nAún no has tenido derrotas, el promedio no puede calcularse.")
    
    elif opcion == 6:
        print("¡Gracias por jugar! Vuelve pronto.")
        break
    
    else:
        print("Opción no válida. Por favor, elige otra.")


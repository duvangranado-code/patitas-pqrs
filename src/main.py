# ===============================================================================
# main.py - Programa principal de Patitas PQRS
# Gestor de PQRS (Peticiones, Quejas, Reclamos y Sugerencias)
# Algoritmia y Programación 2026-2 - Universidad de Antioquia
#
# Para ejecutarlo:   python main.py     (desde la carpeta src o desde fuera)
# ============================================================
import autenticacion
import pqrs
import reportes
import validaciones

def mostrar_logo():
    print(r" ____   _  _____ ___ _____  _    ____  ")
    print(r"|  _ \ / \|_   _|_ _|_   _|/ \  / ___| ")
    print(r"| |_) / _ \ | |  | |  | | / _ \ \___ \ ")
    print(r"|  __/ ___ \| |  | |  | |/ ___ \ ___) |")
    print(r"|_| /_/   \_\_| |___| |_/_/   \_\____/ ")
    print("")
    print("Bienvenido a Patitas - Gestión de PQRS")

def mostrar_menu(usuario):
    print("\n----- MENÚ PRINCIPAL (" + usuario["usuario"] + ") -----")
    print("1. Registrar PQRS")
    print("2. Consultar PQRS")
    print("3. Registrar cambio en PQRS")
    print("4. Estadísticas")
    print("5. Salir")

def main():
    mostrar_logo()
    usuario = autenticacion.iniciar_sesion()       # sin login no hay menú
    if usuario is None:
        print("\nIngreso cancelado. ¡Hasta pronto!")
        return

    opcion = 0
    while opcion != 5:
        mostrar_menu(usuario)
        opcion = validaciones.validar_entero("Elija una opción: ")
        if opcion == 1:
            pqrs.registrar_pqrs(usuario)
        elif opcion == 2:
            pqrs.consultar_pqrs()
        elif opcion == 3:
            pqrs.cambiar_estado()
        elif opcion == 4:
            reportes.menu_estadisticas()
        elif opcion == 5:
            print("\n¡Gracias por usar Patitas PQRS! Hasta pronto.")
        else:
            print("Opción inválida. Elija un número entre 1 y 5.")

if __name__ == "__main__":
    main()

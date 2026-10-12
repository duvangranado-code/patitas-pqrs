import os

DATA_FILE = os.path.join("..", "data", "peticiones.txt")

def asegurar_archivo():
    """Asegura que la carpeta y el archivo de datos existan."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write("ID | TIPO | NOMBRE | DESCRIPCION | ESTADO\n")

def registrar_pqrs():
    print("\n--- Registrar Nueva PQRS ---")
    tipo = input("Ingrese el tipo (Petición, Queja, Reclamo, Sugerencia): ")
    nombre = input("Nombre del ciudadano/usuario: ")
    descripcion = input("Descripción de la solicitud: ")
    estado = "Registrada"
    
    # Generar un ID simple basado en el número de líneas
    asegurar_archivo()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    nuevo_id = len(lineas)
    
    registro = f"{nuevo_id} | {tipo} | {nombre} | {descripcion} | {estado}\n"
    
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(registro)
    
    print(f"\n¡PQRS registrada con éxito bajo el ID: {nuevo_id}!")

def consultar_pqrs():
    print("\n--- Listado de PQRS Registradas ---")
    asegurar_archivo()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        contenido = f.read()
    print(contenido if contenido.strip() else "No hay registros actuales.")

def menu():
    asegurar_archivo()
    while True:
        print("\n=== SISTEMA DE GESTIÓN DE PQRS ===")
        print("1. Registrar nueva PQRS")
        print("2. Consultar PQRS")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_pqrs()
        elif opcion == "2":
            consultar_pqrs()
        elif opcion == "3":
            print("\n¡Saliendo del sistema. Hasta luego!")
            break
        else:
            print("\nOpción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()

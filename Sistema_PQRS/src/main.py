import os

DATA_DIR = os.path.join("..", "data")

def obtener_ruta_archivo(tipo):
    """Retorna la ruta del archivo correspondiente según el tipo."""
    archivos = {
        "Peticion": "Peticion.txt",
        "Queja": "Queja.txt",
        "Reclamo": "Reclamo.txt",
        "Sugerencia": "Sugerencia.txt"
    }
    nombre_archivo = archivos.get(tipo, "Peticion.txt")
    return os.path.join(DATA_DIR, nombre_archivo)

def registrar_pqrs():
    print("\n--- Registrar Nueva Solicitud ---")
    print("Seleccione el tipo:")
    print("1. Peticion")
    print("2. Queja")
    print("3. Reclamo")
    print("4. Sugerencia")
    
    op_tipo = input("Opción (1-4): ")
    tipos = {"1": "Peticion", "2": "Queja", "3": "Reclamo", "4": "Sugerencia"}
    tipo_seleccionado = tipos.get(op_tipo, "Peticion")
    
    nombre = input("Nombre del ciudadano/usuario: ")
    descripcion = input("Descripción de la solicitud: ")
    estado = "Registrada"
    
    ruta_archivo = obtener_ruta_archivo(tipo_seleccionado)
    
    # Generar ID
    nuevo_id = 1
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
            nuevo_id = len(lineas) + 1
            
    registro = f"{nuevo_id} | {nombre} | {descripcion} | {estado}\n"
    
    with open(ruta_archivo, "a", encoding="utf-8") as f:
        f.write(registro)
        
    print(f"\n¡{tipo_seleccionado} registrada con éxito con el ID: {nuevo_id}!")

def consultar_pqrs():
    print("\n--- Consultar Solicitudes ---")
    print("1. Peticiones")
    print("2. Quejas")
    print("3. Reclamos")
    print("4. Sugerencias")
    
    op_tipo = input("Seleccione el tipo a consultar (1-4): ")
    tipos = {"1": "Peticion", "2": "Queja", "3": "Reclamo", "4": "Sugerencia"}
    tipo_seleccionado = tipos.get(op_tipo, "Peticion")
    
    ruta_archivo = obtener_ruta_archivo(tipo_seleccionado)
    
    print(f"\n--- Listado de {tipo_seleccionado}s ---")
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        print(contenido if contenido.strip() else "No hay registros en este archivo.")
    else:
        print("El archivo correspondiente no existe.")

def menu():
    while True:
        print("\n=== SISTEMA DE GESTIÓN PATITAS PQRS ===")
        print("1. Registrar solicitud")
        print("2. Consultar solicitudes")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_pqrs()
        elif opcion == "2":
            consultar_pqrs()
        elif opcion == "3":
            print("\n¡Gracias por usar el sistema Patitas PQRS!")
            break
        else:
            print("\nOpción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()

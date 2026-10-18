# ============================================================
# archivos.py - Lectura y escritura de los archivos planos
# Proyecto: Patitas PQRS (Algoritmia y Programación 2026-2)
#
# Cada tipo de solicitud tiene su propio archivo en la carpeta data/:
#   Peticion.txt, Queja.txt, Reclamo.txt, Sugerencia.txt
# Todos tienen la misma estructura: una línea de encabezado y luego
# un registro por línea, con los campos separados por el símbolo |
# ============================================================
import os

# La carpeta data/ se calcula desde la ubicación de este archivo,
# así funciona sin importar desde dónde se ejecute el programa.
CARPETA_SRC = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(CARPETA_SRC), "data")

SEPARADOR = "|"

# Campos de cada registro (en el mismo orden del encabezado de los archivos)
CAMPOS = (
    "id", "nombre_completo", "tipo_documento", "numero_documento",
    "tipo_telefono", "telefono_contacto", "correo_electronico", "direccion",
    "tipo_solicitud", "fecha_radicacion", "canal_recepcion", "asunto_titulo",
    "descripcion_detallada", "tipo_mascota", "campus_relacionado",
    "fecha_maxima_respuesta", "estado_peticion", "usuario_registro",
    "fecha_respuesta",      # se llena sola cuando la PQRS pasa a "Solucionada"
)

CAMPOS_USUARIO = ("usuario", "nombre_completo", "correo_institucional",
                  "contrasena", "rol", "estado")

# Un archivo por tipo de solicitud
ARCHIVOS = {
    "Peticion": "Peticion.txt",
    "Queja": "Queja.txt",
    "Reclamo": "Reclamo.txt",
    "Sugerencia": "Sugerencia.txt",
}
ARCHIVO_USUARIOS = "Usuarios.txt"


def ruta_archivo(tipo):
    """Devuelve la ruta completa del archivo de un tipo de solicitud."""
    return os.path.join(DATA_DIR, ARCHIVOS[tipo])


def linea_a_diccionario(linea, campos):
    """Convierte una línea de texto en un diccionario {campo: valor}."""
    partes = linea.rstrip("\r\n").split(SEPARADOR)
    registro = {}
    posicion = 0
    for campo in campos:
        if posicion < len(partes):
            registro[campo] = partes[posicion]
        else:
            registro[campo] = ""
        posicion = posicion + 1
    return registro


def diccionario_a_linea(registro):
    """Convierte un diccionario en una línea de texto lista para guardar."""
    valores = []
    for campo in CAMPOS:
        valor = str(registro.get(campo, ""))
        # Por seguridad: el separador y los saltos de línea dañarían el archivo
        valor = valor.replace(SEPARADOR, "/").replace("\n", " ").replace("\r", " ")
        valores.append(valor)
    return SEPARADOR.join(valores)


def asegurar_archivo(tipo):
    """Si el archivo no existe, lo crea con su línea de encabezado."""
    ruta = ruta_archivo(tipo)
    if not os.path.exists(ruta):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(ruta, "w", encoding="utf-8", newline="\n") as archivo:
            archivo.write(SEPARADOR.join(CAMPOS) + "\n")


def leer_registros(tipo):
    """Lee todos los registros de un tipo. Devuelve una lista de diccionarios."""
    ruta = ruta_archivo(tipo)
    registros = []
    if not os.path.exists(ruta):
        return registros
    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    for linea in lineas[1:]:                 # [1:] salta el encabezado
        if linea.strip() != "":
            registros.append(linea_a_diccionario(linea, CAMPOS))
    return registros


def siguiente_id(tipo):
    """ID autoincremental: el mayor ID que existe en ese archivo + 1.
    Cada archivo tiene su propia secuencia, empezando en 1."""
    mayor = 0
    for registro in leer_registros(tipo):
        try:
            numero = int(registro["id"])
        except ValueError:
            continue                          # ignora líneas con ID dañado
        if numero > mayor:
            mayor = numero
    return mayor + 1


def migrar_encabezado(tipo):
    """Si el archivo tiene un encabezado viejo (sin el campo fecha_respuesta),
    lo reescribe con el encabezado actual. Los registros viejos quedan igual."""
    ruta = ruta_archivo(tipo)
    with open(ruta, "r", encoding="utf-8") as archivo:
        primera_linea = archivo.readline().rstrip("\r\n")
    if primera_linea != SEPARADOR.join(CAMPOS):
        reescribir_archivo(tipo, leer_registros(tipo))


def guardar_registro(tipo, registro):
    """Agrega un registro nuevo al final del archivo de su tipo."""
    asegurar_archivo(tipo)
    migrar_encabezado(tipo)
    ruta = ruta_archivo(tipo)
    # Si la última línea no termina en salto de línea, lo agregamos primero
    with open(ruta, "rb") as archivo:
        contenido = archivo.read()
    prefijo = ""
    if len(contenido) > 0 and not contenido.endswith(b"\n"):
        prefijo = "\n"
    with open(ruta, "a", encoding="utf-8", newline="\n") as archivo:
        archivo.write(prefijo + diccionario_a_linea(registro) + "\n")


def reescribir_archivo(tipo, registros):
    """Reemplaza todo el archivo con la lista de registros dada.
    Se usa cuando se cambia un dato (por ejemplo, el estado)."""
    ruta = ruta_archivo(tipo)
    temporal = ruta + ".tmp"
    with open(temporal, "w", encoding="utf-8", newline="\n") as archivo:
        archivo.write(SEPARADOR.join(CAMPOS) + "\n")
        for registro in registros:
            archivo.write(diccionario_a_linea(registro) + "\n")
    os.replace(temporal, ruta)                # reemplazo seguro


def buscar_registro(tipo, id_registro):
    """Busca un registro por su ID. Devuelve el diccionario o None."""
    for registro in leer_registros(tipo):
        if registro["id"] == str(id_registro):
            return registro
    return None


def actualizar_campo(tipo, id_registro, campo, valor):
    """Cambia un campo de un registro y guarda el archivo.
    Devuelve True si lo encontró y False si no existe ese ID."""
    registros = leer_registros(tipo)
    encontrado = False
    for registro in registros:
        if registro["id"] == str(id_registro):
            registro[campo] = valor
            encontrado = True
    if encontrado:
        reescribir_archivo(tipo, registros)
    return encontrado


def actualizar_campos(tipo, id_registro, cambios):
    """Igual que actualizar_campo, pero cambia varios campos a la vez.
    'cambios' es un diccionario {campo: valor_nuevo}."""
    registros = leer_registros(tipo)
    encontrado = False
    for registro in registros:
        if registro["id"] == str(id_registro):
            for campo in cambios:
                registro[campo] = cambios[campo]
            encontrado = True
    if encontrado:
        reescribir_archivo(tipo, registros)
    return encontrado


def leer_usuarios():
    """Lee Usuarios.txt. Devuelve una lista de diccionarios (para el login)."""
    ruta = os.path.join(DATA_DIR, ARCHIVO_USUARIOS)
    usuarios = []
    if not os.path.exists(ruta):
        return usuarios
    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    for linea in lineas[1:]:
        if linea.strip() != "":
            usuarios.append(linea_a_diccionario(linea, CAMPOS_USUARIO))
    return usuarios

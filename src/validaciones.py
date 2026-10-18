# ============================================================
# validaciones.py - Validación de los datos que escribe el usuario
# Proyecto: Patitas PQRS (Algoritmia y Programación 2026-2)
#
# Casi todas las funciones devuelven una tupla (es_valido, mensaje):
#   (True, "")                    -> el dato está bien
#   (False, "texto del error")    -> el dato está mal y dice por qué
# ============================================================
import datetime
import unicodedata

# Días que tiene el equipo para responder una PQRS.
DIAS_RESPUESTA = 15

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

# Listas de valores permitidos (tuplas: no cambian durante la ejecución)

TIPOS_DOCUMENTO = ("CC", "TI", "CE", "PP", "NIT")
TIPOS_TELEFONO = ("Celular", "Fijo", "Corporativo", "Otro")
TIPOS_SOLICITUD = ("Peticion", "Queja", "Reclamo", "Sugerencia")
CANALES = ("Presencial", "Correo electrónico", "Página web",
           "Teléfono", "Redes sociales", "Otro")
TIPOS_MASCOTA = ("Perro", "Gato", "Otro")
CAMPUS = (
    "Campus Medellín - Ciudad Universitaria",
    "Campus Medellín - Ciudadela Robledo",
    "Campus en el Área de la salud",
    "Campus Medellín - Sede de Posgrado",
    "Campus Medellín - Edificio San Ignacio",
    "Campus Medellín - Antigua Escuela de Derecho",
    "Campus Medellín - Edificio Antioquia",
    "Campus Medellín - Casas Patrimoniales",
    "Campus Medellín - Edificio de Extensión",
)
ESTADOS = ("Registrada", "En proceso", "Solucionada")

DIGITOS = "0123456789"
LETRAS_Y_NUMEROS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


# ------------------------------------------------------------
# Funciones de apoyo
# ------------------------------------------------------------
def solo_digitos(texto):
    """True si el texto tiene únicamente números (0-9)."""
    if texto == "":
        return False
    for caracter in texto:
        if caracter not in DIGITOS:
            return False
    return True


def quitar_tildes(texto):
    """'Petición' -> 'Peticion'. Sirve para comparar sin importar tildes."""
    normalizado = unicodedata.normalize("NFD", texto)
    resultado = ""
    for caracter in normalizado:
        if unicodedata.category(caracter) != "Mn":
            resultado = resultado + caracter
    return resultado


def buscar_opcion(valor, opciones):
    """Busca el valor en la tupla de opciones sin importar mayúsculas ni tildes.
    Devuelve la opción oficial (bien escrita) o None si no existe."""
    buscado = quitar_tildes(valor.strip()).lower()
    for opcion in opciones:
        if quitar_tildes(opcion).lower() == buscado:
            return opcion
    return None


def texto_seguro(texto):
    """El símbolo | y los saltos de línea dañarían el archivo plano."""
    return "|" not in texto and "\n" not in texto and "\r" not in texto


# ------------------------------------------------------------
# Validación numérica (try-except)
# ------------------------------------------------------------
def validar_entero(mensaje):
    """Pide un número entero y repite la pregunta hasta que sea válido."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero.")


def validar_float(mensaje):
    """Pide un número (puede tener decimales) y repite hasta que sea válido."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Debe ingresar un número (puede tener decimales).")


# ------------------------------------------------------------
# Datos del solicitante
# ------------------------------------------------------------
def validar_nombre(texto):
    texto = texto.strip()
    if texto == "":
        return False, "El nombre es obligatorio."
    if len(texto) < 3 or len(texto) > 100:
        return False, "El nombre debe tener entre 3 y 100 caracteres."
    for caracter in texto:
        if caracter in DIGITOS:
            return False, "El nombre no puede tener números."
        if not (caracter.isalpha() or caracter in " '-"):
            return False, "El nombre solo puede tener letras, espacios, apóstrofes (') o guiones (-)."
    return True, ""


def validar_opcion(valor, opciones, nombre_campo):
    """Sirve para tipo de documento, tipo de teléfono, canal, mascota, campus, etc."""
    if valor.strip() == "":
        return False, nombre_campo + " es obligatorio."
    if buscar_opcion(valor, opciones) is None:
        return False, nombre_campo + " no es válido. Opciones: " + ", ".join(opciones)
    return True, ""


def validar_numero_documento(texto):
    texto = texto.strip()
    if texto == "":
        return False, "El número de documento es obligatorio."
    if not solo_digitos(texto):
        return False, "El número de documento solo puede tener números (sin letras ni símbolos)."
    if len(texto) < 3 or len(texto) > 15:
        return False, "El número de documento debe tener entre 3 y 15 dígitos."
    return True, ""


def validar_telefono(texto):
    texto = texto.strip()
    if texto == "":
        return False, "El teléfono es obligatorio."
    if not solo_digitos(texto):
        return False, "El teléfono solo puede tener números."
    if len(texto) != 10:
        return False, "El teléfono debe tener exactamente 10 dígitos."
    return True, ""


def validar_correo(texto):
    texto = texto.strip()
    if texto == "":
        return False, "El correo es obligatorio."
    if len(texto) > 254:
        return False, "El correo puede tener máximo 254 caracteres."
    if " " in texto:
        return False, "El correo no puede tener espacios."
    if texto.count("@") != 1:
        return False, "El correo debe tener un único símbolo @ (ejemplo: usuario@correo.com)."
    usuario, dominio = texto.split("@")
    if usuario == "" or dominio == "":
        return False, "El correo debe tener texto antes y después del @."
    for caracter in usuario:
        if caracter not in LETRAS_Y_NUMEROS and caracter not in "._-+":
            return False, "El correo tiene caracteres no permitidos antes del @."
    if "." not in dominio:
        return False, "El dominio del correo debe tener un punto (ejemplo: correo.com)."
    partes = dominio.split(".")
    for parte in partes:
        if parte == "":
            return False, "El dominio del correo no es válido."
        for caracter in parte:
            if caracter not in LETRAS_Y_NUMEROS and caracter != "-":
                return False, "El dominio del correo tiene caracteres no permitidos."
    if len(partes[-1]) < 2:
        return False, "El final del dominio debe tener al menos 2 letras (.com, .co, .edu...)."
    return True, ""


def validar_direccion(texto):
    """La dirección es OPCIONAL: se acepta vacía."""
    texto = texto.strip()
    if texto == "":
        return True, ""
    if len(texto) < 5 or len(texto) > 200:
        return False, "La dirección debe tener entre 5 y 200 caracteres."
    for caracter in texto:
        if not (caracter.isalnum() or caracter in " #-./,"):
            return False, "La dirección solo puede tener letras, números y los símbolos # - . / ,"
    return True, ""


# ------------------------------------------------------------
# Información de la PQRS
# ------------------------------------------------------------
def validar_asunto(texto):
    texto = texto.strip()
    if texto == "":
        return False, "El asunto es obligatorio."
    if len(texto) < 5 or len(texto) > 150:
        return False, "El asunto debe tener entre 5 y 150 caracteres."
    if not texto_seguro(texto):
        return False, "El asunto no puede tener el símbolo | ni saltos de línea."
    return True, ""


def validar_descripcion(texto):
    texto = texto.strip()
    if texto == "":
        return False, "La descripción es obligatoria (no puede estar vacía ni tener solo espacios)."
    if len(texto) < 20:
        return False, "La descripción debe tener mínimo 20 caracteres."
    if len(texto) > 2000:
        return False, "La descripción puede tener máximo 2000 caracteres."
    if not texto_seguro(texto):
        return False, "La descripción no puede tener el símbolo | ni saltos de línea."
    return True, ""


# ------------------------------------------------------------
# Fechas
# ------------------------------------------------------------
def fecha_actual():
    """Fecha y hora de ahora, como texto (ejemplo: 2026-10-18 15:30:00)."""
    return datetime.datetime.now().strftime(FORMATO_FECHA)


def validar_fecha(texto):
    """La fecha debe tener el formato AAAA-MM-DD HH:MM:SS y no ser futura."""
    texto = texto.strip()
    if texto == "":
        return False, "La fecha es obligatoria."
    try:
        fecha = datetime.datetime.strptime(texto, FORMATO_FECHA)
    except ValueError:
        return False, "La fecha debe tener el formato AAAA-MM-DD HH:MM:SS."
    if fecha > datetime.datetime.now():
        return False, "La fecha no puede ser futura."
    return True, ""


def calcular_fecha_maxima(fecha_texto, dias=DIAS_RESPUESTA):
    """Fecha máxima de respuesta = fecha de radicación + días de plazo."""
    fecha = datetime.datetime.strptime(fecha_texto, FORMATO_FECHA)
    limite = fecha + datetime.timedelta(days=dias)
    return limite.strftime(FORMATO_FECHA)


# ------------------------------------------------------------
# Estado de la PQRS
# ------------------------------------------------------------
def validar_cambio_estado(estado_actual, estado_nuevo):
    """El estado solo puede avanzar así: Registrada -> En proceso -> Solucionada."""
    if estado_actual not in ESTADOS or estado_nuevo not in ESTADOS:
        return False, "Estado no válido."
    posicion_actual = ESTADOS.index(estado_actual)
    posicion_nueva = ESTADOS.index(estado_nuevo)
    if posicion_nueva != posicion_actual + 1:
        if estado_actual == "Solucionada":
            return False, "Esta PQRS ya está Solucionada, no puede cambiar de estado."
        return False, "El cambio debe seguir el flujo: Registrada -> En proceso -> Solucionada."
    return True, ""


# ------------------------------------------------------------
# Pedir datos al usuario (repite hasta que el dato sea válido)
# ------------------------------------------------------------
def pedir_dato(mensaje, funcion_validar):
    """Pregunta con input() y repite mientras la función de validación diga que no."""
    while True:
        texto = input(mensaje)
        es_valido, error = funcion_validar(texto)
        if es_valido:
            return texto.strip()
        print("  ->", error)


def pedir_opcion(titulo, opciones):
    """Muestra las opciones numeradas y devuelve la que eligió el usuario."""
    print(titulo)
    numero = 1
    for opcion in opciones:
        print("  " + str(numero) + ". " + opcion)
        numero = numero + 1
    while True:
        eleccion = validar_entero("Elija una opción: ")
        if eleccion >= 1 and eleccion <= len(opciones):
            return opciones[eleccion - 1]
        print("  -> Opción fuera de rango, elija entre 1 y " + str(len(opciones)) + ".")

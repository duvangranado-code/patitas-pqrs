# ======================================================================
# autenticacion.py - Login (control de acceso al sistema)
# Proyecto: Patitas PQRS (Algoritmia y Programación 2026-2)
#
# Reglas del enunciado:
#   - El login es obligatorio antes de ver el menú principal.
#   - Las credenciales se validan contra data/Usuarios.txt
#   - Máximo 3 intentos fallidos y luego la pantalla se bloquea
#     temporalmente (el tiempo se muestra en pantalla).
#   - Al entrar bien, se guarda el usuario activo para vincularlo
#     a cada PQRS que registre.
# ============================================================
import getpass
import time

import archivos

MAX_INTENTOS = 3
TIEMPO_BLOQUEO = 30          # segundos de bloqueo (el equipo puede cambiarlo)


def pedir_clave(mensaje):
    """Pide la clave sin mostrarla en pantalla. Si la consola no lo permite,
    usa input() normal."""
    try:
        return getpass.getpass(mensaje)
    except Exception:
        return input(mensaje)

def buscar_usuario(texto_usuario, clave):
    """Busca un usuario ACTIVO cuyo usuario (o correo institucional) y clave coincidan.
    Devuelve el diccionario del usuario o None."""
    for usuario in archivos.leer_usuarios():
        coincide_usuario = (usuario["usuario"] == texto_usuario or
                            usuario["correo_institucional"].lower() == texto_usuario.lower())
        if coincide_usuario and usuario["contrasena"] == clave and usuario["estado"] == "Activo":
            return usuario
    return None

def bloquear_pantalla(segundos):
    """Muestra una cuenta regresiva mientras el sistema está bloqueado."""
    print("\nDemasiados intentos fallidos. Sistema bloqueado por " + str(segundos) + " segundos.")
    restante = segundos
    while restante > 0:
        print("\r  Podrá intentar de nuevo en " + str(restante) + " s  ", end="", flush=True)
        time.sleep(1)
        restante = restante - 1
    print("\r  Ya puede intentar de nuevo.            ")

def iniciar_sesion():
    """Pide las credenciales. Devuelve el usuario que inició sesión,
    o None si la persona decide cancelar."""
    print("\nPor favor ingrese sus credenciales")
    print("(escriba CANCELAR como usuario para salir)")
    intentos = 0
    while True:
        texto_usuario = input("    1. Ingrese Usuario : ").strip()
        if texto_usuario.upper() == "CANCELAR":
            return None
        clave = pedir_clave("    2. Ingrese Clave   : ")

        usuario = buscar_usuario(texto_usuario, clave)
        if usuario is not None:
            print("\nBienvenido, " + usuario["nombre_completo"] + " (" + usuario["rol"] + ")")
            return usuario

        intentos = intentos + 1
        if intentos >= MAX_INTENTOS:
            bloquear_pantalla(TIEMPO_BLOQUEO)
            intentos = 0
        else:
            faltan = MAX_INTENTOS - intentos
            print("  -> Usuario o clave incorrectos, o usuario inactivo. Intentos restantes: " + str(faltan))

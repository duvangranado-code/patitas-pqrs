# ============================================================
# radicado.py - Comprobante de radicado en texto ASCII
# Proyecto: Patitas PQRS (Algoritmia y Programación 2026-2)
#
# Reglas del enunciado:
#   - Texto ASCII delimitado por un marco (+ - |)
#   - Cada línea mide EXACTAMENTE 120 caracteres
#   - Secciones centradas, sin la descripción detallada
#   - Si la dirección no se ingresó, se muestra "N/A"
# ============================================================
import os
import textwrap

import archivos
import validaciones as val

ANCHO = 120                    # ancho total de cada línea
INTERIOR = ANCHO - 4           # espacio para el texto entre "| " y " |"

PREFIJOS = {"Peticion": "PET", "Queja": "QUE", "Reclamo": "REC", "Sugerencia": "SUG"}


def a_ascii(texto):
    """Quita tildes y deja solo caracteres ASCII (ñ -> n, á -> a)."""
    sin_tildes = val.quitar_tildes(texto)
    return sin_tildes.encode("ascii", "ignore").decode("ascii")


def codigo_radicado(registro):
    """Número de radicado formateado, por ejemplo PET-000123."""
    prefijo = PREFIJOS[registro["tipo_solicitud"]]
    return prefijo + "-" + str(registro["id"]).zfill(6)


# ------------------------------------------------------------
# Piezas del marco (todas miden exactamente 120 caracteres)
# ------------------------------------------------------------
def borde():
    return "+" + "-" * (ANCHO - 2) + "+"


def linea(texto):
    texto = a_ascii(texto)
    if len(texto) > INTERIOR:
        texto = texto[:INTERIOR - 3] + "..."
    return "| " + texto.ljust(INTERIOR) + " |"


def centrada(texto):
    texto = a_ascii(texto)
    return "|" + texto.center(ANCHO - 2) + "|"


def titulo_seccion(texto):
    return "|" + (" " + a_ascii(texto) + " ").center(ANCHO - 2, "=") + "|"


def campo(etiqueta, valor):
    """Una línea 'Etiqueta: valor'. Si el valor está vacío muestra N/A."""
    if valor.strip() == "":
        valor = "N/A"
    return linea(etiqueta + ": " + valor)


# ------------------------------------------------------------
# Construcción del radicado
# ------------------------------------------------------------
def construir_radicado(registro):
    """Devuelve la lista de líneas del radicado (cada una de 120 caracteres)."""
    lineas = []
    lineas.append(borde())
    lineas.append(centrada("PATITAS PQRS"))
    lineas.append(centrada("COMPROBANTE DE RADICADO"))
    lineas.append(centrada("Universidad de Antioquia - Atencion de perros y gatos"))

    lineas.append(titulo_seccion("DATOS DEL RADICADO"))
    lineas.append(campo("Radicado No.", codigo_radicado(registro)))
    lineas.append(campo("Fecha y hora de radicacion", registro["fecha_radicacion"]))
    lineas.append(campo("Estado", registro["estado_peticion"]))
    lineas.append(campo("Fecha maxima de respuesta", registro["fecha_maxima_respuesta"]))
    lineas.append(campo("Registrado por", registro["usuario_registro"]))

    lineas.append(titulo_seccion("DATOS DEL SOLICITANTE"))
    lineas.append(campo("Nombre completo", registro["nombre_completo"]))
    lineas.append(campo("Documento", registro["tipo_documento"] + " " + registro["numero_documento"]))
    lineas.append(campo("Telefono", registro["telefono_contacto"] + " (" + registro["tipo_telefono"] + ")"))
    lineas.append(campo("Correo electronico", registro["correo_electronico"]))
    lineas.append(campo("Direccion", registro["direccion"]))

    lineas.append(titulo_seccion("CLASIFICACION"))
    lineas.append(campo("Tipo de solicitud", registro["tipo_solicitud"]))
    lineas.append(campo("Canal de recepcion", registro["canal_recepcion"]))
    lineas.append(campo("Tipo de mascota", registro["tipo_mascota"]))
    lineas.append(campo("Campus", registro["campus_relacionado"]))

    lineas.append(titulo_seccion("RESUMEN"))
    # El asunto puede ser largo: se parte en varias líneas
    partes = textwrap.wrap(a_ascii(registro["asunto_titulo"]), 100)
    if len(partes) == 0:
        partes = ["N/A"]
    primera = True
    for parte in partes:
        if primera:
            lineas.append(linea("Asunto: " + parte))
            primera = False
        else:
            lineas.append(linea("        " + parte))

    lineas.append(borde())
    return lineas


def imprimir_radicado(registro):
    print("")
    for texto in construir_radicado(registro):
        print(texto)


def guardar_radicado(registro):
    """Guarda el radicado en data/radicados/PET-000123.txt y devuelve la ruta."""
    carpeta = os.path.join(archivos.DATA_DIR, "radicados")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, codigo_radicado(registro) + ".txt")
    with open(ruta, "w", encoding="ascii", newline="\n") as archivo:
        archivo.write("\n".join(construir_radicado(registro)) + "\n")
    return ruta

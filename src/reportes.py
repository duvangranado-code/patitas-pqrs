# ======================================================================================
# reportes.py - Estadísticas de las PQRS
# Proyecto: Patitas PQRS (Algoritmia y Programación 2026-2)
#
# Estadísticas:
#   0. Promedio de días de respuesta (obligatoria, en valores enteros)
#   1. Distribución por tipo de mascota (perro vs gato)
#   2. Proporción por canal de recepción
#   3. Distribución por campus
#   4. Efectividad y resolución por estado
#   5. Alerta de vencimiento (próximas a vencer y vencidas)
# Cada función devuelve una lista de líneas de texto, así sirven tanto
# para mostrar en pantalla como para exportar a un archivo.
# ============================================================
import csv
import datetime
import os

import archivos
import validaciones as val

DIAS_ALERTA = 5          # "próxima a vencer" = faltan 5 días o menos

# ------------------------------------------------------------
# Funciones de apoyo
# ------------------------------------------------------------
def cargar_todos():
    """Junta los registros de los 4 archivos en una sola lista."""
    todos = []
    for tipo in archivos.ARCHIVOS:
        for registro in archivos.leer_registros(tipo):
            todos.append(registro)
    return todos

def a_fecha(texto):
    """Convierte un texto en fecha. Devuelve None si el texto no es una fecha válida."""
    try:
        return datetime.datetime.strptime(texto, val.FORMATO_FECHA)
    except ValueError:
        return None

def contar(registros, campo):
    """Cuenta cuántas veces aparece cada valor de un campo: {valor: cantidad}."""
    conteo = {}
    for registro in registros:
        valor = registro[campo]
        if valor in conteo:
            conteo[valor] = conteo[valor] + 1
        else:
            conteo[valor] = 1
    return conteo

def porcentaje(parte, total):
    if total == 0:
        return 0.0
    return parte * 100 / total

def por_cantidad(par):
    """Sirve para ordenar de mayor a menor cantidad."""
    return par[1]

def lineas_de_conteo(titulo, conteo, total):
    lineas = [titulo]
    for valor, cantidad in sorted(conteo.items(), key=por_cantidad, reverse=True):
        lineas.append("  " + valor.ljust(48) + str(cantidad).rjust(6) + "  (" + format(porcentaje(cantidad, total), ".1f") + "%)")
    lineas.append("  " + "TOTAL".ljust(48) + str(total).rjust(6))
    return lineas

# ------------------------------------------------------------
# Las estadísticas
# ------------------------------------------------------------
def promedio_dias_respuesta(registros):
    """Promedio (entero) de días entre la radicación y la respuesta,
    solo de las PQRS Solucionadas que tienen fecha de respuesta."""
    suma_dias = 0
    cantidad = 0
    for registro in registros:
        if registro["estado_peticion"] == "Solucionada":
            radicacion = a_fecha(registro["fecha_radicacion"])
            respuesta = a_fecha(registro["fecha_respuesta"])
            if radicacion is not None and respuesta is not None:
                suma_dias = suma_dias + (respuesta - radicacion).days
                cantidad = cantidad + 1
    if cantidad == 0:
        return None, 0
    return int(suma_dias / cantidad + 0.5), cantidad

def estadistica_promedio(registros):
    promedio, cantidad = promedio_dias_respuesta(registros)
    lineas = ["PROMEDIO DE DIAS PARA RESPONDER UNA PQRS"]
    if promedio is None:
        lineas.append("  Aún no hay PQRS solucionadas con fecha de respuesta registrada.")
    else:
        lineas.append("  Promedio: " + str(promedio) + " días (calculado con " + str(cantidad) + " PQRS solucionadas)")
    return lineas

def estadistica_mascota(registros):
    return lineas_de_conteo("DISTRIBUCION POR TIPO DE MASCOTA", contar(registros, "tipo_mascota"), len(registros))

def estadistica_canal(registros):
    return lineas_de_conteo("PROPORCION POR CANAL DE RECEPCION", contar(registros, "canal_recepcion"), len(registros))

def estadistica_campus(registros):
    return lineas_de_conteo("DISTRIBUCION POR CAMPUS", contar(registros, "campus_relacionado"), len(registros))

def estadistica_efectividad(registros):
    conteo = contar(registros, "estado_peticion")
    total = len(registros)
    lineas = lineas_de_conteo("EFECTIVIDAD Y RESOLUCION POR ESTADO", conteo, total)
    solucionadas = 0
    if "Solucionada" in conteo:
        solucionadas = conteo["Solucionada"]
    lineas.append("  Tasa de efectividad (Solucionadas / total): " + format(porcentaje(solucionadas, total), ".1f") + "%")
    return lineas

def por_fecha_radicacion(par):
    return par[0]

def estadistica_vencimiento(registros, ahora=None):
    """Cuenta las PQRS activas (no solucionadas) que ya vencieron o están por vencer
    y muestra las 5 más antiguas."""
    if ahora is None:
        ahora = datetime.datetime.now()
    activas = 0
    vencidas = 0
    proximas = 0
    antiguas = []                              # pares (fecha_radicacion, texto)
    for registro in registros:
        if registro["estado_peticion"] == "Solucionada":
            continue
        activas = activas + 1
        limite = a_fecha(registro["fecha_maxima_respuesta"])
        radicacion = a_fecha(registro["fecha_radicacion"])
        if limite is not None:
            if limite < ahora:
                vencidas = vencidas + 1
            elif (limite - ahora).days <= DIAS_ALERTA:
                proximas = proximas + 1
        if radicacion is not None:
            texto = (registro["tipo_solicitud"] + " #" + registro["id"] + " - radicada el " +
                     registro["fecha_radicacion"] + " - " + registro["estado_peticion"])
            antiguas.append((radicacion, texto))

    lineas = ["ALERTA DE VENCIMIENTO Y PLAZO LEGAL (" + str(val.DIAS_RESPUESTA) + " días de plazo)"]
    lineas.append("  PQRS activas (Registrada o En proceso): " + str(activas))
    lineas.append("  Vencidas (superaron el plazo)         : " + str(vencidas) + "  (" + format(porcentaje(vencidas, activas), ".1f") + "% de las activas)")
    lineas.append("  Próximas a vencer (" + str(DIAS_ALERTA) + " días o menos)     : " + str(proximas) + "  (" + format(porcentaje(proximas, activas), ".1f") + "% de las activas)")
    lineas.append("  Las 5 PQRS activas más antiguas:")
    antiguas.sort(key=por_fecha_radicacion)
    for fecha, texto in antiguas[:5]:
        lineas.append("    - " + texto)
    return lineas

def todas_las_estadisticas():
    registros = cargar_todos()
    lineas = ["=" * 70, "ESTADISTICAS PATITAS PQRS  (" + str(len(registros)) + " registros)", "=" * 70]
    funciones = (estadistica_promedio, estadistica_mascota, estadistica_canal,
                 estadistica_campus, estadistica_efectividad, estadistica_vencimiento)
    for funcion in funciones:
        lineas.append("")
        lineas = lineas + funcion(registros)
    return lineas

# ------------------------------------------------------------
# Exportar a archivos planos
# ------------------------------------------------------------
def exportar_resumen():
    """Guarda todas las estadísticas en data/resumen_estadisticas.txt"""
    ruta = os.path.join(archivos.DATA_DIR, "resumen_estadisticas.txt")
    with open(ruta, "w", encoding="utf-8", newline="\n") as archivo:
        archivo.write("\n".join(todas_las_estadisticas()) + "\n")
    return ruta

def exportar_consolidado():
    """Junta las 4 solicitudes en un solo archivo data/consolidado_pqrs.csv
    (base de datos para el tablero de Power BI)."""
    ruta = os.path.join(archivos.DATA_DIR, "consolidado_pqrs.csv")
    registros = cargar_todos()
    with open(ruta, "w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(archivos.CAMPOS)
        for registro in registros:
            fila = []
            for campo in archivos.CAMPOS:
                fila.append(registro[campo])
            escritor.writerow(fila)
    return ruta, len(registros)

# ------------------------------------------------------------
# Menú de estadísticas
# ------------------------------------------------------------
def menu_estadisticas():
    opcion = 0
    while opcion != 9:
        print("\n----- ESTADISTICAS -----")
        print("1. Promedio de días de respuesta")
        print("2. Distribución por tipo de mascota")
        print("3. Proporción por canal de recepción")
        print("4. Distribución por campus")
        print("5. Efectividad por estado")
        print("6. Alerta de vencimiento")
        print("7. Ver todas")
        print("8. Exportar (resumen .txt y consolidado .csv para Power BI)")
        print("9. Volver al menú principal")
        opcion = val.validar_entero("Elija una opción: ")

        registros = cargar_todos()
        if opcion == 1:
            mostrar(estadistica_promedio(registros))
        elif opcion == 2:
            mostrar(estadistica_mascota(registros))
        elif opcion == 3:
            mostrar(estadistica_canal(registros))
        elif opcion == 4:
            mostrar(estadistica_campus(registros))
        elif opcion == 5:
            mostrar(estadistica_efectividad(registros))
        elif opcion == 6:
            mostrar(estadistica_vencimiento(registros))
        elif opcion == 7:
            mostrar(todas_las_estadisticas())
        elif opcion == 8:
            ruta_resumen = exportar_resumen()
            ruta_csv, cantidad = exportar_consolidado()
            print("Resumen guardado en: " + ruta_resumen)
            print("Consolidado (" + str(cantidad) + " registros) guardado en: " + ruta_csv)
        elif opcion == 9:
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida. Elija un número entre 1 y 9.")


def mostrar(lineas):
    print("")
    for texto in lineas:
        print(texto)

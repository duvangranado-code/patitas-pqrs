# ======================================================================================
# reportes.py - Estadísticas de las PQRS (con pandas y numpy)
# Proyecto: Patitas PQRS (Algoritmia y Programación 2026-2)
#
# Estadísticas:
#   1. Promedio de días de respuesta (obligatoria, en valores enteros)
#   2. Distribución por tipo de mascota (perro vs gato)
#   3. Proporción por canal de recepción
#   4. Distribución por campus
#   5. Efectividad y resolución por estado
#   6. Alerta de vencimiento (próximas a vencer y vencidas)
#   7. Perfil del solicitante (Interno / Externo) y PQRS por usuario y perfil del sistema
# Los datos se leen de los 4 archivos como una tabla (DataFrame de pandas).
# Cada función devuelve una lista de líneas de texto, así sirven tanto
# para mostrar en pantalla como para exportar a un archivo.
# ============================================================
import datetime
import os

import numpy as np
import pandas as pd

import archivos
import validaciones as val

DIAS_ALERTA = 5          # "próxima a vencer" = faltan 5 días o menos

# ------------------------------------------------------------
# Funciones de apoyo
# ------------------------------------------------------------
def cargar_todos():
    """Junta los 4 archivos en una sola tabla (DataFrame)."""
    return archivos.leer_todas_las_tablas()

def a_fechas(columna):
    """Convierte una columna de texto en fechas. Si un texto no es fecha, queda vacío (NaT)."""
    return pd.to_datetime(columna, format=val.FORMATO_FECHA, errors="coerce")

def con_perfil_usuario(tabla):
    """Cruza (merge) las PQRS con Usuarios.txt para saber el perfil de quien registró cada una.
    El dato en común es usuario_registro (en las PQRS) = usuario (en Usuarios.txt)."""
    usuarios = archivos.leer_tabla_usuarios()[["usuario", "perfil"]]
    unida = tabla.merge(usuarios, how="left", left_on="usuario_registro", right_on="usuario")
    unida["perfil_usuario"] = unida["perfil"].fillna("Sin perfil")
    return unida.drop(columns=["usuario", "perfil"])

def porcentaje(parte, total):
    if total == 0:
        return 0.0
    return parte * 100 / total

def lineas_de_conteo(titulo, conteo, total):
    """'conteo' es el resultado de value_counts(): cuántas veces aparece cada valor
    (ya viene ordenado de mayor a menor)."""
    lineas = [titulo]
    for valor, cantidad in conteo.items():
        lineas.append("  " + str(valor).ljust(48) + str(cantidad).rjust(6) + "  (" + format(porcentaje(cantidad, total), ".1f") + "%)")
    lineas.append("  " + "TOTAL".ljust(48) + str(total).rjust(6))
    return lineas

# ------------------------------------------------------------
# Las estadísticas
# ------------------------------------------------------------
def promedio_dias_respuesta(tabla):
    """Promedio (entero) de días entre la radicación y la respuesta,
    solo de las PQRS Solucionadas que tienen fecha de respuesta."""
    solucionadas = tabla[tabla["estado_peticion"] == "Solucionada"]
    radicacion = a_fechas(solucionadas["fecha_radicacion"])
    respuesta = a_fechas(solucionadas["fecha_respuesta"])
    dias = (respuesta - radicacion).dt.days          # resta de fechas, en días
    dias = dias.dropna()                             # quita las que no tienen fecha de respuesta
    if len(dias) == 0:
        return None, 0
    promedio = int(np.floor(np.mean(dias) + 0.5))    # promedio redondeado a entero
    return promedio, len(dias)

def estadistica_promedio(tabla):
    promedio, cantidad = promedio_dias_respuesta(tabla)
    lineas = ["PROMEDIO DE DIAS PARA RESPONDER UNA PQRS"]
    if promedio is None:
        lineas.append("  Aún no hay PQRS solucionadas con fecha de respuesta registrada.")
    else:
        lineas.append("  Promedio: " + str(promedio) + " días (calculado con " + str(cantidad) + " PQRS solucionadas)")
    return lineas

def estadistica_mascota(tabla):
    return lineas_de_conteo("DISTRIBUCION POR TIPO DE MASCOTA", tabla["tipo_mascota"].value_counts(), len(tabla))

def estadistica_canal(tabla):
    return lineas_de_conteo("PROPORCION POR CANAL DE RECEPCION", tabla["canal_recepcion"].value_counts(), len(tabla))

def estadistica_campus(tabla):
    return lineas_de_conteo("DISTRIBUCION POR CAMPUS", tabla["campus_relacionado"].value_counts(), len(tabla))

def estadistica_efectividad(tabla):
    conteo = tabla["estado_peticion"].value_counts()
    total = len(tabla)
    lineas = lineas_de_conteo("EFECTIVIDAD Y RESOLUCION POR ESTADO", conteo, total)
    solucionadas = conteo.get("Solucionada", 0)
    lineas.append("  Tasa de efectividad (Solucionadas / total): " + format(porcentaje(solucionadas, total), ".1f") + "%")
    return lineas

def estadistica_vencimiento(tabla, ahora=None):
    """Cuenta las PQRS activas (no solucionadas) que ya vencieron o están por vencer
    y muestra las 5 más antiguas."""
    if ahora is None:
        ahora = datetime.datetime.now()
    activas = tabla[tabla["estado_peticion"] != "Solucionada"].copy()
    limite = a_fechas(activas["fecha_maxima_respuesta"])
    activas["radicacion"] = a_fechas(activas["fecha_radicacion"])

    cantidad_activas = len(activas)
    vencidas = int((limite < ahora).sum())                         # ya pasó el plazo
    faltan = (limite - ahora).dt.days                              # días que faltan
    proximas = int(((limite >= ahora) & (faltan <= DIAS_ALERTA)).sum())

    lineas = ["ALERTA DE VENCIMIENTO Y PLAZO LEGAL (" + str(val.DIAS_RESPUESTA) + " días de plazo)"]
    lineas.append("  PQRS activas (Registrada o En proceso): " + str(cantidad_activas))
    lineas.append("  Vencidas (superaron el plazo)         : " + str(vencidas) + "  (" + format(porcentaje(vencidas, cantidad_activas), ".1f") + "% de las activas)")
    lineas.append("  Próximas a vencer (" + str(DIAS_ALERTA) + " días o menos)     : " + str(proximas) + "  (" + format(porcentaje(proximas, cantidad_activas), ".1f") + "% de las activas)")
    lineas.append("  Las 5 PQRS activas más antiguas:")
    antiguas = activas.dropna(subset=["radicacion"]).sort_values("radicacion", kind="stable").head(5)
    for _, fila in antiguas.iterrows():
        lineas.append("    - " + fila["tipo_solicitud"] + " #" + fila["id"] + " - radicada el " +
                      fila["fecha_radicacion"] + " - " + fila["estado_peticion"])
    return lineas

def estadistica_perfil(tabla):
    """Quién presenta las PQRS (Interno = correo @udea.edu.co, Externo = otro correo)
    y cuántas PQRS registró cada usuario del sistema, también agrupadas por su perfil."""
    total = len(tabla)
    lineas = lineas_de_conteo("PERFIL DEL SOLICITANTE (Interno = correo @udea.edu.co)", tabla["tipo_usuario"].value_counts(), total)
    lineas.append("")
    lineas = lineas + lineas_de_conteo("PQRS REGISTRADAS POR CADA USUARIO DEL SISTEMA", tabla["usuario_registro"].value_counts(), total)
    lineas.append("")
    unida = con_perfil_usuario(tabla)
    lineas = lineas + lineas_de_conteo("PQRS REGISTRADAS SEGUN EL PERFIL DEL USUARIO (Usuarios.txt)", unida["perfil_usuario"].value_counts(), total)
    return lineas

def todas_las_estadisticas():
    tabla = cargar_todos()
    lineas = ["=" * 70, "ESTADISTICAS PATITAS PQRS  (" + str(len(tabla)) + " registros)", "=" * 70]
    funciones = (estadistica_promedio, estadistica_mascota, estadistica_canal,
                 estadistica_campus, estadistica_efectividad, estadistica_vencimiento,
                 estadistica_perfil)
    for funcion in funciones:
        lineas.append("")
        lineas = lineas + funcion(tabla)
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
    tabla = con_perfil_usuario(cargar_todos())               # agrega la columna perfil_usuario
    tabla.to_csv(ruta, index=False, encoding="utf-8-sig")    # utf-8-sig para que Power BI lea las tildes
    return ruta, len(tabla)

# ------------------------------------------------------------
# Menú de estadísticas
# ------------------------------------------------------------
def menu_estadisticas():
    opcion = 0
    while opcion != 10:
        print("\n----- ESTADISTICAS -----")
        print("1. Promedio de días de respuesta")
        print("2. Distribución por tipo de mascota")
        print("3. Proporción por canal de recepción")
        print("4. Distribución por campus")
        print("5. Efectividad por estado")
        print("6. Alerta de vencimiento")
        print("7. Perfil del solicitante (Interno / Externo)")
        print("8. Ver todas")
        print("9. Exportar (resumen .txt y consolidado .csv para Power BI)")
        print("10. Volver al menú principal")
        opcion = val.validar_entero("Elija una opción: ")

        tabla = cargar_todos()
        if opcion == 1:
            mostrar(estadistica_promedio(tabla))
        elif opcion == 2:
            mostrar(estadistica_mascota(tabla))
        elif opcion == 3:
            mostrar(estadistica_canal(tabla))
        elif opcion == 4:
            mostrar(estadistica_campus(tabla))
        elif opcion == 5:
            mostrar(estadistica_efectividad(tabla))
        elif opcion == 6:
            mostrar(estadistica_vencimiento(tabla))
        elif opcion == 7:
            mostrar(estadistica_perfil(tabla))
        elif opcion == 8:
            mostrar(todas_las_estadisticas())
        elif opcion == 9:
            ruta_resumen = exportar_resumen()
            ruta_csv, cantidad = exportar_consolidado()
            print("Resumen guardado en: " + ruta_resumen)
            print("Consolidado (" + str(cantidad) + " registros) guardado en: " + ruta_csv)
        elif opcion == 10:
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida. Elija un número entre 1 y 10.")


def mostrar(lineas):
    print("")
    for texto in lineas:
        print(texto)

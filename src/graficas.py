# ======================================================================================
# graficas.py - Gráficos de las PQRS (con pandas y matplotlib)
# Proyecto: Patitas PQRS (Algoritmia y Programación 2026-2)
#
# Gráficos:
#   1. PQRS por tipo de solicitud (barras)
#   2. PQRS por estado (barras horizontales)
#   3. PQRS radicadas por mes (línea)
#   4. PQRS por tipo de mascota (pastel)
#   5. PQRS por canal de recepción (barras)
#   6. Promedio de días de respuesta por tipo de solicitud (barras)
#
# Cada gráfico se dibuja en un 'ax' (el gráfico) dentro de una 'fig' (la hoja).
# Los gráficos se guardan en PNG y en PDF dentro de la carpeta graficos/.
# ======================================================================================
import os

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

import archivos
import validaciones as val

CARPETA_GRAFICOS = os.path.join(os.path.dirname(archivos.CARPETA_SRC), "graficos")
CARPETA_PNG = os.path.join(CARPETA_GRAFICOS, "png")
CARPETA_PDF = os.path.join(CARPETA_GRAFICOS, "pdf")

# ------------------------------------------------------------
# Funciones de apoyo
# ------------------------------------------------------------
def cargar_tabla():
    """Junta los 4 archivos en una sola tabla y convierte las fechas."""
    tabla = archivos.leer_todas_las_tablas()
    tabla["fecha_radicacion"] = pd.to_datetime(tabla["fecha_radicacion"], format=val.FORMATO_FECHA, errors="coerce")
    tabla["fecha_respuesta"] = pd.to_datetime(tabla["fecha_respuesta"], format=val.FORMATO_FECHA, errors="coerce")
    return tabla

def guardar_grafico(fig, nombre):
    """Guarda la figura en PNG y en PDF (cada una en su carpeta)."""
    os.makedirs(CARPETA_PNG, exist_ok=True)
    os.makedirs(CARPETA_PDF, exist_ok=True)
    fig.savefig(os.path.join(CARPETA_PNG, nombre + ".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(CARPETA_PDF, nombre + ".pdf"), bbox_inches="tight")

# ------------------------------------------------------------
# Los 6 gráficos: cada función recibe la tabla y el 'ax' donde dibuja
# ------------------------------------------------------------
def grafico_por_tipo(tabla, ax):
    conteo = tabla["tipo_solicitud"].value_counts()
    barras = ax.bar(conteo.index, conteo.values, color="tab:blue")
    ax.bar_label(barras)
    ax.set_title("PQRS por tipo de solicitud", fontweight="bold")
    ax.set_xlabel("Tipo de solicitud")
    ax.set_ylabel("Cantidad de PQRS")

def grafico_por_estado(tabla, ax):
    conteo = tabla["estado_peticion"].value_counts()
    barras = ax.barh(conteo.index, conteo.values, color="tab:green")
    ax.bar_label(barras)
    ax.margins(x=0.12)
    ax.set_title("PQRS por estado", fontweight="bold")
    ax.set_xlabel("Cantidad de PQRS")
    ax.set_ylabel("Estado")

def grafico_por_mes(tabla, ax):
    meses = tabla["fecha_radicacion"].dt.strftime("%Y-%m")       # año-mes de cada PQRS
    conteo = meses.value_counts().sort_index()                   # se ordena por mes
    ax.plot(conteo.index, conteo.values, marker="o", color="tab:red")
    ax.set_title("PQRS radicadas por mes", fontweight="bold")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Cantidad de PQRS")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True)

def grafico_por_mascota(tabla, ax):
    conteo = tabla["tipo_mascota"].value_counts()
    ax.pie(conteo.values, labels=conteo.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("PQRS por tipo de mascota", fontweight="bold")

def grafico_por_canal(tabla, ax):
    conteo = tabla["canal_recepcion"].value_counts()
    barras = ax.bar(conteo.index, conteo.values, color="tab:orange")
    ax.bar_label(barras)
    ax.set_title("PQRS por canal de recepción", fontweight="bold")
    ax.set_xlabel("Canal")
    ax.set_ylabel("Cantidad de PQRS")
    ax.tick_params(axis="x", rotation=20)

def grafico_dias_respuesta(tabla, ax):
    resueltas = tabla.dropna(subset=["fecha_radicacion", "fecha_respuesta"]).copy()
    resueltas["dias"] = (resueltas["fecha_respuesta"] - resueltas["fecha_radicacion"]).dt.days
    promedio = resueltas.groupby("tipo_solicitud")["dias"].mean().round(0)
    barras = ax.bar(promedio.index, promedio.values, color="tab:purple")
    ax.bar_label(barras)
    ax.axhline(val.DIAS_RESPUESTA, color="gray", linestyle="--")   # línea del plazo de 15 días
    ax.set_title("Promedio de días de respuesta (plazo: " + str(val.DIAS_RESPUESTA) + " días)", fontweight="bold")
    ax.set_xlabel("Tipo de solicitud")
    ax.set_ylabel("Días")

# (nombre del archivo, función que dibuja)
GRAFICOS = (
    ("grafico_1_pqrs_por_tipo", grafico_por_tipo),
    ("grafico_2_pqrs_por_estado", grafico_por_estado),
    ("grafico_3_pqrs_por_mes", grafico_por_mes),
    ("grafico_4_pqrs_por_mascota", grafico_por_mascota),
    ("grafico_5_pqrs_por_canal", grafico_por_canal),
    ("grafico_6_dias_respuesta", grafico_dias_respuesta),
)

# ------------------------------------------------------------
# Generar todos los gráficos
# ------------------------------------------------------------
def generar_graficos(mostrar=False):
    """Crea los 6 gráficos por separado y una figura con los 6 juntos (3 filas x 2 columnas).
    Todo se guarda en graficos/png y graficos/pdf. Devuelve la lista de nombres creados."""
    tabla = cargar_tabla()
    if len(tabla) == 0:
        return []
    creados = []

    # Cada gráfico en su propia figura
    for nombre, funcion in GRAFICOS:
        fig, ax = plt.subplots(figsize=(8, 5))
        funcion(tabla, ax)
        fig.tight_layout()
        guardar_grafico(fig, nombre)
        plt.close(fig)
        creados.append(nombre)

    # Los 6 juntos en una sola figura
    fig, axs = plt.subplots(3, 2, figsize=(14, 15))
    fig.suptitle("Patitas PQRS - Resumen de gráficos (" + str(len(tabla)) + " PQRS)",
                 fontsize=16, fontweight="bold")
    posiciones = ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1))
    for numero in range(len(GRAFICOS)):
        fila, columna = posiciones[numero]
        GRAFICOS[numero][1](tabla, axs[fila, columna])
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    guardar_grafico(fig, "resumen_graficos")
    creados.append("resumen_graficos")
    if mostrar:
        plt.show()
    plt.close(fig)
    return creados

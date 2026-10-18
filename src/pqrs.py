# ============================================================
# pqrs.py - Registrar, consultar y cambiar el estado de las PQRS
# Proyecto: Patitas PQRS (Algoritmia y Programación 2026-2)
# ============================================================
import archivos
import radicado
import validaciones as val

# Nombre bonito de cada campo (para mostrar en pantalla)
ETIQUETAS = (
    ("id", "ID"),
    ("tipo_solicitud", "Tipo de solicitud"),
    ("estado_peticion", "Estado"),
    ("fecha_radicacion", "Fecha de radicación"),
    ("fecha_maxima_respuesta", "Fecha máxima de respuesta"),
    ("nombre_completo", "Nombre completo"),
    ("tipo_documento", "Tipo de documento"),
    ("numero_documento", "Número de documento"),
    ("tipo_telefono", "Tipo de teléfono"),
    ("telefono_contacto", "Teléfono de contacto"),
    ("correo_electronico", "Correo electrónico"),
    ("direccion", "Dirección"),
    ("canal_recepcion", "Canal de recepción"),
    ("asunto_titulo", "Asunto"),
    ("descripcion_detallada", "Descripción"),
    ("tipo_mascota", "Tipo de mascota"),
    ("campus_relacionado", "Campus"),
    ("usuario_registro", "Registrado por"),
    ("fecha_respuesta", "Fecha de respuesta"),
)


def mostrar_registro(registro):
    """Imprime todos los datos de un registro, uno por línea."""
    print("-" * 60)
    for campo, etiqueta in ETIQUETAS:
        valor = registro.get(campo, "")
        if valor == "":
            valor = "N/A"
        print(etiqueta + ": " + valor)
    print("-" * 60)


def elegir_tipo(titulo):
    """Pregunta qué tipo de solicitud y devuelve 'Peticion', 'Queja', etc."""
    return val.pedir_opcion(titulo, val.TIPOS_SOLICITUD)


# ------------------------------------------------------------
# 1. Registrar PQRS
# ------------------------------------------------------------
def registrar_pqrs(usuario_activo):
    print("\n--- Registrar PQRS ---")
    tipo = elegir_tipo("Tipo de solicitud:")

    print("\nDatos del solicitante")
    nombre = val.pedir_dato("Nombre completo: ", val.validar_nombre)
    tipo_documento = val.pedir_opcion("Tipo de documento:", val.TIPOS_DOCUMENTO)
    numero_documento = val.pedir_dato("Número de documento (3 a 15 dígitos): ", val.validar_numero_documento)
    tipo_telefono = val.pedir_opcion("Tipo de teléfono:", val.TIPOS_TELEFONO)
    telefono = val.pedir_dato("Teléfono de contacto (10 dígitos): ", val.validar_telefono)
    correo = val.pedir_dato("Correo electrónico: ", val.validar_correo)
    direccion = val.pedir_dato("Dirección (opcional, Enter para omitir): ", val.validar_direccion)

    print("\nInformación de la solicitud")
    canal = val.pedir_opcion("Canal de recepción:", val.CANALES)
    asunto = val.pedir_dato("Asunto o título (5 a 150 caracteres): ", val.validar_asunto)
    descripcion = val.pedir_dato("Descripción detallada (mínimo 20 caracteres): ", val.validar_descripcion)

    print("\nInformación relacionada")
    mascota = val.pedir_opcion("Tipo de mascota:", val.TIPOS_MASCOTA)
    campus = val.pedir_opcion("Campus relacionado:", val.CAMPUS)

    # Datos que el sistema calcula solo
    fecha_radicacion = val.fecha_actual()
    fecha_maxima = val.calcular_fecha_maxima(fecha_radicacion)

    registro = {
        "id": archivos.siguiente_id(tipo),
        "nombre_completo": nombre,
        "tipo_documento": tipo_documento,
        "numero_documento": numero_documento,
        "tipo_telefono": tipo_telefono,
        "telefono_contacto": telefono,
        "correo_electronico": correo,
        "direccion": direccion,
        "tipo_solicitud": tipo,
        "fecha_radicacion": fecha_radicacion,
        "canal_recepcion": canal,
        "asunto_titulo": asunto,
        "descripcion_detallada": descripcion,
        "tipo_mascota": mascota,
        "campus_relacionado": campus,
        "fecha_maxima_respuesta": fecha_maxima,
        "estado_peticion": val.ESTADOS[0],                 # siempre empieza en "Registrada"
        "usuario_registro": usuario_activo["usuario"],     # viene de la sesión
        "fecha_respuesta": "",                             # se llena al pasar a Solucionada
    }
    archivos.guardar_registro(tipo, registro)

    print("\n¡" + tipo + " registrada con éxito!")
    print("ID asignado: " + str(registro["id"]))
    print("Fecha de radicación: " + fecha_radicacion)
    print("Fecha máxima de respuesta: " + fecha_maxima)

    # Comprobante: se muestra en pantalla y se guarda como archivo .txt
    radicado.imprimir_radicado(registro)
    ruta = radicado.guardar_radicado(registro)
    print("\nRadicado guardado en: " + ruta)
    return registro


# ------------------------------------------------------------
# 2. Consultar PQRS
# ------------------------------------------------------------
def consultar_pqrs():
    print("\n--- Consultar PQRS ---")
    tipo = elegir_tipo("¿Qué tipo de solicitud desea consultar?")
    id_buscado = val.validar_entero("ID de la solicitud: ")
    registro = archivos.buscar_registro(tipo, id_buscado)
    if registro is None:
        print("No existe " + tipo + " con el ID " + str(id_buscado) + ".")
        return
    radicado.imprimir_radicado(registro)         # el estado se ve como un radicado
    ver = input("\n¿Ver la descripción completa? (s/n): ").strip().lower()
    if ver == "s":
        print("Descripción: " + registro["descripcion_detallada"])


# ------------------------------------------------------------
# 3. Registrar cambio de estado
# ------------------------------------------------------------
def cambiar_estado():
    print("\n--- Registrar cambio en PQRS ---")
    tipo = elegir_tipo("¿De qué tipo es la solicitud?")
    id_buscado = val.validar_entero("ID de la solicitud: ")
    registro = archivos.buscar_registro(tipo, id_buscado)
    if registro is None:
        print("No existe " + tipo + " con el ID " + str(id_buscado) + ".")
        return

    estado_actual = registro["estado_peticion"]
    print("Estado actual: " + estado_actual)
    if estado_actual == val.ESTADOS[-1]:                  # ya está Solucionada
        print("Esta PQRS ya está Solucionada, no puede cambiar de estado.")
        return

    estado_nuevo = val.ESTADOS[val.ESTADOS.index(estado_actual) + 1]
    es_valido, error = val.validar_cambio_estado(estado_actual, estado_nuevo)
    if not es_valido:
        print(error)
        return

    respuesta = input("¿Cambiar el estado a '" + estado_nuevo + "'? (s/n): ").strip().lower()
    if respuesta != "s":
        print("No se hicieron cambios.")
        return
    cambios = {"estado_peticion": estado_nuevo}
    if estado_nuevo == val.ESTADOS[-1]:                   # pasa a Solucionada: se anota cuándo
        cambios["fecha_respuesta"] = val.fecha_actual()
    archivos.actualizar_campos(tipo, id_buscado, cambios)
    print("Estado actualizado: " + estado_actual + " -> " + estado_nuevo)

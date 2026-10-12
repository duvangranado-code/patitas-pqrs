# 5. Reporte de Visión

## Descripción del Proyecto
Nuestro sistema es una aplicación de consola desarrollada en la aplicación Python, esta diseñada para automatizar y optimizar la gestión de las Peticiones, Quejas, Reclamos y las correspondientes Sugerencias (PQRS) en apoyo al Movimiento Estudiantil de Perritos y Gaticos (Patitas) de la Universidad de Antioquia.

## Propósito y Beneficios
El propósito principal es ofrecer a la organización una herramienta digital centralizada y ordenada que permita el manejo de los casos reportados por los solicitantes en relación con la atención de perros, gatos y otros animales. Los beneficios clave son:

* **Trazabilidad:** Llevar un registro claro de cada solicitud, su estado y su evolución en el periodo de tiempo que tarda en recibirse, procesarse y en dar una respuesta adecuada.
* **Control de acceso:** Uso de un sistema de inicio de sesión basado en roles (Administrador y Operador) para proteger los datos.
* **Gestión de plazos legales:** Llevar un control estricto del tiempo máximo de respuesta (hasta 15 días calendario) para evitar vencimientos en las solicitudes recibidas.
* **Análisis de gestión:** Generación automática de los radicados y de las estadísticas que facilitan la toma en las decisiones.
* **Análisis estadístico e integración:** Preparación de los datos para su posterior exportación y visualización en tableros de control interactivos en Power BI.

# 6. Especificación de Requisitos

## Requisitos Funcionales (Lo que el sistema puede hacer)

1. **Gestión de Usuarios (Login):** El sistema exige una autenticación previa mediante la verificación de las credenciales en archivos autorizados y controlando intentos fallidos.
2. **Registro de PQRS:** Permite registrar las solicitudes (Petición, Queja, Reclamo, Sugerencia) validando los datos estrictos del solicitante (nombre, documento, teléfono, correo y dirección).
3. **Almacenamiento en Archivos Planos:** Almacena de forma independiente los registros en la carpeta `data/` (`Peticion.txt`, `Queja.txt`, `Reclamo.txt`, `Sugerencia.txt`, `Usuarios.txt`) utilizando codificación `utf-8`.
4. **Consulta y Actualización:** Permite consultar los registros que se encuentran activos, cambiar estados de manera secuencial (`Registrada` - `En proceso` - `Solucionada`) e imprimir comprobantes en formato ASCII de 120 caracteres.
5. **Cálculo de Plazos y Estadísticas:** Calcula automáticamente la fecha máxima de respuesta en 15 días calendario y genera los reportes de gestión.

## Requisitos No Funcionales (Características de calidad y técnicas)

1. **Modularización del Código:** El código fuente se organiza estrictamente en la carpeta `src/` dividiéndose en módulos clave (`validaciones.py`, `archivos.py`, `reportes.py`).
2. **Control de Versiones y Estructura:** El proyecto se gestiona de forma colaborativa con el equipo de trabajo en el repositorio de GitHub utilizando las carpetas obligatorias (`src`, `docs`, `images`, `data`).
3. **Validación Robusta de Entradas:** El programa valida formatos de correo, longitudes de texto, números y fechas mediante la librería `datetime` de Python para evitar caídas del sistema.
4. **Compatibilidad:** Solución ejecutable en entornos de consola compatibles con Python y Visual Studio Code.    

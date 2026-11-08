# Plan de versionado — Patitas PQRS

**Curso:** Algoritmia y Programación 2026-2 · **Docente:** Víctor Hugo Mercado Ramos
**Equipo:** Duvan Estiben Granado Alzate · Mario Estrada García · Samuel González Contreras · Yeison Solar Barroso

El proyecto inició el **16 de septiembre de 2026 (día 1)** según el cronograma (el repositorio se creó el 18 de septiembre) y termina con la entrega final el **18 de noviembre de 2026 (día 64)**.
Cada versión se registra en GitHub con un *commit* y una etiqueta (*tag*) cuando se completa un procedimiento relevante.

Formato de versión: `vMAYOR.MENOR` (0.x = en desarrollo, 1.0 = entrega final).

| Versión | Fecha | Día desde el inicio | Estado | Qué se hizo / se hará |
|---|---|---|---|---|
| v0.1 | 20-sep-2026 | 5 | Hecha | Creación del repositorio: README, licencia, plan de proyecto y reporte de visión. |
| v0.2 | 28-sep-2026 | 13 | Hecha | Cronograma (diagrama de Gantt) y ajuste del presupuesto del plan de proyecto. |
| v0.3 | 30-sep-2026 | 15 | Hecha | **Entrega 1:** actas de entendimiento, colaboración y responsabilidad, y documentos de los puntos 1 a 7. |
| v0.4 | 11-oct-2026 | 26 | Hecha | Cambio de nombre a **Patitas PQRS**, logo nuevo y primer `main.py` (registrar y consultar solicitudes). |
| v0.5 | 18-oct-2026 | 33 | Hecha | Primer programa completo: login con máximo 3 intentos (`Usuarios.txt`); archivos planos `Peticion.txt`, `Queja.txt`, `Reclamo.txt`, `Sugerencia.txt`; validaciones; registrar y consultar PQRS; cambio de estado (Registrada → En proceso → Solucionada); radicado de 120 caracteres; modularización (`validaciones.py`, `archivos.py`, `reportes.py`) y estadísticas. |
| v0.6 | 25-oct-2026 | 40 | Hecha | Código limpio y comentado, manual de usuario en `docs/`, README y plan de versionado. |
| v0.7 | 8-nov-2026 | 54 | Hecha | Ajustes tras la asesoría con el docente: campo `fecha_respuesta` en los archivos, campo `tipo_usuario` (Interno/Externo según el correo), estadísticas con **pandas y numpy**, nueva estadística de perfil del solicitante y `requirements.txt`. |
| v0.8 | 10-nov-2026 | 56 | Planeada | Tablero de Power BI (a partir de `consolidado_pqrs.csv`) y la librería adicional que indique el docente. |
| v0.9 | 11-nov-2026 | 57 | Planeada | Programa completo entregado al docente y al monitor en cuestión para su revisión, se debe de entregar una semana antes de la sustentación con los compañeros del grupo. |
| v1.0 | 18-nov-2026 | 64 | Planeada | **Entrega final:** correcciones, manual de usuario en `docs/`, tablero de Power BI y repositorio completo. |

> Nota: las fechas de las versiones planeadas se pueden ajustar según las reuniones con el equipo de trabajo. Cada ajuste se anota y reporta aquí con su respectiva fecha.
> Las versiones v0.1 a v0.6 se publicaron como *releases* en GitHub el 2 de noviembre de 2026, cada una apuntando al *commit* que corresponde a su fecha en el historial del repositorio.

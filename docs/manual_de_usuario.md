# Manual de usuario — Patitas PQRS

Gestor de Peticiones, Quejas, Reclamos y Sugerencias (PQRS) para la atención de perros, gatos y demás animales.
Programa de consola en Python — Algoritmia y Programación 2026-2, Universidad de Antioquia.

## 1. Requisitos

- Python 3.8 o una versión superior.
- No se requiere o necesita de la instalación librerías adicionales.
- La carpeta `data/` debe estar junto a la carpeta de `src/' igual que en el repositorio.

## 2. Cómo se debe abrir el programa

1. Abra una terminal en la carpeta `src` del proyecto.
2. Escriba `python main.py` después de ello pulse Enter.

También puede abrir `main.py` en Visual Studio Code y pulsar el botón de ejecutar para correr el programa.
Al iniciar aparece el logo del programa (Patitas) y la pantalla de ingreso.

## 3. Inicio de sesión
El programa pide:
```
Por favor ingrese sus credenciales
(escriba CANCELAR como usuario para salir)
    1. Ingrese Usuario :
    2. Ingrese Clave   :
```
- Puede escribir el **usuario** (por ejemplo `admin_udea`) o bien el **correo institucional**.
- La clave no se muestra en pantalla mientras se escribe por motivos de seguridad.
- Los usuarios autorizados están en `data/Usuarios.txt`. Solo pueden ingresar usuarios con estado que se encuentren **Activo**.
- Se permiten **3 intentos**. Si los 3 fallan, el sistema se **bloquea 30 segundos** y va mostrando la cuenta regresiva.
- Para salir sin ingresar, escriba `CANCELAR` como usuario.
- 
Al ingresar bien, el sistema muestra el nombre y el rol, y guarda el usuario para anotarlo en cada PQRS que registre.

## 4. Menú principal
```
1. Registrar PQRS
2. Consultar PQRS
3. Registrar cambio en PQRS
4. Estadísticas
5. Salir
```
Escriba el número de la opción y pulse Enter. Si escribe letras o un número fuera de rango, el programa avisa y le vuelve a preguntar a los usuarios.

## 5. Registrar PQRS (opción 1)

El sistema pide los datos uno por uno. Si un dato no es válido, explica el error y lo vuelve a pedir. Donde hay una lista de opciones, se elige escribiendo el número.

| Dato | Reglas | Ejemplo válido |
|---|---|---|
| Tipo de solicitud | Elegir: Petición, Queja, Reclamo o Sugerencia | 2 |
| Nombre completo | 3 a 100 caracteres. Solo letras, espacios, apóstrofe (') y guion (-). Sin números | Juan David Pérez Gómez |
| Tipo de documento | Elegir: CC, TI, CE, PP o NIT | 1 |
| Número de documento | Solo números, de 3 a 15 dígitos | 1037654321 |
| Tipo de teléfono | Elegir: Celular, Fijo, Corporativo u Otro | 1 |
| Teléfono de contacto | Exactamente 10 dígitos | 3001234567 |
| Correo electrónico | Un solo `@` y un dominio válido. Máximo 254 caracteres | usuario@correo.com |
| Dirección | **Opcional** (Enter para omitirla). 5 a 200 caracteres | Avenida Siempreviva 742 |
| Canal de recepción | Elegir: Presencial, Correo electrónico, Página web, Teléfono, Redes sociales u Otro | 3 |
| Asunto o título | 5 a 150 caracteres | Solicitud de información sobre servicio veterinario |
| Descripción detallada | 20 a 2000 caracteres. No puede estar vacía ni tener solo espacios | Solicito información sobre los servicios de consulta para caninos. |
| Tipo de mascota | Elegir: Perro, Gato u Otro | 1 |
| Campus relacionado | Elegir uno de los 9 campus de la lista | 4 |

No se pueden usar el símbolo `|` ni saltos de línea en el asunto y la descripción.

El sistema asigna **solo**:
- El **ID** (número de consecutivo, independiente en cada tipo de solicitud).
- La **fecha de radicación** (la fecha y hora actuales).
- La **fecha máxima de respuesta** (fecha de radicación + **15 días**).
- El **estado inicial**: Registrada.
- El **usuario que registra** (la persona que inició sesión).

Al terminar, se muestra el **radicado** y se guarda como archivo de texto en `data/radicados/` (por ejemplo `PET-003001.txt`).

## 6. Consultar PQRS (opción 2)
1. Elija el tipo de solicitud.
2. Escriba el ID.
3. El programa muestra la PQRS como **radicado** este muestra el ancho de 120 caracteres, con el estado y fechas.
4. Puede pedir ver la **descripción completa**, que no aparece en el radicado.
Si el ID no existe, el programa lo avisa.

## 7. Registrar cambio en PQRS (opción 3)
1. Elija el tipo de solicitud y escriba el ID.
2. El programa muestra el estado actual y propone el siguiente.
3. Confirme con `s` (sí) o `n` (no).
El estado solo puede avanzar en este orden:

**Registrada → En proceso → Solucionada**
No se puede saltar ninguno de los estados ni devolverlos. Una PQRS **Solucionada** ya no cambia (Respuesta otorgada al usuario). Al pasar a Solucionada, el sistema anota la **fecha de respuesta** en la que se le dio la solución después del periodo de los 15 días hábiles. 

## 8. Estadísticas (opción 4)
```
1. Promedio de días de respuesta
2. Distribución por tipo de mascota
3. Proporción por canal de recepción
4. Distribución por campus
5. Efectividad por estado
6. Alerta de vencimiento
7. Ver todas
8. Exportar
9. Volver al menú principal
```
| Opción | Qué muestra |
|---|---|
| 1 | Promedio, en días enteros, que toma responder una PQRS (con las PQRS Solucionadas que tienen fecha de respuesta) |
| 2 | Cantidad y porcentaje de PQRS de perros, gatos y otros |
| 3 | Porcentaje de PQRS por canal de recepción |
| 4 | Cantidad y porcentaje por campus de la UdeA |
| 5 | Cuántas PQRS están Registradas, En proceso y Solucionadas, y la tasa de efectividad |
| 6 | PQRS activas que ya vencieron o vencen en 5 días o menos, y las 5 más antiguas |
| 7 | Todas las anteriores juntas |
| 8 | Exporta los resultados (ver sección 9) |

## 9. Archivos que genera el programa

| Archivo | Carpeta | Contenido |
|---|---|---|
| `Peticion.txt`, `Queja.txt`, `Reclamo.txt`, `Sugerencia.txt` | `data/` | Registros de cada tipo (campos separados por `\|`) |
| `PET-000001.txt` (y similares) | `data/radicados/` | Comprobante de radicado de cada PQRS registrada |
| `resumen_estadisticas.txt` | `data/` | Todas las estadísticas en texto (opción 4 → 8) |
| `consolidado_pqrs.csv` | `data/` | Las cuatro solicitudes en un solo archivo, para el tablero de Power BI (opción 4 → 8) |

## 10. Problemas frecuentes

| Problema | Causa y solución |
|---|---|
| "Usuario o clave incorrectos, o usuario inactivo" | Revise el usuario y la clave en `data/Usuarios.txt`. El usuario debe estar Activo |
| El sistema se bloquea | Se escribieron mal las credenciales 3 veces. Espere a que termine la cuenta regresiva |
| "Debe ingresar un número entero" | El programa esperaba un número y se escribió otra cosa |
| No encuentra los archivos de datos | La carpeta `data/` debe estar al lado de `src/`, como en el repositorio |
| "No existe Queja con el ID ..." | Ese ID no está registrado en ese tipo. Cada tipo tiene su propia numeración |
| El promedio de días sale vacío | Aún no hay PQRS pasadas a Solucionada con fecha de respuesta registrada |

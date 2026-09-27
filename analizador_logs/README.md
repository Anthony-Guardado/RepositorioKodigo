# Analizador de Logs

Script en Python que analiza un archivo de logs, identifica el nivel de
severidad de cada evento (`INFO`, `WARNING`, `ERROR`) y valida si la línea
contiene una fecha en formato `YYYY-MM-DD`. Al final muestra un resumen
claro en consola.

**Autor:** Anthony Guardado
**Python:** 3.12.10
**Dependencias:** ninguna (solo librería estándar)

---

## 🎯 Objetivo

Desarrollar una solución funcional en Python que:
- Lea un archivo de logs elegido por el usuario.
- Identifique el nivel de severidad de cada línea.
- Detecte si la línea contiene o no una fecha válida.
- Genere un resumen: total de eventos, conteo por severidad y líneas
  mal formadas.

---

## 📁 Estructura del proyecto

```
analizador_logs/
├── analizador_logs.py
├── README.md
├── requirements.txt
└── pruebas/
    ├── logs_bueno.txt
    └── logs_malo.txt
```

---

## ⚙️ Requisitos

- Python 3.10 o superior (probado en **3.12.10**).
- No se requieren librerías externas.
- Sistema operativo: Windows, Linux o macOS.

---

## 🚀 Cómo ejecutar

1. Abre una terminal en la carpeta del proyecto.
    ```bash
   cd analizador_logs
   ```
2. Ejecuta:

   ```bash
   python analizador_logs.py
   ```

3. Cuando lo solicite, escribe la ruta del archivo de logs. Ejemplos:

   ```
   pruebas/logs_bueno.txt
   ```

   o en Windows:

   ```
   pruebas\logs_bueno.txt
   ```

4. El script imprimirá el resumen en consola.

---

## 🧠 Reglas de validación (DECISIONES DEL ESTUDIANTE)

Estas reglas fueron definidas explícitamente por el estudiante. La IA solo
apoyó con la sintaxis de expresiones regulares, pero **no decidió** los
criterios.

| Regla | Descripción |
|-------|-------------|
| Severidad válida | Solo `[INFO]`, `[WARNING]`, `[ERROR]` (case sensitive). |
| Severidades prohibidas | `[DEBUG]`, `[CRITICAL]`, `[TRACE]`, etc. → cuentan como malformadas. |
| Formato de fecha | `YYYY-MM-DD` validado con `datetime.strptime`. |
| Fecha inexistente | `2025-13-45` coincide con el patrón pero es inválida → malformada. |
| Línea sin severidad | Se cuenta como malformada. |
| Línea sin fecha | Se cuenta como malformada y como "sin fecha válida". |
| Líneas vacías | Se ignoran por completo (no cuentan como evento). |
| Ejecución | El script NO se detiene por errores; acumula y reporta al final. |

---

## 🧪 Pruebas

### Prueba 1 — Archivo bien formado (`pruebas/logs_bueno.txt`)

**Contenido:**
```
[INFO] 2025-01-10 User logged in
[ERROR] 2025-01-10 Failed to connect to database
[WARNING] 2025-01-11 Invalid password attempt
[INFO] 2025-01-11 User logged out
[ERROR] 2025-01-12 Timeout on API request
[INFO] 2025-01-12 Scheduled backup completed
[WARNING] 2025-01-13 Disk usage above 80 percent
[ERROR] 2025-01-13 Null pointer exception in module core
[INFO] 2025-01-14 New user registered
[WARNING] 2025-01-14 Multiple login attempts detected
```

**Comando:**
```bash
python analizador_logs.py
# Ingresar: pruebas/logs_bueno.txt
```

**Resultado esperado:**
```
Total de eventos analizados : 10
INFO     : 4
WARNING  : 3
ERROR    : 3
Líneas mal formadas         : 0
Líneas sin fecha válida     : 0
```

---

### Prueba 2 — Archivo con errores (`pruebas/logs_malo.txt`)

**Contenido:**
```
[INFO] 2025-01-10 User logged in
[ERROR] Failed to connect to database
[WARNING] 2025-13-45 Invalid password attempt
[INFO] 2025-01-11 User logged out
esta linea no tiene severidad ni fecha
[ERROR] 2025-01-12 Timeout on API request
[DEBUG] 2025-01-12 This severity is not allowed
[INFO] 2025/01/13 Wrong date separator
[WARNING] 2025-01-13 Disk usage above 80 percent
[CRITICAL] 2025-01-13 Unknown severity level
```

**Comando:**
```bash
python analizador_logs.py
# Ingresar: pruebas/logs_malo.txt
```

**Resultado esperado:**
```
Total de eventos analizados : 10
INFO     : 2
WARNING  : 1
ERROR    : 1
Líneas mal formadas         : 5   (líneas: 2, 5, 7, 8, 10)
Líneas sin fecha válida     : 4   (líneas: 2, 3, 5, 8)
```



## 🔍 Casos borde manejados

| Caso | Comportamiento |
|------|----------------|
| Línea vacía | Se ignora, no suma al total. |
| Fecha inválida (`2025-13-45`) | Se marca malformada y sin fecha válida. |
| Separador distinto (`2025/01/13`) | No coincide con el patrón → sin fecha válida. |
| Severidad no permitida (`[DEBUG]`) | Cuenta como malformada (no suma en el conteo por severidad). |
| Archivo inexistente | El script avisa y termina sin errores críticos. |

## 🚫 Casos borde NO manejados (fuera de alcance)

- Zonas horarias o formatos de fecha alternativos (`DD/MM/YYYY`, ISO con hora).
- Logs multilínea (un evento repartido en varias líneas).
- Codificaciones distintas a UTF-8.

---

## 📝 Decisiones clave en el código

1. **Regex de severidad con `^` anclado al inicio** — evita falsos positivos
   si la palabra `INFO` aparece dentro del mensaje.
2. **Regex de fecha sin anclaje** — permite que la fecha aparezca en cualquier
   posición de la línea.
3. **Doble validación de fecha** — primero el patrón, luego `datetime.strptime`
   para descartar fechas como `2025-13-45`.
4. **Uso de `Counter`** — simplifica el conteo por severidad sin condicionales.
5. **Retorno de diccionario en `analizar_linea`** — separa la lógica de análisis
   de la impresión, facilitando pruebas unitarias futuras.

---

## 👤 Créditos

Desarrollado por **ANTHONY GUARDADO** como parte de la actividad de
"Uso de IA como herramienta de apoyo en el desarrollo".
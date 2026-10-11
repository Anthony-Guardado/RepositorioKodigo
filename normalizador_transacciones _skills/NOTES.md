
**Cómo lo corregí:**
Reemplacé los f-strings anidados por concatenación de strings con
`.format()` y separé el render de secciones en funciones dedicadas
(`_render_skills_section`, `_render_metrics_block`).

**Por qué importa:** demuestra que el código generado por IA debe validarse
contra la versión exacta del intérprete, no solo contra "Python moderno".

### 3.3 Otra corrección humana

El comando que me dio la IA para el archivo `.opencode/opencode.json`
incluía los marcadores markdown (` ```json `) como parte del contenido.
OpenCode falló con `InvalidSymbol at line 1, column 1`. Detecté que los
backticks no debían estar dentro del archivo y los eliminé.

### 3.4 Decisiones que NO delegué a la IA

- **Reglas de validación**: definí explícitamente las 5 reglas y su orden.
- **Umbral de detección de fuente** (`SOURCE_DETECTION_MIN_MATCHES = 2`):
  decisión humana tras analizar falsos positivos.
- **Comportamiento ante inválidas**: conservarlas con trazabilidad en vez
  de descartarlas.
- **Formato de las skills**: los 5 bloques fueron definidos por mí antes
  de pedirle a la IA que los redactara.

---

## 4. Evidencia de validación

### 4.1 Pruebas ejecutadas

| # | Prueba | Resultado esperado | Resultado obtenido |
|---|---|---|---|
| 1 | Normalizar `wallet_app` con `pesos` | `currency=MXN`, `status=completed` | ✅ Coincide |
| 2 | Validar transacción con todos los errores | 5 errores detectados | ✅ Coincide |
| 3 | Detectar fuente de un JSON sin `source` | `exchange_crypto` | ✅ Coincide (score 5/5) |
| 4 | Métricas del dataset por defecto | 13 total, 8 válidas, 5 inválidas | ✅ Coincide |
| 5 | Generar README desde skills | `README.md` con 5 skills | ✅ Coincide (5.5 KB) |

### 4.2 Cambio de comportamiento observado

Las métricas cambiaron respecto a la versión previa al refactor:
**antes 7 válidas / 6 inválidas, ahora 8 válidas / 5 inválidas**. Esto no
es un bug: la detección de fuente ahora clasifica correctamente un registro
que antes caía en el branch de "fuente desconocida". Documentar este cambio
es parte de la validación del refactor.

### 4.3 Error detectado y ajuste realizado

Durante la prueba #4, OpenCode pasó un `str` a `load_transactions()` en
lugar de un `Path`. El agente **leyó `loaders.py`, entendió el contrato y
reintentó** con el tipo correcto. Este es un ejemplo de que la IA opera
como par técnico con supervisión: no solo ejecuta, verifica.

---

## 5. Reflexión final

### 5.1 Qué aprendí usando IA para programar

Que un prompt estructurado (rol + stack + formato + criterios) produce
código mucho más cercano al objetivo que un prompt genérico. También que
la IA es excelente para generar **estructura** y **boilerplate**, pero
el **criterio de dominio** (qué es válido, qué no, qué hacer con errores)
debe venir del humano.

### 5.2 Ventajas y límites del vibecoding

**Ventajas:**
- Acelera la creación de esqueletos y la escritura repetitiva.
- Detecta y corrige errores propios en tiempo de ejecución.
- Mantiene consistencia entre módulos si el prompt inicial es sólido.

**Límites:**
- Comete errores por versión de intérprete (f-strings en 3.12).
- Copia marcadores markdown en archivos técnicos si no se le especifica.
- No conoce las reglas de negocio del dominio: hay que definirlas antes.

### 5.3 Qué comprendo y qué debo reforzar

**Comprendo:** la arquitectura por skills, la separación de módulos, el
contrato de entrada/salida de cada skill, y el patrón de orquestación.

**Debo reforzar:** el manejo de encoding en consolas de Windows, la
escritura de tests automatizados por skill, y la expiración/rotación de
API keys en configuraciones de agentes.

---

## 6. Créditos

Desarrollado por **ANTHONY GUARDADO** como parte de la actividad
"Refactorización y Personalización de un Sistema Agéntico mediante Skills Propias".
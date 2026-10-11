# Normalizador de Transacciones — Refactorizado con Skills

> Este README fue generado automáticamente por la skill `documentar-refactor` y revisado manualmente por el autor.

**Autor:** Anthony Guardado
**Fecha de refactor:** 2026-10-10
**Python:** 3.12.10
**Dependencias:** ninguna (solo librería estándar)

---

## 🎯 Objetivo de la refactorización

Convertir un proyecto monolítico de normalización de transacciones en un
sistema modular donde cada responsabilidad está encapsulada en una **skill
propia** ejecutable por un agente de OpenCode.

---

## 🏗️ Arquitectura modular

| Antes | Después |
|---|---|
| Lógica de normalización en `normalizer.py` | Skill `normalizar-transaccion` + orquestador delgado |
| Validación hardcodeada dentro del normalizador | Skill `validar-reglas-negocio` en `validators.py` |
| Fuente asumida explícita en el JSON | Skill `detectar-fuente-transaccion` en `source_detector.py` |
| Métricas acopladas a la CLI | Skill `generar-metricas` con contrato fijo |
| README escrito a mano | Skill `documentar-refactor` + `refactor_docs.py` |

---

## 🧩 Skills disponibles

Las skills se listan en el orden del flujo lógico del pipeline:
detectar → normalizar → validar → agregar → documentar.

### 1. `detectar-fuente-transaccion`

**Qué hace:** Analiza la estructura de un dict crudo de transacción y determina a qué fuente pertenece (`banco_central`, `wallet_app`, `exchange_crypto`) basándose en la firma de sus campos. Devuelve el nombre de la fuente o `desconocida` si no puede determinarla.

**Cuándo se usa:**

- Cuando el campo `source` **no viene presente** en el registro crudo.
- Cuando el valor de `source` es ambiguo o no está en el catálogo de fuentes soportadas.
- Cuando el usuario pregunte "¿de dónde viene esta transacción?".
- Frases típicas: *"detecta la fuente"*, *"¿qué tipo de transacción es?"*, *"identifica el origen"*.

### 2. `normalizar-transaccion`

**Qué hace:** Convierte un registro crudo de transacción (dict con campos variables según la fuente) en una instancia de `NormalizedTransaction` con campos canónicos: `id`, `source`, `amount` (Decimal), `currency` (ISO), `status` (canónico), `timestamp` (datetime), `is_valid`, `errors`.

**Cuándo se usa:**

- Cuando el usuario pida "normaliza esta transacción" o "pásala al formato canónico".
- Cuando se procese un lote de transacciones crudas desde un JSON.
- Cuando se reciba un registro de una fuente nueva no clasificada aún.
- Frases típicas: *"normaliza el archivo X"*, *"convierte estas transacciones"*, *"limpia los registros"*.

### 3. `validar-reglas-negocio`

**Qué hace:** Aplica el conjunto de reglas de validación del dominio sobre una transacción normalizada. Devuelve el mismo objeto con `is_valid` actualizado y la lista `errors` poblada. No descarta la transacción: la marca para trazabilidad.

**Cuándo se usa:**

- Después de normalizar cualquier transacción (skill `normalizar-transaccion`).
- Cuando el usuario pida "valida estas transacciones" o "muéstrame las inválidas".
- Al procesar un lote completo desde un archivo JSON.
- Frases típicas: *"verifica que estén bien"*, *"¿cuáles son inválidas?"*, *"checa las reglas"*.

### 4. `generar-metricas`

**Qué hace:** Recibe una lista de `NormalizedTransaction` ya normalizadas y validadas, y produce un diccionario con todas las métricas del dataset: totales, conteos y sumas monetarias por moneda.

**Cuándo se usa:**

- Cuando el usuario pida "dame el resumen", "muéstrame las métricas" o "estadísticas del dataset".
- Antes de exportar un JSON con resultados (skill de exportación).
- Al finalizar el procesamiento de un lote para reportar al usuario.
- Frases típicas: *"¿cuántas transacciones válidas hay?"*, *"total por moneda"*, *"resumen general"*.

### 5. `documentar-refactor`

**Qué hace:** Produce la documentación técnica completa del proyecto refactorizado: README con arquitectura, listado y descripción de skills, ejemplos de uso, changelog de decisiones humanas vs IA, y guía de ejecución. Su salida es el entregable de documentación de la actividad.

**Cuándo se usa:**

- Al terminar una refactorización significativa del proyecto.
- Cuando el usuario pida "genera el README", "documenta las skills" o "escribe el changelog".
- Antes de hacer commit final de una entrega.
- Frases típicas: *"documenta esto"*, *"arma el README"*, *"explica qué cambió"*.

---

## 🚀 Cómo ejecutar

```bash
python main.py                                   # dataset por defecto
python main.py pruebas/transacciones_ok.json     # dataset limpio
python main.py pruebas/transacciones_mixtas.json # dataset con errores
```

Desde el menú de la CLI:

- Opción 7 → exportar dataset normalizado a JSON.
- Opción 8 → **regenerar este README** desde las skills.

---

## 📊 Última ejecución

- Total procesadas: **13**
- Válidas: **8**
- Inválidas: **5**

---

## 🤖 Integración con OpenCode

Este proyecto está diseñado para ser operado por un agente de OpenCode que
carga las skills automáticamente desde `.opencode/skills/`.

### Configuración de permisos (`.opencode/opencode.json`)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "skill": {
      "normalizar-transaccion": "allow",
      "validar-reglas-negocio": "allow",
      "detectar-fuente-transaccion": "allow",
      "generar-metricas": "allow",
      "documentar-refactor": "allow",
      "*": "ask"
    },
    "bash": {
      "python main.py*": "allow",
      "python -m pytest*": "allow",
      "*": "ask"
    }
  }
}
```

### Cómo OpenCode descubre las skills

OpenCode lee el frontmatter YAML de cada `SKILL.md` (campos `name` y
`description`) y construye un catálogo. Cuando el prompt del usuario coincide
semánticamente con la descripción de una skill, el agente la carga y ejecuta
los pasos definidos en el `SKILL.md`.

### Evidencia de invocación automática

Se ejecutaron 5 pruebas, una por skill, desde el chat de OpenCode en la raíz
del proyecto. En cada caso, el agente reconoció la skill correspondiente sin
que el usuario la nombrara explícitamente:

| Prompt del usuario | Skill activada | Resultado |
|---|---|---|
| *"Normaliza esta transacción: {...}"* | `normalizar-transaccion` | `amount=250.5`, `currency=MXN`, `status=completed` |
| *"Valida esta transacción y dime si es válida"* | `validar-reglas-negocio` | `is_valid=False`, 5 errores detectados |
| *"¿De qué fuente viene esta transacción?"* | `detectar-fuente-transaccion` | `exchange_crypto` (score 5/5) |
| *"Ejecuta el proyecto y dame el resumen"* | `generar-metricas` | JSON con totales, conteos y sumas por moneda |
| *"Genera el README del proyecto"* | `documentar-refactor` | `README.md` de 5.5 KB generado |

### Ejemplo de autocorrección del agente

Durante la prueba de `generar-metricas`, el agente ejecutó inicialmente
`load_transactions('data/transacciones.json')` pasando un `str`. El código
esperaba un `Path` y lanzó `AttributeError`. El agente leyó `loaders.py`,
detectó el tipo esperado y reintentó con `Path(...)` exitosamente. Este
comportamiento demuestra que el agente no ejecuta a ciegas: lee el código,
entiende el contrato y se corrige.

---

## 🔍 Casos borde manejados

| Caso | Comportamiento |
|------|---------------|
| Monto con separador de miles (`"1,250.50 USD"`) | Se limpia y convierte a `1250.50` |
| Moneda en español (`"pesos"`, `"dólares"`) | Alias → ISO (`MXN`, `USD`) |
| Estado en español (`"completado"`, `"fallido"`) | Mapeo a valor canónico |
| Fecha Unix timestamp (int) | Se convierte a `datetime` UTC |
| Fecha inválida (`32/13/2025`) | Se marca como error, no rompe |
| Monto cero o negativo | Se rechaza |
| Fuente desconocida | Se marca inválida con error explícito |
| JSON malformado | Error controlado, no rompe el programa |

---

## 🧠 Decisiones humanas vs IA

| Cambio | Sugerido por IA | Decisión humana |
|---|---|---|
| Separar validación en `validators.py` | Sí | Sí — el estudiante fijó las 5 reglas |
| Extraer detección de fuente a módulo propio | Sí | Sí — se agregó umbral mínimo de confianza |
| `normalizer.py` como orquestador delgado | Sí | Sí — se definió el orden de delegación |
| Generar README desde las skills | Sí | Sí — se revisó y ajustó la estructura |
| Orden de validaciones en `validate()` | No | Decisión del estudiante |

---

## 👤 Créditos

Desarrollado por **ANTHONY GUARDADO** como parte de la actividad
"Refactorización y Personalización de un Sistema Agéntico mediante Skills Propias".
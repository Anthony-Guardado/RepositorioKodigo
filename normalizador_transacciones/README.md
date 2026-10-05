# Normalizador de Transacciones Multifuente

Sistema en Python que lee transacciones heterogéneas desde un archivo JSON,
las normaliza a un modelo canónico, valida cada registro y permite
explorarlas mediante una CLI interactiva. Incluye exportación del dataset
normalizado a JSON limpio.

**Autor:** Anthony Guardado
**Python:** 3.12.10
**Dependencias:** ninguna (solo librería estándar)

---

## 🎯 Objetivo

Aplicar normalización de datos heterogéneos, modelado correcto y exposición
interactiva de la información, demostrando criterio técnico en las reglas
de transformación y en el manejo de registros inválidos.

---

## 📁 Estructura

```
normalizador_transacciones/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── transacciones.json
├── pruebas/
│   ├── transacciones_ok.json
│   └── transacciones_mixtas.json
└── src/
    ├── __init__.py
    ├── config.py
    ├── models.py
    ├── loaders.py
    ├── normalizer.py
    ├── metrics.py
    ├── exporter.py
    └── cli.py
```

---

## 🚀 Cómo ejecutar

```bash
# Dataset por defecto
python main.py

# Dataset alternativo
python main.py pruebas/transacciones_ok.json
python main.py pruebas/transacciones_mixtas.json
```

Verás un menú:

```
===== NORMALIZADOR DE TRANSACCIONES =====
 1. Ver todas las transacciones
 2. Filtrar por fuente
 3. Filtrar por estado
 4. Filtrar por moneda
 5. Ver solo inválidas
 6. Ver métricas
 7. Exportar dataset normalizado a JSON
 8. Salir
```

---

## 🧠 Modelo normalizado

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | str | Identificador único de la transacción |
| `source` | str | Fuente original: `banco_central`, `wallet_app`, `exchange_crypto` |
| `amount` | Decimal | Monto positivo, sin símbolo ni separador de miles |
| `currency` | str | Código ISO: `USD`, `MXN`, `EUR`, `BTC`, `ETH` |
| `status` | str | Canónico: `completed`, `pending`, `failed`, `refunded` |
| `timestamp` | datetime | Fecha normalizada |
| `is_valid` | bool | Resultado de la validación |
| `errors` | list[str] | Errores detectados (vacío si es válida) |

---

## 📥 Fuentes soportadas y mapeo

### `banco_central`
| Campo original | Campo normalizado | Regla |
|---|---|---|
| `id` | `id` | directo |
| `amount` (ej. `"1,250.50 USD"`) | `amount` + `currency` | Se separa número y moneda |
| `status` | `status` | mapeo a canónico |
| `date` (ISO) | `timestamp` | parseo ISO |

### `wallet_app`
| Campo original | Campo normalizado | Regla |
|---|---|---|
| `tx_id` | `id` | renombre |
| `monto` | `amount` | numérico directo |
| `moneda` | `currency` | alias → ISO |
| `estado` | `status` | mapeo (español → inglés) |
| `fecha` (`DD/MM/YYYY`) | `timestamp` | parseo con formato |

### `exchange_crypto`
| Campo original | Campo normalizado | Regla |
|---|---|---|
| `transaction_id` | `id` | renombre |
| `value` | `amount` | numérico directo |
| `currency` | `currency` | ISO directo |
| `state` | `status` | mapeo a canónico |
| `timestamp` (Unix) | `timestamp` | `fromtimestamp` UTC |

---

## ✅ Reglas de validación (DECISIONES DEL ESTUDIANTE)

Una transacción es **válida** solo si cumple TODAS estas reglas:

1. `id` no vacío.
2. `amount` parseable y **estrictamente mayor a 0**.
3. `currency` reconocida dentro del catálogo soportado.
4. `status` mapeable a uno de los 4 valores canónicos.
5. `timestamp` parseable en ISO 8601, `DD/MM/YYYY` o Unix.

Las transacciones inválidas **no se descartan**: se conservan en el dataset
con `is_valid=False` y la lista de `errors` para trazabilidad.

---

## 📤 Exportación a JSON

La opción **7** del menú exporta el dataset normalizado a un archivo JSON
limpio, listo para consumir por otras herramientas o para entregar como
evidencia.

**Contenido del archivo exportado:**
- `generated_at`: timestamp de cuándo se generó.
- `summary`: todas las métricas (total, válidas, inválidas, por estado,
  por fuente, totales por moneda).
- `transactions`: lista completa de transacciones normalizadas, incluyendo
  las inválidas con sus errores.

**Ruta por defecto:** `exports/transacciones_normalizadas.json`
(puedes escribir otra ruta cuando el menú te la pida).

**Ejemplo de uso:**

```
Elige una opción [1-8]: 7
Ruta de salida [exports/transacciones_normalizadas.json]:
[✓] Exportado correctamente en: /ruta/proyecto/exports/transacciones_normalizadas.json
```

**Ejemplo del JSON generado:**

```json
{
  "generated_at": "2025-10-04T15:22:11",
  "summary": {
    "total": 13,
    "validas": 7,
    "invalidas": 6,
    "por_estado": {
      "completed": 3,
      "pending": 2,
      "failed": 1,
      "refunded": 1
    },
    "por_fuente": {
      "banco_central": 5,
      "wallet_app": 5,
      "exchange_crypto": 3
    },
    "totales_por_moneda": {
      "USD": "1521.25",
      "MXN": "980.00",
      "EUR": "500.75",
      "BTC": "0.025",
      "ETH": "1.5"
    }
  },
  "transactions": [
    {
      "id": "BC-001",
      "source": "banco_central",
      "amount": 1250.50,
      "currency": "USD",
      "status": "completed",
      "timestamp": "2025-01-10T14:23:00",
      "is_valid": true,
      "errors": []
    },
    {
      "id": "BC-005",
      "source": "banco_central",
      "amount": null,
      "currency": null,
      "status": "completed",
      "timestamp": "2025-01-14T12:00:00",
      "is_valid": false,
      "errors": ["monto no parseable", "moneda no reconocida"]
    }
  ]
}
```

---

## 🧪 Pruebas

### Prueba 1 — `pruebas/transacciones_ok.json`
**Esperado:** 3 procesadas, 3 válidas, 0 inválidas.
**Obtenido:** ✅ (3/3 válidas)

### Prueba 2 — `pruebas/transacciones_mixtas.json`
**Esperado:** 3 procesadas, 0 válidas, 3 inválidas con errores distintos:
- monto no parseable
- moneda no reconocida + estado no reconocido + fecha no parseable
- monto <= 0 + fecha fuera de rango

**Obtenido:** ✅ (3/3 inválidas con errores reportados)

### Prueba 3 — `data/transacciones.json`
**Esperado:** 13 procesadas, 7 válidas, 6 inválidas.
**Obtenido:** ✅

### Prueba 4 — Exportación a JSON
**Comando:** opción 7 del menú con ruta por defecto.
**Esperado:** archivo creado en `exports/transacciones_normalizadas.json`
con `summary` + `transactions`.
**Obtenido:** ✅ archivo generado y validado con `json.load` sin errores.

---

## 🔍 Casos borde manejados

| Caso | Comportamiento |
|------|---------------|
| Monto con separador de miles (`"1,250.50 USD"`) | Se limpia y convierte a `1250.50` |
| Moneda en español (`"pesos"`, `"dólares"`) | Alias → ISO (`MXN`, `USD`) |
| Estado en español (`"completado"`, `"fallido"`) | Mapeo a canónico |
| Fecha Unix timestamp (int) | Se convierte a datetime UTC |
| Fecha inválida (`32/13/2025`) | Se marca como error |
| Monto cero o negativo | Se rechaza |
| Fuente desconocida | Se marca como inválida con error explícito |
| Archivo JSON malformado | Error controlado, no rompe el programa |
| Ruta de exportación inexistente | Se crea automáticamente la carpeta |

---

## 📊 Métricas expuestas

- Total procesadas
- Válidas vs inválidas
- Conteo por estado (solo válidas)
- Conteo por fuente (todas)
- Totales monetarios por moneda (solo válidas)

---

## 👤 Créditos

Desarrollado por **ANTHONY GUARDADO** como parte de la actividad
"Normalización y Exploración de Transacciones Multifuente".
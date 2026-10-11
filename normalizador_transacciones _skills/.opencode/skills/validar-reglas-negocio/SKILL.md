---
name: validar-reglas-negocio
description: "Aplica las reglas de validación del dominio de transacciones sobre una instancia de NormalizedTransaction: id no vacío, monto estrictamente mayor a cero, moneda en catálogo soportado, estado en valores canónicos, fecha parseable. Marca la transacción como válida o inválida y acumula los errores detectados sin detener el procesamiento. Usar después de normalizar una transacción o un lote completo."
---

# Validar Reglas de Negocio

## QUÉ HACE

Aplica el conjunto de reglas de validación del dominio sobre una transacción normalizada. Devuelve el mismo objeto con `is_valid` actualizado y la lista `errors` poblada. No descarta la transacción: la marca para trazabilidad.

## CUÁNDO USARLA

- Después de normalizar cualquier transacción (skill `normalizar-transaccion`).
- Cuando el usuario pida "valida estas transacciones" o "muéstrame las inválidas".
- Al procesar un lote completo desde un archivo JSON.
- Frases típicas: *"verifica que estén bien"*, *"¿cuáles son inválidas?"*, *"checa las reglas"*.

## PASOS QUE DEBE SEGUIR

1. **Recibir** una `NormalizedTransaction` ya normalizada.
2. **Limpiar** la lista de errores previa (por si se revalida).
3. **Verificar regla por regla** en este orden estricto:
   - `id` no vacío ni None.
   - `amount` distinto de None y estrictamente mayor a 0.
   - `currency` presente y dentro del catálogo `{USD, MXN, EUR, BTC, ETH}`.
   - `status` dentro de `{completed, pending, failed, refunded}`.
   - `timestamp` distinto de None.
4. **Acumular errores** en `tx.errors` con descripciones claras en español (ej. `"monto <= 0"`, `"moneda no reconocida"`).
5. **Marcar** `tx.is_valid = (len(tx.errors) == 0)`.
6. **Nunca lanzar excepción** por regla incumplida: el sistema procesa lotes completos.

## FORMATO DE SALIDA ESPERADO

La misma `NormalizedTransaction` con dos campos modificados:

- `is_valid`: `True` si no hay errores, `False` en caso contrario.
- `errors`: lista de strings describiendo cada violación.

Ejemplo de lista de errores posibles:
- `"id vacío"`
- `"monto no parseable"`
- `"monto <= 0"`
- `"moneda no reconocida"`
- `"estado no reconocido"`
- `"fecha no parseable"`

## EJEMPLO DE ENTRADA Y SALIDA

**Entrada:**

```python
NormalizedTransaction(
    id="BC-005",
    source="banco_central",
    amount=None,          # no parseable
    currency=None,        # no reconocida
    status="completed",
    timestamp=datetime(2025, 1, 14, 12, 0, 0),
)
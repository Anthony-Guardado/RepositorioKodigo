---
name: normalizar-transaccion
description: "Normaliza una transacción cruda proveniente de cualquiera de las fuentes soportadas (banco_central, wallet_app, exchange_crypto) a un modelo canónico único. Convierte montos heterogéneos a Decimal, monedas a ISO 4217, estados a valores canónicos y fechas a datetime. Usar cuando se reciba un registro crudo de transacción y se necesite llevarlo al formato normalizado del sistema."
---

# Normalizar Transacción

## QUÉ HACE

Convierte un registro crudo de transacción (dict con campos variables según la fuente) en una instancia de `NormalizedTransaction` con campos canónicos: `id`, `source`, `amount` (Decimal), `currency` (ISO), `status` (canónico), `timestamp` (datetime), `is_valid`, `errors`.

## CUÁNDO USARLA

- Cuando el usuario pida "normaliza esta transacción" o "pásala al formato canónico".
- Cuando se procese un lote de transacciones crudas desde un JSON.
- Cuando se reciba un registro de una fuente nueva no clasificada aún.
- Frases típicas: *"normaliza el archivo X"*, *"convierte estas transacciones"*, *"limpia los registros"*.

## PASOS QUE DEBE SEGUIR

1. **Recibir el dict crudo** de la transacción y detectar su fuente (usar skill `detectar-fuente-transaccion` si no viene explícita).
2. **Delegar al normalizador correspondiente** según la fuente detectada.
3. **Parsear el monto**: eliminar símbolos, separadores de miles y convertir a `Decimal`. Si el monto trae moneda embebida (ej. `"1,250.50 USD"`), separarla.
4. **Normalizar la moneda**: buscar en catálogo ISO directo; si no, resolver alias (`pesos` → `MXN`, `dólares` → `USD`).
5. **Mapear el estado**: convertir cualquier variante (español/inglés) a uno de los 4 canónicos: `completed`, `pending`, `failed`, `refunded`.
6. **Parsear la fecha**: aceptar ISO 8601, `DD/MM/YYYY` o Unix timestamp (int).
7. **Construir el `NormalizedTransaction`** con los campos ya normalizados.
8. **Invocar la skill `validar-reglas-negocio`** sobre la transacción resultante.

## FORMATO DE SALIDA ESPERADO

Objeto `NormalizedTransaction` con:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | str | Identificador único |
| `source` | str | Fuente original |
| `amount` | Decimal \| None | Monto positivo |
| `currency` | str \| None | ISO 4217 |
| `status` | str \| None | Valor canónico |
| `timestamp` | datetime \| None | Fecha normalizada |
| `is_valid` | bool | Resultado de validación |
| `errors` | list[str] | Errores detectados |
| `raw` | dict | Registro original crudo |

## EJEMPLO DE ENTRADA Y SALIDA

**Entrada (cruda, fuente `banco_central`):**

```json
{
  "source": "banco_central",
  "id": "BC-001",
  "amount": "1,250.50 USD",
  "status": "completado",
  "date": "2025-01-10T14:23:00"
}
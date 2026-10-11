---
name: detectar-fuente-transaccion
description: "Detecta automáticamente la fuente de origen de una transacción cruda analizando la forma de sus campos (nombres de claves, tipos de valores) cuando el campo 'source' no viene explícito o es ambiguo. Reconoce los perfiles de banco_central, wallet_app y exchange_crypto. Usar antes de normalizar cuando la fuente es desconocida."
---

# Detectar Fuente de Transacción

## QUÉ HACE

Analiza la estructura de un dict crudo de transacción y determina a qué fuente pertenece (`banco_central`, `wallet_app`, `exchange_crypto`) basándose en la firma de sus campos. Devuelve el nombre de la fuente o `desconocida` si no puede determinarla.

## CUÁNDO USARLA

- Cuando el campo `source` **no viene presente** en el registro crudo.
- Cuando el valor de `source` es ambiguo o no está en el catálogo de fuentes soportadas.
- Cuando el usuario pregunte "¿de dónde viene esta transacción?".
- Frases típicas: *"detecta la fuente"*, *"¿qué tipo de transacción es?"*, *"identifica el origen"*.

## PASOS QUE DEBE SEGUIR

1. **Recibir** el dict crudo de la transacción.
2. **Si trae `source` explícito** y está en `{banco_central, wallet_app, exchange_crypto}`, devolverlo directamente sin analizar más.
3. **Aplicar reglas de detección** en este orden:
   - Si tiene las claves `tx_id`, `monto`, `moneda`, `estado`, `fecha` → **`wallet_app`**.
   - Si tiene las claves `transaction_id`, `value`, `currency`, `state`, `timestamp` → **`exchange_crypto`**.
   - Si tiene las claves `id`, `amount` (string con moneda embebida), `status`, `date` → **`banco_central`**.
4. **Calcular un score** por cantidad de claves coincidentes; la fuente con mayor score gana.
5. **Si ninguna fuente supera el umbral mínimo** (2 claves coincidentes), devolver `"desconocida"`.

## FORMATO DE SALIDA ESPERADO

String simple con uno de estos valores:

- `"banco_central"`
- `"wallet_app"`
- `"exchange_crypto"`
- `"desconocida"`

Opcionalmente, un dict con la fuente detectada y el score de confianza:

```python
{"source": "wallet_app", "confidence": 5, "matched_keys": ["tx_id", "monto", "moneda", "estado", "fecha"]}
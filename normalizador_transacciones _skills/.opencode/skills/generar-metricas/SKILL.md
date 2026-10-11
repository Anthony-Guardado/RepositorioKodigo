---
name: generar-metricas
description: "Calcula métricas agregadas sobre un lote de transacciones normalizadas: total procesadas, válidas vs inválidas, conteo por estado, conteo por fuente y totales monetarios por moneda (solo válidas). Devuelve un dict estructurado listo para exportar o mostrar en CLI. Usar cuando el usuario pida un resumen, estadísticas o números del dataset."
---

# Generar Métricas

## QUÉ HACE

Recibe una lista de `NormalizedTransaction` ya normalizadas y validadas, y produce un diccionario con todas las métricas del dataset: totales, conteos y sumas monetarias por moneda.

## CUÁNDO USARLA

- Cuando el usuario pida "dame el resumen", "muéstrame las métricas" o "estadísticas del dataset".
- Antes de exportar un JSON con resultados (skill de exportación).
- Al finalizar el procesamiento de un lote para reportar al usuario.
- Frases típicas: *"¿cuántas transacciones válidas hay?"*, *"total por moneda"*, *"resumen general"*.

## PASOS QUE DEBE SEGUIR

1. **Recibir** la lista completa de transacciones (válidas e inválidas mezcladas).
2. **Contar el total** de transacciones procesadas.
3. **Separar** en válidas (`is_valid=True`) e inválidas (`is_valid=False`).
4. **Contar por estado** (solo válidas) usando `Counter` sobre `tx.status`.
5. **Contar por fuente** (todas) usando `Counter` sobre `tx.source`.
6. **Sumar montos por moneda** (solo válidas): agrupar por `tx.currency` y acumular `Decimal`.
7. **Construir el dict de resultado** con las claves estándar del sistema.

## FORMATO DE SALIDA ESPERADO

Dict con esta estructura exacta:

```python
{
    "total": int,
    "validas": int,
    "invalidas": int,
    "por_estado": {"completed": int, "pending": int, "failed": int, "refunded": int},
    "por_fuente": {"banco_central": int, "wallet_app": int, "exchange_crypto": int},
    "totales_por_moneda": {"USD": "str(Decimal)", "MXN": "str(Decimal)", ...}
}
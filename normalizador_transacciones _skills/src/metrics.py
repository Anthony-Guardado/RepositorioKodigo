"""
Métricas agregadas del dataset normalizado.

Skill asociada: generar-metricas
Contrato de entrada: list[NormalizedTransaction]
Contrato de salida: dict con claves fijas (ver compute_metrics).
"""

from collections import Counter
from decimal import Decimal

from src.models import NormalizedTransaction


# Claves fijas del contrato de salida. No cambiar sin actualizar la skill.
METRICS_KEYS = (
    "total",
    "validas",
    "invalidas",
    "por_estado",
    "por_fuente",
    "totales_por_moneda",
)


def compute_metrics(transactions: list[NormalizedTransaction]) -> dict:
    """
    Calcula todas las métricas del dataset.

    Reglas:
    - 'por_estado' cuenta SOLO válidas.
    - 'por_fuente' cuenta TODAS (válidas + inválidas).
    - 'totales_por_moneda' suma SOLO válidas.
    - Los totales se serializan como str para compatibilidad JSON.
    """
    total = len(transactions)
    validas = [t for t in transactions if t.is_valid]
    invalidas = [t for t in transactions if not t.is_valid]

    por_estado = Counter(t.status for t in validas if t.status)
    por_fuente = Counter(t.source for t in transactions)

    totales_moneda: dict[str, Decimal] = {}
    for t in validas:
        if t.currency and t.amount is not None:
            totales_moneda[t.currency] = (
                totales_moneda.get(t.currency, Decimal("0")) + t.amount
            )

    return {
        "total": total,
        "validas": len(validas),
        "invalidas": len(invalidas),
        "por_estado": dict(por_estado),
        "por_fuente": dict(por_fuente),
        "totales_por_moneda": {k: str(v) for k, v in totales_moneda.items()},
    }
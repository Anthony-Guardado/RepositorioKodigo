"""
Generación de métricas agregadas sobre las transacciones normalizadas.
"""

from collections import Counter
from decimal import Decimal


def compute_metrics(transactions: list) -> dict:
    """Devuelve un diccionario con todas las métricas del resumen."""
    total = len(transactions)
    validas = [t for t in transactions if t.is_valid]
    invalidas = [t for t in transactions if not t.is_valid]

    por_estado = Counter(t.status for t in validas if t.status)
    por_fuente = Counter(t.source for t in transactions)

    # Totales por moneda (solo válidas)
    totales_moneda: dict[str, Decimal] = {}
    for t in validas:
        if t.currency and t.amount is not None:
            totales_moneda[t.currency] = totales_moneda.get(t.currency, Decimal("0")) + t.amount

    return {
        "total": total,
        "validas": len(validas),
        "invalidas": len(invalidas),
        "por_estado": dict(por_estado),
        "por_fuente": dict(por_fuente),
        "totales_por_moneda": {k: str(v) for k, v in totales_moneda.items()},
    }
"""
Reglas de validación del dominio de transacciones.

Skill asociada: validar-reglas-negocio
Responsabilidad única: aplicar las reglas de negocio sobre una
NormalizedTransaction ya normalizada. No normaliza. No transforma.
"""

from src.config import CANONICAL_STATUSES, MIN_AMOUNT, SUPPORTED_CURRENCIES
from src.models import NormalizedTransaction


def validate(tx: NormalizedTransaction) -> None:
    """
    Aplica todas las reglas de validación sobre la transacción (in-place).

    Reglas (DECISIÓN DEL ESTUDIANTE):
    1. id no vacío.
    2. amount parseable y estrictamente mayor a MIN_AMOUNT.
    3. currency presente y dentro de SUPPORTED_CURRENCIES.
    4. status dentro de CANONICAL_STATUSES.
    5. timestamp distinto de None.

    Nunca lanza excepción: acumula errores y marca is_valid.
    """
    # Limpiar errores previos por si se revalida
    tx.errors = []

    if not tx.id:
        tx.errors.append("id vacío")

    if tx.amount is None:
        tx.errors.append("monto no parseable")
    elif tx.amount <= MIN_AMOUNT:
        tx.errors.append(f"monto <= {MIN_AMOUNT}")

    if tx.currency is None:
        tx.errors.append("moneda no reconocida")
    elif tx.currency not in SUPPORTED_CURRENCIES:
        tx.errors.append(f"moneda fuera de catálogo: {tx.currency}")

    if tx.status is None:
        tx.errors.append("estado no reconocido")
    elif tx.status not in CANONICAL_STATUSES:
        tx.errors.append(f"estado fuera de catálogo: {tx.status}")

    if tx.timestamp is None:
        tx.errors.append("fecha no parseable")

    tx.is_valid = len(tx.errors) == 0


def validate_all(transactions: list[NormalizedTransaction]) -> list[NormalizedTransaction]:
    """Aplica validate() a una lista completa. Devuelve la misma lista."""
    for tx in transactions:
        validate(tx)
    return transactions
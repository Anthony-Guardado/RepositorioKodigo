"""
Exportación del dataset normalizado a JSON limpio.
Genera un archivo listo para consumir por otras herramientas.
"""

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from src.metrics import compute_metrics


def _serialize_value(v):
    """Convierte tipos no serializables por json.dumps a tipos nativos."""
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, datetime):
        return v.isoformat()
    if isinstance(v, Path):
        return str(v)
    return v


def _tx_to_dict(tx) -> dict:
    """Convierte una NormalizedTransaction a dict exportable."""
    return {
        "id": tx.id,
        "source": tx.source,
        "amount": float(tx.amount) if tx.amount is not None else None,
        "currency": tx.currency,
        "status": tx.status,
        "timestamp": tx.timestamp.isoformat() if tx.timestamp else None,
        "is_valid": tx.is_valid,
        "errors": list(tx.errors),
    }


def export_to_json(transactions: list, output_path: Path) -> Path:
    """
    Exporta las transacciones normalizadas + métricas a un JSON limpio.
    Crea las carpetas necesarias si no existen.
    Devuelve la ruta final del archivo.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    metrics = compute_metrics(transactions)

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "summary": metrics,
        "transactions": [_tx_to_dict(t) for t in transactions],
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=_serialize_value)

    return output_path
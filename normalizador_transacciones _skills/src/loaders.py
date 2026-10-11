"""
Lectura del archivo JSON de transacciones.
"""

import json
from pathlib import Path


def load_transactions(path: Path) -> list[dict]:
    """
    Lee el archivo JSON y devuelve la lista cruda de transacciones.
    Lanza ValueError si el archivo no tiene la estructura esperada.
    """
    if not path.is_file():
        raise FileNotFoundError(f"No existe el archivo: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict) or "transactions" not in data:
        raise ValueError("El JSON debe tener una clave raíz 'transactions'.")

    txs = data["transactions"]
    if not isinstance(txs, list):
        raise ValueError("'transactions' debe ser una lista.")

    return txs
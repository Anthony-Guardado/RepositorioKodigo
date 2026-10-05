"""
Punto de entrada: carga, normaliza y lanza la CLI interactiva.

Uso:
    python main.py                       # usa data/transacciones.json por defecto
    python main.py pruebas/transacciones_mixtas.json
"""

import sys
from pathlib import Path

from src.loaders import load_transactions
from src.normalizer import normalize_all
from src.metrics import compute_metrics
from src.cli import run_cli


def main() -> None:
    default_path = Path("data/transacciones.json")
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path

    try:
        raw = load_transactions(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"[X] {e}")
        sys.exit(1)

    normalized = normalize_all(raw)
    metrics = compute_metrics(normalized)

    print(f"\n[✓] Archivo cargado: {path}")
    print(f"[✓] Total procesadas: {metrics['total']} "
          f"(válidas: {metrics['validas']}, inválidas: {metrics['invalidas']})")

    run_cli(normalized, metrics)


if __name__ == "__main__":
    main()
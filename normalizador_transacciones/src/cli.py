"""
Interfaz interactiva por terminal: menú numerado con filtros y métricas.
Incluye exportación del dataset normalizado a JSON.
"""

from pathlib import Path

from src.metrics import compute_metrics
from src.exporter import export_to_json


# ---------------------------------------------------------------------------
# Render de tablas
# ---------------------------------------------------------------------------

def _print_table(rows: list[dict]) -> None:
    """Imprime una tabla simple alineada."""
    if not rows:
        print("   (sin resultados)")
        return
    cols = ["id", "source", "amount", "currency", "status", "timestamp", "valid", "errors"]
    widths = {c: max(len(c), max(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    header = " | ".join(c.ljust(widths[c]) for c in cols)
    print(header)
    print("-" * len(header))
    for r in rows:
        print(" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))


def _show(transactions: list) -> None:
    _print_table([t.to_row() for t in transactions])


# ---------------------------------------------------------------------------
# Submenús
# ---------------------------------------------------------------------------

def _filter_by_source(transactions: list) -> None:
    fuentes = sorted({t.source for t in transactions})
    print("\nFuentes disponibles:")
    for i, f in enumerate(fuentes, 1):
        print(f"  {i}. {f}")
    try:
        op = int(input("Elige una fuente: ").strip())
        elegida = fuentes[op - 1]
    except (ValueError, IndexError):
        print("Opción inválida.")
        return
    _show([t for t in transactions if t.source == elegida])


def _filter_by_status(transactions: list) -> None:
    estados = ["completed", "pending", "failed", "refunded"]
    print("\nEstados:")
    for i, e in enumerate(estados, 1):
        print(f"  {i}. {e}")
    try:
        op = int(input("Elige un estado: ").strip())
        elegido = estados[op - 1]
    except (ValueError, IndexError):
        print("Opción inválida.")
        return
    _show([t for t in transactions if t.status == elegido])


def _filter_by_currency(transactions: list) -> None:
    monedas = sorted({t.currency for t in transactions if t.currency})
    print("\nMonedas disponibles:")
    for i, m in enumerate(monedas, 1):
        print(f"  {i}. {m}")
    try:
        op = int(input("Elige una moneda: ").strip())
        elegida = monedas[op - 1]
    except (ValueError, IndexError):
        print("Opción inválida.")
        return
    _show([t for t in transactions if t.currency == elegida])


def _show_metrics(transactions: list) -> None:
    m = compute_metrics(transactions)
    print("\n" + "=" * 55)
    print("               MÉTRICAS DEL DATASET")
    print("=" * 55)
    print(f"Total procesadas      : {m['total']}")
    print(f"Válidas               : {m['validas']}")
    print(f"Inválidas             : {m['invalidas']}")
    print("-" * 55)
    print("Conteo por estado:")
    for estado, n in m["por_estado"].items():
        print(f"   {estado:<12}: {n}")
    print("-" * 55)
    print("Conteo por fuente:")
    for fuente, n in m["por_fuente"].items():
        print(f"   {fuente:<18}: {n}")
    print("-" * 55)
    print("Totales por moneda (solo válidas):")
    for moneda, total in m["totales_por_moneda"].items():
        print(f"   {moneda:<5}: {total}")
    print("=" * 55)


def _export_to_json(transactions: list) -> None:
    """Pide ruta al usuario y exporta el dataset normalizado a JSON."""
    default = "exports/transacciones_normalizadas.json"
    ruta_raw = input(f"Ruta de salida [{default}]: ").strip().strip('"')
    ruta = Path(ruta_raw) if ruta_raw else Path(default)

    try:
        ruta_final = export_to_json(transactions, ruta)
        print(f"\n[✓] Exportado correctamente en: {ruta_final.resolve()}")
    except OSError as e:
        print(f"\n[X] Error al escribir el archivo: {e}")


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------

def run_cli(transactions: list, _metrics_unused=None) -> None:
    """Menú interactivo principal."""
    while True:
        print("\n===== NORMALIZADOR DE TRANSACCIONES =====")
        print(" 1. Ver todas las transacciones")
        print(" 2. Filtrar por fuente")
        print(" 3. Filtrar por estado")
        print(" 4. Filtrar por moneda")
        print(" 5. Ver solo inválidas")
        print(" 6. Ver métricas")
        print(" 7. Exportar dataset normalizado a JSON")
        print(" 8. Salir")
        opcion = input("Elige una opción [1-8]: ").strip()

        if opcion == "1":
            _show(transactions)
        elif opcion == "2":
            _filter_by_source(transactions)
        elif opcion == "3":
            _filter_by_status(transactions)
        elif opcion == "4":
            _filter_by_currency(transactions)
        elif opcion == "5":
            _show([t for t in transactions if not t.is_valid])
        elif opcion == "6":
            _show_metrics(transactions)
        elif opcion == "7":
            _export_to_json(transactions)
        elif opcion == "8":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")
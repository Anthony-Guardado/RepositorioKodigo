"""
Analizador de Logs
------------------
Lee un archivo de logs, identifica la severidad (INFO / WARNING / ERROR)
y valida si cada línea contiene una fecha en formato YYYY-MM-DD.

Decisiones de diseño (tomadas por el estudiante):
1. Una línea se considera "mal formada" si:
   - No comienza con [INFO], [WARNING] o [ERROR] (case sensitive).
   - No contiene una fecha en formato YYYY-MM-DD.
2. Una línea con severidad desconocida (ej. [DEBUG], [CRITICAL]) se cuenta
   como mal formada porque no pertenece al conjunto permitido.
3. Las líneas vacías se ignoran por completo (no cuentan como eventos).
4. Una fecha que coincide con el patrón pero es inválida (ej. 2025-13-45)
   se cuenta como "sin fecha válida" y como malformada.
5. Los errores no detienen la ejecución: se acumulan y se reportan al final.
"""

import re
import os
from collections import Counter
from datetime import datetime


# --- Reglas de validación (DECISIÓN DEL ESTUDIANTE) ---
SEVERIDADES_VALIDAS = ("INFO", "WARNING", "ERROR")
SEVERIDAD_REGEX = re.compile(r"^\s*\[(INFO|WARNING|ERROR)\]")
FECHA_REGEX = re.compile(r"(\d{4}-\d{2}-\d{2})")
FORMATO_FECHA = "%Y-%m-%d"


def seleccionar_archivo() -> str | None:
    """Pide al usuario la ruta del archivo y valida que exista."""
    ruta = input("Ingresa la ruta del archivo de logs: ").strip().strip('"')
    if not os.path.isfile(ruta):
        print(f"[X] Error: el archivo '{ruta}' no existe o no es accesible.")
        return None
    return ruta


def validar_fecha(fecha_str: str) -> bool:
    """Verifica que la cadena sea una fecha real en formato YYYY-MM-DD."""
    try:
        datetime.strptime(fecha_str, FORMATO_FECHA)
        return True
    except ValueError:
        return False


def analizar_linea(linea: str) -> dict:
    """
    Analiza una sola línea y devuelve un diccionario con:
      - severidad: str | None
      - fecha_valida: bool
      - malformada: bool
    """
    resultado = {
        "severidad": None,
        "fecha_valida": False,
        "malformada": False,
    }

    # 1. Detectar severidad al inicio de la línea
    match_sev = SEVERIDAD_REGEX.match(linea)
    if match_sev:
        resultado["severidad"] = match_sev.group(1)
    else:
        resultado["malformada"] = True

    # 2. Detectar y validar fecha en cualquier parte de la línea
    match_fecha = FECHA_REGEX.search(linea)
    if match_fecha:
        resultado["fecha_valida"] = validar_fecha(match_fecha.group(1))
        if not resultado["fecha_valida"]:
            resultado["malformada"] = True
    else:
        # Sin fecha → se marca como malformada (según decisión del estudiante)
        resultado["malformada"] = True

    return resultado


def analizar_archivo(ruta: str) -> dict:
    """Recorre el archivo y acumula estadísticas."""
    total = 0
    conteo_sev = Counter()
    malformadas = 0
    sin_fecha = 0
    detalle_malformadas = []  # guardamos número de línea para reporte

    with open(ruta, "r", encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, start=1):
            linea = linea.rstrip("\n")

            # Ignorar líneas completamente vacías (decisión del estudiante)
            if not linea.strip():
                continue

            total += 1
            res = analizar_linea(linea)

            if res["severidad"]:
                conteo_sev[res["severidad"]] += 1

            if res["malformada"]:
                malformadas += 1
                detalle_malformadas.append(num_linea)

            if not res["fecha_valida"]:
                sin_fecha += 1

    return {
        "total": total,
        "por_severidad": conteo_sev,
        "malformadas": malformadas,
        "detalle_malformadas": detalle_malformadas,
        "sin_fecha": sin_fecha,
    }


def mostrar_resumen(resumen: dict) -> None:
    """Imprime el resumen en consola de forma clara."""
    print("\n" + "=" * 55)
    print("           RESUMEN DEL ANÁLISIS DE LOGS")
    print("=" * 55)
    print(f"Total de eventos analizados : {resumen['total']}")
    print("-" * 55)
    print("Eventos por severidad:")
    for sev in SEVERIDADES_VALIDAS:
        print(f"   {sev:<8}: {resumen['por_severidad'].get(sev, 0)}")
    print("-" * 55)
    print(f"Líneas mal formadas         : {resumen['malformadas']}")
    if resumen["detalle_malformadas"]:
        nums = ", ".join(str(n) for n in resumen["detalle_malformadas"])
        print(f"   (líneas: {nums})")
    print(f"Líneas sin fecha válida     : {resumen['sin_fecha']}")
    print("=" * 55)


def main() -> None:
    print("=== ANALIZADOR DE LOGS ===")
    ruta = seleccionar_archivo()
    if not ruta:
        return
    resumen = analizar_archivo(ruta)
    mostrar_resumen(resumen)


if __name__ == "__main__":
    main()
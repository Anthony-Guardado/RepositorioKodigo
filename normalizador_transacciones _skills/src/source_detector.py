"""
Detector automático de fuente de transacción.

Skill asociada: detectar-fuente-transaccion
Responsabilidad única: identificar a qué fuente pertenece un dict crudo
analizando la firma de sus campos (nombres de claves).

NO normaliza. NO valida. Solo detecta la fuente.
"""

from src.config import (
    SOURCE_DETECTION_MIN_MATCHES,
    SOURCE_SIGNATURES,
    SUPPORTED_SOURCES,
)


def detect_source(raw: dict) -> str:
    """
    Devuelve el nombre de la fuente detectada o 'desconocida'.

    Reglas (DECISIÓN DEL ESTUDIANTE):
    1. Si el dict trae 'source' explícito y está en el catálogo → se respeta.
    2. Si no, se comparan las claves del dict contra las firmas conocidas.
    3. La fuente con mayor cantidad de coincidencias gana.
    4. Si ninguna fuente supera SOURCE_DETECTION_MIN_MATCHES → 'desconocida'.
    """
    if not isinstance(raw, dict):
        return "desconocida"

    # Regla 1: source explícito
    explicit = raw.get("source")
    if explicit in SUPPORTED_SOURCES:
        return explicit

    # Regla 2 y 3: puntuar cada fuente por coincidencia de claves
    keys = set(raw.keys())
    scores = {
        source: len(keys & signature)
        for source, signature in SOURCE_SIGNATURES.items()
    }

    # Regla 4: umbral mínimo
    best_source = max(scores, key=scores.get)
    if scores[best_source] < SOURCE_DETECTION_MIN_MATCHES:
        return "desconocida"

    return best_source


def detect_with_confidence(raw: dict) -> dict:
    """
    Variante que devuelve más detalle: fuente, score y claves coincidentes.
    Útil para depuración y para logs.
    """
    keys = set(raw.keys()) if isinstance(raw, dict) else set()
    scores = {
        source: sorted(keys & signature)
        for source, signature in SOURCE_SIGNATURES.items()
    }
    source = detect_source(raw)
    return {
        "source": source,
        "confidence": len(scores.get(source, [])),
        "matched_keys": scores.get(source, []),
    }
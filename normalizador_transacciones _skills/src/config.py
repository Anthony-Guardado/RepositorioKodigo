"""
Configuración global: catálogos, mapeos y constantes de normalización.
Todas las reglas de negocio viven aquí para facilitar su auditoría.
"""

# --- Catálogo de monedas soportadas (ISO 4217 + cripto comunes) ---
SUPPORTED_CURRENCIES = {"USD", "MXN", "EUR", "BTC", "ETH"}

# --- Alias de moneda -> ISO canónico ---
CURRENCY_ALIASES = {
    "DOLAR": "USD",
    "DOLARES": "USD",
    "DOLLAR": "USD",
    "USD$": "USD",
    "EURO": "EUR",
    "EUROS": "EUR",
    "PESO": "MXN",
    "PESOS": "MXN",
    "MXN$": "MXN",
    "BITCOIN": "BTC",
    "BTC$": "BTC",
    "ETHEREUM": "ETH",
}

# --- Mapeo de estados -> valor canónico ---
STATUS_MAP = {
    # completed
    "COMPLETED": "completed",
    "COMPLETE": "completed",
    "SUCCESS": "completed",
    "SUCCESSFUL": "completed",
    "COMPLETADO": "completed",
    "COMPLETADA": "completed",
    "EXITOSO": "completed",
    "EXITOSA": "completed",
    # pending
    "PENDING": "pending",
    "IN_PROGRESS": "pending",
    "PENDIENTE": "pending",
    "EN_PROCESO": "pending",
    # failed
    "FAILED": "failed",
    "FAIL": "failed",
    "ERROR": "failed",
    "FALLIDO": "failed",
    "FALLIDA": "failed",
    "RECHAZADO": "failed",
    # refunded
    "REFUNDED": "refunded",
    "REEMBOLSADO": "refunded",
    "REEMBOLSADA": "refunded",
}

CANONICAL_STATUSES = ("completed", "pending", "failed", "refunded")

# --- Fuentes soportadas ---
SUPPORTED_SOURCES = ("banco_central", "wallet_app", "exchange_crypto")

# --- Reglas de validación ---
MIN_AMOUNT = 0  # monto debe ser estrictamente mayor a 0


# ---------------------------------------------------------------------------
# NUEVO: configuración para detección de fuente y generación de docs
# ---------------------------------------------------------------------------

# --- Firmas de campos por fuente (para detección automática) ---
# Cada fuente tiene un conjunto característico de claves en el JSON crudo.
SOURCE_SIGNATURES = {
    "banco_central": {"id", "amount", "status", "date"},
    "wallet_app": {"tx_id", "monto", "moneda", "estado", "fecha"},
    "exchange_crypto": {"transaction_id", "value", "currency", "state", "timestamp"},
}

# Umbral mínimo de coincidencias para aceptar una fuente detectada
SOURCE_DETECTION_MIN_MATCHES = 2

# Ruta de las skills (para el generador de documentación)
SKILLS_DIR = ".opencode/skills"

# Salida del README generado
REFACTOR_README_PATH = "README.md"
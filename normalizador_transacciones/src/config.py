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
    "PESO": "MXN",       # ambiguo: asumimos MXN por contexto
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
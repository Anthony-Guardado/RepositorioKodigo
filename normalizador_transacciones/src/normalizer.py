"""
Reglas de normalización por fuente + validación.
Cada fuente tiene su propio normalizador porque los campos cambian.
"""

import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from src.config import (
    CURRENCY_ALIASES,
    MIN_AMOUNT,
    STATUS_MAP,
    SUPPORTED_CURRENCIES,
)
from src.models import NormalizedTransaction


# ---------------------------------------------------------------------------
# Helpers de parseo
# ---------------------------------------------------------------------------

_AMOUNT_CLEAN = re.compile(r"[^\d\.\-,]")


def parse_amount(value) -> Decimal | None:
    """Convierte un monto heterogéneo a Decimal. Devuelve None si falla."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return Decimal(str(value))
        except InvalidOperation:
            return None
    if isinstance(value, str):
        limpio = _AMOUNT_CLEAN.sub("", value).replace(",", "")
        # Si quedan dos puntos, asumimos el último como decimal
        if limpio.count(".") > 1:
            limpio = limpio.replace(".", "", limpio.count(".") - 1)
        try:
            return Decimal(limpio)
        except InvalidOperation:
            return None
    return None


def parse_currency(value) -> str | None:
    """Normaliza un código/nombre de moneda a ISO canónico."""
    if not value:
        return None
    s = str(value).strip().upper()
    if s in SUPPORTED_CURRENCIES:
        return s
    if s in CURRENCY_ALIASES:
        return CURRENCY_ALIASES[s]
    return None


def parse_status(value) -> str | None:
    """Mapea cualquier variante de estado a un valor canónico."""
    if not value:
        return None
    key = str(value).strip().upper().replace(" ", "_")
    return STATUS_MAP.get(key)


def parse_timestamp(value) -> datetime | None:
    """Acepta ISO 8601, DD/MM/YYYY y Unix timestamp (int)."""
    if value is None:
        return None

    # Unix timestamp
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(float(value), tz=timezone.utc).replace(tzinfo=None)
        except (OverflowError, OSError, ValueError):
            return None

    s = str(value).strip()

    # ISO 8601 (con o sin hora)
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        pass

    # DD/MM/YYYY
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue

    return None


# ---------------------------------------------------------------------------
# Normalizadores por fuente
# ---------------------------------------------------------------------------

def _normalize_banco_central(raw: dict) -> NormalizedTransaction:
    """Fuente: banco_central. Monto incluye moneda embebida ('1,250.50 USD')."""
    tx_id = raw.get("id")
    amount_raw = raw.get("amount", "")
    currency = None
    amount = None
    if isinstance(amount_raw, str):
        partes = amount_raw.split()
        if len(partes) >= 2:
            amount = parse_amount(partes[0])
            currency = parse_currency(partes[1])
    else:
        amount = parse_amount(amount_raw)

    return NormalizedTransaction(
        id=str(tx_id) if tx_id else "",
        source="banco_central",
        amount=amount,
        currency=currency,
        status=parse_status(raw.get("status")),
        timestamp=parse_timestamp(raw.get("date")),
        raw=raw,
    )


def _normalize_wallet_app(raw: dict) -> NormalizedTransaction:
    """Fuente: wallet_app. Campos en español, monto numérico, fecha DD/MM/YYYY."""
    tx_id = raw.get("tx_id")
    return NormalizedTransaction(
        id=str(tx_id) if tx_id else "",
        source="wallet_app",
        amount=parse_amount(raw.get("monto")),
        currency=parse_currency(raw.get("moneda")),
        status=parse_status(raw.get("estado")),
        timestamp=parse_timestamp(raw.get("fecha")),
        raw=raw,
    )


def _normalize_exchange_crypto(raw: dict) -> NormalizedTransaction:
    """Fuente: exchange_crypto. Campos en inglés, fecha como Unix timestamp."""
    tx_id = raw.get("transaction_id")
    return NormalizedTransaction(
        id=str(tx_id) if tx_id else "",
        source="exchange_crypto",
        amount=parse_amount(raw.get("value")),
        currency=parse_currency(raw.get("currency")),
        status=parse_status(raw.get("state")),
        timestamp=parse_timestamp(raw.get("timestamp")),
        raw=raw,
    )


NORMALIZERS = {
    "banco_central": _normalize_banco_central,
    "wallet_app": _normalize_wallet_app,
    "exchange_crypto": _normalize_exchange_crypto,
}


# ---------------------------------------------------------------------------
# Validación + orquestación
# ---------------------------------------------------------------------------

def validate(tx: NormalizedTransaction) -> None:
    """Marca errores sobre la transacción normalizada (in-place)."""
    if not tx.id:
        tx.errors.append("id vacío")
    if tx.amount is None:
        tx.errors.append("monto no parseable")
    elif tx.amount <= MIN_AMOUNT:
        tx.errors.append(f"monto <= {MIN_AMOUNT}")
    if tx.currency is None:
        tx.errors.append("moneda no reconocida")
    if tx.status is None:
        tx.errors.append("estado no reconocido")
    if tx.timestamp is None:
        tx.errors.append("fecha no parseable")

    tx.is_valid = len(tx.errors) == 0


def normalize_all(raw_transactions: list[dict]) -> list[NormalizedTransaction]:
    """Normaliza y valida la lista completa. No descarta inválidas."""
    resultado: list[NormalizedTransaction] = []
    for raw in raw_transactions:
        source = raw.get("source")
        normalizer = NORMALIZERS.get(source)
        if normalizer is None:
            # Fuente desconocida: la marcamos como inválida
            tx = NormalizedTransaction(
                id=str(raw.get("id", "")),
                source=str(source or "desconocida"),
                amount=None, currency=None, status=None, timestamp=None,
                raw=raw,
            )
            tx.errors.append(f"fuente no soportada: {source}")
            tx.is_valid = False
            resultado.append(tx)
            continue

        tx = normalizer(raw)
        validate(tx)
        resultado.append(tx)

    return resultado
"""
Normalizador de transacciones crudas al modelo canónico.

Skill asociada: normalizar-transaccion
Responsabilidad: ORQUESTAR la normalización. Delega la detección de fuente
a source_detector y la validación a validators.

Este módulo ya NO contiene la lógica de validación (movida a validators.py)
ni la de detección de fuente (movida a source_detector.py).
"""

import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from src.config import CURRENCY_ALIASES, STATUS_MAP, SUPPORTED_CURRENCIES
from src.models import NormalizedTransaction
from src.source_detector import detect_source
from src.validators import validate


# ---------------------------------------------------------------------------
# Helpers de parseo (responsabilidad única de este módulo)
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
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(float(value), tz=timezone.utc).replace(tzinfo=None)
        except (OverflowError, OSError, ValueError):
            return None
    s = str(value).strip()
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        pass
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Normalizadores por fuente (una función por fuente)
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
    """Fuente: wallet_app. Campos en español, fecha DD/MM/YYYY."""
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
    """Fuente: exchange_crypto. Fecha como Unix timestamp."""
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
# Orquestador principal
# ---------------------------------------------------------------------------

def normalize_one(raw: dict) -> NormalizedTransaction:
    """
    Normaliza UNA transacción cruda y la valida.
    Si la fuente es desconocida, la marca como inválida con error explícito.
    """
    source = detect_source(raw)
    normalizer = NORMALIZERS.get(source)

    if normalizer is None:
        tx = NormalizedTransaction(
            id=str(raw.get("id", "")) if isinstance(raw, dict) else "",
            source=source,
            amount=None, currency=None, status=None, timestamp=None,
            raw=raw if isinstance(raw, dict) else {},
        )
        tx.errors.append(f"fuente no soportada: {source}")
        tx.is_valid = False
        return tx

    tx = normalizer(raw)
    validate(tx)
    return tx


def normalize_all(raw_transactions: list[dict]) -> list[NormalizedTransaction]:
    """Normaliza y valida un lote completo. No descarta inválidas."""
    return [normalize_one(raw) for raw in raw_transactions]
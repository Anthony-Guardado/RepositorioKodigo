"""
Modelo normalizado de una transacción.
Todas las fuentes se mapean a esta estructura única.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass
class NormalizedTransaction:
    """Representación canónica de una transacción normalizada."""
    id: str
    source: str
    amount: Decimal | None
    currency: str | None
    status: str | None
    timestamp: datetime | None
    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    def to_row(self) -> dict:
        """Devuelve un dict plano para tablas y exportación."""
        return {
            "id": self.id,
            "source": self.source,
            "amount": f"{self.amount:.2f}" if self.amount is not None else "-",
            "currency": self.currency or "-",
            "status": self.status or "-",
            "timestamp": (
                self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                if self.timestamp else "-"
            ),
            "valid": "OK" if self.is_valid else "ERR",
            "errors": "; ".join(self.errors) if self.errors else "",
        }
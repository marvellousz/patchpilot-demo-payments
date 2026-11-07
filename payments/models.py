from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Payment:
    order_id: str
    amount: Decimal
    currency: str = "USD"


@dataclass(frozen=True)
class PaymentResult:
    order_id: str
    transaction_id: str
    attempts: int


class PaymentError(Exception):
    """The charge could not be completed."""


class PaymentDeclined(PaymentError):
    """The gateway refused the charge."""

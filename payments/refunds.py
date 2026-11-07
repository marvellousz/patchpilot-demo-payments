from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def split_refund(amount: Decimal, installments: int) -> list[Decimal]:
    """Split a refund into equal installments that add up to `amount`."""
    if installments < 1:
        raise ValueError("installments must be at least 1")
    share = (amount / installments).quantize(CENT, rounding=ROUND_HALF_UP)
    return [share] * installments


def remaining_refundable(paid: Decimal, refunds: list[Decimal]) -> Decimal:
    """How much of a payment can still be refunded."""
    remaining = paid - sum(refunds, Decimal("0"))
    if remaining < 0:
        raise ValueError("refunds exceed the amount paid")
    return remaining

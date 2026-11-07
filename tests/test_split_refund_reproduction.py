import pytest
from decimal import Decimal
from payments.refunds import split_refund

@pytest.mark.parametrize("amount,installments,expected", [
    (Decimal("10.00"), 3, [Decimal("3.33"), Decimal("3.33"), Decimal("3.34")]),
    (Decimal("20.00"), 3, [Decimal("6.67"), Decimal("6.67"), Decimal("6.66")]),
])
def test_split_refund_adds_up(amount, installments, expected):
    result = split_refund(amount, installments)
    assert result == expected
    assert sum(result, Decimal("0")) == amount

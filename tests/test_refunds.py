from decimal import Decimal

import pytest

from payments.refunds import remaining_refundable, split_refund


def test_split_evenly():
    assert split_refund(Decimal("9.00"), 3) == [Decimal("3.00")] * 3


def test_single_installment():
    assert split_refund(Decimal("12.34"), 1) == [Decimal("12.34")]


def test_installments_must_be_positive():
    with pytest.raises(ValueError):
        split_refund(Decimal("5.00"), 0)


def test_remaining_refundable():
    assert remaining_refundable(Decimal("50.00"), [Decimal("10.00"), Decimal("5.50")]) == Decimal("34.50")


def test_refunds_cannot_exceed_payment():
    with pytest.raises(ValueError):
        remaining_refundable(Decimal("10.00"), [Decimal("10.01")])

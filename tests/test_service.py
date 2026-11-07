from dataclasses import replace
from decimal import Decimal

import pytest

from payments.models import PaymentDeclined, PaymentError
from payments.service import PaymentService

SUCCESS = {"status": "SUCCESS", "transaction_id": "txn_1"}
PENDING = {"status": "PENDING"}


def test_charge_succeeds_first_try(payment, scripted_gateway):
    gateway = scripted_gateway(SUCCESS)
    result = PaymentService(gateway).process(payment)
    assert result.transaction_id == "txn_1"
    assert result.attempts == 1


def test_declined_charge_raises(payment, scripted_gateway):
    gateway = scripted_gateway({"status": "DECLINED", "reason": "insufficient funds"})
    with pytest.raises(PaymentDeclined, match="insufficient funds"):
        PaymentService(gateway).process(payment)


def test_pending_is_retried(payment, scripted_gateway):
    gateway = scripted_gateway(PENDING, SUCCESS)
    result = PaymentService(gateway).process(payment)
    assert result.attempts == 2


def test_gives_up_after_max_retries(payment, scripted_gateway):
    gateway = scripted_gateway(PENDING, PENDING, PENDING)
    with pytest.raises(PaymentError):
        PaymentService(gateway, max_retries=2).process(payment)
    assert gateway.calls == 3


def test_rejects_non_positive_amount(payment, scripted_gateway):
    with pytest.raises(ValueError):
        PaymentService(scripted_gateway()).process(replace(payment, amount=Decimal("0")))

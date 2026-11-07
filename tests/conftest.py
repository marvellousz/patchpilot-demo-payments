from decimal import Decimal

import pytest

from payments.models import Payment


class ScriptedGateway:
    """Fake gateway that replays a fixed sequence of replies."""

    def __init__(self, *replies):
        self.replies = list(replies)
        self.calls = 0

    def charge(self, payment):
        self.calls += 1
        return self.replies.pop(0)


@pytest.fixture
def payment():
    return Payment(order_id="ord_123", amount=Decimal("49.99"))


@pytest.fixture
def scripted_gateway():
    return ScriptedGateway

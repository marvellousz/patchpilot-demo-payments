import pytest
from payments.models import PaymentError
from payments.service import PaymentService

# Use the existing scripted_gateway fixture but supply None to simulate a timeout


def test_gateway_timeout_is_retried_and_gives_up(payment, scripted_gateway):
    # gateway returns None (timeout) three times, then stops
    gateway = scripted_gateway(None, None, None)
    with pytest.raises(PaymentError):
        PaymentService(gateway, max_retries=2).process(payment)
    # After 3 attempts it should raise PaymentError
    assert gateway.calls == 3


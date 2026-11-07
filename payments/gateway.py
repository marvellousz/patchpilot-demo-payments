"""Client for the upstream card gateway."""

import json
import socket
import urllib.request

from payments.models import Payment


class HttpGateway:
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def charge(self, payment: Payment) -> dict | None:
        """Return the gateway's JSON reply, or None if it did not answer in time."""
        body = json.dumps(
            {
                "order_id": payment.order_id,
                "amount": str(payment.amount),
                "currency": payment.currency,
            }
        ).encode()
        request = urllib.request.Request(
            f"{self.base_url}/charges",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except (socket.timeout, TimeoutError):
            return None

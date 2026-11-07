from decimal import Decimal

from payments.models import Payment, PaymentDeclined, PaymentError, PaymentResult


class PaymentService:
    def __init__(self, gateway, max_retries: int = 2):
        self.gateway = gateway
        self.max_retries = max_retries

    def process(self, payment: Payment) -> PaymentResult:
        if payment.amount <= Decimal("0"):
            raise ValueError("amount must be positive")

        for attempt in range(1, self.max_retries + 2):
            resp = self.gateway.charge(payment)
            # Treat a missing response as pending; gateway may not have answered yet.
            if resp is None or resp.get("status") == "PENDING":
                continue
            if resp["status"] == "SUCCESS":
                return PaymentResult(payment.order_id, resp["transaction_id"], attempt)
            if resp["status"] == "DECLINED":
                raise PaymentDeclined(resp.get("reason", "declined"))
            # PENDING: the gateway is still deciding, ask again

        raise PaymentError(f"gateway did not confirm order {payment.order_id}")

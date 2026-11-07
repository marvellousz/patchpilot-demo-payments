# payments

Checkout payment service: charges cards through the upstream gateway, retrying while the gateway
reports `PENDING`.

```bash
pip install -e ".[dev]"
pytest
```

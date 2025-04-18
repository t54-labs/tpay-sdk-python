# TPay SDK

A Python SDK for payment processing and agent tracking.

## Installation

```bash
pip install tpay-sdk
```

## Quick Start

```python
from tpay import tpay_initialize, TPayAgent

# Initialize TPay
tpay_initialize(api_key="your-api-key", api_secret="your-api-secret")

# Create TPayAgent instance
agent = TPayAgent()

# Create a payment
payment = agent.create_payment(
    receiving_agent_id="recipient123",
    payment_amount=100.0,
    currency="USDT",
    settlement_network="solana"
)

print(f"Payment created: {payment['id']}")
```

## Features

- Payment processing
- Agent tracking
- OpenAI integration
- Context-aware tool verification

## Documentation

For more information, see the [documentation](docs/).

## License

MIT

# UCP Merchant Agent Skill

Build Python-based A2A agents that integrate with UCP (Universal Commerce Protocol) merchants for agentic commerce.

## Quick Start

### 1. Create a New Agent

```bash
python scripts/create_ucp_agent.py my-shopping-agent --path ./agents
cd agents/my-shopping-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your agent profile URL
```

### 4. Run the Agent

```bash
python main.py
```

### 5. Test Health Endpoint

```bash
curl http://localhost:8000/health
```

## What is UCP?

UCP (Universal Commerce Protocol) is an open standard for agentic commerce developed by Google with Shopify, Stripe, Visa, Mastercard, and 20+ partners. It enables AI agents to:

- Discover merchant capabilities
- Manage checkout sessions
- Process payments autonomously
- Handle order fulfillment

## Key Features

- **Profile-Based Discovery**: Merchants publish capabilities at `/.well-known/ucp`
- **Capability Negotiation**: Agents and merchants compute capability intersection
- **Payment Handlers**: Support for Google Pay, direct tokenization, and AP2 mandates
- **Date-Based Versioning**: Current version `2026-01-11`

## Documentation

- [SKILL.md](SKILL.md) - Complete skill documentation with workflows
- [references/ucp_protocol.md](references/ucp_protocol.md) - UCP specification reference
- [references/checkout_patterns.md](references/checkout_patterns.md) - Checkout session patterns
- [references/payment_handlers.md](references/payment_handlers.md) - Payment integration patterns

## Example Usage

```python
from ucp_client import UCPClient

# Initialize client with your agent profile
ucp = UCPClient(agent_profile_url="https://my-agent.example/profile.json")

# Discover merchant
merchant = await ucp.discover("https://merchant.example")
print(f"Merchant: {merchant.name}")
print(f"Capabilities: {merchant.capabilities}")

# Create checkout session
session = await ucp.create_checkout(
    merchant_url="https://merchant.example",
    line_items=[
        {"sku": "PROD-001", "quantity": 1, "price_cents": 2999}
    ]
)

# Complete checkout
order = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={"handler_id": "...", "credential": "..."}
)
```

## External Resources

- [UCP Official Documentation](https://ucp.dev/)
- [UCP Specification](https://ucp.dev/specification/overview)
- [Google Developers UCP Guide](https://developers.google.com/merchant/ucp)
- [UCP GitHub Repository](https://github.com/Universal-Commerce-Protocol/ucp)

## Requirements

- Python 3.10+
- FastAPI
- httpx
- pydantic
- a2a-sdk

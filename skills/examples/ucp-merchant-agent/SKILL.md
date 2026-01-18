---
name: ucp-merchant-agent
description: Comprehensive toolkit for building Python-based A2A agents that interact with UCP (Universal Commerce Protocol) merchant agents. Use when creating shopping agents, integrating with UCP merchants, managing checkout sessions, or implementing payment flows. Triggers include "ucp", "universal commerce protocol", "shopping agent", "merchant agent", "checkout session", "agentic commerce", or when building agents that need to purchase from online stores.
---

# UCP Merchant Agent Development Skill

Build production-ready A2A agents that integrate with UCP (Universal Commerce Protocol) merchants for agentic commerce, including discovery, checkout, and payment flows.

## Workflow Decision Tree

Use this decision tree to determine the workflow:

**1. Creating a new UCP shopping agent?**
   → Use [Create UCP Agent](#create-ucp-agent) workflow

**2. Discovering merchant capabilities?**
   → Use [Discover Merchant](#discover-merchant) workflow

**3. Managing checkout sessions?**
   → Use [Checkout Session](#checkout-session) workflow

**4. Handling payments?**
   → Use [Payment Integration](#payment-integration) workflow

**5. Need reference patterns or examples?**
   → Read [references/ucp_protocol.md](references/ucp_protocol.md), [references/checkout_patterns.md](references/checkout_patterns.md), or [references/payment_handlers.md](references/payment_handlers.md)

## Create UCP Agent

Use the `create_ucp_agent.py` script to scaffold a new agent:

```bash
python scripts/create_ucp_agent.py <agent-name> [--path <output-path>]
```

**Example:**
```bash
python scripts/create_ucp_agent.py my-shopping-agent --path ./agents
```

**After creation:**
1. Navigate to agent directory: `cd agents/my-shopping-agent`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment: `cp .env.example .env`
4. Run agent: `python main.py`
5. Test health endpoint: `curl http://localhost:8000/health`

**Template files:**
- Basic template: `templates/basic-shopping-agent/`

## Discover Merchant

Discover and negotiate capabilities with UCP merchants.

### Fetch Merchant Profile

Every UCP merchant publishes their capabilities at `/.well-known/ucp`:

```python
from ucp_client import UCPClient

ucp = UCPClient(agent_profile_url="https://my-agent.example/profile.json")

# Discover merchant capabilities
merchant = await ucp.discover("https://merchant.example")
print(f"Merchant: {merchant.name}")
print(f"Capabilities: {merchant.capabilities}")
print(f"Endpoint: {merchant.rest_endpoint}")
```

### Negotiate Capabilities

The agent and merchant compute capability intersection:

```python
# Automatic negotiation happens on first request
# Or explicitly negotiate:
negotiated = await ucp.negotiate(merchant)

if "dev.ucp.shopping.checkout" in negotiated.capabilities:
    print("Checkout capability available")

if "dev.ucp.shopping.fulfillment" in negotiated.extensions:
    print("Fulfillment extension supported")
```

### Profile Advertisement

Your agent must advertise its profile in requests:

```python
# UCP-Agent header is automatically added by UCPClient
# Profile URL is configured in UCPClient initialization

# For manual requests:
headers = {
    "UCP-Agent": f'profile="{agent_profile_url}"',
    "Content-Type": "application/json"
}
```

**For detailed protocol information, read:**
- `references/ucp_protocol.md` - Profile structure, discovery, negotiation

## Checkout Session

Manage the complete checkout lifecycle.

### Create Session

```python
from models import LineItem

# Create checkout session
session = await ucp.create_checkout(
    merchant_url="https://merchant.example",
    line_items=[
        LineItem(sku="PROD-001", quantity=1, price_cents=2999),
        LineItem(sku="PROD-002", quantity=2, price_cents=1499)
    ]
)

print(f"Session ID: {session.id}")
print(f"Status: {session.status}")  # "incomplete"
print(f"Subtotal: ${session.subtotal_cents / 100:.2f}")
```

### Update Session

```python
# Add shipping address
session = await ucp.update_checkout(
    session_id=session.id,
    shipping_address={
        "name": "John Doe",
        "line1": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "postal_code": "94102",
        "country": "US"
    }
)

# Tax is automatically calculated
print(f"Tax: ${session.tax_cents / 100:.2f}")
print(f"Total: ${session.total_cents / 100:.2f}")

# Add/remove items
session = await ucp.update_checkout(
    session_id=session.id,
    line_items=[
        LineItem(sku="PROD-001", quantity=2)  # Update quantity
    ]
)

# Apply discount code
session = await ucp.update_checkout(
    session_id=session.id,
    discount_code="SAVE10"
)
```

### Complete Checkout

```python
# Complete with payment data
order = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={
        "handler_id": "google-pay-handler-id",
        "type": "card",
        "brand": "visa",
        "last_digits": "4242",
        "credential": {
            "type": "PAYMENT_GATEWAY",
            "token": "{encrypted_token}"
        }
    }
)

print(f"Order ID: {order.id}")
print(f"Status: {order.status}")  # "confirmed"
```

### Session Lifecycle

```
┌─────────────┐   create    ┌────────────┐   update   ┌────────────┐
│   (start)   │ ─────────▶  │ incomplete │ ─────────▶ │ incomplete │
└─────────────┘             └────────────┘            └────────────┘
                                                            │
                                                    complete│
                                                            ▼
                                                     ┌────────────┐
                                                     │ confirmed  │
                                                     └────────────┘
```

**For checkout patterns, read:**
- `references/checkout_patterns.md` - Session management, cart operations

## Payment Integration

Handle payment processing with UCP payment handlers.

### Supported Payment Handlers

UCP supports multiple payment handler types:

1. **Digital Wallets** (Google Pay, Apple Pay)
2. **Direct Tokenization** with 3DS support
3. **AP2 Mandates** for autonomous agents

### Google Pay Integration

```python
# Get merchant's payment handlers
handlers = session.payment_handlers

for handler in handlers:
    if handler.type == "com.google.pay":
        # Get merchant config for Google Pay
        gpay_config = handler.config

        # Call Google Pay API with config
        # (Client-side in browser/app)
        gpay_token = await get_gpay_token(gpay_config)

        # Complete with token
        order = await ucp.complete_checkout(
            session_id=session.id,
            payment_data={
                "handler_id": handler.id,
                "credential": gpay_token
            }
        )
```

### Direct Tokenization with 3DS

```python
# For handlers requiring 3DS verification
order_result = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={
        "handler_id": handler.id,
        "credential": card_token
    }
)

if order_result.status == "requires_3ds":
    # Redirect user to 3DS verification
    verification_url = order_result.continue_url

    # After verification, order completes automatically
```

### AP2 Mandates (Autonomous Agents)

For agents acting autonomously with pre-authorized payment mandates:

```python
from ucp_client import create_ap2_mandate

# Create cryptographic mandate
mandate = create_ap2_mandate(
    agent_private_key=private_key,
    checkout_terms=session.terms,
    amount_cents=session.total_cents,
    currency="USD"
)

# Complete with mandate
order = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={
        "handler_id": ap2_handler.id,
        "credential": mandate.token
    },
    ap2={
        "checkout_mandate": mandate.signed_mandate
    }
)
```

**For payment patterns, read:**
- `references/payment_handlers.md` - Handler types, 3DS, AP2 mandates

## Key Concepts

### Agent Profile Structure

Your agent must publish a profile for capability negotiation:

```json
{
  "ucp": {
    "version": "2026-01-11",
    "capabilities": [
      {
        "name": "dev.ucp.shopping.checkout",
        "version": "2026-01-11"
      }
    ],
    "payment_handlers": [
      "com.google.pay",
      "dev.ucp.ap2"
    ]
  },
  "agent": {
    "name": "My Shopping Agent",
    "description": "AI shopping assistant"
  }
}
```

### UCP Versioning

UCP uses date-based versioning (`YYYY-MM-DD`):

```python
# Check version compatibility
if merchant.ucp_version > agent.ucp_version:
    # Merchant may use features agent doesn't support
    # Agent should upgrade or handle gracefully
    pass

# Current version
UCP_VERSION = "2026-01-11"
```

### Error Handling

Handle UCP-specific errors:

```python
from ucp_client import UCPError, VersionError, CapabilityError

try:
    session = await ucp.create_checkout(...)
except VersionError as e:
    print(f"Version mismatch: {e.required_version}")
except CapabilityError as e:
    print(f"Capability not supported: {e.capability}")
except UCPError as e:
    print(f"UCP error: {e.code} - {e.message}")
```

### Response Format

All UCP responses include metadata:

```json
{
  "ucp": {
    "version": "2026-01-11",
    "capabilities": [
      {"name": "dev.ucp.shopping.checkout", "version": "2026-01-11"}
    ]
  },
  "id": "checkout_123",
  "status": "incomplete",
  "line_items": [...]
}
```

## Handler Patterns

Implement A2A handlers for UCP operations:

### Discovery Handler

```python
@a2a_server.handler("shop.discover")
async def handle_discover(request: DiscoverRequest, context: Context):
    """Discover merchant capabilities."""
    merchant = await ucp.discover(request.merchant_url)

    return DiscoverResponse(
        merchant_name=merchant.name,
        capabilities=[c.name for c in merchant.capabilities],
        payment_handlers=[h.type for h in merchant.payment_handlers]
    )
```

### Add to Cart Handler

```python
@a2a_server.handler("shop.add_to_cart")
async def handle_add_to_cart(request: AddToCartRequest, context: Context):
    """Add items to checkout session."""

    if not request.session_id:
        # Create new session
        session = await ucp.create_checkout(
            merchant_url=request.merchant_url,
            line_items=request.items
        )
    else:
        # Update existing session
        session = await ucp.update_checkout(
            session_id=request.session_id,
            line_items=request.items
        )

    return CartResponse(
        session_id=session.id,
        items=session.line_items,
        subtotal_cents=session.subtotal_cents
    )
```

### Checkout Handler

```python
@a2a_server.handler("shop.checkout")
async def handle_checkout(request: CheckoutRequest, context: Context):
    """Complete checkout with payment."""

    order = await ucp.complete_checkout(
        session_id=request.session_id,
        payment_data=request.payment_data,
        shipping_address=request.shipping_address
    )

    return CheckoutResponse(
        order_id=order.id,
        status=order.status,
        confirmation_number=order.confirmation_number
    )
```

## Resources

### Scripts (`scripts/`)
- `create_ucp_agent.py` - Scaffold new UCP shopping agents

### References (`references/`)
- `ucp_protocol.md` - UCP specification, discovery, negotiation
- `checkout_patterns.md` - Session management, cart operations
- `payment_handlers.md` - Payment integration, 3DS, AP2 mandates

### Templates (`templates/`)
- `basic-shopping-agent/` - Minimal UCP agent template

## Common Patterns

### Multi-Merchant Shopping

```python
# Discover multiple merchants
merchants = await asyncio.gather(*[
    ucp.discover(url) for url in merchant_urls
])

# Find best price across merchants
best_offer = None
for merchant in merchants:
    if "dev.ucp.shopping.checkout" in merchant.capabilities:
        price = await get_product_price(merchant, product_sku)
        if not best_offer or price < best_offer.price:
            best_offer = Offer(merchant=merchant, price=price)
```

### Session State Management

```python
# Store sessions in Redis for production
import redis

async def save_session(user_id: str, session: CheckoutSession):
    await redis.set(
        f"ucp:session:{user_id}",
        session.model_dump_json(),
        ex=3600  # 1 hour TTL
    )

async def get_session(user_id: str) -> CheckoutSession | None:
    data = await redis.get(f"ucp:session:{user_id}")
    if data:
        return CheckoutSession.model_validate_json(data)
    return None
```

### Handling Escalations

```python
# Some operations require human intervention
if session.status == "requires_escalation":
    for message in session.messages:
        if message.severity == "requires_buyer_input":
            # Escalate to user
            return EscalationResponse(
                reason=message.message,
                continue_url=session.continue_url
            )
```

## Troubleshooting

**Discovery fails:**
- Verify merchant URL is correct
- Check if `/.well-known/ucp` is accessible
- Ensure HTTPS is used

**Capability negotiation fails:**
- Update agent profile with required capabilities
- Check UCP version compatibility
- Review merchant's supported capabilities

**Checkout session errors:**
- Verify session hasn't expired (typically 15-30 min)
- Check all required fields are provided
- Review error messages in response

**Payment fails:**
- Verify payment handler is supported by both parties
- Check credential format matches handler spec
- For 3DS, ensure redirect URL is handled

**Version mismatch:**
- Update agent to support newer UCP version
- Check protocol changelog for breaking changes
- Implement graceful degradation

## External Resources

- [UCP Official Documentation](https://ucp.dev/)
- [UCP Specification](https://ucp.dev/specification/overview)
- [UCP GitHub Repository](https://github.com/Universal-Commerce-Protocol/ucp)
- [Google Developers UCP Guide](https://developers.google.com/merchant/ucp)

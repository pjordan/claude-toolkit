# Checkout Patterns Reference

Patterns and best practices for managing UCP checkout sessions.

## Session Lifecycle

```
┌─────────────┐   create    ┌────────────┐   update   ┌────────────┐
│   (start)   │ ─────────▶  │ incomplete │ ─────────▶ │ incomplete │
└─────────────┘             └────────────┘            └────────────┘
                                                            │
                                                    complete│
                                                            ▼
                           ┌────────────┐           ┌────────────┐
                           │  expired   │◀──timeout─│ incomplete │
                           └────────────┘           └────────────┘
                                                            │
                                                    complete│
                                                            ▼
                           ┌────────────┐           ┌────────────┐
                           │  requires  │◀──────────│ processing │
                           │    3ds     │           └────────────┘
                           └────────────┘                   │
                                 │                          │
                             verify│                    success│
                                 ▼                          ▼
                           ┌────────────┐           ┌────────────┐
                           │ processing │──────────▶│ confirmed  │
                           └────────────┘           └────────────┘
```

## Creating Sessions

### Basic Session Creation

```python
from models import LineItem

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

### Session with Initial Data

```python
session = await ucp.create_checkout(
    merchant_url="https://merchant.example",
    line_items=[
        LineItem(sku="PROD-001", quantity=1, price_cents=2999)
    ],
    shipping_address={
        "name": "John Doe",
        "line1": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "postal_code": "94102",
        "country": "US"
    },
    email="john@example.com"
)
```

## Updating Sessions

### Add/Update Items

```python
# Add new item
session = await ucp.update_checkout(
    session_id=session.id,
    line_items=[
        LineItem(sku="PROD-003", quantity=1, price_cents=999)
    ]
)

# Update quantity
session = await ucp.update_checkout(
    session_id=session.id,
    line_items=[
        LineItem(sku="PROD-001", quantity=3)  # Change quantity to 3
    ]
)

# Remove item (set quantity to 0)
session = await ucp.update_checkout(
    session_id=session.id,
    line_items=[
        LineItem(sku="PROD-002", quantity=0)
    ]
)
```

### Add Shipping Address

```python
session = await ucp.update_checkout(
    session_id=session.id,
    shipping_address={
        "name": "John Doe",
        "line1": "123 Main St",
        "line2": "Apt 4B",
        "city": "San Francisco",
        "state": "CA",
        "postal_code": "94102",
        "country": "US"
    }
)

# Tax is automatically calculated
print(f"Tax: ${session.tax_cents / 100:.2f}")
print(f"Total: ${session.total_cents / 100:.2f}")
```

### Apply Discount Code

```python
session = await ucp.update_checkout(
    session_id=session.id,
    discount_code="SAVE10"
)

if session.discount_cents > 0:
    print(f"Discount applied: -${session.discount_cents / 100:.2f}")
else:
    print("Discount code not valid")
```

### Select Shipping Method

```python
# Get available shipping options
shipping_options = session.shipping_options

for option in shipping_options:
    print(f"{option.id}: {option.name} - ${option.price_cents / 100:.2f}")
    print(f"  Estimated: {option.estimated_days} days")

# Select shipping method
session = await ucp.update_checkout(
    session_id=session.id,
    shipping_method_id=shipping_options[0].id
)
```

## Session Data Model

### CheckoutSession

```python
@dataclass
class CheckoutSession:
    id: str
    status: str  # "incomplete", "processing", "confirmed", "expired"
    merchant_url: str

    # Line items
    line_items: list[LineItem]

    # Pricing
    subtotal_cents: int
    tax_cents: int
    shipping_cents: int
    discount_cents: int
    total_cents: int
    currency: str  # "USD"

    # Customer info
    email: str | None
    shipping_address: Address | None
    billing_address: Address | None

    # Shipping
    shipping_options: list[ShippingOption]
    selected_shipping_method: str | None

    # Payment
    payment_handlers: list[PaymentHandler]

    # Metadata
    created_at: datetime
    expires_at: datetime
    messages: list[Message]
```

### LineItem

```python
@dataclass
class LineItem:
    sku: str
    quantity: int
    price_cents: int | None = None
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
```

## Completing Checkout

### Basic Completion

```python
order = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={
        "handler_id": handler.id,
        "type": "card",
        "brand": "visa",
        "last_digits": "4242",
        "credential": {
            "type": "PAYMENT_GATEWAY",
            "token": encrypted_token
        }
    }
)

print(f"Order ID: {order.id}")
print(f"Status: {order.status}")
print(f"Confirmation: {order.confirmation_number}")
```

### Handling 3DS Verification

```python
result = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={...}
)

if result.status == "requires_3ds":
    # Redirect user to 3DS verification
    verification_url = result.continue_url

    # After user completes verification, check status
    order = await ucp.get_order(result.order_id)
```

## Session Expiration

Sessions typically expire after 15-30 minutes of inactivity.

### Checking Expiration

```python
from datetime import datetime, timezone

if session.expires_at < datetime.now(timezone.utc):
    # Session expired, create new one
    session = await ucp.create_checkout(...)
```

### Handling Expiration Gracefully

```python
try:
    order = await ucp.complete_checkout(session_id=session.id, ...)
except UCPError as e:
    if e.code == "session_expired":
        # Recreate session with same items
        session = await ucp.create_checkout(
            merchant_url=merchant_url,
            line_items=previous_items
        )
```

## Session State Management

### Storing Sessions

```python
import redis.asyncio as redis

redis_client = redis.Redis()

async def save_session(user_id: str, session: CheckoutSession):
    """Persist session for user."""
    await redis_client.set(
        f"ucp:session:{user_id}",
        session.model_dump_json(),
        ex=3600  # 1 hour TTL
    )

async def get_session(user_id: str) -> CheckoutSession | None:
    """Retrieve user's session."""
    data = await redis_client.get(f"ucp:session:{user_id}")
    if data:
        return CheckoutSession.model_validate_json(data)
    return None

async def clear_session(user_id: str):
    """Clear user's session after completion."""
    await redis_client.delete(f"ucp:session:{user_id}")
```

### Session Locking

Prevent concurrent modifications:

```python
async def update_session_safely(user_id: str, updates: dict):
    """Update session with locking."""
    lock_key = f"ucp:session:{user_id}:lock"

    # Acquire lock
    lock = await redis_client.set(lock_key, "1", nx=True, ex=30)
    if not lock:
        raise UCPError("session_locked", "Session is being modified")

    try:
        session = await get_session(user_id)
        session = await ucp.update_checkout(session.id, **updates)
        await save_session(user_id, session)
        return session
    finally:
        await redis_client.delete(lock_key)
```

## Cart Patterns

### Shopping Cart Service

```python
class CartService:
    def __init__(self, ucp_client: UCPClient, redis: Redis):
        self.ucp = ucp_client
        self.redis = redis

    async def add_item(self, user_id: str, merchant_url: str, item: LineItem):
        """Add item to cart."""
        session = await self.get_or_create_session(user_id, merchant_url)

        # Merge with existing items
        items = list(session.line_items)
        existing = next((i for i in items if i.sku == item.sku), None)

        if existing:
            existing.quantity += item.quantity
        else:
            items.append(item)

        session = await self.ucp.update_checkout(
            session_id=session.id,
            line_items=items
        )

        await self.save_session(user_id, session)
        return session

    async def remove_item(self, user_id: str, sku: str):
        """Remove item from cart."""
        session = await self.get_session(user_id)
        if not session:
            raise UCPError("no_session", "No active cart")

        session = await self.ucp.update_checkout(
            session_id=session.id,
            line_items=[LineItem(sku=sku, quantity=0)]
        )

        await self.save_session(user_id, session)
        return session

    async def get_cart(self, user_id: str) -> CheckoutSession | None:
        """Get current cart."""
        return await self.get_session(user_id)

    async def checkout(self, user_id: str, payment_data: dict):
        """Complete checkout."""
        session = await self.get_session(user_id)
        if not session:
            raise UCPError("no_session", "No active cart")

        order = await self.ucp.complete_checkout(
            session_id=session.id,
            payment_data=payment_data
        )

        await self.clear_session(user_id)
        return order
```

## Multi-Merchant Carts

### Separate Sessions Per Merchant

```python
async def add_to_multi_cart(
    user_id: str,
    merchant_url: str,
    item: LineItem
):
    """Manage separate sessions per merchant."""
    # Key includes merchant for multi-merchant support
    session_key = f"ucp:session:{user_id}:{merchant_url}"

    session_data = await redis.get(session_key)
    if session_data:
        session = CheckoutSession.model_validate_json(session_data)
    else:
        session = await ucp.create_checkout(
            merchant_url=merchant_url,
            line_items=[item]
        )

    # Update and save
    session = await ucp.update_checkout(session.id, line_items=[item])
    await redis.set(session_key, session.model_dump_json(), ex=3600)

    return session

async def get_all_carts(user_id: str) -> list[CheckoutSession]:
    """Get all merchant carts for user."""
    pattern = f"ucp:session:{user_id}:*"
    keys = await redis.keys(pattern)

    sessions = []
    for key in keys:
        data = await redis.get(key)
        if data:
            sessions.append(CheckoutSession.model_validate_json(data))

    return sessions
```

## Handling Messages

Sessions may include messages from the merchant:

```python
for message in session.messages:
    if message.severity == "info":
        print(f"ℹ️ {message.message}")
    elif message.severity == "warning":
        print(f"⚠️ {message.message}")
    elif message.severity == "requires_buyer_input":
        # Escalate to user
        return EscalationResponse(
            reason=message.message,
            continue_url=session.continue_url
        )
```

## Best Practices

1. **Validate Before Update**: Check session status before modifications
2. **Handle Expiration**: Implement session recovery logic
3. **Use Idempotency**: Retry-safe operations prevent duplicates
4. **Store Minimally**: Only persist essential session data
5. **Clean Up**: Remove completed/expired sessions promptly
6. **Log Transitions**: Track session state changes for debugging

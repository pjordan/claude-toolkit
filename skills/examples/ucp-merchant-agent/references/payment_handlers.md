# Payment Handlers Reference

Patterns and integration guides for UCP payment handlers.

## Overview

UCP supports multiple payment handler types to accommodate different scenarios:

| Handler Type | Use Case |
|--------------|----------|
| Digital Wallets | Consumer-facing with Google Pay, Apple Pay |
| Direct Tokenization | Card tokenization with 3DS support |
| AP2 Mandates | Autonomous agent transactions |

## Payment Handler Structure

### Handler in Merchant Profile

```json
{
  "payment_handlers": [
    {
      "id": "handler_gpay_123",
      "type": "com.google.pay",
      "config": {
        "merchantId": "BCR2DN4XXXXX",
        "merchantName": "Example Store",
        "gatewayMerchantId": "exampleGatewayMerchantId"
      }
    },
    {
      "id": "handler_direct_456",
      "type": "dev.ucp.direct_tokenization",
      "config": {
        "gateway": "stripe",
        "publishable_key": "pk_live_XXXXX",
        "supports_3ds": true
      }
    },
    {
      "id": "handler_ap2_789",
      "type": "dev.ucp.ap2",
      "config": {
        "mandate_required": true,
        "max_amount_cents": 100000
      }
    }
  ]
}
```

### Handler in Checkout Session

```python
for handler in session.payment_handlers:
    print(f"ID: {handler.id}")
    print(f"Type: {handler.type}")
    print(f"Config: {handler.config}")
```

## Google Pay Integration

### Configuration

```python
# Get Google Pay handler from session
gpay_handler = next(
    (h for h in session.payment_handlers if h.type == "com.google.pay"),
    None
)

if gpay_handler:
    gpay_config = gpay_handler.config
```

### Payment Request (Client-Side)

```javascript
// Browser/App code
const paymentDataRequest = {
  apiVersion: 2,
  apiVersionMinor: 0,
  allowedPaymentMethods: [{
    type: 'CARD',
    parameters: {
      allowedAuthMethods: ['PAN_ONLY', 'CRYPTOGRAM_3DS'],
      allowedCardNetworks: ['VISA', 'MASTERCARD']
    },
    tokenizationSpecification: {
      type: 'PAYMENT_GATEWAY',
      parameters: {
        gateway: gpayConfig.gateway,
        gatewayMerchantId: gpayConfig.gatewayMerchantId
      }
    }
  }],
  merchantInfo: {
    merchantId: gpayConfig.merchantId,
    merchantName: gpayConfig.merchantName
  },
  transactionInfo: {
    totalPriceStatus: 'FINAL',
    totalPrice: session.total_cents / 100,
    currencyCode: session.currency
  }
};

const paymentData = await paymentsClient.loadPaymentData(paymentDataRequest);
```

### Completing Checkout

```python
# After receiving Google Pay token
order = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={
        "handler_id": gpay_handler.id,
        "type": "card",
        "brand": payment_data["paymentMethodData"]["info"]["cardNetwork"].lower(),
        "last_digits": payment_data["paymentMethodData"]["info"]["cardDetails"],
        "credential": {
            "type": "PAYMENT_GATEWAY",
            "token": payment_data["paymentMethodData"]["tokenizationData"]["token"]
        }
    }
)
```

## Apple Pay Integration

### Configuration

```python
apple_pay_handler = next(
    (h for h in session.payment_handlers if h.type == "com.apple.pay"),
    None
)
```

### Payment Request (Client-Side)

```javascript
// Safari/iOS code
const paymentRequest = {
  countryCode: 'US',
  currencyCode: session.currency,
  supportedNetworks: ['visa', 'masterCard', 'amex'],
  merchantCapabilities: ['supports3DS'],
  total: {
    label: applePayConfig.merchantName,
    amount: (session.total_cents / 100).toFixed(2)
  }
};

const session = new ApplePaySession(3, paymentRequest);
session.onpaymentauthorized = (event) => {
  const token = event.payment.token;
  // Send token to agent
};
session.begin();
```

### Completing Checkout

```python
order = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={
        "handler_id": apple_pay_handler.id,
        "type": "card",
        "brand": token["paymentMethod"]["network"].lower(),
        "credential": {
            "type": "APPLE_PAY",
            "token": token["paymentData"]
        }
    }
)
```

## Direct Tokenization

For scenarios where you handle card details directly.

### Configuration

```python
direct_handler = next(
    (h for h in session.payment_handlers if h.type == "dev.ucp.direct_tokenization"),
    None
)

# Check 3DS support
supports_3ds = direct_handler.config.get("supports_3ds", False)
```

### Stripe Integration Example

```javascript
// Client-side tokenization
const stripe = Stripe(directHandler.config.publishable_key);

const { token, error } = await stripe.createToken(cardElement);
if (error) {
  // Handle error
} else {
  // Send token.id to agent
}
```

### Completing Without 3DS

```python
order = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={
        "handler_id": direct_handler.id,
        "type": "card",
        "brand": "visa",
        "last_digits": "4242",
        "credential": {
            "type": "CARD_TOKEN",
            "token": stripe_token_id
        }
    }
)
```

### Handling 3DS Verification

```python
result = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={
        "handler_id": direct_handler.id,
        "type": "card",
        "brand": "visa",
        "last_digits": "4242",
        "credential": {
            "type": "CARD_TOKEN",
            "token": stripe_token_id
        }
    }
)

if result.status == "requires_3ds":
    # 3DS verification required
    verification_url = result.continue_url

    # Option 1: Redirect user
    return RedirectResponse(verification_url)

    # Option 2: Use Stripe.js for inline verification
    # const { error } = await stripe.confirmCardPayment(result.client_secret)

# After 3DS completion
order = await ucp.get_order(result.order_id)
if order.status == "confirmed":
    print("Payment successful!")
```

## AP2 Mandates (Autonomous Agents)

AP2 (Agent Payment Protocol 2) enables agents to make purchases autonomously with cryptographically-signed mandates.

### Prerequisites

1. Agent has a registered key pair
2. User has pre-authorized payment mandates
3. Merchant supports AP2 handler

### Mandate Structure

```json
{
  "agent_id": "agent_abc123",
  "user_id": "user_xyz789",
  "max_amount_cents": 50000,
  "currency": "USD",
  "valid_until": "2026-02-01T00:00:00Z",
  "merchant_restrictions": ["merchant.example"],
  "category_restrictions": ["electronics", "home"]
}
```

### Creating Signed Mandate

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import json
import base64

def create_ap2_mandate(
    private_key,
    checkout_terms: dict,
    amount_cents: int,
    currency: str
) -> dict:
    """Create a signed AP2 mandate for checkout."""

    mandate_data = {
        "checkout_id": checkout_terms["id"],
        "amount_cents": amount_cents,
        "currency": currency,
        "timestamp": datetime.utcnow().isoformat(),
        "terms_hash": hash_terms(checkout_terms)
    }

    # Sign the mandate
    mandate_json = json.dumps(mandate_data, sort_keys=True)
    signature = private_key.sign(
        mandate_json.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return {
        "token": base64.b64encode(mandate_json.encode()).decode(),
        "signed_mandate": base64.b64encode(signature).decode()
    }
```

### Completing with AP2

```python
from ucp_client import create_ap2_mandate

# Get AP2 handler
ap2_handler = next(
    (h for h in session.payment_handlers if h.type == "dev.ucp.ap2"),
    None
)

if not ap2_handler:
    raise UCPError("ap2_not_supported", "Merchant doesn't support AP2")

# Check amount limits
max_amount = ap2_handler.config.get("max_amount_cents", 0)
if session.total_cents > max_amount:
    raise UCPError("amount_exceeded", f"Amount exceeds AP2 limit of {max_amount}")

# Create mandate
mandate = create_ap2_mandate(
    private_key=agent_private_key,
    checkout_terms=session.terms,
    amount_cents=session.total_cents,
    currency=session.currency
)

# Complete checkout
order = await ucp.complete_checkout(
    session_id=session.id,
    payment_data={
        "handler_id": ap2_handler.id,
        "credential": mandate["token"]
    },
    ap2={
        "checkout_mandate": mandate["signed_mandate"]
    }
)
```

### AP2 Key Management

```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_agent_keys():
    """Generate RSA key pair for AP2 signing."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    # Export for registration
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key, public_pem

def load_agent_key(key_path: str):
    """Load agent private key from file."""
    with open(key_path, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None  # Or use password for encrypted keys
        )
```

## Payment Data Model

### PaymentData

```python
@dataclass
class PaymentData:
    handler_id: str
    type: str | None = None  # "card", "bank_transfer", etc.
    brand: str | None = None  # "visa", "mastercard", etc.
    last_digits: str | None = None
    credential: dict = field(default_factory=dict)
```

### Credential Types

| Type | Description | Fields |
|------|-------------|--------|
| `PAYMENT_GATEWAY` | Gateway-encrypted token | `token` |
| `CARD_TOKEN` | Tokenized card | `token` |
| `APPLE_PAY` | Apple Pay token | `token` |
| `AP2_MANDATE` | Signed mandate | `token`, `signature` |

## Error Handling

### Payment-Specific Errors

```python
try:
    order = await ucp.complete_checkout(...)
except UCPError as e:
    if e.code == "payment_declined":
        print(f"Payment declined: {e.details.get('reason')}")
    elif e.code == "insufficient_funds":
        print("Insufficient funds")
    elif e.code == "card_expired":
        print("Card has expired")
    elif e.code == "3ds_failed":
        print("3DS verification failed")
    elif e.code == "mandate_invalid":
        print("AP2 mandate signature invalid")
    elif e.code == "mandate_expired":
        print("AP2 mandate has expired")
```

### Retry Logic

```python
async def complete_with_retry(
    session_id: str,
    payment_data: dict,
    max_retries: int = 2
):
    """Attempt payment with retry for transient failures."""

    for attempt in range(max_retries + 1):
        try:
            return await ucp.complete_checkout(
                session_id=session_id,
                payment_data=payment_data
            )
        except UCPError as e:
            # Only retry on transient errors
            if e.code in ["gateway_timeout", "network_error"]:
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
            raise

    raise UCPError("max_retries", "Payment failed after retries")
```

## PCI Compliance

### Best Practices

1. **Never handle raw card numbers**: Always use tokenization
2. **Use HTTPS**: All payment data must be encrypted in transit
3. **Minimize data retention**: Don't store payment credentials
4. **Log safely**: Never log full card numbers or tokens

### Compliance Checklist

```python
def validate_payment_data(payment_data: dict) -> bool:
    """Validate payment data doesn't contain raw card numbers."""

    dangerous_patterns = [
        r'\d{13,19}',  # Full card number
        r'\d{3,4}',    # CVV (when isolated)
    ]

    data_str = json.dumps(payment_data)

    for pattern in dangerous_patterns:
        if re.search(pattern, data_str):
            # Log warning but don't expose in error
            logger.warning("Potential raw card data detected")
            return False

    return True
```

## Testing

### Test Card Numbers

For development/testing environments:

| Card Number | Behavior |
|-------------|----------|
| `4242424242424242` | Success |
| `4000000000000002` | Declined |
| `4000000000003220` | Requires 3DS |
| `4000000000009995` | Insufficient funds |

### Mock Payment Handler

```python
class MockPaymentHandler:
    """Mock payment handler for testing."""

    async def process(self, payment_data: dict) -> dict:
        card_number = payment_data.get("test_card", "4242424242424242")

        if card_number == "4000000000000002":
            raise UCPError("payment_declined", "Card declined")

        if card_number == "4000000000003220":
            return {
                "status": "requires_3ds",
                "continue_url": "https://test.example/3ds"
            }

        return {
            "status": "confirmed",
            "order_id": f"order_{uuid4().hex[:8]}"
        }
```

## Best Practices

1. **Prefer Digital Wallets**: Better UX and security
2. **Implement 3DS**: Required in many regions
3. **Use Idempotency Keys**: Prevent duplicate charges
4. **Handle Webhooks**: For async payment confirmations
5. **Log Transaction IDs**: Aid reconciliation and support
6. **Set Timeouts**: Payment APIs can be slow
7. **Test Edge Cases**: Declined cards, network failures, etc.

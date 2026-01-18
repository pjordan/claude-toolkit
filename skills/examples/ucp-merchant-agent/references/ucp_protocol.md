# UCP Protocol Reference

Detailed reference for the Universal Commerce Protocol (UCP) specification.

## Overview

UCP is a transport-agnostic protocol for agentic commerce. It supports REST, MCP, and A2A communication patterns while maintaining consistent semantics across all transports.

## Versioning

UCP uses date-based versioning in `YYYY-MM-DD` format.

**Current Version**: `2026-01-11`

```python
UCP_VERSION = "2026-01-11"

# Version comparison
if merchant_version > agent_version:
    # Merchant may use features agent doesn't support
    pass
```

### Version Negotiation

When agent and merchant have different versions:
1. Both parties advertise their version
2. Intersection of capabilities is computed
3. Communication uses the common subset

## Profile Structure

### Agent Profile

Agents must publish a profile for capability advertisement:

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
    "description": "AI shopping assistant",
    "contact": "support@example.com"
  }
}
```

### Merchant Profile

Merchants publish profiles at `/.well-known/ucp`:

```json
{
  "ucp": {
    "version": "2026-01-11",
    "capabilities": [
      {
        "name": "dev.ucp.shopping.checkout",
        "version": "2026-01-11"
      },
      {
        "name": "dev.ucp.shopping.order",
        "version": "2026-01-11"
      }
    ],
    "extensions": [
      "dev.ucp.shopping.fulfillment"
    ],
    "payment_handlers": [
      {
        "type": "com.google.pay",
        "config": { ... }
      },
      {
        "type": "dev.ucp.direct_tokenization",
        "config": { ... }
      }
    ]
  },
  "merchant": {
    "name": "Example Store",
    "description": "Online electronics retailer",
    "rest_endpoint": "https://merchant.example/api/v2"
  }
}
```

## Discovery

### Well-Known Endpoint

Every UCP merchant publishes their profile at:

```
https://merchant.example/.well-known/ucp
```

### Discovery Request

```http
GET /.well-known/ucp HTTP/1.1
Host: merchant.example
Accept: application/json
UCP-Agent: profile="https://agent.example/profile.json"
```

### Discovery Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "ucp": {
    "version": "2026-01-11",
    "capabilities": [...],
    "payment_handlers": [...]
  },
  "merchant": {...}
}
```

## Capability Negotiation

### Core Capabilities

| Capability | Description |
|------------|-------------|
| `dev.ucp.shopping.checkout` | Create and manage checkout sessions |
| `dev.ucp.shopping.order` | Query order status and history |
| `dev.ucp.common.identity_linking` | Link agent identity to merchant account |

### Negotiation Algorithm

```python
def negotiate_capabilities(agent_profile, merchant_profile):
    """Compute capability intersection."""
    agent_caps = {c["name"] for c in agent_profile["ucp"]["capabilities"]}
    merchant_caps = {c["name"] for c in merchant_profile["ucp"]["capabilities"]}

    # Intersection of capabilities
    common_caps = agent_caps & merchant_caps

    # Check version compatibility for each capability
    negotiated = []
    for cap_name in common_caps:
        agent_ver = get_capability_version(agent_profile, cap_name)
        merchant_ver = get_capability_version(merchant_profile, cap_name)

        # Use minimum version for compatibility
        negotiated.append({
            "name": cap_name,
            "version": min(agent_ver, merchant_ver)
        })

    return negotiated
```

### Payment Handler Negotiation

```python
def negotiate_payment_handlers(agent_profile, merchant_profile):
    """Find common payment handlers."""
    agent_handlers = set(agent_profile["ucp"]["payment_handlers"])
    merchant_handlers = {h["type"] for h in merchant_profile["ucp"]["payment_handlers"]}

    return agent_handlers & merchant_handlers
```

## Request Headers

### UCP-Agent Header

All requests must include the agent profile:

```http
UCP-Agent: profile="https://agent.example/profile.json"
```

### UCP-Version Header (Optional)

Explicitly specify UCP version:

```http
UCP-Version: 2026-01-11
```

## Response Format

All UCP responses include metadata:

```json
{
  "ucp": {
    "version": "2026-01-11",
    "capabilities": [
      {"name": "dev.ucp.shopping.checkout", "version": "2026-01-11"}
    ]
  },
  "id": "resource_123",
  "status": "...",
  ...
}
```

## Error Handling

### Error Response Format

```json
{
  "ucp": {
    "version": "2026-01-11"
  },
  "error": {
    "code": "capability_not_supported",
    "message": "The requested capability is not available",
    "details": {
      "capability": "dev.ucp.shopping.checkout",
      "required_version": "2026-01-11"
    }
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| `version_mismatch` | UCP version incompatibility |
| `capability_not_supported` | Requested capability unavailable |
| `invalid_profile` | Agent profile validation failed |
| `authentication_required` | Request needs authentication |
| `session_expired` | Checkout session has expired |
| `payment_failed` | Payment processing error |
| `invalid_request` | Malformed request data |

### Error Handling in Code

```python
from ucp_client import UCPError, VersionError, CapabilityError

try:
    session = await ucp.create_checkout(...)
except VersionError as e:
    print(f"Version mismatch: agent={e.agent_version}, required={e.required_version}")
except CapabilityError as e:
    print(f"Capability not supported: {e.capability}")
except UCPError as e:
    print(f"UCP error [{e.code}]: {e.message}")
```

## Security

### Transport Security

- All UCP communication must use HTTPS
- TLS 1.2 or higher required
- Certificate validation mandatory

### Profile Verification

```python
async def verify_agent_profile(profile_url: str) -> bool:
    """Verify agent profile is accessible and valid."""
    response = await httpx.get(profile_url)

    if response.status_code != 200:
        return False

    profile = response.json()

    # Validate required fields
    required_fields = ["ucp", "agent"]
    return all(field in profile for field in required_fields)
```

### Rate Limiting

Merchants may implement rate limiting. Handle `429 Too Many Requests`:

```python
async def request_with_retry(url: str, max_retries: int = 3):
    for attempt in range(max_retries):
        response = await httpx.get(url)

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            await asyncio.sleep(retry_after)
            continue

        return response

    raise UCPError("rate_limited", "Max retries exceeded")
```

## Extensions

Extensions provide optional functionality beyond core capabilities.

### Available Extensions

| Extension | Description |
|-----------|-------------|
| `dev.ucp.shopping.fulfillment` | Track order fulfillment status |
| `dev.ucp.shopping.returns` | Process returns and refunds |
| `dev.ucp.shopping.subscriptions` | Manage recurring orders |

### Checking Extension Support

```python
if "dev.ucp.shopping.fulfillment" in merchant.extensions:
    # Use fulfillment tracking
    tracking = await ucp.get_fulfillment_status(order_id)
```

## Best Practices

1. **Cache Discovery Results**: Merchant profiles change infrequently
2. **Handle Version Drift**: Implement graceful degradation
3. **Validate Capabilities**: Check before using features
4. **Log UCP Exchanges**: Aid debugging and compliance
5. **Implement Timeouts**: Set reasonable request timeouts
6. **Handle Partial Failures**: Some operations may partially succeed

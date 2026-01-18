# Checkout Flow Implementation Example

An example session using the UCP Commerce Developer subagent to implement a complete checkout flow.

## User Request

```
Create a ShoppingAgent class that implements a complete UCP checkout flow:
1. Discover a merchant and negotiate capabilities
2. Create a checkout session
3. Add items to cart with quantity management
4. Apply shipping address and select shipping method
5. Complete payment with Google Pay token
6. Return order confirmation

Include proper error handling and logging.
```

## Expected Response

Here's a complete `ShoppingAgent` implementation with full UCP checkout flow:

```python
"""
UCP Shopping Agent - Complete checkout flow implementation.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

import httpx
from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)

# === UCP Models ===

class UCPVersion(str, Enum):
    """Supported UCP versions."""
    V2026_01_11 = "2026-01-11"

class PaymentHandlerType(str, Enum):
    """Supported payment handler types."""
    GOOGLE_PAY = "google_pay"
    APPLE_PAY = "apple_pay"
    DIRECT_TOKENIZATION = "direct_tokenization"
    AP2_MANDATE = "ap2_mandate"

class Address(BaseModel):
    """Shipping/billing address."""
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = "US"

class LineItem(BaseModel):
    """Cart line item."""
    product_id: str
    name: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price

class ShippingMethod(BaseModel):
    """Available shipping method."""
    id: str
    name: str
    price: float
    estimated_days: int

class MerchantProfile(BaseModel):
    """UCP Merchant profile from /.well-known/ucp."""
    merchant_id: str
    name: str
    ucp_version: str
    capabilities: list[str]
    payment_handlers: list[str]
    checkout_endpoint: str

class CheckoutSession(BaseModel):
    """Active checkout session."""
    session_id: str
    merchant_id: str
    items: list[LineItem] = Field(default_factory=list)
    shipping_address: Optional[Address] = None
    shipping_method: Optional[ShippingMethod] = None
    subtotal: float = 0
    shipping_cost: float = 0
    tax: float = 0
    total: float = 0
    status: str = "active"

class Order(BaseModel):
    """Completed order."""
    order_id: str
    merchant_id: str
    items: list[LineItem]
    total: float
    status: str
    created_at: datetime
    confirmation_number: str

class GooglePayToken(BaseModel):
    """Google Pay payment token."""
    token: str
    card_network: str
    card_last_four: str

# === UCP Errors ===

class UCPError(Exception):
    """Base UCP error."""
    def __init__(self, message: str, code: str, details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)

class VersionError(UCPError):
    """UCP version incompatibility."""
    def __init__(self, merchant_version: str, agent_version: str):
        super().__init__(
            f"Version mismatch: merchant={merchant_version}, agent={agent_version}",
            "VERSION_ERROR",
            {"merchant_version": merchant_version, "agent_version": agent_version}
        )

class CapabilityError(UCPError):
    """Missing required capabilities."""
    def __init__(self, missing: list[str]):
        super().__init__(
            f"Missing capabilities: {', '.join(missing)}",
            "CAPABILITY_ERROR",
            {"missing_capabilities": missing}
        )

class CheckoutError(UCPError):
    """Checkout session error."""
    pass

class PaymentError(UCPError):
    """Payment processing error."""
    pass

# === Shopping Agent ===

@dataclass
class ShoppingAgent:
    """
    UCP Shopping Agent for autonomous commerce.

    Implements the complete UCP checkout flow:
    discover -> negotiate -> checkout -> pay
    """

    agent_name: str = "shopping-agent"
    agent_version: str = UCPVersion.V2026_01_11.value
    supported_payment_handlers: list[str] = field(
        default_factory=lambda: [PaymentHandlerType.GOOGLE_PAY.value]
    )

    # Internal state
    _client: httpx.AsyncClient = field(default=None, init=False)
    _profile_cache: dict[str, MerchantProfile] = field(default_factory=dict, init=False)
    _active_session: Optional[CheckoutSession] = field(default=None, init=False)

    async def __aenter__(self):
        """Initialize HTTP client."""
        self._client = httpx.AsyncClient(
            timeout=30.0,
            headers=self._get_agent_headers()
        )
        return self

    async def __aexit__(self, *args):
        """Cleanup HTTP client."""
        if self._client:
            await self._client.aclose()

    def _get_agent_headers(self) -> dict:
        """Get UCP agent headers for requests."""
        return {
            "UCP-Agent": f"{self.agent_name}/{self.agent_version}",
            "UCP-Capabilities": ",".join(self.supported_payment_handlers),
            "Content-Type": "application/json"
        }

    # === Discovery ===

    async def discover(self, merchant_url: str, use_cache: bool = True) -> MerchantProfile:
        """
        Discover merchant UCP capabilities.

        Args:
            merchant_url: Base URL of the merchant
            use_cache: Whether to use cached profile

        Returns:
            MerchantProfile with merchant capabilities

        Raises:
            UCPError: If discovery fails
        """
        cache_key = merchant_url.rstrip("/")

        if use_cache and cache_key in self._profile_cache:
            logger.debug(f"Using cached profile for {merchant_url}")
            return self._profile_cache[cache_key]

        discovery_url = f"{cache_key}/.well-known/ucp"
        logger.info(f"Discovering merchant at {discovery_url}")

        try:
            response = await self._client.get(discovery_url)
            response.raise_for_status()

            data = response.json()
            profile = MerchantProfile(**data)

            # Cache the profile
            self._profile_cache[cache_key] = profile
            logger.info(f"Discovered merchant: {profile.name} (v{profile.ucp_version})")

            return profile

        except httpx.HTTPStatusError as e:
            raise UCPError(
                f"Discovery failed: {e.response.status_code}",
                "DISCOVERY_ERROR",
                {"status_code": e.response.status_code}
            )
        except Exception as e:
            raise UCPError(f"Discovery failed: {str(e)}", "DISCOVERY_ERROR")

    async def negotiate(self, profile: MerchantProfile) -> dict:
        """
        Negotiate capabilities with merchant.

        Args:
            profile: Merchant's UCP profile

        Returns:
            Dict with negotiated capabilities

        Raises:
            VersionError: If versions incompatible
            CapabilityError: If required capabilities missing
        """
        # Check version compatibility
        if profile.ucp_version != self.agent_version:
            # For now, require exact match (could implement range checking)
            raise VersionError(profile.ucp_version, self.agent_version)

        # Compute capability intersection
        agent_payment_handlers = set(self.supported_payment_handlers)
        merchant_payment_handlers = set(profile.payment_handlers)
        common_handlers = agent_payment_handlers & merchant_payment_handlers

        if not common_handlers:
            raise CapabilityError(list(agent_payment_handlers))

        logger.info(f"Negotiated payment handlers: {common_handlers}")

        return {
            "ucp_version": profile.ucp_version,
            "payment_handlers": list(common_handlers),
            "checkout_endpoint": profile.checkout_endpoint
        }

    # === Checkout ===

    async def create_checkout(self, merchant_url: str) -> CheckoutSession:
        """
        Create a new checkout session with merchant.

        Args:
            merchant_url: Merchant base URL

        Returns:
            New CheckoutSession
        """
        profile = await self.discover(merchant_url)
        capabilities = await self.negotiate(profile)

        endpoint = f"{merchant_url.rstrip('/')}{capabilities['checkout_endpoint']}"
        logger.info(f"Creating checkout session at {endpoint}")

        try:
            response = await self._client.post(
                endpoint,
                json={"action": "create"}
            )
            response.raise_for_status()

            data = response.json()
            self._active_session = CheckoutSession(
                session_id=data["session_id"],
                merchant_id=profile.merchant_id
            )

            logger.info(f"Created session: {self._active_session.session_id}")
            return self._active_session

        except httpx.HTTPStatusError as e:
            raise CheckoutError(
                f"Failed to create session: {e.response.status_code}",
                "SESSION_CREATE_ERROR"
            )

    async def add_item(
        self,
        merchant_url: str,
        product_id: str,
        name: str,
        quantity: int,
        unit_price: float
    ) -> CheckoutSession:
        """
        Add item to cart.

        Args:
            merchant_url: Merchant base URL
            product_id: Product identifier
            name: Product name
            quantity: Quantity to add
            unit_price: Price per unit

        Returns:
            Updated CheckoutSession
        """
        if not self._active_session:
            raise CheckoutError("No active session", "NO_SESSION")

        item = LineItem(
            product_id=product_id,
            name=name,
            quantity=quantity,
            unit_price=unit_price
        )

        profile = await self.discover(merchant_url)
        endpoint = f"{merchant_url.rstrip('/')}{profile.checkout_endpoint}"

        try:
            response = await self._client.post(
                endpoint,
                json={
                    "action": "add_item",
                    "session_id": self._active_session.session_id,
                    "item": item.model_dump()
                }
            )
            response.raise_for_status()

            data = response.json()
            self._active_session.items.append(item)
            self._active_session.subtotal = data.get("subtotal", self._active_session.subtotal)
            self._active_session.total = data.get("total", self._active_session.total)

            logger.info(f"Added item: {name} x{quantity}")
            return self._active_session

        except httpx.HTTPStatusError as e:
            raise CheckoutError(
                f"Failed to add item: {e.response.status_code}",
                "ADD_ITEM_ERROR"
            )

    async def set_shipping(
        self,
        merchant_url: str,
        address: Address,
        method_id: str
    ) -> CheckoutSession:
        """
        Set shipping address and method.

        Args:
            merchant_url: Merchant base URL
            address: Shipping address
            method_id: Selected shipping method ID

        Returns:
            Updated CheckoutSession
        """
        if not self._active_session:
            raise CheckoutError("No active session", "NO_SESSION")

        profile = await self.discover(merchant_url)
        endpoint = f"{merchant_url.rstrip('/')}{profile.checkout_endpoint}"

        try:
            response = await self._client.post(
                endpoint,
                json={
                    "action": "set_shipping",
                    "session_id": self._active_session.session_id,
                    "shipping_address": address.model_dump(),
                    "shipping_method_id": method_id
                }
            )
            response.raise_for_status()

            data = response.json()
            self._active_session.shipping_address = address
            self._active_session.shipping_method = ShippingMethod(**data["shipping_method"])
            self._active_session.shipping_cost = data.get("shipping_cost", 0)
            self._active_session.tax = data.get("tax", 0)
            self._active_session.total = data.get("total", self._active_session.total)

            logger.info(f"Set shipping: {self._active_session.shipping_method.name}")
            return self._active_session

        except httpx.HTTPStatusError as e:
            raise CheckoutError(
                f"Failed to set shipping: {e.response.status_code}",
                "SHIPPING_ERROR"
            )

    # === Payment ===

    async def complete_with_google_pay(
        self,
        merchant_url: str,
        payment_token: GooglePayToken
    ) -> Order:
        """
        Complete checkout with Google Pay.

        Args:
            merchant_url: Merchant base URL
            payment_token: Google Pay token from client

        Returns:
            Completed Order

        Raises:
            PaymentError: If payment fails
        """
        if not self._active_session:
            raise CheckoutError("No active session", "NO_SESSION")

        profile = await self.discover(merchant_url)
        endpoint = f"{merchant_url.rstrip('/')}{profile.checkout_endpoint}"

        logger.info(f"Processing Google Pay payment for ${self._active_session.total:.2f}")

        try:
            response = await self._client.post(
                endpoint,
                json={
                    "action": "complete",
                    "session_id": self._active_session.session_id,
                    "payment_handler": PaymentHandlerType.GOOGLE_PAY.value,
                    "payment_data": {
                        "token": payment_token.token,
                        "card_network": payment_token.card_network,
                        "card_last_four": payment_token.card_last_four
                    }
                }
            )
            response.raise_for_status()

            data = response.json()

            order = Order(
                order_id=data["order_id"],
                merchant_id=self._active_session.merchant_id,
                items=self._active_session.items,
                total=self._active_session.total,
                status=data.get("status", "confirmed"),
                created_at=datetime.now(),
                confirmation_number=data["confirmation_number"]
            )

            # Clear session after successful order
            self._active_session = None

            logger.info(f"Order complete: {order.confirmation_number}")
            return order

        except httpx.HTTPStatusError as e:
            error_data = e.response.json() if e.response.content else {}
            raise PaymentError(
                f"Payment failed: {error_data.get('error', 'Unknown error')}",
                error_data.get("code", "PAYMENT_ERROR"),
                error_data
            )

# === Usage Example ===

async def example_checkout():
    """Example of complete checkout flow."""

    async with ShoppingAgent() as agent:
        merchant = "https://shop.example.com"

        # 1. Create checkout session
        session = await agent.create_checkout(merchant)
        print(f"Session created: {session.session_id}")

        # 2. Add items
        await agent.add_item(
            merchant,
            product_id="SKU-001",
            name="Wireless Headphones",
            quantity=1,
            unit_price=99.99
        )

        await agent.add_item(
            merchant,
            product_id="SKU-002",
            name="USB-C Cable",
            quantity=2,
            unit_price=14.99
        )

        # 3. Set shipping
        address = Address(
            line1="123 Main St",
            city="San Francisco",
            state="CA",
            postal_code="94102"
        )

        session = await agent.set_shipping(merchant, address, "standard")
        print(f"Total: ${session.total:.2f}")

        # 4. Complete payment
        token = GooglePayToken(
            token="eyJhbGc...",
            card_network="VISA",
            card_last_four="4242"
        )

        order = await agent.complete_with_google_pay(merchant, token)
        print(f"Order confirmed: {order.confirmation_number}")

        return order

if __name__ == "__main__":
    asyncio.run(example_checkout())
```

## Key Design Decisions

1. **Async Context Manager**: Proper resource management for HTTP client
2. **Profile Caching**: Reduces discovery overhead for repeated operations
3. **Pydantic Models**: Type-safe data handling throughout
4. **Structured Errors**: Custom exception hierarchy for specific error types
5. **Stateful Session**: Tracks checkout progress internally
6. **Logging**: Comprehensive logging for debugging and monitoring

## Testing This Agent

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_discovery():
    async with ShoppingAgent() as agent:
        with patch.object(agent._client, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.json.return_value = {
                "merchant_id": "test-merchant",
                "name": "Test Shop",
                "ucp_version": "2026-01-11",
                "capabilities": ["checkout"],
                "payment_handlers": ["google_pay"],
                "checkout_endpoint": "/api/checkout"
            }
            mock_get.return_value.raise_for_status = lambda: None

            profile = await agent.discover("https://test.shop")
            assert profile.merchant_id == "test-merchant"
```

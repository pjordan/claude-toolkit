"""
UCP Client

Client library for interacting with UCP-compliant merchants.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import httpx


class UCPError(Exception):
    """Base exception for UCP errors."""

    def __init__(self, code: str, message: str, details: dict | None = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(f"[{code}] {message}")


class VersionError(UCPError):
    """UCP version mismatch error."""

    def __init__(self, agent_version: str, required_version: str):
        self.agent_version = agent_version
        self.required_version = required_version
        super().__init__(
            "version_mismatch",
            f"Version mismatch: agent={agent_version}, required={required_version}",
            {"agent_version": agent_version, "required_version": required_version},
        )


class CapabilityError(UCPError):
    """Capability not supported error."""

    def __init__(self, capability: str):
        self.capability = capability
        super().__init__(
            "capability_not_supported",
            f"Capability not supported: {capability}",
            {"capability": capability},
        )


@dataclass
class Capability:
    """UCP capability."""

    name: str
    version: str


@dataclass
class PaymentHandler:
    """Payment handler configuration."""

    id: str
    type: str
    config: dict = field(default_factory=dict)


@dataclass
class MerchantProfile:
    """Merchant profile from discovery."""

    name: str
    description: str
    rest_endpoint: str
    ucp_version: str
    capabilities: list[Capability]
    payment_handlers: list[PaymentHandler]
    extensions: list[str] = field(default_factory=list)


@dataclass
class LineItem:
    """Checkout line item."""

    sku: str
    quantity: int
    price_cents: int | None = None
    name: str | None = None
    description: str | None = None


@dataclass
class CheckoutSession:
    """Checkout session state."""

    id: str
    status: str
    merchant_url: str
    line_items: list[LineItem]
    subtotal_cents: int
    tax_cents: int
    shipping_cents: int
    discount_cents: int
    total_cents: int
    currency: str
    payment_handlers: list[PaymentHandler]
    created_at: datetime
    expires_at: datetime
    terms: dict = field(default_factory=dict)


@dataclass
class Order:
    """Completed order."""

    id: str
    status: str
    confirmation_number: str | None = None
    total_cents: int = 0
    currency: str = "USD"


class UCPClient:
    """Client for UCP merchant integration."""

    UCP_VERSION = "2026-01-11"

    def __init__(self, agent_profile_url: str, timeout: float = 30.0):
        """
        Initialize UCP client.

        Args:
            agent_profile_url: URL to this agent's profile JSON
            timeout: Request timeout in seconds
        """
        self.agent_profile_url = agent_profile_url
        self.timeout = timeout
        self._http_client: httpx.AsyncClient | None = None
        self._merchant_cache: dict[str, MerchantProfile] = {}

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(
                timeout=self.timeout,
                headers={
                    "UCP-Agent": f'profile="{self.agent_profile_url}"',
                    "Content-Type": "application/json",
                },
            )
        return self._http_client

    async def close(self):
        """Close the HTTP client."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    async def discover(self, merchant_url: str) -> MerchantProfile:
        """
        Discover merchant capabilities.

        Args:
            merchant_url: Base URL of the merchant

        Returns:
            MerchantProfile with capabilities and payment handlers
        """
        # Check cache
        if merchant_url in self._merchant_cache:
            return self._merchant_cache[merchant_url]

        client = await self._get_client()

        # Fetch well-known UCP endpoint
        well_known_url = f"{merchant_url.rstrip('/')}/.well-known/ucp"

        try:
            response = await client.get(well_known_url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise UCPError(
                "discovery_failed",
                f"Failed to discover merchant: {e.response.status_code}",
            )
        except httpx.RequestError as e:
            raise UCPError("network_error", f"Network error during discovery: {e}")

        data = response.json()

        # Parse profile
        ucp_data = data.get("ucp", {})
        merchant_data = data.get("merchant", {})

        profile = MerchantProfile(
            name=merchant_data.get("name", "Unknown"),
            description=merchant_data.get("description", ""),
            rest_endpoint=merchant_data.get("rest_endpoint", merchant_url),
            ucp_version=ucp_data.get("version", ""),
            capabilities=[
                Capability(name=c["name"], version=c.get("version", ""))
                for c in ucp_data.get("capabilities", [])
            ],
            payment_handlers=[
                PaymentHandler(
                    id=h.get("id", ""),
                    type=h.get("type", ""),
                    config=h.get("config", {}),
                )
                for h in ucp_data.get("payment_handlers", [])
            ],
            extensions=ucp_data.get("extensions", []),
        )

        # Cache the profile
        self._merchant_cache[merchant_url] = profile

        return profile

    async def negotiate(
        self, merchant_profile: MerchantProfile
    ) -> dict[str, Any]:
        """
        Negotiate capabilities with merchant.

        Args:
            merchant_profile: Merchant's profile from discovery

        Returns:
            Dict with negotiated capabilities and payment handlers
        """
        # Agent capabilities (would typically come from agent profile)
        agent_capabilities = {"dev.ucp.shopping.checkout"}
        agent_handlers = {"com.google.pay", "dev.ucp.ap2"}

        # Compute intersection
        merchant_caps = {c.name for c in merchant_profile.capabilities}
        merchant_handlers = {h.type for h in merchant_profile.payment_handlers}

        return {
            "capabilities": list(agent_capabilities & merchant_caps),
            "payment_handlers": list(agent_handlers & merchant_handlers),
        }

    async def create_checkout(
        self,
        merchant_url: str,
        line_items: list[dict],
        **kwargs,
    ) -> CheckoutSession:
        """
        Create a new checkout session.

        Args:
            merchant_url: Merchant base URL
            line_items: List of items to add
            **kwargs: Additional checkout options

        Returns:
            CheckoutSession object
        """
        # Discover merchant if not cached
        merchant = await self.discover(merchant_url)

        # Check capability
        if not any(c.name == "dev.ucp.shopping.checkout" for c in merchant.capabilities):
            raise CapabilityError("dev.ucp.shopping.checkout")

        client = await self._get_client()

        # Create checkout request
        payload = {
            "line_items": line_items,
            **kwargs,
        }

        endpoint = f"{merchant.rest_endpoint.rstrip('/')}/checkout"

        try:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._handle_error_response(e.response)
        except httpx.RequestError as e:
            raise UCPError("network_error", f"Network error: {e}")

        data = response.json()

        return self._parse_checkout_session(data, merchant_url, merchant.payment_handlers)

    async def update_checkout(
        self,
        session_id: str,
        **kwargs,
    ) -> CheckoutSession:
        """
        Update an existing checkout session.

        Args:
            session_id: Session ID to update
            **kwargs: Fields to update (line_items, shipping_address, etc.)

        Returns:
            Updated CheckoutSession
        """
        client = await self._get_client()

        # Extract merchant URL from session (would need to track this)
        # For simplicity, assume it's passed in kwargs
        merchant_url = kwargs.pop("merchant_url", None)
        if not merchant_url:
            raise UCPError("invalid_request", "merchant_url required for update")

        merchant = await self.discover(merchant_url)
        endpoint = f"{merchant.rest_endpoint.rstrip('/')}/checkout/{session_id}"

        try:
            response = await client.patch(endpoint, json=kwargs)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._handle_error_response(e.response)
        except httpx.RequestError as e:
            raise UCPError("network_error", f"Network error: {e}")

        data = response.json()

        return self._parse_checkout_session(data, merchant_url, merchant.payment_handlers)

    async def complete_checkout(
        self,
        session_id: str,
        payment_data: dict,
        **kwargs,
    ) -> Order:
        """
        Complete checkout with payment.

        Args:
            session_id: Session ID to complete
            payment_data: Payment handler and credential
            **kwargs: Additional options (ap2 mandate, etc.)

        Returns:
            Order object
        """
        client = await self._get_client()

        # Would need to track merchant URL per session in production
        merchant_url = kwargs.pop("merchant_url", None)
        if not merchant_url:
            raise UCPError("invalid_request", "merchant_url required for completion")

        merchant = await self.discover(merchant_url)
        endpoint = f"{merchant.rest_endpoint.rstrip('/')}/checkout/{session_id}/complete"

        payload = {
            "payment": payment_data,
            **kwargs,
        }

        try:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._handle_error_response(e.response)
        except httpx.RequestError as e:
            raise UCPError("network_error", f"Network error: {e}")

        data = response.json()

        return Order(
            id=data.get("id", ""),
            status=data.get("status", "unknown"),
            confirmation_number=data.get("confirmation_number"),
            total_cents=data.get("total_cents", 0),
            currency=data.get("currency", "USD"),
        )

    async def get_order(self, order_id: str, merchant_url: str) -> Order:
        """
        Get order status.

        Args:
            order_id: Order ID to query
            merchant_url: Merchant base URL

        Returns:
            Order object
        """
        client = await self._get_client()
        merchant = await self.discover(merchant_url)

        endpoint = f"{merchant.rest_endpoint.rstrip('/')}/orders/{order_id}"

        try:
            response = await client.get(endpoint)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._handle_error_response(e.response)
        except httpx.RequestError as e:
            raise UCPError("network_error", f"Network error: {e}")

        data = response.json()

        return Order(
            id=data.get("id", ""),
            status=data.get("status", "unknown"),
            confirmation_number=data.get("confirmation_number"),
            total_cents=data.get("total_cents", 0),
            currency=data.get("currency", "USD"),
        )

    def _parse_checkout_session(
        self,
        data: dict,
        merchant_url: str,
        payment_handlers: list[PaymentHandler],
    ) -> CheckoutSession:
        """Parse checkout session from response data."""
        return CheckoutSession(
            id=data.get("id", ""),
            status=data.get("status", "incomplete"),
            merchant_url=merchant_url,
            line_items=[
                LineItem(
                    sku=item.get("sku", ""),
                    quantity=item.get("quantity", 0),
                    price_cents=item.get("price_cents"),
                    name=item.get("name"),
                    description=item.get("description"),
                )
                for item in data.get("line_items", [])
            ],
            subtotal_cents=data.get("subtotal_cents", 0),
            tax_cents=data.get("tax_cents", 0),
            shipping_cents=data.get("shipping_cents", 0),
            discount_cents=data.get("discount_cents", 0),
            total_cents=data.get("total_cents", 0),
            currency=data.get("currency", "USD"),
            payment_handlers=payment_handlers,
            created_at=datetime.fromisoformat(
                data.get("created_at", datetime.now().isoformat())
            ),
            expires_at=datetime.fromisoformat(
                data.get("expires_at", datetime.now().isoformat())
            ),
            terms=data.get("terms", {}),
        )

    def _handle_error_response(self, response: httpx.Response):
        """Handle error response from merchant."""
        try:
            data = response.json()
            error = data.get("error", {})
            code = error.get("code", "unknown_error")
            message = error.get("message", "Unknown error")
            details = error.get("details", {})
        except Exception:
            code = f"http_{response.status_code}"
            message = response.text or "Unknown error"
            details = {}

        if code == "version_mismatch":
            raise VersionError(
                self.UCP_VERSION,
                details.get("required_version", "unknown"),
            )
        elif code == "capability_not_supported":
            raise CapabilityError(details.get("capability", "unknown"))
        else:
            raise UCPError(code, message, details)

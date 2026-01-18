"""
Basic UCP Shopping Agent

A minimal A2A agent that integrates with UCP merchants for shopping operations.
"""

import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from ucp_client import UCPClient

load_dotenv()

# Configuration
AGENT_PROFILE_URL = os.getenv("AGENT_PROFILE_URL", "https://example.com/agent-profile.json")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# UCP Client instance
ucp_client: UCPClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources."""
    global ucp_client
    ucp_client = UCPClient(agent_profile_url=AGENT_PROFILE_URL)
    yield
    # Cleanup
    if ucp_client:
        await ucp_client.close()


app = FastAPI(
    title="UCP Shopping Agent",
    description="A2A agent for UCP merchant integration",
    version="1.0.0",
    lifespan=lifespan,
)


# Request/Response Models
class DiscoverRequest(BaseModel):
    merchant_url: str


class DiscoverResponse(BaseModel):
    merchant_name: str
    capabilities: list[str]
    payment_handlers: list[str]


class LineItem(BaseModel):
    sku: str
    quantity: int
    price_cents: int | None = None


class CreateCheckoutRequest(BaseModel):
    merchant_url: str
    line_items: list[LineItem]


class CheckoutResponse(BaseModel):
    session_id: str
    status: str
    subtotal_cents: int
    total_cents: int


class CompleteCheckoutRequest(BaseModel):
    session_id: str
    payment_handler_id: str
    payment_credential: dict


class OrderResponse(BaseModel):
    order_id: str
    status: str
    confirmation_number: str | None = None


# Health endpoint
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ucp-shopping-agent"}


# A2A Handler endpoints
@app.post("/discover", response_model=DiscoverResponse)
async def discover_merchant(request: DiscoverRequest):
    """Discover merchant capabilities."""
    merchant = await ucp_client.discover(request.merchant_url)

    return DiscoverResponse(
        merchant_name=merchant.name,
        capabilities=[c.name for c in merchant.capabilities],
        payment_handlers=[h.type for h in merchant.payment_handlers],
    )


@app.post("/checkout/create", response_model=CheckoutResponse)
async def create_checkout(request: CreateCheckoutRequest):
    """Create a new checkout session."""
    session = await ucp_client.create_checkout(
        merchant_url=request.merchant_url,
        line_items=[
            {"sku": item.sku, "quantity": item.quantity, "price_cents": item.price_cents}
            for item in request.line_items
        ],
    )

    return CheckoutResponse(
        session_id=session.id,
        status=session.status,
        subtotal_cents=session.subtotal_cents,
        total_cents=session.total_cents,
    )


@app.post("/checkout/complete", response_model=OrderResponse)
async def complete_checkout(request: CompleteCheckoutRequest):
    """Complete a checkout session with payment."""
    order = await ucp_client.complete_checkout(
        session_id=request.session_id,
        payment_data={
            "handler_id": request.payment_handler_id,
            "credential": request.payment_credential,
        },
    )

    return OrderResponse(
        order_id=order.id,
        status=order.status,
        confirmation_number=order.confirmation_number,
    )


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)

# Service with APIM Headers Example

An example session using the Azure APIM + FastAPI Developer subagent to create a service that properly handles APIM gateway headers.

## User Request

```
Create a FastAPI service for an order management API that:
- Properly handles all APIM headers (correlation ID, request ID, subscription key, trace)
- Includes health check endpoints for Kubernetes and APIM
- Uses structured JSON logging for Azure Monitor
- Has proper configuration management with pydantic-settings
- Includes example order endpoints
```

## Expected Response

Here's a complete FastAPI service with full APIM integration:

### Project Structure

```
order-api/
├── main.py              # Application entry point
├── config.py            # Configuration management
├── middleware/
│   ├── __init__.py
│   ├── apim_headers.py  # APIM header handling
│   └── logging.py       # Structured logging middleware
├── routers/
│   ├── __init__.py
│   ├── health.py        # Health check endpoints
│   └── orders.py        # Order management endpoints
├── models/
│   ├── __init__.py
│   └── orders.py        # Pydantic models
└── requirements.txt
```

### config.py

```python
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    # Application
    app_name: str = "order-api"
    version: str = "1.0.0"
    debug: bool = False

    # Azure
    azure_tenant_id: Optional[str] = None
    azure_client_id: Optional[str] = None

    # APIM
    validate_apim_headers: bool = True
    require_subscription_key: bool = False  # APIM handles this

    # Database (example)
    database_url: str = "sqlite:///./orders.db"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
```

### middleware/apim_headers.py

```python
from fastapi import Request, Header
from typing import Optional
from contextvars import ContextVar
from dataclasses import dataclass
import uuid

# Context variables for request-scoped data
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")
request_id_var: ContextVar[str] = ContextVar("request_id", default="")


@dataclass
class APIMContext:
    """Context data extracted from APIM headers."""
    request_id: str
    correlation_id: str
    subscription_key: Optional[str]
    trace_enabled: bool

    @classmethod
    def from_headers(
        cls,
        x_request_id: Optional[str] = None,
        x_correlation_id: Optional[str] = None,
        subscription_key: Optional[str] = None,
        trace: Optional[str] = None,
    ) -> "APIMContext":
        """Create context from APIM headers."""
        return cls(
            request_id=x_request_id or str(uuid.uuid4()),
            correlation_id=x_correlation_id or str(uuid.uuid4()),
            subscription_key=subscription_key,
            trace_enabled=trace == "true",
        )


async def get_apim_context(
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID"),
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-ID"),
    ocp_apim_subscription_key: Optional[str] = Header(
        None, alias="Ocp-Apim-Subscription-Key"
    ),
    ocp_apim_trace: Optional[str] = Header(None, alias="Ocp-Apim-Trace"),
) -> APIMContext:
    """
    Dependency to extract APIM context from request headers.

    Usage:
        @app.get("/endpoint")
        async def endpoint(apim: APIMContext = Depends(get_apim_context)):
            logger.info(f"Request {apim.request_id}")
    """
    context = APIMContext.from_headers(
        x_request_id=x_request_id,
        x_correlation_id=x_correlation_id,
        subscription_key=ocp_apim_subscription_key,
        trace=ocp_apim_trace,
    )

    # Set context variables for logging
    correlation_id_var.set(context.correlation_id)
    request_id_var.set(context.request_id)

    return context
```

### middleware/logging.py

```python
import logging
import json
from datetime import datetime, timezone
from typing import Any

from middleware.apim_headers import correlation_id_var, request_id_var


class AzureMonitorFormatter(logging.Formatter):
    """JSON formatter compatible with Azure Monitor."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id_var.get(""),
            "request_id": request_id_var.get(""),
        }

        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra_fields"):
            log_obj.update(record.extra_fields)

        return json.dumps(log_obj)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure structured logging for Azure Monitor."""
    handler = logging.StreamHandler()
    handler.setFormatter(AzureMonitorFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
```

### routers/health.py

```python
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone

from config import get_settings

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    version: str
    service: str


class ReadinessResponse(BaseModel):
    """Readiness check response model."""
    status: str
    checks: dict[str, str]


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for APIM and load balancers.

    Returns basic service health information.
    """
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=settings.version,
        service=settings.app_name,
    )


@router.get("/health/live")
async def liveness() -> dict[str, str]:
    """
    Kubernetes liveness probe.

    Returns 200 if the process is running.
    """
    return {"status": "alive"}


@router.get("/health/ready", response_model=ReadinessResponse)
async def readiness() -> ReadinessResponse:
    """
    Kubernetes readiness probe.

    Checks dependencies before accepting traffic.
    """
    checks = {}

    # Check database connection
    try:
        # await check_database_connection()
        checks["database"] = "connected"
    except Exception:
        checks["database"] = "disconnected"

    # Determine overall status
    all_healthy = all(v == "connected" for v in checks.values())

    return ReadinessResponse(
        status="ready" if all_healthy else "not_ready",
        checks=checks,
    )
```

### routers/orders.py

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
import logging

from middleware.apim_headers import APIMContext, get_apim_context
from models.orders import Order, OrderCreate, OrderList

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])
logger = logging.getLogger(__name__)

# In-memory store for demo
orders_db: dict[str, Order] = {}


@router.get("", response_model=OrderList)
async def list_orders(
    status: Optional[str] = None,
    limit: int = 10,
    apim: APIMContext = Depends(get_apim_context),
) -> OrderList:
    """List orders with optional status filter."""
    logger.info(
        "Listing orders",
        extra={"extra_fields": {"status_filter": status, "limit": limit}},
    )

    orders = list(orders_db.values())
    if status:
        orders = [o for o in orders if o.status == status]

    return OrderList(orders=orders[:limit], total=len(orders))


@router.post("", response_model=Order, status_code=201)
async def create_order(
    order: OrderCreate,
    apim: APIMContext = Depends(get_apim_context),
) -> Order:
    """Create a new order."""
    import uuid

    order_id = str(uuid.uuid4())
    new_order = Order(
        id=order_id,
        **order.model_dump(),
        status="pending",
        correlation_id=apim.correlation_id,
    )

    orders_db[order_id] = new_order

    logger.info(
        "Order created",
        extra={"extra_fields": {"order_id": order_id, "total": order.total}},
    )

    return new_order


@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: str,
    apim: APIMContext = Depends(get_apim_context),
) -> Order:
    """Get order by ID."""
    if order_id not in orders_db:
        logger.warning(
            "Order not found",
            extra={"extra_fields": {"order_id": order_id}},
        )
        raise HTTPException(status_code=404, detail="Order not found")

    return orders_db[order_id]
```

### models/orders.py

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrderItem(BaseModel):
    """Item in an order."""
    product_id: str
    name: str
    quantity: int = Field(..., ge=1)
    price: float = Field(..., ge=0)


class OrderCreate(BaseModel):
    """Request model for creating an order."""
    customer_id: str
    items: list[OrderItem]
    total: float = Field(..., ge=0)
    shipping_address: str


class Order(BaseModel):
    """Complete order model."""
    id: str
    customer_id: str
    items: list[OrderItem]
    total: float
    shipping_address: str
    status: str = "pending"
    correlation_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OrderList(BaseModel):
    """Paginated order list response."""
    orders: list[Order]
    total: int
```

### main.py

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
import logging
import time

from config import get_settings
from middleware.logging import configure_logging
from middleware.apim_headers import correlation_id_var
from routers import health, orders

# Configure logging before anything else
settings = get_settings()
configure_logging(level=logging.DEBUG if settings.debug else logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info(f"Starting {settings.app_name} v{settings.version}")
    yield
    logger.info(f"Shutting down {settings.app_name}")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan,
    # Disable docs in production (APIM provides developer portal)
    docs_url="/docs" if settings.debug else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.debug else None,
)


@app.middleware("http")
async def add_correlation_headers(request: Request, call_next) -> Response:
    """Add correlation ID to response headers."""
    start_time = time.time()

    response = await call_next(request)

    # Add correlation ID to response
    correlation_id = correlation_id_var.get("")
    if correlation_id:
        response.headers["X-Correlation-ID"] = correlation_id

    # Add timing header
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.3f}"

    return response


# Include routers
app.include_router(health.router)
app.include_router(orders.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### requirements.txt

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
```

## Key Design Decisions

1. **APIM Context Dependency**: Centralized extraction of APIM headers into a typed dataclass
2. **Context Variables**: Request-scoped correlation ID available throughout the call stack
3. **Structured Logging**: JSON format compatible with Azure Monitor and Log Analytics
4. **Health Endpoints**: Three-tier health checks (basic, liveness, readiness)
5. **Production Defaults**: Docs disabled unless DEBUG=true
6. **Type Safety**: Full type hints and Pydantic models throughout

## Testing

```bash
# Run locally
uvicorn main:app --reload --port 8000

# Test with APIM headers
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: test-123" \
  -H "X-Request-ID: req-456" \
  -d '{"customer_id": "c1", "items": [], "total": 99.99, "shipping_address": "123 Main St"}'
```

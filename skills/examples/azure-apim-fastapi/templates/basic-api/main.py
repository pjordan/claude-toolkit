"""
Basic FastAPI service designed for Azure APIM integration.

This template provides:
- APIM header handling
- Health check endpoint
- Structured logging
- Correlation ID propagation
"""

from fastapi import FastAPI, Request, Header, Depends, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4
import logging
import json

from config import settings

# Structured JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if hasattr(record, 'correlation_id'):
            log_obj["correlationId"] = record.correlation_id
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

# Configure logging
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.root.handlers = [handler]
logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Service starting", extra={"correlation_id": "startup"})
    yield
    logger.info("Service shutting down", extra={"correlation_id": "shutdown"})


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="FastAPI service behind Azure APIM",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.debug else None,
)


# Models
class APIMContext(BaseModel):
    """Context extracted from APIM headers."""
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    subscription_key: Optional[str] = None
    user_id: Optional[str] = None
    client_ip: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str


class ItemRequest(BaseModel):
    name: str = Field(..., description="Item name", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Item description")


class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: str
    request_id: Optional[str]


class ErrorResponse(BaseModel):
    error: str
    message: str
    correlation_id: Optional[str] = None


# Dependencies
async def get_apim_context(
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID"),
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-ID"),
    ocp_apim_subscription_key: Optional[str] = Header(None, alias="Ocp-Apim-Subscription-Key"),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    x_forwarded_for: Optional[str] = Header(None, alias="X-Forwarded-For"),
) -> APIMContext:
    """Extract APIM context from request headers."""
    return APIMContext(
        request_id=x_request_id,
        correlation_id=x_correlation_id or x_request_id or str(uuid4()),
        subscription_key=ocp_apim_subscription_key,
        user_id=x_user_id,
        client_ip=x_forwarded_for.split(",")[0].strip() if x_forwarded_for else None,
    )


# Middleware
@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    """Add correlation ID to response headers."""
    correlation_id = request.headers.get(
        "X-Correlation-ID",
        request.headers.get("X-Request-ID", str(uuid4()))
    )

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    correlation_id = request.headers.get("X-Correlation-ID", "unknown")
    logger.exception("Unhandled exception", extra={"correlation_id": correlation_id})

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="internal_error",
            message="An unexpected error occurred",
            correlation_id=correlation_id,
        ).model_dump()
    )


# Endpoints
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for APIM and load balancers."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version=settings.version,
    )


@app.get("/health/live", tags=["Health"])
async def liveness():
    """Kubernetes liveness probe."""
    return {"status": "alive"}


@app.get("/health/ready", tags=["Health"])
async def readiness():
    """Kubernetes readiness probe."""
    return {"status": "ready"}


@app.get("/api/v1/items", tags=["Items"])
async def list_items(ctx: APIMContext = Depends(get_apim_context)):
    """List all items."""
    logger.info(
        "Listing items",
        extra={"correlation_id": ctx.correlation_id, "user_id": ctx.user_id}
    )

    # Mock data - replace with actual implementation
    return {
        "items": [
            {"id": "1", "name": "Item 1", "description": "First item"},
            {"id": "2", "name": "Item 2", "description": "Second item"},
        ],
        "request_id": ctx.request_id,
    }


@app.post("/api/v1/items", response_model=ItemResponse, status_code=201, tags=["Items"])
async def create_item(
    item: ItemRequest,
    ctx: APIMContext = Depends(get_apim_context)
):
    """Create a new item."""
    logger.info(
        f"Creating item: {item.name}",
        extra={"correlation_id": ctx.correlation_id, "user_id": ctx.user_id}
    )

    # Mock creation - replace with actual implementation
    return ItemResponse(
        id=str(uuid4()),
        name=item.name,
        description=item.description,
        created_at=datetime.utcnow().isoformat(),
        request_id=ctx.request_id,
    )


@app.get("/api/v1/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def get_item(
    item_id: str,
    ctx: APIMContext = Depends(get_apim_context)
):
    """Get a specific item by ID."""
    logger.info(
        f"Getting item: {item_id}",
        extra={"correlation_id": ctx.correlation_id}
    )

    # Mock - replace with actual implementation
    if item_id == "not-found":
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemResponse(
        id=item_id,
        name="Sample Item",
        description="A sample item",
        created_at=datetime.utcnow().isoformat(),
        request_id=ctx.request_id,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )

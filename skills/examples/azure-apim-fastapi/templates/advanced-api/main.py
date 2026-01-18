"""
Advanced FastAPI service with full Azure APIM integration.

This template provides:
- Complete APIM header handling with user context
- JWT validation fallback
- Role-based access control
- Structured logging for Azure Monitor
- Health checks with dependency status
- API versioning
- Request/response correlation
- Rate limiting awareness
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config import settings
from middleware.logging import RequestLoggingMiddleware
from middleware.correlation import CorrelationIdMiddleware
from middleware.security import SecurityHeadersMiddleware
from routers import health, items, admin
from models.errors import setup_exception_handlers
from services.logging import configure_logging

# Configure structured logging
configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Service starting", extra={"event": "startup"})

    # Initialize resources
    # await database.connect()
    # await cache.connect()

    yield

    # Cleanup resources
    # await database.disconnect()
    # await cache.disconnect()

    logger.info("Service shutting down", extra={"event": "shutdown"})


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Advanced FastAPI service with Azure APIM integration",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

# Middleware (order matters - first added = last executed)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)

# CORS for local development only
if settings.debug:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Exception handlers
setup_exception_handlers(app)

# Routers
app.include_router(health.router)
app.include_router(items.router)
app.include_router(admin.router)


# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.version,
        description="Advanced API with Azure APIM integration",
        routes=app.routes,
    )

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Ocp-Apim-Subscription-Key",
            "description": "APIM subscription key"
        },
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Azure AD JWT token"
        }
    }

    # Add servers
    if settings.apim_gateway_url:
        openapi_schema["servers"] = [
            {"url": settings.apim_gateway_url, "description": "Production (APIM)"},
            {"url": f"http://localhost:{settings.port}", "description": "Development"},
        ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.workers,
    )

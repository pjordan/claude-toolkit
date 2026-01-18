# FastAPI Integration with Azure APIM

Comprehensive reference for building FastAPI services that integrate with Azure API Management.

## Application Setup

### Basic Application

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Starting application")
    # Initialize resources (DB connections, caches, etc.)
    yield
    # Cleanup resources
    logger.info("Shutting down application")

app = FastAPI(
    title="My API Service",
    description="FastAPI service behind Azure APIM",
    version="1.0.0",
    lifespan=lifespan,
)
```

### Production Configuration

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    app_name: str = "my-api"
    debug: bool = False
    environment: str = "production"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    # APIM
    apim_gateway_url: str = ""
    validate_subscription_key: bool = True

    # Azure AD
    azure_tenant_id: str = ""
    azure_client_id: str = ""
    azure_audience: str = ""

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

# Conditional documentation based on environment
app = FastAPI(
    title=settings.app_name,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)
```

## APIM Header Handling

### Header Dependencies

```python
from fastapi import Header, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel

class APIMContext(BaseModel):
    """Context extracted from APIM headers."""
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    subscription_id: Optional[str] = None
    subscription_key: Optional[str] = None
    product_name: Optional[str] = None
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_roles: list[str] = []
    client_ip: Optional[str] = None
    trace_enabled: bool = False

async def get_apim_context(
    # Standard APIM headers
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID"),
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-ID"),
    ocp_apim_subscription_key: Optional[str] = Header(None, alias="Ocp-Apim-Subscription-Key"),
    ocp_apim_trace: Optional[str] = Header(None, alias="Ocp-Apim-Trace"),

    # Custom headers forwarded from APIM policies
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    x_user_email: Optional[str] = Header(None, alias="X-User-Email"),
    x_user_roles: Optional[str] = Header(None, alias="X-User-Roles"),
    x_subscription_id: Optional[str] = Header(None, alias="X-Subscription-Id"),
    x_product_name: Optional[str] = Header(None, alias="X-Product-Name"),
    x_forwarded_for: Optional[str] = Header(None, alias="X-Forwarded-For"),
) -> APIMContext:
    """Extract APIM context from request headers."""
    return APIMContext(
        request_id=x_request_id,
        correlation_id=x_correlation_id,
        subscription_id=x_subscription_id,
        subscription_key=ocp_apim_subscription_key,
        product_name=x_product_name,
        user_id=x_user_id,
        user_email=x_user_email,
        user_roles=x_user_roles.split(",") if x_user_roles else [],
        client_ip=x_forwarded_for.split(",")[0].strip() if x_forwarded_for else None,
        trace_enabled=ocp_apim_trace == "true",
    )

# Usage in endpoints
@app.get("/api/v1/resource")
async def get_resource(ctx: APIMContext = Depends(get_apim_context)):
    return {
        "data": "...",
        "request_id": ctx.request_id,
        "user": ctx.user_id,
    }
```

### Subscription Key Validation

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(
    name="Ocp-Apim-Subscription-Key",
    auto_error=False,
    description="APIM subscription key"
)

async def validate_subscription_key(
    api_key: Optional[str] = Security(api_key_header),
) -> str:
    """
    Validate subscription key.

    Note: APIM typically validates this, but this provides
    defense-in-depth for direct backend access.
    """
    if settings.validate_subscription_key:
        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="Subscription key required",
                headers={"WWW-Authenticate": "ApiKey"}
            )
        # Optional: Additional validation against known keys
    return api_key or ""

@app.get("/api/v1/protected")
async def protected_endpoint(
    subscription_key: str = Depends(validate_subscription_key)
):
    return {"status": "authenticated"}
```

## Middleware Patterns

### Correlation ID Middleware

```python
from contextvars import ContextVar
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

correlation_id_var: ContextVar[str] = ContextVar('correlation_id', default='')

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get from APIM header or generate new
        correlation_id = request.headers.get(
            "X-Correlation-ID",
            request.headers.get("X-Request-ID", str(uuid4()))
        )
        correlation_id_var.set(correlation_id)

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response

app.add_middleware(CorrelationIdMiddleware)
```

### Request Logging Middleware

```python
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        # Log request
        logger.info(
            "Request started",
            extra={
                "correlation_id": correlation_id_var.get(),
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.headers.get("X-Forwarded-For", request.client.host),
            }
        )

        response = await call_next(request)

        # Log response
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "Request completed",
            extra={
                "correlation_id": correlation_id_var.get(),
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            }
        )

        return response

app.add_middleware(RequestLoggingMiddleware)
```

### Security Headers Middleware

```python
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Security headers (some may be set by APIM)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        # Remove server identification
        response.headers.pop("Server", None)

        return response

app.add_middleware(SecurityHeadersMiddleware)
```

## Authentication Patterns

### JWT Claims from APIM

When APIM validates JWT and forwards claims via headers:

```python
from pydantic import BaseModel
from typing import Optional

class UserContext(BaseModel):
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    roles: list[str] = []
    tenant_id: Optional[str] = None

async def get_user_context(
    x_user_id: str = Header(..., alias="X-User-Id"),
    x_user_email: Optional[str] = Header(None, alias="X-User-Email"),
    x_user_name: Optional[str] = Header(None, alias="X-User-Name"),
    x_user_roles: Optional[str] = Header(None, alias="X-User-Roles"),
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-Id"),
) -> UserContext:
    """Extract validated user context from APIM-forwarded headers."""
    return UserContext(
        user_id=x_user_id,
        email=x_user_email,
        name=x_user_name,
        roles=x_user_roles.split(",") if x_user_roles else [],
        tenant_id=x_tenant_id,
    )

# Role-based authorization
def require_roles(*required_roles: str):
    async def check_roles(user: UserContext = Depends(get_user_context)):
        if not any(role in user.roles for role in required_roles):
            raise HTTPException(
                status_code=403,
                detail=f"Required roles: {required_roles}"
            )
        return user
    return check_roles

@app.get("/api/v1/admin")
async def admin_endpoint(
    user: UserContext = Depends(require_roles("Admin", "SuperAdmin"))
):
    return {"message": f"Hello admin {user.name}"}
```

### Direct JWT Validation (Fallback)

For scenarios where backend needs to validate JWT directly:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import jwt

security = HTTPBearer(auto_error=False)

class JWTValidator:
    def __init__(self):
        self.jwks_client = None
        self.jwks_uri = f"https://login.microsoftonline.com/{settings.azure_tenant_id}/discovery/v2.0/keys"

    async def get_jwks(self):
        if not self.jwks_client:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.jwks_uri)
                self.jwks_client = jwt.PyJWKClient(self.jwks_uri)
        return self.jwks_client

    async def validate_token(self, token: str) -> dict:
        try:
            jwks = await self.get_jwks()
            signing_key = jwks.get_signing_key_from_jwt(token)

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=settings.azure_audience,
                issuer=f"https://login.microsoftonline.com/{settings.azure_tenant_id}/v2.0",
            )
            return payload
        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(status_code=401, detail=str(e))

jwt_validator = JWTValidator()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return await jwt_validator.validate_token(credentials.credentials)
```

## Health Check Endpoints

### Comprehensive Health Checks

```python
from fastapi import APIRouter, Response
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
import asyncio

router = APIRouter(prefix="/health", tags=["Health"])

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class DependencyHealth(BaseModel):
    name: str
    status: HealthStatus
    latency_ms: Optional[float] = None
    message: Optional[str] = None

class HealthResponse(BaseModel):
    status: HealthStatus
    timestamp: str
    version: str
    environment: str
    dependencies: list[DependencyHealth]

async def check_database() -> DependencyHealth:
    """Check database connectivity."""
    start = time.perf_counter()
    try:
        # Your database health check logic
        await db.execute("SELECT 1")
        latency = (time.perf_counter() - start) * 1000
        return DependencyHealth(
            name="database",
            status=HealthStatus.HEALTHY,
            latency_ms=round(latency, 2)
        )
    except Exception as e:
        return DependencyHealth(
            name="database",
            status=HealthStatus.UNHEALTHY,
            message=str(e)
        )

async def check_cache() -> DependencyHealth:
    """Check cache connectivity."""
    start = time.perf_counter()
    try:
        await redis.ping()
        latency = (time.perf_counter() - start) * 1000
        return DependencyHealth(
            name="cache",
            status=HealthStatus.HEALTHY,
            latency_ms=round(latency, 2)
        )
    except Exception as e:
        return DependencyHealth(
            name="cache",
            status=HealthStatus.DEGRADED,  # Cache failure is degraded, not unhealthy
            message=str(e)
        )

@router.get("", response_model=HealthResponse)
async def health_check(response: Response):
    """
    Comprehensive health check for APIM and monitoring.

    Returns overall health status based on dependency checks.
    """
    # Run all health checks concurrently
    checks = await asyncio.gather(
        check_database(),
        check_cache(),
        return_exceptions=True
    )

    dependencies = []
    for check in checks:
        if isinstance(check, Exception):
            dependencies.append(DependencyHealth(
                name="unknown",
                status=HealthStatus.UNHEALTHY,
                message=str(check)
            ))
        else:
            dependencies.append(check)

    # Determine overall status
    if any(d.status == HealthStatus.UNHEALTHY for d in dependencies):
        overall_status = HealthStatus.UNHEALTHY
        response.status_code = 503
    elif any(d.status == HealthStatus.DEGRADED for d in dependencies):
        overall_status = HealthStatus.DEGRADED
    else:
        overall_status = HealthStatus.HEALTHY

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat(),
        version=settings.version,
        environment=settings.environment,
        dependencies=dependencies
    )

@router.get("/live")
async def liveness():
    """
    Kubernetes liveness probe.

    Returns 200 if the application is running.
    """
    return {"status": "alive"}

@router.get("/ready")
async def readiness():
    """
    Kubernetes readiness probe.

    Returns 200 if the application is ready to receive traffic.
    """
    # Check if critical dependencies are ready
    db_health = await check_database()
    if db_health.status == HealthStatus.UNHEALTHY:
        raise HTTPException(status_code=503, detail="Database not ready")

    return {"status": "ready"}

app.include_router(router)
```

## Error Handling

### Global Exception Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    error: str
    message: str
    correlation_id: Optional[str] = None
    details: Optional[dict] = None

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    correlation_id = correlation_id_var.get()

    logger.exception(
        "Unhandled exception",
        extra={
            "correlation_id": correlation_id,
            "path": request.url.path,
        }
    )

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="internal_error",
            message="An unexpected error occurred",
            correlation_id=correlation_id,
        ).model_dump()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    correlation_id = correlation_id_var.get()

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail if isinstance(exc.detail, str) else "error",
            message=str(exc.detail),
            correlation_id=correlation_id,
        ).model_dump(),
        headers=exc.headers,
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="validation_error",
            message="Request validation failed",
            correlation_id=correlation_id_var.get(),
            details={"errors": exc.errors()},
        ).model_dump()
    )
```

## Structured Logging

### JSON Log Formatter for Azure Monitor

```python
import logging
import json
from datetime import datetime
from typing import Any

class AzureMonitorFormatter(logging.Formatter):
    """JSON formatter compatible with Azure Monitor."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add correlation ID if available
        if hasattr(record, 'correlation_id'):
            log_obj["correlationId"] = record.correlation_id
        else:
            try:
                log_obj["correlationId"] = correlation_id_var.get()
            except LookupError:
                pass

        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ('name', 'msg', 'args', 'created', 'filename',
                          'funcName', 'levelname', 'levelno', 'lineno',
                          'module', 'msecs', 'pathname', 'process',
                          'processName', 'relativeCreated', 'stack_info',
                          'thread', 'threadName', 'exc_info', 'exc_text',
                          'correlation_id', 'message', 'taskName'):
                log_obj[key] = value

        # Add exception info
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj, default=str)

def configure_logging():
    """Configure logging for Azure Monitor integration."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper()))

    # Remove existing handlers
    root_logger.handlers = []

    # Add JSON handler
    handler = logging.StreamHandler()
    handler.setFormatter(AzureMonitorFormatter())
    root_logger.addHandler(handler)

# Call during startup
configure_logging()
```

## API Versioning

### URL Path Versioning

```python
from fastapi import APIRouter

# Version 1
v1_router = APIRouter(prefix="/api/v1", tags=["v1"])

@v1_router.get("/users")
async def get_users_v1():
    return {"version": "1", "users": [...]}

# Version 2
v2_router = APIRouter(prefix="/api/v2", tags=["v2"])

@v2_router.get("/users")
async def get_users_v2():
    return {"version": "2", "data": {"users": [...]}, "pagination": {...}}

app.include_router(v1_router)
app.include_router(v2_router)
```

### Header-Based Versioning

```python
async def get_api_version(
    api_version: str = Header("1", alias="X-API-Version")
) -> str:
    if api_version not in ["1", "2"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported API version: {api_version}"
        )
    return api_version

@app.get("/api/users")
async def get_users(version: str = Depends(get_api_version)):
    if version == "1":
        return {"users": [...]}
    else:
        return {"data": {"users": [...]}, "pagination": {...}}
```

## Response Models

### Standard Response Wrapper

```python
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    data: T
    meta: Optional[dict] = None

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response."""
    data: list[T]
    pagination: dict

    @classmethod
    def create(cls, items: list[T], total: int, page: int, page_size: int):
        return cls(
            data=items,
            pagination={
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size,
            }
        )

# Usage
@app.get("/api/v1/users", response_model=PaginatedResponse[User])
async def list_users(page: int = 1, page_size: int = 20):
    users, total = await user_service.get_users(page, page_size)
    return PaginatedResponse.create(users, total, page, page_size)
```

## OpenAPI Customization

### Custom OpenAPI for APIM

```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="API service behind Azure APIM",
        routes=app.routes,
    )

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Ocp-Apim-Subscription-Key"
        },
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Add servers
    openapi_schema["servers"] = [
        {"url": settings.apim_gateway_url, "description": "Production (APIM)"},
        {"url": "http://localhost:8000", "description": "Development"},
    ]

    # Add global security
    openapi_schema["security"] = [
        {"ApiKeyAuth": []},
        {"BearerAuth": []}
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

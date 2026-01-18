---
name: azure-apim-fastapi
description: Comprehensive development toolkit for building FastAPI services behind Azure API Management (APIM). Use when creating APIs with APIM gateway integration, implementing authentication/authorization patterns, configuring policies, setting up rate limiting, or deploying FastAPI services to Azure. Triggers include "azure apim", "api management", "apim fastapi", "azure gateway", "apim policy", or when building production APIs requiring enterprise features like throttling, caching, and transformation.
---

# Azure APIM + FastAPI Development Skill

Build production-ready FastAPI services integrated with Azure API Management for enterprise-grade API delivery with security, monitoring, and governance.

## Workflow Decision Tree

Use this decision tree to determine the workflow:

**1. Creating a new FastAPI service for APIM?**
   → Use [Create New Service](#create-new-service) workflow

**2. Configuring APIM gateway and policies?**
   → Use [Configure APIM](#configure-apim) workflow

**3. Implementing authentication/authorization?**
   → Use [Add Authentication](#add-authentication) workflow

**4. Adding rate limiting, caching, or transformation?**
   → Use [Add Policies](#add-policies) workflow

**5. Deploying to Azure?**
   → Use [Deploy Service](#deploy-service) workflow

**6. Need reference patterns or examples?**
   → Read [references/apim_patterns.md](references/apim_patterns.md) or [references/fastapi_apim_integration.md](references/fastapi_apim_integration.md)

## Create New Service

Create a FastAPI service designed to work behind Azure APIM.

### Quick Start

```bash
# Clone basic template
cp -r templates/basic-api my-api
cd my-api

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload --port 8000
```

### Project Structure

```
my-api/
├── main.py                 # FastAPI application
├── routers/               # API route modules
│   └── v1/               # Versioned endpoints
├── middleware/           # Custom middleware
│   ├── apim_headers.py  # APIM header handling
│   └── correlation.py   # Request correlation
├── models/              # Pydantic models
├── services/            # Business logic
├── config.py            # Configuration management
├── requirements.txt     # Dependencies
└── Dockerfile           # Container build
```

### Basic Service Pattern

```python
from fastapi import FastAPI, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Configure structured logging for Azure Monitor
logging.basicConfig(
    format='{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s","correlation_id":"%(correlation_id)s"}',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize connections
    logger.info("Service starting", extra={"correlation_id": "startup"})
    yield
    # Shutdown: Cleanup resources
    logger.info("Service shutting down", extra={"correlation_id": "shutdown"})

app = FastAPI(
    title="My APIM Service",
    version="1.0.0",
    lifespan=lifespan,
    # Disable docs in production (APIM provides developer portal)
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.DEBUG else None
)

# CORS for local development (APIM handles CORS in production)
if settings.DEBUG:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

### APIM Header Handling

APIM forwards important headers that your service should process:

```python
from fastapi import Header, Depends
from typing import Optional

async def get_apim_context(
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID"),
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-ID"),
    ocp_apim_subscription_key: Optional[str] = Header(None, alias="Ocp-Apim-Subscription-Key"),
    ocp_apim_trace: Optional[str] = Header(None, alias="Ocp-Apim-Trace"),
) -> dict:
    """Extract APIM context from headers."""
    return {
        "request_id": x_request_id,
        "correlation_id": x_correlation_id,
        "subscription_key": ocp_apim_subscription_key,
        "trace_enabled": ocp_apim_trace == "true"
    }

@app.get("/api/v1/resource")
async def get_resource(apim_context: dict = Depends(get_apim_context)):
    logger.info(f"Processing request", extra={"correlation_id": apim_context["correlation_id"]})
    return {"status": "ok", "request_id": apim_context["request_id"]}
```

## Configure APIM

Configure Azure API Management to front your FastAPI service.

### Import OpenAPI Specification

FastAPI automatically generates OpenAPI specs. Import into APIM:

```bash
# Export OpenAPI spec from FastAPI
curl http://localhost:8000/openapi.json > openapi.json

# Import to APIM using Azure CLI
az apim api import \
  --resource-group myResourceGroup \
  --service-name myApimInstance \
  --api-id my-api \
  --path /my-api \
  --specification-format OpenApiJson \
  --specification-path ./openapi.json \
  --display-name "My API" \
  --service-url https://my-backend.azurewebsites.net
```

### Backend Configuration

Configure APIM to route to your FastAPI backend:

```xml
<!-- API-level policy -->
<policies>
    <inbound>
        <base />
        <set-backend-service base-url="https://my-fastapi-app.azurewebsites.net" />
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

### Named Values for Configuration

Store configuration in APIM named values:

```bash
# Create named value (plain text)
az apim nv create \
  --resource-group myResourceGroup \
  --service-name myApimInstance \
  --named-value-id backend-url \
  --display-name "Backend URL" \
  --value "https://my-fastapi-app.azurewebsites.net"

# Create secret named value (from Key Vault)
az apim nv create \
  --resource-group myResourceGroup \
  --service-name myApimInstance \
  --named-value-id api-key \
  --display-name "API Key" \
  --secret true \
  --key-vault "https://myvault.vault.azure.net/secrets/api-key"
```

Use in policies:
```xml
<set-header name="X-API-Key" exists-action="override">
    <value>{{api-key}}</value>
</set-header>
```

## Add Authentication

Implement authentication patterns for APIM and FastAPI.

### Subscription Key Validation

APIM handles subscription keys. Validate in FastAPI as backup:

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="Ocp-Apim-Subscription-Key", auto_error=False)

async def verify_subscription(api_key: str = Security(api_key_header)):
    """Validate subscription key (backup validation)."""
    if not api_key:
        raise HTTPException(status_code=401, detail="Subscription key required")
    # Additional validation if needed
    return api_key

@app.get("/api/v1/protected")
async def protected_endpoint(subscription: str = Depends(verify_subscription)):
    return {"status": "authenticated"}
```

### JWT Validation (Azure AD / Entra ID)

APIM validates JWT tokens. Configure in policy:

```xml
<inbound>
    <validate-jwt header-name="Authorization" failed-validation-httpcode="401">
        <openid-config url="https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration" />
        <audiences>
            <audience>api://my-api</audience>
        </audiences>
        <issuers>
            <issuer>https://sts.windows.net/{tenant-id}/</issuer>
        </issuers>
        <required-claims>
            <claim name="roles" match="any">
                <value>API.Read</value>
                <value>API.Write</value>
            </claim>
        </required-claims>
    </validate-jwt>
    <!-- Forward claims to backend -->
    <set-header name="X-User-Id" exists-action="override">
        <value>@(context.Request.Headers.GetValueOrDefault("Authorization","").AsJwt()?.Claims.GetValueOrDefault("oid", ""))</value>
    </set-header>
</inbound>
```

FastAPI receives validated claims via headers:

```python
from fastapi import Header

@app.get("/api/v1/user-data")
async def get_user_data(
    x_user_id: str = Header(..., alias="X-User-Id"),
    x_user_roles: str = Header(None, alias="X-User-Roles")
):
    """Endpoint receiving validated user context from APIM."""
    return {
        "user_id": x_user_id,
        "roles": x_user_roles.split(",") if x_user_roles else []
    }
```

### Client Certificate Authentication (mTLS)

Configure APIM for client certificates:

```xml
<inbound>
    <choose>
        <when condition="@(context.Request.Certificate == null)">
            <return-response>
                <set-status code="403" reason="Client certificate required" />
            </return-response>
        </when>
        <when condition="@(!context.Request.Certificate.Verify())">
            <return-response>
                <set-status code="403" reason="Invalid client certificate" />
            </return-response>
        </when>
    </choose>
    <set-header name="X-Client-Cert-Thumbprint" exists-action="override">
        <value>@(context.Request.Certificate.Thumbprint)</value>
    </set-header>
</inbound>
```

## Add Policies

Configure APIM policies for rate limiting, caching, and transformation.

### Rate Limiting

```xml
<inbound>
    <!-- Rate limit by subscription key -->
    <rate-limit-by-key
        calls="100"
        renewal-period="60"
        counter-key="@(context.Subscription.Id)"
        increment-condition="@(context.Response.StatusCode >= 200 && context.Response.StatusCode < 400)" />

    <!-- Quota by subscription -->
    <quota-by-key
        calls="10000"
        bandwidth="50000"
        renewal-period="86400"
        counter-key="@(context.Subscription.Id)" />
</inbound>

<outbound>
    <!-- Return rate limit headers -->
    <set-header name="X-RateLimit-Remaining" exists-action="override">
        <value>@(context.Variables.GetValueOrDefault<string>("remainingCalls", ""))</value>
    </set-header>
</outbound>
```

Handle rate limit responses in FastAPI:

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(429)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded",
            "message": "Too many requests. Please retry later.",
            "retry_after": 60
        },
        headers={"Retry-After": "60"}
    )
```

### Response Caching

```xml
<inbound>
    <!-- Cache GET requests for 5 minutes -->
    <cache-lookup vary-by-developer="false" vary-by-developer-groups="false">
        <vary-by-header>Accept</vary-by-header>
        <vary-by-query-parameter>version</vary-by-query-parameter>
    </cache-lookup>
</inbound>

<outbound>
    <cache-store duration="300" />
</outbound>
```

Control caching from FastAPI:

```python
from fastapi import Response

@app.get("/api/v1/cacheable")
async def cacheable_resource(response: Response):
    response.headers["Cache-Control"] = "public, max-age=300"
    return {"data": "cacheable content"}

@app.get("/api/v1/no-cache")
async def non_cacheable_resource(response: Response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return {"data": "fresh content"}
```

### Request/Response Transformation

```xml
<inbound>
    <!-- Add correlation ID if not present -->
    <set-header name="X-Correlation-ID" exists-action="skip">
        <value>@(Guid.NewGuid().ToString())</value>
    </set-header>

    <!-- Transform request body -->
    <set-body>@{
        var body = context.Request.Body.As<JObject>();
        body["timestamp"] = DateTime.UtcNow.ToString("o");
        body["source"] = "apim";
        return body.ToString();
    }</set-body>
</inbound>

<outbound>
    <!-- Remove internal headers -->
    <set-header name="X-Powered-By" exists-action="delete" />
    <set-header name="Server" exists-action="delete" />

    <!-- Add API version header -->
    <set-header name="X-API-Version" exists-action="override">
        <value>1.0</value>
    </set-header>
</outbound>
```

### Error Handling

```xml
<on-error>
    <set-header name="Content-Type" exists-action="override">
        <value>application/json</value>
    </set-header>
    <set-body>@{
        return new JObject(
            new JProperty("error", new JObject(
                new JProperty("code", context.Response.StatusCode),
                new JProperty("message", context.LastError.Message),
                new JProperty("correlation_id", context.RequestId)
            ))
        ).ToString();
    }</set-body>
</on-error>
```

## Deploy Service

Deploy FastAPI to Azure with APIM integration.

### Deploy to Azure Container Apps

```bash
# Build and push container
az acr build --registry myregistry --image my-api:latest .

# Create Container App
az containerapp create \
  --name my-api \
  --resource-group myResourceGroup \
  --environment myEnvironment \
  --image myregistry.azurecr.io/my-api:latest \
  --target-port 8000 \
  --ingress internal \
  --min-replicas 1 \
  --max-replicas 10

# Get internal URL for APIM backend
az containerapp show --name my-api --resource-group myResourceGroup --query "properties.configuration.ingress.fqdn"
```

### Deploy to Azure App Service

```bash
# Create App Service plan
az appservice plan create \
  --name myPlan \
  --resource-group myResourceGroup \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --name my-api \
  --resource-group myResourceGroup \
  --plan myPlan \
  --runtime "PYTHON:3.11"

# Configure startup command
az webapp config set \
  --name my-api \
  --resource-group myResourceGroup \
  --startup-file "gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker"

# Deploy code
az webapp deployment source config-local-git \
  --name my-api \
  --resource-group myResourceGroup
```

### Configure APIM Backend

```bash
# Create backend entity
az apim backend create \
  --resource-group myResourceGroup \
  --service-name myApimInstance \
  --backend-id my-fastapi-backend \
  --protocol http \
  --url https://my-api.azurewebsites.net \
  --validate-certificate-chain true \
  --validate-certificate-name true

# Update API to use backend
az apim api update \
  --resource-group myResourceGroup \
  --service-name myApimInstance \
  --api-id my-api \
  --service-url https://my-api.azurewebsites.net
```

### Health Check Endpoint

Always implement health checks for APIM and Azure:

```python
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(tags=["Health"])

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    dependencies: dict

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for APIM and load balancers."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        dependencies={
            "database": "connected",
            "cache": "connected"
        }
    )

@router.get("/health/live")
async def liveness():
    """Kubernetes liveness probe."""
    return {"status": "alive"}

@router.get("/health/ready")
async def readiness():
    """Kubernetes readiness probe."""
    # Check dependencies
    return {"status": "ready"}
```

## Key Concepts

### APIM Gateway Architecture

```
Client → APIM Gateway → FastAPI Backend
           │
           ├── Authentication (JWT, API Key, mTLS)
           ├── Rate Limiting
           ├── Caching
           ├── Request/Response Transformation
           ├── Logging & Monitoring
           └── Policy Enforcement
```

### Policy Execution Order

1. **Inbound**: Client → APIM (before backend call)
2. **Backend**: APIM → Backend service
3. **Outbound**: Backend → APIM → Client (after backend response)
4. **On-Error**: Executed when errors occur

### Environment Configuration

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    app_name: str = "my-api"
    debug: bool = False
    version: str = "1.0.0"

    # Azure
    azure_tenant_id: str = ""
    azure_client_id: str = ""

    # APIM
    apim_gateway_url: str = ""
    validate_apim_headers: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## Resources

### Scripts (`scripts/`)
- `import_to_apim.sh` - Import OpenAPI spec to APIM
- `deploy_backend.sh` - Deploy FastAPI to Azure
- `test_policies.sh` - Test APIM policies locally

### References (`references/`)
- `apim_patterns.md` - APIM policy patterns, expressions, and best practices
- `fastapi_apim_integration.md` - FastAPI patterns for APIM integration

### Templates (`templates/`)
- `basic-api/` - Minimal FastAPI service with APIM header handling
- `advanced-api/` - Full-featured service with auth, middleware, and monitoring

## Common Patterns

### API Versioning

```python
from fastapi import APIRouter

# Version via URL path
v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

app.include_router(v1_router)
app.include_router(v2_router)
```

APIM versioning scheme:
```xml
<api-version-set>
    <display-name>My API</display-name>
    <versioning-scheme>Segment</versioning-scheme>
</api-version-set>
```

### Correlation ID Propagation

```python
from contextvars import ContextVar
from uuid import uuid4

correlation_id: ContextVar[str] = ContextVar('correlation_id', default='')

@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    # Get from APIM or generate
    corr_id = request.headers.get("X-Correlation-ID", str(uuid4()))
    correlation_id.set(corr_id)

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = corr_id
    return response
```

### Structured Logging for Azure Monitor

```python
import logging
import json
from datetime import datetime

class AzureLogFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "correlation_id": getattr(record, 'correlation_id', ''),
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)
```

## Troubleshooting

**APIM returns 500 but backend works locally:**
- Check backend URL configuration
- Verify SSL certificate chain
- Enable APIM tracing to see backend response

**Authentication failures:**
- Verify JWT audience and issuer match APIM config
- Check token expiration
- Validate required claims are present

**Rate limiting not working:**
- Ensure counter-key is correctly configured
- Check if requests are being cached (cached requests don't count)
- Verify policy is at correct scope (API vs operation)

**CORS issues:**
- APIM handles CORS in production; configure in APIM policy
- Only enable CORS middleware in FastAPI for local development

**Performance issues:**
- Enable response caching in APIM
- Use async handlers in FastAPI
- Configure proper connection pooling

For additional guidance, read the reference documentation in `references/`.

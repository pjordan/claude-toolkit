# FastAPI Integration Guide

## Table of Contents
1. [Application Setup](#application-setup)
2. [Middleware](#middleware)
3. [Authentication](#authentication)
4. [CORS Configuration](#cors-configuration)
5. [OpenAPI Documentation](#openapi-documentation)
6. [Background Tasks](#background-tasks)

## Application Setup

### Basic Setup
```python
from fastapi import FastAPI
from a2a import A2AServer

app = FastAPI(
    title="My A2A Agent",
    description="Agent description",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

a2a_server = A2AServer(
    app=app,
    agent_name="my-agent",
    agent_description="My agent description"
)
```

### Production Setup
```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Production Agent",
    docs_url=None if settings.production else "/docs",
    redoc_url=None if settings.production else "/redoc"
)

# Add security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## Middleware

### Request Logging
```python
from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url}")

    # Process request
    response = await call_next(request)

    # Log response
    duration = time.time() - start_time
    logger.info(f"Response: {response.status_code} (took {duration:.2f}s)")

    return response
```

### Request ID Middleware
```python
from uuid import uuid4

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response
```

### Rate Limiting
```python
from fastapi import HTTPException
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
        self.clients = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        # Clean old requests
        self.clients[client_id] = [
            ts for ts in self.clients[client_id]
            if now - ts < self.window
        ]

        if len(self.clients[client_id]) >= self.requests:
            return False

        self.clients[client_id].append(now)
        return True

rate_limiter = RateLimiter(requests=100, window=60)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = request.client.host

    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(status_code=429, detail="Too many requests")

    return await call_next(request)
```

## Authentication

### API Key Authentication
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# Use in handlers
@app.post("/protected")
async def protected_endpoint(api_key: str = Security(verify_api_key)):
    return {"message": "Authorized"}
```

### JWT Authentication
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=["HS256"]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
```

## CORS Configuration

### Basic CORS
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Production CORS
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,
)
```

## OpenAPI Documentation

### Custom OpenAPI Schema
```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Custom Agent API",
        version="1.0.0",
        description="Custom agent API documentation",
        routes=app.routes,
    )

    # Add custom fields
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### Tags and Metadata
```python
tags_metadata = [
    {
        "name": "agents",
        "description": "Agent operations",
    },
    {
        "name": "health",
        "description": "Health check endpoints",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}
```

## Background Tasks

### Simple Background Task
```python
from fastapi import BackgroundTasks

def send_notification(email: str, message: str):
    # Send email notification
    logger.info(f"Sending notification to {email}")

@app.post("/process")
async def process_data(background_tasks: BackgroundTasks):
    # Process synchronously
    result = process_immediately()

    # Schedule background task
    background_tasks.add_task(send_notification, "user@example.com", "Processing complete")

    return {"result": result}
```

### Complex Background Tasks
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def process_in_background(data: dict):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, heavy_computation, data)

@app.post("/heavy-process")
async def heavy_process(background_tasks: BackgroundTasks, data: dict):
    background_tasks.add_task(process_in_background, data)
    return {"status": "processing started"}
```

### Startup and Shutdown Events
```python
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up agent...")
    # Initialize connections
    await database.connect()
    await redis.connect()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down agent...")
    # Close connections
    await database.disconnect()
    await redis.disconnect()
```

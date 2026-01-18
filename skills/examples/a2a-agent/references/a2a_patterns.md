# A2A SDK Patterns and Best Practices

## Table of Contents
1. [Handler Patterns](#handler-patterns)
2. [Request/Response Models](#requestresponse-models)
3. [Context Usage](#context-usage)
4. [Streaming Patterns](#streaming-patterns)
5. [Error Handling](#error-handling)
6. [State Management](#state-management)
7. [Testing Patterns](#testing-patterns)
8. [Deployment Patterns](#deployment-patterns)

## Handler Patterns

### Basic Handler
```python
@a2a_server.handler("action_name", request_model=RequestModel, response_model=ResponseModel)
async def handle_action(request: RequestModel, context: Context) -> ResponseModel:
    # Process request
    result = await process(request)
    return ResponseModel(**result)
```

### Streaming Handler
```python
@a2a_server.streaming_handler("stream_action", request_model=RequestModel)
async def handle_stream(request: RequestModel, context: StreamingContext) -> AsyncGenerator[str, None]:
    async for item in data_source:
        yield f"data: {item}\n"
```

### Multiple Handlers
Organize related handlers together:
```python
# Text processing handlers
@a2a_server.handler("text.analyze", ...)
async def analyze_text(...): ...

@a2a_server.handler("text.summarize", ...)
async def summarize_text(...): ...

# Data handlers
@a2a_server.handler("data.query", ...)
async def query_data(...): ...
```

## Request/Response Models

### Basic Models
Always use Pydantic models with Field descriptions:
```python
class MyRequest(BaseModel):
    text: str = Field(..., description="Input text to process")
    options: Optional[dict] = Field(default_factory=dict, description="Processing options")
    max_length: int = Field(100, description="Maximum output length", ge=1, le=1000)

class MyResponse(BaseModel):
    result: str = Field(..., description="Processed result")
    metadata: dict = Field(default_factory=dict, description="Processing metadata")
```

### Validation Patterns
```python
from pydantic import validator, Field

class Request(BaseModel):
    email: str = Field(..., description="User email")
    age: int = Field(..., description="User age", ge=0, le=150)

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v
```

### Nested Models
```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class UserRequest(BaseModel):
    name: str
    address: Address
    tags: List[str] = Field(default_factory=list)
```

## Context Usage

### Accessing Context
```python
async def handle_request(request: RequestModel, context: Context):
    # Agent information
    agent_name = context.agent_name

    # Request metadata
    request_id = context.request_id
    timestamp = context.timestamp

    # Custom context data
    user_id = context.get("user_id")
```

### Adding Context Data
```python
@app.middleware("http")
async def add_context(request: Request, call_next):
    # Extract and add context data
    request.state.user_id = extract_user_id(request)
    response = await call_next(request)
    return response
```

## Streaming Patterns

### Server-Sent Events (SSE)
```python
@a2a_server.streaming_handler("generate", request_model=GenerateRequest)
async def handle_generate(request: GenerateRequest, context: StreamingContext) -> AsyncGenerator[str, None]:
    for token in generate_tokens(request.prompt):
        yield f"data: {token}\n\n"
    yield "data: [DONE]\n\n"
```

### Progress Updates
```python
async def process_with_progress(data: list) -> AsyncGenerator[dict, None]:
    total = len(data)
    for i, item in enumerate(data):
        result = await process_item(item)
        yield {
            "progress": (i + 1) / total,
            "current": i + 1,
            "total": total,
            "result": result
        }
```

### Error Handling in Streams
```python
async def safe_stream(source: AsyncGenerator) -> AsyncGenerator[str, None]:
    try:
        async for item in source:
            yield f"data: {json.dumps(item)}\n\n"
    except Exception as e:
        logger.error(f"Stream error: {e}")
        yield f"error: {str(e)}\n\n"
    finally:
        yield "event: close\n\n"
```

## Error Handling

### Custom Error Classes
```python
class AgentError(Exception):
    """Base exception for agent errors."""
    pass

class ValidationError(AgentError):
    """Validation failed."""
    pass

class ProcessingError(AgentError):
    """Processing failed."""
    pass
```

### Error Handler Middleware
```python
@app.exception_handler(AgentError)
async def agent_error_handler(request: Request, exc: AgentError):
    logger.error(f"Agent error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )
```

### Handler Error Pattern
```python
async def handle_with_errors(request: RequestModel, context: Context) -> ResponseModel:
    try:
        # Validate input
        if not request.text:
            raise ValidationError("Text cannot be empty")

        # Process
        result = await process(request.text)

        # Validate output
        if not result:
            raise ProcessingError("Processing returned no result")

        return ResponseModel(result=result)

    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except ProcessingError as e:
        logger.error(f"Processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

## State Management

### In-Memory State (Development)
```python
class StateStore:
    def __init__(self):
        self._data = {}
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: any, ttl: Optional[int] = None):
        async with self._lock:
            self._data[key] = {
                "value": value,
                "timestamp": datetime.now(),
                "ttl": ttl
            }

    async def get(self, key: str) -> Optional[any]:
        async with self._lock:
            item = self._data.get(key)
            if item and self._is_expired(item):
                del self._data[key]
                return None
            return item["value"] if item else None
```

### Redis State (Production)
```python
import redis.asyncio as redis

class RedisStateStore:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def set(self, key: str, value: any, ttl: int = 3600):
        await self.redis.setex(
            key,
            ttl,
            json.dumps(value)
        )

    async def get(self, key: str) -> Optional[any]:
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    async def delete(self, key: str):
        await self.redis.delete(key)
```

### Session Management
```python
from uuid import uuid4

class SessionManager:
    def __init__(self, store: StateStore):
        self.store = store

    async def create_session(self, data: dict) -> str:
        session_id = str(uuid4())
        await self.store.set(f"session:{session_id}", data, ttl=3600)
        return session_id

    async def get_session(self, session_id: str) -> Optional[dict]:
        return await self.store.get(f"session:{session_id}")

    async def update_session(self, session_id: str, data: dict):
        await self.store.set(f"session:{session_id}", data, ttl=3600)
```

## Testing Patterns

### Unit Tests
```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_handler(client):
    response = client.post("/a2a/action", json={"text": "test"})
    assert response.status_code == 200
    assert "result" in response.json()
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_full_workflow():
    # Setup
    agent = create_test_agent()

    # Execute workflow
    result = await agent.execute({
        "action": "process",
        "data": test_data
    })

    # Verify
    assert result["status"] == "success"
```

### Mocking External Services
```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_external_service():
    with patch('agent.external_api_call', new_callable=AsyncMock) as mock:
        mock.return_value = {"data": "mocked"}

        result = await handler(request, context)

        assert mock.called
        assert result.data == "mocked"
```

## Deployment Patterns

### Environment Configuration
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    agent_name: str
    agent_port: int = 8000
    log_level: str = "info"
    redis_url: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
```

### Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agent": settings.agent_name,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health/detailed")
async def detailed_health():
    return {
        "status": "healthy",
        "agent": settings.agent_name,
        "dependencies": {
            "redis": await check_redis(),
            "database": await check_database()
        },
        "metrics": await get_metrics()
    }
```

### Graceful Shutdown
```python
import signal

async def shutdown_handler(sig):
    logger.info(f"Received signal {sig}, shutting down...")

    # Close connections
    await state_store.close()
    await database.close()

    # Stop accepting new requests
    await app.shutdown()

def setup_signals():
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda s, f: asyncio.create_task(shutdown_handler(s)))
```

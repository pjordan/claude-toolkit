---
name: a2a-agent
description: Comprehensive A2A (Agent-to-Agent) development toolkit for building Python agents using a2a-sdk and FastAPI. Use when creating new A2A agents, implementing agent handlers, adding streaming capabilities, testing agents, or deploying agents. Triggers include "a2a agent", "agent-to-agent", "a2a-sdk", "create agent", "agent handler", "streaming agent", or when working with FastAPI-based agent architectures.
---

# A2A Agent Development Skill

Build production-ready A2A agents using a2a-sdk and FastAPI with comprehensive templates, patterns, and deployment tools.

## Workflow Decision Tree

Use this decision tree to determine the workflow:

**1. Creating a new agent from scratch?**
   → Use [Create New Agent](#create-new-agent) workflow

**2. Adding handlers or capabilities to existing agent?**
   → Use [Add Handler](#add-handler) workflow

**3. Testing an existing agent?**
   → Use [Test Agent](#test-agent) workflow

**4. Deploying an agent?**
   → Use [Deploy Agent](#deploy-agent) workflow

**5. Need reference patterns or examples?**
   → Read [references/a2a_patterns.md](references/a2a_patterns.md) or [references/fastapi_integration.md](references/fastapi_integration.md)

## Create New Agent

Use the `create_agent.py` script to scaffold a new agent project:

```bash
python scripts/create_agent.py <agent-name> [--type basic|advanced] [--path <output-path>]
```

**Available templates:**
- `basic`: Minimal agent with simple handler example (recommended for getting started)
- `advanced`: Full-featured agent with streaming, error handling, state management, and middleware

**Example:**
```bash
python scripts/create_agent.py my-agent --type basic --path ./agents
```

**After creation:**
1. Navigate to agent directory: `cd agents/my-agent`
2. Install dependencies: `pip install -r requirements.txt`
3. Run agent: `python main.py`
4. Test health endpoint: `curl http://localhost:8000/health`
5. View docs: `http://localhost:8000/docs`

**Template files:**
- Basic template: `assets/basic-agent/`
- Advanced template: `assets/advanced-agent/`

## Add Handler

Add new capabilities to an existing agent by implementing handlers.

### Basic Handler Pattern

```python
from pydantic import BaseModel, Field
from a2a import Context

# Define request/response models
class MyRequest(BaseModel):
    input_text: str = Field(..., description="Input text to process")
    options: dict = Field(default_factory=dict, description="Processing options")

class MyResponse(BaseModel):
    result: str = Field(..., description="Processing result")
    metadata: dict = Field(default_factory=dict, description="Response metadata")

# Register handler
@a2a_server.handler("my_action", request_model=MyRequest, response_model=MyResponse)
async def handle_my_action(request: MyRequest, context: Context) -> MyResponse:
    """Handle my action requests."""

    # Process request
    result = process_text(request.input_text, request.options)

    # Return response
    return MyResponse(
        result=result,
        metadata={"agent": context.agent_name}
    )
```

### Streaming Handler Pattern

```python
from typing import AsyncGenerator
from a2a import StreamingContext

@a2a_server.streaming_handler("stream_action", request_model=StreamRequest)
async def handle_stream(request: StreamRequest, context: StreamingContext) -> AsyncGenerator[str, None]:
    """Stream data back to client."""

    async for item in data_source:
        yield f"data: {item}\n\n"

    yield "data: [DONE]\n\n"
```

**Key patterns:**
- Always use Pydantic models with Field descriptions
- Add error handling with try/except
- Use context for agent metadata
- Return properly typed responses

**For advanced patterns, read:**
- `references/a2a_patterns.md` - Handler patterns, error handling, state management
- `references/fastapi_integration.md` - Middleware, authentication, CORS

## Test Agent

Test agents using the provided test script or manual testing.

### Automated Testing

```bash
bash scripts/test_agent.sh
```

This script:
1. Runs unit tests (if `test_agent.py` exists)
2. Tests agent startup
3. Verifies health endpoint

### Manual Testing

**1. Unit tests with pytest:**
```bash
pytest test_agent.py -v
```

**2. Test health endpoint:**
```bash
curl http://localhost:8000/health
```

**3. Test handler:**
```bash
curl -X POST http://localhost:8000/a2a/<handler-name> \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

**4. Test streaming:**
```bash
curl -N http://localhost:8000/a2a/<stream-handler-name> \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

### Writing Tests

Use the test pattern from `assets/advanced-agent/test_agent.py`:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_handler(client):
    response = client.post("/a2a/action", json={"text": "test"})
    assert response.status_code == 200
    assert "result" in response.json()
```

**For comprehensive testing patterns, read:**
- `references/a2a_patterns.md` - Section "Testing Patterns"

## Deploy Agent

Deploy agents using Docker for production environments.

### Quick Deploy

```bash
bash scripts/deploy_agent.sh --name my-agent --port 8000
```

### Manual Docker Deploy

**1. Build image:**
```bash
docker build -t my-agent:latest .
```

**2. Run container:**
```bash
docker run -d \
  --name my-agent \
  -p 8000:8000 \
  --restart unless-stopped \
  my-agent:latest
```

**3. Verify deployment:**
```bash
curl http://localhost:8000/health
```

### Docker Compose Deploy

For agents with dependencies (Redis, databases):

```bash
docker-compose up -d
```

See `assets/advanced-agent/docker-compose.yml` for example configuration.

### Environment Configuration

Create `.env` file from template:
```bash
cp .env.example .env
```

Configure variables:
```bash
AGENT_NAME=my-agent
AGENT_PORT=8000
LOG_LEVEL=info
```

**For production deployment patterns, read:**
- `references/a2a_patterns.md` - Section "Deployment Patterns"
- `references/fastapi_integration.md` - Production setup, middleware

## Key Concepts

### A2A Server Initialization

```python
from fastapi import FastAPI
from a2a import A2AServer

app = FastAPI(title="My Agent")

a2a_server = A2AServer(
    app=app,
    agent_name="my-agent",
    agent_description="Agent description"
)
```

### Handler Registration

Handlers are registered using decorators:
- `@a2a_server.handler()` - Regular request/response
- `@a2a_server.streaming_handler()` - Streaming responses

### Context Access

Context provides agent and request metadata:
```python
async def handler(request: Request, context: Context):
    agent_name = context.agent_name
    request_id = context.request_id
```

### Error Handling

Always wrap handlers in try/except:
```python
try:
    result = await process(request)
    return Response(result=result)
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.error(f"Error: {e}")
    raise HTTPException(status_code=500, detail="Internal error")
```

## Resources

### Scripts (`scripts/`)
- `create_agent.py` - Scaffold new agents from templates
- `test_agent.sh` - Run comprehensive agent tests
- `deploy_agent.sh` - Deploy agents using Docker

### References (`references/`)
- `a2a_patterns.md` - Comprehensive A2A patterns: handlers, streaming, error handling, state management, testing
- `fastapi_integration.md` - FastAPI integration: middleware, authentication, CORS, background tasks

### Assets (`assets/`)
- `basic-agent/` - Minimal agent template with simple handler
- `advanced-agent/` - Full-featured agent with streaming, state, tests, and Docker setup

## Common Patterns

### Adding Multiple Related Handlers

Organize handlers by domain:
```python
# Text processing
@a2a_server.handler("text.analyze", ...)
async def analyze_text(...): ...

@a2a_server.handler("text.summarize", ...)
async def summarize_text(...): ...

# Data operations
@a2a_server.handler("data.query", ...)
async def query_data(...): ...
```

### State Management

Use in-memory store for development, Redis for production:
```python
# Development
state_store = {}

async def set_state(key: str, value: any):
    state_store[key] = value

# Production - use Redis pattern from references/a2a_patterns.md
```

### Middleware

Add request logging, authentication, rate limiting:
```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response
```

See `references/fastapi_integration.md` for complete middleware patterns.

## Troubleshooting

**Agent won't start:**
- Check port availability: `lsof -i :8000`
- Verify dependencies: `pip install -r requirements.txt`
- Check logs for errors

**Handler not found:**
- Verify handler is registered with `@a2a_server.handler()`
- Check handler name matches request
- Ensure handler is defined before `if __name__ == "__main__"`

**Streaming not working:**
- Use `@a2a_server.streaming_handler()` decorator
- Return `AsyncGenerator[str, None]`
- Use `yield` not `return`

**Tests failing:**
- Install test dependencies: `pip install pytest pytest-asyncio httpx`
- Use `TestClient` from FastAPI
- Clear state between tests

For additional guidance, read the reference documentation in `references/`.

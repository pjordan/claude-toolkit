# A2A Agent Development Skill

Comprehensive toolkit for building production-ready A2A (Agent-to-Agent) agents using a2a-sdk and FastAPI.

## 🎯 Purpose

Build Python-based A2A agents with best practices for handlers, streaming, error handling, state management, testing, and deployment.

## 📦 What's Included

### Agent Templates
- **Basic Agent**: Minimal starter template with simple handler
- **Advanced Agent**: Full-featured template with streaming, state management, error handling, middleware, and tests

### Helper Scripts
- `create_agent.py`: Scaffold new agents from templates
- `test_agent.sh`: Automated testing script
- `deploy_agent.sh`: Docker deployment script

### Reference Documentation
- `a2a_patterns.md`: Handler patterns, streaming, error handling, state management, testing
- `fastapi_integration.md`: Middleware, authentication, CORS, background tasks

## 🚀 Quick Start

### Create a New Agent

```bash
python scripts/create_agent.py my-agent --type basic --path ./agents
cd agents/my-agent
pip install -r requirements.txt
python main.py
```

### Add a Handler

```python
from pydantic import BaseModel, Field
from a2a import Context

class MyRequest(BaseModel):
    text: str = Field(..., description="Input text")

class MyResponse(BaseModel):
    result: str = Field(..., description="Processed result")

@a2a_server.handler("process", request_model=MyRequest, response_model=MyResponse)
async def handle_process(request: MyRequest, context: Context) -> MyResponse:
    result = process_text(request.text)
    return MyResponse(result=result)
```

### Test Agent

```bash
bash scripts/test_agent.sh
```

### Deploy Agent

```bash
bash scripts/deploy_agent.sh --name my-agent --port 8000
```

## 🔧 Use When

- Creating new A2A agents from scratch
- Implementing agent handlers and routes
- Adding streaming capabilities to agents
- Testing and debugging agent behavior
- Deploying agents to production
- Working with FastAPI-based agent architectures

## 📚 Workflows

1. **Create New Agent**: Scaffold project with templates
2. **Add Handler**: Implement new capabilities
3. **Test Agent**: Automated and manual testing
4. **Deploy Agent**: Docker-based deployment

## 💡 Key Features

- **Two Ready-to-Use Templates**: Basic and advanced agent starters
- **Comprehensive Patterns**: Handler registration, streaming, error handling
- **State Management**: In-memory and Redis patterns
- **Testing Suite**: Unit tests, integration tests, mocking patterns
- **Production Ready**: Docker, health checks, graceful shutdown
- **FastAPI Integration**: Middleware, authentication, CORS, background tasks

## 📖 Documentation

- **SKILL.md**: Complete usage guide with workflows
- **references/a2a_patterns.md**: Detailed A2A SDK patterns
- **references/fastapi_integration.md**: FastAPI integration guide

## 🏗️ Structure

```
a2a-agent/
├── SKILL.md                    # Main skill documentation
├── README.md                   # This file
├── scripts/                    # Helper scripts
│   ├── create_agent.py        # Agent scaffolding
│   ├── test_agent.sh          # Testing automation
│   └── deploy_agent.sh        # Deployment automation
├── references/                 # Reference documentation
│   ├── a2a_patterns.md        # A2A SDK patterns
│   └── fastapi_integration.md # FastAPI integration
└── templates/                  # Agent templates
    ├── basic-agent/           # Minimal template
    └── advanced-agent/        # Full-featured template
```

## 🎓 Learning Path

1. **Beginner**: Start with basic template, create simple handlers
2. **Intermediate**: Add streaming, error handling, middleware
3. **Advanced**: Implement state management, testing, production deployment

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional agent templates (e.g., database-integrated agents)
- More testing patterns
- Cloud deployment guides (AWS, GCP, Azure)
- Performance optimization patterns
- Security best practices

## 📄 License

Same as claude-toolkit repository.

# Azure APIM + FastAPI Development Skill

Build production-ready FastAPI services integrated with Azure API Management (APIM) for enterprise-grade API delivery.

## Quick Start

### 1. Create a New Service

```bash
# Copy the basic template
cp -r templates/basic-api my-api
cd my-api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload --port 8000
```

### 2. Test Locally

```bash
# Health check
curl http://localhost:8000/health

# View OpenAPI docs
open http://localhost:8000/docs

# Export OpenAPI spec for APIM import
curl http://localhost:8000/openapi.json > openapi.json
```

### 3. Import to APIM

```bash
az apim api import \
  --resource-group myResourceGroup \
  --service-name myApimInstance \
  --api-id my-api \
  --path /my-api \
  --specification-format OpenApiJson \
  --specification-path ./openapi.json
```

## What's Included

| Directory | Description |
|-----------|-------------|
| `SKILL.md` | Complete skill documentation with all workflows |
| `templates/basic-api/` | Minimal FastAPI service with APIM integration |
| `templates/advanced-api/` | Full-featured service with auth, caching, and monitoring |
| `references/` | Detailed documentation on APIM policies and FastAPI patterns |
| `scripts/` | Helper scripts for deployment and testing |

## When to Use This Skill

- Building APIs that require enterprise features (rate limiting, caching, authentication)
- Deploying FastAPI services to Azure with API gateway
- Implementing Azure AD/Entra ID authentication for APIs
- Creating multi-tenant APIs with subscription management
- Adding observability and monitoring to API services

## Key Features

### APIM Integration Patterns
- Subscription key handling
- JWT validation with Azure AD
- Client certificate (mTLS) authentication
- Request/response transformation
- Rate limiting and quotas
- Response caching

### FastAPI Best Practices
- Structured logging for Azure Monitor
- Correlation ID propagation
- Health check endpoints
- API versioning
- Environment configuration

## Prerequisites

- Python 3.9+
- Azure subscription with APIM instance
- Azure CLI installed and authenticated
- Basic understanding of FastAPI and REST APIs

## File Structure

```
azure-apim-fastapi/
├── SKILL.md                              # Main skill documentation
├── README.md                             # This file
├── references/
│   ├── apim_patterns.md                 # APIM policy patterns
│   └── fastapi_apim_integration.md      # FastAPI integration patterns
├── templates/
│   ├── basic-api/                       # Minimal template
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── advanced-api/                    # Full-featured template
│       ├── main.py
│       ├── routers/
│       ├── middleware/
│       ├── models/
│       ├── config.py
│       ├── requirements.txt
│       ├── Dockerfile
│       └── docker-compose.yml
└── scripts/
    ├── import_to_apim.sh               # Import OpenAPI to APIM
    ├── deploy_backend.sh               # Deploy to Azure
    └── test_policies.sh                # Test APIM policies
```

## Resources

- [Azure API Management Documentation](https://docs.microsoft.com/azure/api-management/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Azure AD Authentication](https://docs.microsoft.com/azure/active-directory/)

## Related Skills

- **A2A Agent Development**: For building agent-to-agent services with FastAPI
- **Code Review**: For reviewing API implementations

## Author

Claude Toolkit Contributors

## Version

- **Created**: 2026-01-18
- **Version**: 1.0.0

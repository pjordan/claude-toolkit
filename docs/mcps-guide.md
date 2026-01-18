# MCPs Guide

A guide to building Model Context Protocol servers for Claude.

## Overview

Model Context Protocol (MCP) is a standard for connecting Claude to external tools, data sources, and services. MCP servers expose tools that Claude can discover and use.

## Core Concepts

### What is MCP?

MCP provides:
- **Standardized protocol** for tool integration
- **Discovery mechanism** for available tools
- **Type-safe interfaces** between Claude and tools
- **Bidirectional communication** for complex workflows

### Architecture

```
┌─────────────┐
│   Claude    │
└──────┬──────┘
       │ MCP Protocol
┌──────┴──────┐
│ MCP Server  │
└──────┬──────┘
       │
┌──────┴──────┐
│   External  │
│   Service   │
└─────────────┘
```

### Tools vs Resources

**Tools**: Actions Claude can perform
- `search_database(query)`
- `send_email(to, subject, body)`
- `create_task(title, description)`

**Resources**: Data Claude can read
- `list_files(directory)`
- `read_config(key)`
- `get_user_info(user_id)`

## Creating an MCP Server

### Prerequisites

- Python 3.10+
- MCP SDK: `pip install mcp`
- Understanding of async Python
- API/service you want to integrate

### Minimal Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio

# Create server instance
app = Server("my-server")

# Define available tools
@app.list_tools()
async def list_tools():
    return [
        {
            "name": "greet",
            "description": "Greet a user by name",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of person to greet"
                    }
                },
                "required": ["name"]
            }
        }
    ]

# Handle tool calls
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "greet":
        return {"greeting": f"Hello, {arguments['name']}!"}
    raise ValueError(f"Unknown tool: {name}")

# Start server
if __name__ == "__main__":
    asyncio.run(stdio_server(app))
```

### Step-by-Step Guide

#### 1. Plan Your Tools

Ask:
- What actions should Claude be able to perform?
- What parameters do these actions need?
- What data should be returned?

Example:
```
Tool: search_products
Parameters:
  - query (string): search terms
  - category (string, optional): product category
  - max_results (integer, optional): number of results
Returns:
  - products (array): list of matching products
    - id, name, price, description
```

#### 2. Set Up Project

```bash
mkdir my-mcp-server
cd my-mcp-server
python -m venv venv
source venv/bin/activate
pip install mcp python-dotenv

touch server.py requirements.txt .env.example README.md
```

#### 3. Implement Server

**server.py:**
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = Server("product-search")

@app.list_tools()
async def list_tools():
    return [
        {
            "name": "search_products",
            "description": "Search for products in the catalog",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by category"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        }
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_products":
        # Your API call here
        query = arguments["query"]
        category = arguments.get("category")
        max_results = arguments.get("max_results", 10)
        
        # Example: call your API
        results = await search_api(query, category, max_results)
        
        return {"products": results}
    
    raise ValueError(f"Unknown tool: {name}")

async def search_api(query, category, max_results):
    # Implement your API call
    # This is just a placeholder
    return [
        {
            "id": "1",
            "name": "Product A",
            "price": 29.99,
            "category": category or "general"
        }
    ]

if __name__ == "__main__":
    asyncio.run(stdio_server(app))
```

**requirements.txt:**
```
mcp>=1.0.0
python-dotenv>=1.0.0
httpx>=0.24.0  # for API calls
```

**.env.example:**
```
API_KEY=your_api_key_here
API_ENDPOINT=https://api.example.com
```

#### 4. Configure in Claude

**Claude Desktop:**

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "product-search": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "API_KEY": "your_actual_key"
      }
    }
  }
}
```

**Claude Code:**

```bash
claude-code mcp add product-search python /path/to/server.py
```

#### 5. Test

Start Claude and try:
```
Search for "laptop" in the electronics category
```

Claude should discover and use your `search_products` tool.

## Best Practices

### Tool Design

**Good Tool:**
```json
{
  "name": "create_task",
  "description": "Create a new task in the project management system",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "Task title (max 100 chars)"
      },
      "description": {
        "type": "string",
        "description": "Detailed task description"
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high"],
        "description": "Task priority level"
      },
      "due_date": {
        "type": "string",
        "format": "date",
        "description": "Due date in YYYY-MM-DD format"
      }
    },
    "required": ["title"]
  }
}
```

**Bad Tool:**
```json
{
  "name": "do_stuff",
  "description": "Does things",
  "inputSchema": {
    "type": "object",
    "properties": {
      "data": {"type": "string"}
    }
  }
}
```

### Error Handling

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "search":
            # Validate inputs
            query = arguments.get("query")
            if not query or len(query) < 2:
                return {
                    "error": "Query must be at least 2 characters",
                    "code": "INVALID_QUERY"
                }
            
            # Make API call
            results = await api_search(query)
            return {"results": results}
            
    except APIError as e:
        return {
            "error": f"API error: {str(e)}",
            "code": "API_ERROR"
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "code": "INTERNAL_ERROR"
        }
```

### Security

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Never hardcode credentials
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not set")

# Validate inputs
def validate_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Rate limiting
from collections import defaultdict
from time import time

rate_limits = defaultdict(list)

def check_rate_limit(user_id: str, limit: int = 10) -> bool:
    now = time()
    # Clean old entries
    rate_limits[user_id] = [
        t for t in rate_limits[user_id] 
        if now - t < 60
    ]
    
    if len(rate_limits[user_id]) >= limit:
        return False
    
    rate_limits[user_id].append(now)
    return True
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.info(f"Tool called: {name}")
    logger.debug(f"Arguments: {arguments}")
    
    try:
        result = await process_tool(name, arguments)
        logger.info(f"Tool succeeded: {name}")
        return result
    except Exception as e:
        logger.error(f"Tool failed: {name}, Error: {e}")
        raise
```

## Advanced Topics

### Resources (Read-Only Data)

```python
@app.list_resources()
async def list_resources():
    return [
        {
            "uri": "config://database",
            "name": "Database Configuration",
            "mimeType": "application/json"
        }
    ]

@app.read_resource()
async def read_resource(uri: str):
    if uri == "config://database":
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "application/json",
                    "text": json.dumps({
                        "host": "localhost",
                        "port": 5432
                    })
                }
            ]
        }
```

### Prompts (Templates)

```python
@app.list_prompts()
async def list_prompts():
    return [
        {
            "name": "analyze_data",
            "description": "Analyze data and provide insights",
            "arguments": [
                {
                    "name": "dataset",
                    "description": "Name of dataset to analyze",
                    "required": True
                }
            ]
        }
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict):
    if name == "analyze_data":
        dataset = arguments["dataset"]
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Analyze the {dataset} dataset and provide key insights"
                    }
                }
            ]
        }
```

### Streaming Responses

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "long_running_task":
        async def stream_progress():
            for i in range(10):
                await asyncio.sleep(1)
                yield {"progress": i * 10, "status": f"Step {i+1}"}
        
        return stream_progress()
```

## Testing

### Unit Tests

```python
import pytest
from server import app

@pytest.mark.asyncio
async def test_search_tool():
    tools = await app.list_tools()
    assert len(tools) > 0
    assert tools[0]["name"] == "search"

@pytest.mark.asyncio
async def test_search_execution():
    result = await app.call_tool("search", {"query": "test"})
    assert "results" in result
    assert isinstance(result["results"], list)
```

### Integration Tests

```bash
# Start server
python server.py &
SERVER_PID=$!

# Test with MCP client
mcp-client test localhost:5000

# Cleanup
kill $SERVER_PID
```

## Troubleshooting

### Common Issues

**1. Server not showing in Claude**
- Check config file syntax
- Verify absolute paths
- Restart Claude application

**2. Tools not being called**
- Check tool descriptions are clear
- Verify input schema is correct
- Test tool manually first

**3. Authentication errors**
- Verify .env file exists
- Check environment variables are loaded
- Confirm credentials are valid

**4. Timeout errors**
- Implement proper error handling
- Add timeouts to external calls
- Consider async operations

## Examples Repository

See [mcps/servers/](../mcps/servers/) for complete examples:

- **custom-api**: REST API integration template
- **database-connector**: Database query interface
- **file-system**: File operations
- **email**: Email sending/receiving

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Official Servers](https://github.com/modelcontextprotocol/servers)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)

## Contributing

To contribute an MCP server:

1. Use the [template](../mcps/TEMPLATE.md)
2. Implement and test thoroughly
3. Document all tools and configuration
4. Include security considerations
5. Provide usage examples
6. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full guidelines.

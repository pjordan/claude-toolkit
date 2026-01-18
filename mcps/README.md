# MCP Servers

Model Context Protocol (MCP) servers extend Claude's capabilities with custom tool integrations.

## 📖 What are MCP Servers?

MCP servers provide Claude with:
- Access to external APIs and services
- Database connectivity
- File system operations
- Custom business logic
- Real-time data retrieval

## 🎯 Available Servers

### Custom API
**Path**: `servers/custom-api/`  
**Purpose**: Template for integrating third-party APIs  
**Best For**: REST API integrations, web services

### Database Connector
**Path**: `servers/database-connector/`  
**Purpose**: Query and interact with databases  
**Best For**: Data retrieval, reporting, analytics

## 🔧 Using an MCP Server

### Prerequisites

- Python 3.10 or higher
- Claude Desktop app or Claude Code
- Basic understanding of APIs (for API-based servers)

### Setup Steps

1. **Navigate to Server Directory**
   ```bash
   cd mcps/servers/your-server-name
   ```

2. **Install Dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Test the Server**
   ```bash
   python server.py
   ```

### Connecting to Claude

#### Claude Desktop

Edit your configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the server:
```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "API_KEY": "your_key_here"
      }
    }
  }
}
```

Restart Claude Desktop.

#### Claude Code

```bash
claude-code mcp add your-server-name python /path/to/server.py
```

## ✨ Creating a New MCP Server

### Quick Start

1. Copy the template:
   ```bash
   cp -r mcps/TEMPLATE.md mcps/servers/your-server-name/README.md
   ```

2. Create server structure:
   ```bash
   cd mcps/servers/your-server-name
   touch server.py requirements.txt .env.example
   ```

3. Implement the server using the MCP SDK

4. Test thoroughly

5. Document all tools and configuration

6. Submit via Pull Request

### Server Structure

```
mcps/servers/your-server-name/
├── README.md              # Documentation
├── server.py              # Main server code
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── tests/                # Unit tests
│   └── test_server.py
└── examples/             # Usage examples
    └── example1.md
```

### Minimal Server Example

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio

app = Server("my-server")

@app.list_tools()
async def list_tools():
    return [
        {
            "name": "example_tool",
            "description": "An example tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
                "required": ["text"]
            }
        }
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "example_tool":
        return {"result": f"Processed: {arguments['text']}"}
    raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    asyncio.run(stdio_server(app))
```

## 📋 Server Categories

- **APIs**: REST, GraphQL, SOAP integrations
- **Databases**: SQL, NoSQL, graph databases
- **Files**: Local filesystem, cloud storage
- **External Services**: Payment, messaging, email
- **Internal Tools**: Business logic, calculations
- **AI Services**: Computer vision, NLP, embedding

## 💡 Best Practices

### Design
- Keep tools focused and single-purpose
- Use clear, descriptive tool names
- Provide detailed parameter descriptions
- Return structured data when possible
- Handle errors gracefully

### Security
- Never hardcode credentials
- Use environment variables
- Validate all inputs
- Implement rate limiting
- Log security events
- Follow least privilege principle

### Performance
- Cache responses when appropriate
- Implement timeouts
- Handle rate limits
- Use async operations
- Monitor resource usage

### Error Handling
- Return clear error messages
- Include error codes
- Log errors for debugging
- Provide troubleshooting hints
- Fail gracefully

## 🔍 Testing

### Unit Tests

```python
import pytest
from server import app

@pytest.mark.asyncio
async def test_example_tool():
    result = await app.call_tool(
        "example_tool", 
        {"text": "test"}
    )
    assert result["result"] == "Processed: test"
```

### Integration Tests

Test the complete flow:
1. Server starts correctly
2. Tools are listed properly
3. Tool calls work as expected
4. Errors are handled gracefully
5. Cleanup happens correctly

## 🔧 Debugging

### Enable Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Common Issues

**Server not appearing in Claude**
- Check config file syntax
- Verify absolute paths
- Restart Claude application

**Authentication errors**
- Verify environment variables
- Check .env file location
- Confirm credentials are valid

**Tool calls failing**
- Review parameter validation
- Check API connectivity
- Examine server logs

## 📚 Documentation Requirements

Each server must include:

1. **README.md**
   - Clear purpose and use cases
   - Installation instructions
   - Configuration guide
   - Tool descriptions
   - Example usage

2. **requirements.txt**
   - All Python dependencies
   - Pinned versions recommended

3. **.env.example**
   - All required environment variables
   - Example values (non-sensitive)

4. **Tests**
   - Unit tests for core functionality
   - Integration tests when applicable

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

Checklist:
- [ ] Server follows MCP specification
- [ ] All tools documented
- [ ] Tests included
- [ ] Error handling implemented
- [ ] Security best practices followed
- [ ] Example usage provided

## 📖 Resources

- [MCP Template](TEMPLATE.md)
- [Example Servers](servers/)
- [MCPs Guide](../docs/mcps-guide.md)
- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)

## 🆘 Support

- Check [troubleshooting](#-debugging) section
- Review [MCP docs](https://modelcontextprotocol.io)
- Open an issue for bugs
- Start a discussion for questions

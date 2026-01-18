# MCP Server Template

Use this template to create new Model Context Protocol servers.

## Server Name

[Brief one-line description]

## Overview

[Detailed description of what this MCP server provides]

## Features

- [Feature 1]
- [Feature 2]
- [Feature 3]

## Prerequisites

- Python 3.10 or higher
- [Additional requirements]

## Installation

### From Source

```bash
# Clone the repository
cd mcps/servers/your-server-name

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`
2. Fill in required credentials:
   ```
   API_KEY=your_api_key_here
   API_ENDPOINT=https://api.example.com
   ```

## Usage

### Starting the Server

```bash
python server.py
```

### Configuration in Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your_api_key"
      }
    }
  }
}
```

### Configuration in Claude Code

Add to your MCP settings:

```bash
claude-code mcp add your-server-name python /path/to/server.py
```

## Available Tools

### tool_name_1

**Description**: [What this tool does]

**Parameters**:
- `param1` (string, required): [Description]
- `param2` (integer, optional): [Description]

**Returns**: [Description of return value]

**Example**:
```python
# Example usage
result = await call_tool("tool_name_1", {
    "param1": "example",
    "param2": 42
})
```

### tool_name_2

**Description**: [What this tool does]

**Parameters**:
- `param1` (string, required): [Description]

**Returns**: [Description of return value]

**Example**:
```python
# Example usage
result = await call_tool("tool_name_2", {
    "param1": "example"
})
```

## API Reference

### Server Implementation

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("your-server-name")

@app.list_tools()
async def list_tools():
    """Return list of available tools."""
    return [
        {
            "name": "tool_name_1",
            "description": "Tool description",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param1"]
            }
        }
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls."""
    if name == "tool_name_1":
        # Implementation
        return {"result": "success"}
    raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(stdio_server(app))
```

## Examples

### Example 1: [Use Case]

**Prompt:**
```
[User request to Claude]
```

**Claude's Tool Use:**
```json
{
  "tool": "tool_name_1",
  "parameters": {
    "param1": "example"
  }
}
```

**Result:**
```
[Expected output]
```

### Example 2: [Use Case]

**Prompt:**
```
[User request to Claude]
```

**Claude's Tool Use:**
```json
{
  "tool": "tool_name_2",
  "parameters": {
    "param1": "example"
  }
}
```

**Result:**
```
[Expected output]
```

## Error Handling

### Common Errors

**Error**: `Authentication failed`
- **Cause**: Invalid or missing API key
- **Solution**: Check your `.env` file and ensure API_KEY is set

**Error**: `Connection timeout`
- **Cause**: Unable to reach API endpoint
- **Solution**: Verify network connection and endpoint URL

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Tools

1. Define tool schema in `list_tools()`
2. Implement handler in `call_tool()`
3. Add tests in `tests/`
4. Update documentation

## Security

- Never commit API keys or credentials
- Use environment variables for sensitive data
- Validate all input parameters
- Implement rate limiting
- Log security-relevant events

## Performance

- Expected response time: [X]ms
- Rate limits: [X] requests per minute
- Caching strategy: [Description]

## Troubleshooting

### Issue: Server won't start
- Check Python version (3.10+)
- Verify all dependencies installed
- Review error logs

### Issue: Tools not appearing in Claude
- Restart Claude application
- Verify config file syntax
- Check server logs

## Limitations

- [Known limitation 1]
- [Known limitation 2]
- [Known limitation 3]

## Roadmap

- [ ] [Planned feature 1]
- [ ] [Planned feature 2]
- [ ] [Planned feature 3]

## Contributing

See main [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

## License

MIT License - see repository LICENSE file

## Author

[Your name or GitHub username]

## Version

- **Current**: 1.0.0
- **Created**: [Date]
- **Last Updated**: [Date]

## Compatibility

- **Python**: >= 3.10
- **MCP SDK**: >= 1.0.0
- **Claude Interfaces**:
  - Claude Desktop: ✅
  - Claude Code: ✅
  - API (direct): ❌ (requires MCP client)
- **Operating Systems**: [e.g., Linux, macOS, Windows]

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Example Servers](https://github.com/modelcontextprotocol/servers)

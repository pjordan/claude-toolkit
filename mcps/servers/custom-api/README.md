# Custom API MCP Server

A template for integrating third-party REST APIs with Claude via MCP.

## Overview

This is a template server that demonstrates how to:
- Connect to external REST APIs
- Handle authentication
- Map API responses to Claude-friendly formats
- Implement error handling and rate limiting

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API credentials

# Run server
python server.py
```

## Configuration

Add to your Claude configuration:

```json
{
  "mcpServers": {
    "custom-api": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your_key"
      }
    }
  }
}
```

## Example Usage

Once configured, Claude can use the tools provided by this server:

```
Claude, search for products matching "laptop"
```

## Customization

This is a template - customize it for your specific API by:
1. Updating the API endpoint configuration
2. Modifying tool definitions for your use case
3. Adjusting authentication method
4. Adding API-specific error handling

See [MCP Guide](../../../docs/mcps-guide.md) for detailed instructions.

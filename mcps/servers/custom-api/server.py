"""
Custom API MCP Server Template

A template for integrating third-party REST APIs with Claude via MCP.
Customize this template for your specific API integration needs.
"""

import asyncio
import os

from mcp.server import Server
from mcp.server.stdio import stdio_server

# Initialize the MCP server
app = Server("custom-api")


@app.list_tools()
async def list_tools():
    """Return list of available tools."""
    return [
        {
            "name": "api_request",
            "description": "Make a request to the configured API endpoint",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "The API endpoint path to call"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST", "PUT", "DELETE"],
                        "description": "HTTP method to use"
                    },
                    "params": {
                        "type": "object",
                        "description": "Query parameters or request body"
                    }
                },
                "required": ["endpoint"]
            }
        }
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls."""
    if name == "api_request":
        # TODO: Implement your API integration here
        # Example:
        # api_key = os.environ.get("API_KEY")
        # response = await make_api_call(arguments)
        # return response
        return {
            "status": "not_implemented",
            "message": "This is a template. Implement your API integration."
        }
    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

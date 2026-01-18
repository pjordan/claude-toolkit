# Database Connector MCP Server

A template for connecting Claude to databases (PostgreSQL, MySQL, SQLite, etc.).

## Overview

This template demonstrates how to:
- Connect to databases safely
- Execute queries with proper parameterization
- Return results in structured format
- Implement connection pooling
- Handle database errors gracefully

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure database connection
cp .env.example .env
# Edit .env with your database credentials

# Run server
python server.py
```

## Configuration

Add to your Claude configuration:

```json
{
  "mcpServers": {
    "database": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "mydb",
        "DB_USER": "user",
        "DB_PASSWORD": "password"
      }
    }
  }
}
```

## Example Usage

```
Claude, query the users table for accounts created in the last week
```

Claude will use the database connector to execute queries and return results.

## Security Notes

- Never commit database credentials
- Use read-only database users when possible
- Implement query allowlists for production
- Validate and sanitize all inputs
- Use parameterized queries always

## Customization

Adapt this template for your database:
1. Update connection string format
2. Add database-specific optimizations
3. Implement custom query helpers
4. Add schema introspection tools

See [MCP Guide](../../../docs/mcps-guide.md) for detailed instructions.

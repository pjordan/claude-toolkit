# Examples Index

A quick reference to all available skills, subagents, and MCP servers in the Claude Toolkit.

## Skills

Domain-specific knowledge packages that enhance Claude's expertise.

| Name | Description | Use Cases |
|------|-------------|-----------|
| [Code Review](skills/examples/code-review/) | Comprehensive code review covering quality, security, and performance | PR reviews, security audits, code quality |
| [Data Analysis](skills/examples/data-analysis/) | Statistical analysis and data exploration workflows | EDA, pattern identification, reporting |
| [A2A Agent](skills/examples/a2a-agent/) | Build production-ready Agent-to-Agent systems with FastAPI | Agent development, streaming, deployment |

## Subagents

Pre-configured Claude instances optimized for specific tasks.

| Name | Description | Temperature | Best For |
|------|-------------|-------------|----------|
| [Research Assistant](subagents/examples/research-assistant/) | Academic research, literature review, citation management | 0.5 | Graduate students, researchers |
| [Code Generator](subagents/examples/code-generator/) | Boilerplate code, project scaffolding, code templates | 0.3 | Starting projects, common patterns |

## MCP Servers

Model Context Protocol servers for extending Claude's tool access.

| Name | Description | Status |
|------|-------------|--------|
| [Custom API](mcps/servers/custom-api/) | Template for REST API integrations | Template |
| [Database Connector](mcps/servers/database-connector/) | Template for database query interfaces | Template |

## By Category

### Development

- [Code Review](skills/examples/code-review/) - Review code for quality and security
- [Code Generator](subagents/examples/code-generator/) - Generate boilerplate and scaffolds
- [A2A Agent](skills/examples/a2a-agent/) - Build agent systems

### Research & Analysis

- [Research Assistant](subagents/examples/research-assistant/) - Literature review and synthesis
- [Data Analysis](skills/examples/data-analysis/) - Statistical analysis workflows

### Integration Templates

- [Custom API](mcps/servers/custom-api/) - Connect to REST APIs
- [Database Connector](mcps/servers/database-connector/) - Query databases

## Quick Start

### Using a Skill

```
Please use the code-review skill to review this code:
[paste code]
```

### Using a Subagent

1. Create a Project in Claude.ai
2. Copy the system prompt from the subagent's README
3. Add as custom instructions

### Using an MCP Server

1. Copy the server directory
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment: `cp .env.example .env`
4. Add to Claude configuration

## Contributing

Want to add an example? See:

- [Skills Template](skills/TEMPLATE.md)
- [Subagents Template](subagents/TEMPLATE.md)
- [MCPs Template](mcps/TEMPLATE.md)
- [Contributing Guide](CONTRIBUTING.md)

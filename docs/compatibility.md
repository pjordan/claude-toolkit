# Compatibility Guide

This guide explains version and compatibility information for Claude Toolkit resources.

## Claude Models

### Model Tiers

| Tier | Models | Best For |
|------|--------|----------|
| Opus | claude-opus-4-20250514, claude-3-opus-20240229 | Complex reasoning, nuanced tasks |
| Sonnet | claude-sonnet-4-20250514, claude-3-5-sonnet-20241022 | Balanced performance (recommended) |
| Haiku | claude-3-5-haiku-20241022, claude-3-haiku-20240307 | Fast, simple tasks |

### Model Selection

- **Skills**: Generally work with all Claude 3+ models. More complex skills benefit from Sonnet or Opus.
- **Subagents**: Specify recommended model in configuration. Temperature settings may need adjustment per model.
- **MCP Servers**: Model-agnostic; work with any Claude interface that supports MCP.

## Interfaces

### Claude.ai

| Feature | Skills | Subagents | MCPs |
|---------|--------|-----------|------|
| Direct chat | ✅ Paste content | ✅ Paste system prompt | ❌ |
| Projects | ✅ Add as knowledge | ✅ Custom instructions | ❌ |
| Artifacts | ✅ | ✅ | ❌ |

### Claude API

| Feature | Skills | Subagents | MCPs |
|---------|--------|-----------|------|
| Messages API | ✅ Include in messages | ✅ Use system parameter | ❌ |
| Streaming | ✅ | ✅ | ❌ |
| Tool use | ✅ | ✅ | ❌ |

### Claude Code

| Feature | Skills | Subagents | MCPs |
|---------|--------|-----------|------|
| System prompts | ✅ | ✅ | ✅ |
| MCP integration | N/A | N/A | ✅ |
| Custom commands | ✅ | ✅ | ✅ |

### Claude Desktop

| Feature | Skills | Subagents | MCPs |
|---------|--------|-----------|------|
| Projects | ✅ | ✅ | ✅ |
| MCP servers | N/A | N/A | ✅ |

## API Versions

The Anthropic API uses date-based versioning. Resources in this toolkit are tested against:

- **Current**: `2024-01-01` and later
- **Minimum**: `2023-06-01`

### Version Headers

When using the API, specify the version:

```python
import anthropic

client = anthropic.Anthropic()
# SDK handles versioning automatically

# Or explicitly:
client = anthropic.Anthropic(
    default_headers={"anthropic-version": "2024-01-01"}
)
```

## Python Requirements

For MCP servers:

| Dependency | Minimum Version | Recommended |
|------------|-----------------|-------------|
| Python | 3.10 | 3.11+ |
| mcp | 1.0.0 | Latest |
| asyncio | stdlib | stdlib |

## MCP Protocol

MCP servers follow the [Model Context Protocol](https://modelcontextprotocol.io) specification.

### Supported Features

- Tool definitions and calls
- Resource access
- Prompts
- Sampling (where supported)

### Client Compatibility

| Client | Status |
|--------|--------|
| Claude Desktop | ✅ Full support |
| Claude Code | ✅ Full support |
| Custom clients | ✅ Via MCP SDK |

## Specifying Compatibility

When contributing resources, include compatibility information:

### Skills

```markdown
## Compatibility

- **Claude Models**: All Claude 3+ models, Claude Sonnet 4 recommended
- **Interfaces**: Claude.ai, API, Claude Code
- **Minimum API Version**: 2024-01-01
```

### Subagents

```markdown
## Compatibility

- **Tested Models**: claude-sonnet-4-20250514
- **Minimum Model**: Claude 3 Sonnet
- **API Version**: 2024-01-01
- **Interfaces**: Claude.ai Projects, API, Claude Code
```

### MCP Servers

```markdown
## Compatibility

- **Python**: >= 3.10
- **MCP SDK**: >= 1.0.0
- **Claude Interfaces**: Claude Desktop, Claude Code
- **Operating Systems**: Linux, macOS, Windows
```

## Troubleshooting

### "Model not found"

Ensure you're using a valid model ID. Model IDs include dates (e.g., `claude-sonnet-4-20250514`).

### "API version not supported"

Update your API version header or SDK to the latest version.

### "MCP server not connecting"

1. Verify Python version: `python --version`
2. Check MCP SDK: `pip show mcp`
3. Review server logs for errors

### "Skill not working as expected"

- Try a more capable model (Sonnet or Opus)
- Ensure the full skill content is included
- Check for truncation in long conversations

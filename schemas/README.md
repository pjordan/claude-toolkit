# JSON Schemas

This directory contains JSON Schema definitions for validating Claude Toolkit configurations.

## Available Schemas

### `subagent.schema.json`

Validates subagent configuration objects.

**Usage in VS Code:**

Add to your JSON file:
```json
{
  "$schema": "../../../schemas/subagent.schema.json",
  "name": "My Subagent",
  "model": "claude-sonnet-4-20250514",
  "system": "You are..."
}
```

**Required fields:**
- `name` - Human-readable name
- `model` - Claude model identifier
- `system` - System prompt

**Optional fields:**
- `max_tokens` - Response length limit (default: 4096)
- `temperature` - Creativity (0.0-1.0, default: 1.0)
- `top_p`, `top_k` - Sampling parameters
- `stop_sequences` - Generation stop sequences
- `metadata` - Version, author, tags, description

### `mcp-server.schema.json`

Validates MCP server manifest files.

**Usage:**
```json
{
  "$schema": "../../../schemas/mcp-server.schema.json",
  "name": "my-server",
  "version": "1.0.0",
  "description": "My MCP server"
}
```

**Required fields:**
- `name` - Server identifier (lowercase, hyphens)
- `version` - Semantic version
- `description` - Brief description

**Optional fields:**
- `author`, `license`, `repository`
- `python` - Python configuration (requires, entrypoint)
- `tools` - List of provided tools
- `environment` - Required environment variables
- `tags` - Categorization tags

## IDE Integration

### VS Code

Schemas provide autocomplete and validation automatically when referenced via `$schema`.

For workspace-wide validation, add to `.vscode/settings.json`:
```json
{
  "json.schemas": [
    {
      "fileMatch": ["subagents/**/config.json"],
      "url": "./schemas/subagent.schema.json"
    },
    {
      "fileMatch": ["mcps/**/manifest.json"],
      "url": "./schemas/mcp-server.schema.json"
    }
  ]
}
```

### JetBrains IDEs

Add schema mappings in Preferences > Languages & Frameworks > Schemas and DTDs > JSON Schema Mappings.

## Programmatic Validation

### Python

```python
import json
import jsonschema

with open("schemas/subagent.schema.json") as f:
    schema = json.load(f)

with open("subagents/examples/research-assistant/config.json") as f:
    config = json.load(f)

jsonschema.validate(config, schema)
```

### Node.js

```javascript
const Ajv = require("ajv");
const ajv = new Ajv();

const schema = require("./schemas/subagent.schema.json");
const validate = ajv.compile(schema);

const config = require("./subagents/examples/research-assistant/config.json");
if (!validate(config)) {
  console.error(validate.errors);
}
```

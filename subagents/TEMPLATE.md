# Subagent Template

Use this template to create new subagent configurations.

## Subagent Name

[Brief one-line description]

## Overview

[Detailed description of this subagent's purpose and capabilities]

## Configuration

### System Prompt

```
[The system prompt that defines this subagent's role and behavior]
```

### Model Recommendation

- **Recommended Model**: [e.g., Claude Sonnet 4]
- **Reasoning**: [Why this model is recommended]

### Parameters

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096,
  "temperature": 0.7,
  "system": "[System prompt here]"
}
```

## Use Cases

### Primary Use Cases
- [Use case 1]
- [Use case 2]
- [Use case 3]

### Examples

#### Example 1: [Scenario Name]

**User Input:**
```
[Example user message]
```

**Expected Behavior:**
```
[How the subagent should respond]
```

#### Example 2: [Scenario Name]

**User Input:**
```
[Example user message]
```

**Expected Behavior:**
```
[How the subagent should respond]
```

## Capabilities

### Strengths
- [Strength 1]
- [Strength 2]
- [Strength 3]

### Limitations
- [Limitation 1]
- [Limitation 2]
- [Limitation 3]

## Setup Instructions

### Via API

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system="[System prompt]",
    messages=[
        {"role": "user", "content": "Your message here"}
    ]
)

print(message.content)
```

### Via Claude.ai

1. Start a new conversation
2. In your first message, include: "Please act as [subagent role] with these capabilities: [brief description]"
3. Proceed with your task

### Via Projects (Recommended)

1. Create a new Project in Claude.ai
2. Set the custom instructions to the system prompt above
3. Add relevant knowledge files if needed
4. Use the project for all related tasks

## Customization

### Adjustable Parameters

- **Temperature**: [Recommendations for different use cases]
- **Max Tokens**: [When to adjust]
- **Additional Context**: [What to include]

### Extending the Subagent

[How to add capabilities or modify behavior]

## Performance Tips

- [Tip 1]
- [Tip 2]
- [Tip 3]

## Troubleshooting

### Common Issues

**Issue 1**: [Description]
- **Cause**: [Why this happens]
- **Solution**: [How to fix]

**Issue 2**: [Description]
- **Cause**: [Why this happens]
- **Solution**: [How to fix]

## Related Resources

- [Related skill 1]
- [Related subagent 1]
- [External documentation]

## Version History

- **v1.0.0** ([Date]): Initial release
  - [Key features]

## Author

[Your name or GitHub username]

## License

MIT License - see repository LICENSE file

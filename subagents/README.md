# Claude Subagents

Subagents are pre-configured Claude instances optimized for specific tasks and domains.

## 📖 What are Subagents?

Subagents are specialized configurations of Claude that:
- Have domain-specific system prompts
- Are optimized for particular workflows
- Include recommended parameters and settings
- Can be deployed via API, Projects, or Claude.ai

## 🎯 Available Subagents

### Research Assistant
**Path**: `examples/research-assistant/`
**Purpose**: Academic research, literature review, citation management
**Best For**: Students, researchers, academics

### Code Generator
**Path**: `examples/code-generator/`
**Purpose**: Boilerplate code creation, scaffolding, templates
**Best For**: Developers starting new projects or features

### A2A Agent Developer
**Path**: `examples/a2a-agent-developer/`
**Purpose**: Building A2A agents with a2a-sdk and FastAPI
**Best For**: Developers building agent-to-agent systems

### UCP Commerce Developer
**Path**: `examples/ucp-commerce-developer/`
**Purpose**: Integrating with UCP merchants for agentic commerce
**Best For**: Developers building shopping agents and payment flows

### Agent Testing Specialist
**Path**: `examples/agent-testing-specialist/`
**Purpose**: Testing A2A and UCP agents with pytest
**Best For**: QA engineers and developers writing comprehensive tests

## 🔧 Using a Subagent

### Via Claude.ai Projects (Recommended)

1. Create a new Project
2. Copy the system prompt from the subagent's README
3. Paste it into the Project's custom instructions
4. Add any recommended knowledge files
5. Start using the project

### Via API

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Load subagent configuration
with open("config.json", "r") as f:
    config = json.load(f)

message = client.messages.create(
    model=config["model"],
    max_tokens=config["max_tokens"],
    system=config["system"],
    messages=[
        {"role": "user", "content": "Your task"}
    ]
)
```

### Via Claude.ai Chat

1. Read the subagent's system prompt
2. Start your conversation with: "Please act as [role] with the following capabilities..."
3. Include key aspects of the system prompt
4. Proceed with your task

## ✨ Creating a New Subagent

1. Copy `TEMPLATE.md` to `examples/your-subagent-name/`
2. Create a `README.md` with overview and setup
3. Define the system prompt and parameters
4. Include example interactions
5. Test thoroughly with various use cases
6. Document limitations and best practices
7. Submit via Pull Request

### Subagent Structure

```
subagents/examples/your-subagent-name/
├── README.md         # Overview and usage
├── config.json       # Model parameters
└── examples/         # Example conversations
    ├── example1.md
    └── example2.md
```

### config.json Format

```json
{
  "name": "Your Subagent Name",
  "description": "Brief description",
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096,
  "temperature": 0.7,
  "system": "Your detailed system prompt here..."
}
```

## 📋 Subagent Categories

- **Development**: Code generation, review, debugging
- **Agent Development**: A2A agents, UCP commerce, agent testing
- **Research**: Literature review, analysis, synthesis
- **Writing**: Content creation, editing, style
- **Analysis**: Data analysis, insights, reporting
- **Learning**: Tutoring, explanation, practice
- **Operations**: DevOps, monitoring, incident response

## 💡 Best Practices

### Designing Subagents
- Define clear scope and boundaries
- Include specific examples in system prompt
- Set appropriate temperature (0.0 for deterministic, 0.7+ for creative)
- Specify output format when relevant
- Document edge cases

### System Prompts
- Be specific about the role
- Include key capabilities
- Specify response format if needed
- Add relevant constraints
- Include example interactions

### Testing
- Test with various input types
- Verify behavior at boundaries
- Check error handling
- Validate output quality
- Document any quirks

## 🔍 Choosing a Subagent

Consider:
- **Task Type**: What are you trying to accomplish?
- **Domain**: What specialized knowledge is needed?
- **Output Format**: What format do you need?
- **Interaction Style**: One-shot vs. conversational?

## ⚙️ Customization

All subagents can be customized:
- Adjust temperature for creativity vs. consistency
- Modify system prompt for specific needs
- Add domain-specific context
- Include example formats
- Set constraints or guidelines

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

Quick checklist:
- [ ] Clear, focused purpose
- [ ] Well-tested system prompt
- [ ] Example interactions
- [ ] Documented limitations
- [ ] Recommended parameters

## 📚 Resources

- [Subagents Template](TEMPLATE.md)
- [Example Subagents](examples/)
- [Subagents Guide](../docs/subagents-guide.md)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)

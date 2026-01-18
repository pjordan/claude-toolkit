# Code Review Skill

A comprehensive code review skill for Claude that covers quality, security, performance, and best practices.

## Quick Start

Provide Claude with the SKILL.md content and ask it to review your code:

```
Please review this code using the code-review skill from claude-toolkit:

[paste your code here]
```

## What It Covers

- ✅ Functional correctness
- 🔒 Security vulnerabilities
- ⚡ Performance issues
- 📚 Code quality and maintainability
- 🧪 Testing considerations
- 📖 Documentation quality

## Best For

- Pull request reviews
- Learning code review practices
- Pre-commit checks
- Security audits
- Code quality improvements

## Usage Example

**Input:**
```python
def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
```

**Output:**
Claude will provide structured feedback on functionality, potential issues, and improvements.

## See Also

- [SKILL.md](SKILL.md) - Complete skill documentation
- [Skills Template](../../TEMPLATE.md)

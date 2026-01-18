# Contributing to Claude Toolkit

Thank you for your interest in contributing! This guide will help you get started.

## 🎯 Ways to Contribute

- **Skills**: Share specialized knowledge and workflows
- **Subagents**: Contribute pre-configured Claude assistants
- **MCP Servers**: Build tool integrations
- **Documentation**: Improve guides and examples
- **Bug Reports**: Help us identify issues
- **Feature Requests**: Suggest improvements

## 📝 Contribution Guidelines

### Code Style

#### Python

- Follow PEP 8 style guidelines
- Use type hints where applicable
- Include docstrings for functions and classes
- Maximum line length: 100 characters

```python
def example_function(param: str) -> dict:
    """
    Brief description of function.

    Args:
        param: Description of parameter

    Returns:
        Description of return value
    """
    return {"result": param}
```

#### Markdown

- Use clear, descriptive headers
- Include code examples where relevant
- Keep line length reasonable (80-100 chars when practical)
- Use proper formatting for code blocks with language specification

### File Organization

- Place skills in `skills/examples/<skill-name>/`
- Place subagents in `subagents/examples/<subagent-name>/`
- Place MCP servers in `mcps/servers/<server-name>/`
- Each contribution should include a README.md

### Documentation Requirements

All contributions must include:

1. **Clear README**: Purpose, usage, and examples
2. **Dependencies**: List all requirements
3. **Installation**: Step-by-step setup instructions
4. **Examples**: At least one working example
5. **Limitations**: Known issues or constraints

## 🔍 Pull Request Process

1. **Fork and Clone**

   ```bash
   git clone https://github.com/YOUR_USERNAME/claude-toolkit.git
   cd claude-toolkit
   ```

2. **Create Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow the appropriate template
   - Test your contribution thoroughly
   - Update documentation

4. **Run Tests**

   ```bash
   python tests/validate_skills.py
   python tests/validate_mcps.py
   ```

5. **Commit Changes**

   Or run all checks via pre-commit:
   ```bash
   pre-commit run --all-files
   ```

6. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

   Commit message format:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for improvements
   - `Docs:` for documentation

7. **Push and PR**
   ```bash
   git push origin feature/your-feature-name
   ```

   Then open a Pull Request on GitHub

### PR Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is complete
- [ ] Examples are included
- [ ] README is clear and detailed
- [ ] No sensitive data (API keys, passwords)

## 🧪 Testing

### Skills

- Verify SKILL.md follows the template
- Test with Claude to ensure it works as documented

### MCP Servers

- Include unit tests where applicable
- Test connection and core functionality
- Document API requirements

### Subagents

- Validate configuration format
- Test key use cases
- Document expected behavior

## 🚫 What Not to Include

- API keys, tokens, or credentials
- Copyrighted content without permission
- Malicious code or exploits
- Large binary files (>1MB)
- Personal or sensitive information

## 💡 Best Practices

### Skills

- Focus on a specific domain or task
- Include concrete examples
- Explain the reasoning behind approaches
- Link to relevant documentation

### MCP Servers

- Follow MCP specification
- Handle errors gracefully
- Include comprehensive logging
- Provide clear setup instructions

### Subagents

- Define clear use cases
- Document configuration options
- Include prompt examples
- Specify expected inputs/outputs

## ❓ Questions?

- Open an [issue](https://github.com/pjordan/claude-toolkit/issues) for bugs
- Start a [discussion](https://github.com/pjordan/claude-toolkit/discussions) for questions
- Check existing issues before creating new ones

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the contribution, not the contributor
- Help create a welcoming environment

## 🎉 Recognition

Contributors will be:

- Listed in repository acknowledgments
- Credited in release notes
- Mentioned in related documentation

Thank you for helping make Claude more capable!

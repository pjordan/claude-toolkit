# Claude Toolkit

[![Validate Repository](https://github.com/pjordan/claude-toolkit/actions/workflows/validate.yml/badge.svg)](https://github.com/pjordan/claude-toolkit/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A collection of Claude skills, subagents, and MCP servers for extending Claude's capabilities.

## 📋 Overview

This repository contains resources to enhance and extend Claude's functionality:

- **Skills**: Specialized knowledge and workflows for specific tasks
- **Subagents**: Configured Claude instances for particular domains
- **MCP Servers**: Model Context Protocol servers for tool integration

## 🚀 Quick Start

### Skills
Browse the [skills/](skills/) directory for domain-specific expertise. Each skill includes a `SKILL.md` file with instructions and best practices.

### Subagents
Check out [subagents/](subagents/) for pre-configured Claude assistants optimized for specific tasks.

### MCP Servers
Explore [mcps/servers/](mcps/servers/) for custom tool integrations. Each server includes setup instructions and example usage.

## 📚 Documentation

- [Skills Guide](docs/skills-guide.md) - Creating and using skills
- [Subagents Guide](docs/subagents-guide.md) - Configuring subagents
- [MCPs Guide](docs/mcps-guide.md) - Building MCP servers

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-skill`)
3. Follow the appropriate template in [skills/TEMPLATE.md](skills/TEMPLATE.md), [subagents/TEMPLATE.md](subagents/TEMPLATE.md), or [mcps/TEMPLATE.md](mcps/TEMPLATE.md)
4. Commit your changes (`git commit -m 'Add amazing skill'`)
5. Push to the branch (`git push origin feature/amazing-skill`)
6. Open a Pull Request

## 📖 Examples

### Skills
- [Code Review](skills/examples/code-review/) - Automated code review assistant
- [Data Analysis](skills/examples/data-analysis/) - Statistical analysis workflows

### Subagents
- [Research Assistant](subagents/examples/research-assistant/) - Academic research helper
- [Code Generator](subagents/examples/code-generator/) - Boilerplate code creation

### MCP Servers
- [Custom API](mcps/servers/custom-api/) - Template for API integrations
- [Database Connector](mcps/servers/database-connector/) - Database query interface

## 🧪 Testing

Run validation tests before submitting:

```bash
python tests/validate_skills.py
python tests/validate_mcps.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built for the Claude community to share and extend Claude's capabilities.

## 📞 Support

- Open an [issue](https://github.com/pjordan/claude-toolkit/issues) for bug reports
- Start a [discussion](https://github.com/pjordan/claude-toolkit/discussions) for questions
- Check the [wiki](https://github.com/pjordan/claude-toolkit/wiki) for detailed guides

## 🔗 Resources

- [Anthropic Documentation](https://docs.anthropic.com)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Claude API Reference](https://docs.anthropic.com/en/api)

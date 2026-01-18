# Claude Skills

Skills are specialized knowledge packages that enhance Claude's capabilities in specific domains.

## 📖 What are Skills?

Skills provide Claude with:
- Domain-specific knowledge and best practices
- Step-by-step workflows for complex tasks
- Examples and templates
- Common pitfalls and how to avoid them

## 🎯 Available Skills

### Code Review
**Path**: `examples/code-review/`  
**Purpose**: Automated code review with best practices and style checking  
**Use When**: Reviewing code for quality, security, and maintainability

### Data Analysis
**Path**: `examples/data-analysis/`  
**Purpose**: Statistical analysis and data exploration workflows  
**Use When**: Analyzing datasets, creating visualizations, finding insights

## 🔧 Using a Skill

1. Browse available skills in the `examples/` directory
2. Read the `SKILL.md` file for the skill you need
3. Provide the skill content to Claude when starting a conversation
4. Reference the skill in your prompts

Example:
```
I need help with [task]. Please use the [skill-name] skill approach 
from the claude-toolkit repository.
```

## ✨ Creating a New Skill

1. Copy `TEMPLATE.md` to a new directory: `examples/your-skill-name/`
2. Rename it to `SKILL.md`
3. Fill in all sections with detailed information
4. Include at least 2 concrete examples
5. Test with Claude to ensure it works
6. Submit via Pull Request

### Skill Structure

```
skills/examples/your-skill-name/
├── SKILL.md          # Main skill content (required)
├── README.md         # Overview and usage (required)
└── examples/         # Additional examples (optional)
```

## 📋 Skill Categories

- **Development**: Code generation, review, debugging
- **Analysis**: Data analysis, research, reporting
- **Content**: Writing, editing, documentation
- **Operations**: DevOps, automation, monitoring
- **Learning**: Tutoring, explanation, curriculum design

## 💡 Best Practices

### Writing Skills
- Be specific and actionable
- Include concrete examples
- Explain the "why" behind approaches
- Note edge cases and limitations
- Keep language clear and concise

### Organizing Skills
- One skill per directory
- Clear, descriptive naming
- Complete documentation
- Working examples
- Version tracking

## 🔍 Finding Skills

Browse by:
- **Category**: Check directory structure
- **Use Case**: Read skill descriptions
- **Keywords**: Search README files

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

Quick start:
1. Use the template
2. Test thoroughly
3. Document completely
4. Submit PR

## 📚 Resources

- [Skills Template](TEMPLATE.md)
- [Example Skills](examples/)
- [Skills Guide](../docs/skills-guide.md)
- [Anthropic Docs](https://docs.anthropic.com)

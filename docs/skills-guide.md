# Skills Guide

A comprehensive guide to creating, using, and contributing Claude skills.

## Table of Contents

- [What are Skills?](#what-are-skills)
- [Using Skills](#using-skills)
- [Creating Skills](#creating-skills)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [FAQ](#faq)

## What are Skills?

Skills are structured knowledge packages that give Claude specialized expertise in specific domains. Think of them as instruction manuals that guide Claude's approach to particular types of tasks.

### Key Components

1. **Domain Knowledge**: Specific facts, concepts, and terminology
2. **Methodology**: Step-by-step approaches to tasks
3. **Best Practices**: Proven techniques and patterns
4. **Examples**: Concrete demonstrations
5. **Pitfalls**: Common mistakes to avoid

### Skills vs. Prompts

| Aspect      | Skills                          | Prompts                   |
|-------------|--------------------------------|---------------------------|
| Scope       | Comprehensive domain coverage  | Single task instruction   |
| Reusability | High - works across many scenarios | Low - task-specific   |
| Structure   | Organized methodology          | Free-form request         |
| Learning    | Teaches approach               | Requests action           |

## Using Skills

### Method 1: Direct Inclusion

Copy the skill content into your conversation:

```text
I need help with [task]. Please use the following skill:

[paste SKILL.md content]

Now, [specific request]
```

### Method 2: Reference

If Claude has access to the file:

```text
Please use the code-review skill from
/path/to/claude-toolkit/skills/examples/code-review/SKILL.md
to review this code: [code]
```

### Method 3: Projects (Recommended)

1. Create a Claude Project
2. Upload the SKILL.md as project knowledge
3. Reference the skill in your instructions
4. All conversations in that project can use the skill

### When to Use Multiple Skills

Skills can be combined for complex tasks:

```text
Use the data-analysis skill to analyze this dataset,
then use the data-visualization skill to recommend charts,
and finally use the technical-writing skill to create a report.
```

## Creating Skills

### Planning Your Skill

Ask yourself:

1. **What problem does this solve?**
   - Be specific about the use case
   - Identify the target audience

2. **What knowledge is needed?**
   - Domain-specific facts
   - Relevant terminology
   - Key concepts

3. **What's the methodology?**
   - Step-by-step process
   - Decision points
   - Alternative approaches

4. **What are common pitfalls?**
   - Mistakes beginners make
   - Edge cases to consider
   - Limitations to acknowledge

### Structure

Use the provided template:

```text
skills/examples/your-skill-name/
├── SKILL.md          # Main skill content
└── README.md         # Overview and quick start
```

### Writing Process

1. **Start with Overview**
   - One-sentence description
   - Detailed explanation
   - When to use this skill

2. **Define Prerequisites**
   - Required knowledge
   - Necessary tools
   - Dependencies

3. **Detail the Approach**
   - Break into clear steps
   - Explain the reasoning
   - Provide context

4. **Add Examples**
   - At least 2 concrete examples
   - Show input and output
   - Explain the process

5. **Document Limitations**
   - What the skill can't do
   - Known edge cases
   - When to seek alternatives

### Testing Your Skill

1. **Test with Claude**

   ```text
   Please use this skill to [task]:
   [paste skill content]
   ```

2. **Try Different Scenarios**
   - Simple cases
   - Complex cases
   - Edge cases

3. **Get Feedback**
   - Share with colleagues
   - Ask for improvements
   - Iterate based on usage

## Best Practices

### Writing Style

**Do:**

- Use clear, active language
- Be specific and concrete
- Include reasoning, not just steps
- Provide context for decisions
- Use examples liberally

**Don't:**

- Use vague language
- Assume prior knowledge
- Skip over important details
- Forget edge cases
- Overcomplicate simple concepts

### Organization

**Effective Structure:**

```text
1. Overview (what & why)
2. Prerequisites (what's needed)
3. Core Concepts (key knowledge)
4. Step-by-Step Process (how)
5. Examples (demonstrations)
6. Best Practices (tips)
7. Common Pitfalls (warnings)
8. Limitations (boundaries)
```

### Examples

**Good Example:**

```text
### Example 1: Simple Login Form Validation

**Input:**
```

```html
<form>
  <input type="text" name="username" />
  <input type="password" name="password" />
</form>
```

```text
**Review Focus:**
```

- Input validation
- Security considerations
- Accessibility

**Expected Findings:**

1. Missing CSRF protection
2. No input validation
3. Missing labels for accessibility

**Bad Example:**

```text
Example: Review this form for issues.
```

### Documentation

Include:

- Purpose and scope
- Target audience
- Prerequisites
- Usage instructions
- Examples
- Limitations
- Version history
- Author information

## Examples

### Example Skill: API Design Review

```markdown
# API Design Review Skill

## Overview
Reviews REST API designs for usability, consistency, and best practices.

## When to Use
- Designing new APIs
- Reviewing API specifications
- Improving existing APIs

## Approach

1. **Consistency Check**
   - Naming conventions
   - URL patterns
   - Response formats

2. **RESTful Principles**
   - Proper HTTP methods
   - Resource-based URLs
   - Status codes

3. **Usability**
   - Clear documentation
   - Error messages
   - Pagination

4. **Security**
   - Authentication
   - Authorization
   - Data validation

## Example

**API Endpoint:**
GET /api/getUsers?id=123

**Issues:**
- Non-RESTful URL (verb in path)
- Should be: GET /api/users/123
- Missing version in URL
- No pagination info

**Improved:**
GET /api/v1/users/123
```

### Example Skill: SQL Query Optimization

Focus on:

- Query structure analysis
- Index recommendations
- Join optimization
- Common anti-patterns

Include examples of slow queries and optimized versions.

## FAQ

### How long should a skill be?

Long enough to be comprehensive, short enough to be useful. Typically:

- Simple skills: 300-500 lines
- Moderate skills: 500-1000 lines
- Complex skills: 1000-2000 lines

### Can skills reference other skills?

Yes! Include a "Related Skills" section to reference complementary skills.

### How specific should skills be?

Balance specificity with reusability:

- ✅ "Python Code Review" (good specificity)
- ❌ "Review Flask App Login Function" (too specific)
- ❌ "Code Review" (too broad)

### Should I include code in skills?

Yes, when it helps demonstrate concepts. But focus on:

- Illustrative examples
- Common patterns
- Before/after comparisons

Avoid:

- Complete implementations
- Library-specific code (unless that's the skill's focus)
- Code without explanation

### How do I update a skill?

1. Make your changes
2. Update the version number
3. Add to version history
4. Submit a pull request
5. Explain what changed and why

### Can one skill depend on another?

Yes, but document dependencies clearly:

```markdown
## Prerequisites
- Understanding of the **Data Cleaning** skill
- Basic knowledge from **Statistical Testing** skill
```

### What if my skill becomes outdated?

Mark it as deprecated with:

```markdown
> ⚠️ **DEPRECATED**: This skill is outdated.
> Use [new-skill-name] instead.
```

Then create or reference the updated version.

## Contributing

Ready to create a skill?

1. Read [CONTRIBUTING.md](../CONTRIBUTING.md)
2. Copy [TEMPLATE.md](../skills/TEMPLATE.md)
3. Write your skill
4. Test thoroughly
5. Submit a PR

## Resources

- [Skills Template](../skills/TEMPLATE.md)
- [Example Skills](../skills/examples/)
- [Anthropic Docs](https://docs.anthropic.com)
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)

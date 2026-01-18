# Subagents Guide

A guide to creating and using specialized Claude configurations.

## Overview

Subagents are Claude instances configured with specific system prompts, parameters, and behavior patterns for particular domains or tasks.

## Core Concepts

### What Makes a Good Subagent?

1. **Clear Purpose**: Solves a specific problem or serves a defined role
2. **Optimized Prompt**: System prompt tailored to the task
3. **Appropriate Parameters**: Temperature, max_tokens tuned for use case
4. **Consistent Behavior**: Predictable responses for similar inputs

### System Prompt Design

The system prompt is the heart of a subagent. It should include:

```
You are a [role] that helps with [purpose].

Your capabilities include:
- [capability 1]
- [capability 2]
- [capability 3]

When responding:
- [guideline 1]
- [guideline 2]
- [guideline 3]

Output format:
[specification of expected format]
```

### Parameter Selection

| Parameter | Low (0.0-0.3) | Medium (0.4-0.7) | High (0.8-1.0) |
|-----------|---------------|------------------|----------------|
| Temperature | Deterministic tasks, code, math | General conversation, analysis | Creative writing, brainstorming |
| Use Cases | SQL queries, data extraction | Problem solving, tutoring | Story writing, art concepts |

## Creating a Subagent

### Step 1: Define the Use Case

Ask:
- What specific problem does this solve?
- Who is the target user?
- What are the inputs and outputs?
- What makes this different from general Claude?

Example:
```
Use Case: Database Query Assistant
Target: Developers needing SQL help
Input: Natural language database questions
Output: Optimized SQL queries with explanations
Differentiation: Specialized in query optimization and indexing
```

### Step 2: Craft the System Prompt

Start broad, then refine:

**Initial Draft:**
```
You are a database expert who helps write SQL queries.
```

**Refined:**
```
You are a database optimization specialist with expertise in PostgreSQL, 
MySQL, and SQL Server. You help developers write efficient, secure SQL 
queries by:

1. Translating natural language requirements into SQL
2. Optimizing queries for performance
3. Explaining indexing strategies
4. Identifying potential N+1 query problems
5. Suggesting query refactoring

Always provide:
- The SQL query
- Explanation of key parts
- Performance considerations
- Indexing recommendations when relevant

Use standard SQL syntax unless asked for database-specific features.
```

### Step 3: Set Parameters

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096,
  "temperature": 0.3,
  "system": "[your refined system prompt]"
}
```

**Reasoning:**
- Sonnet 4 for technical accuracy
- 4096 tokens for code + explanation
- Low temperature (0.3) for consistent, accurate SQL

### Step 4: Test and Iterate

Test with:
1. Simple cases (validate basic functionality)
2. Edge cases (test boundaries)
3. Real-world scenarios (verify practical utility)

Example test:
```
Prompt: "Get all users who signed up in the last 30 days"

Expected: SQL query + explanation + index recommendation
Actual: [test the output]
Iterate: [adjust system prompt based on results]
```

## Using Subagents

### Via Claude.ai Projects

**Best for:** Regular use, team collaboration

1. Create a new Project
2. Add system prompt to custom instructions
3. Upload any reference materials
4. Use for all related tasks

### Via API

**Best for:** Automation, integration, programmatic access

```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

def query_subagent(user_message):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        temperature=0.3,
        system="[your system prompt]",
        messages=[{"role": "user", "content": user_message}]
    )
    return response.content[0].text
```

### Via Claude.ai Chat

**Best for:** One-off tasks, experimentation

Include the essence of your system prompt in your first message:

```
Act as a [role] that [purpose]. For this conversation, 
please [key behaviors]. 

Now, [specific task]
```

## Best Practices

### System Prompt Writing

**Do:**
- Be specific about the role and capabilities
- Include output format specifications
- Provide examples of expected behavior
- Set clear boundaries (what to do and not do)
- Use consistent structure

**Don't:**
- Be vague about the purpose
- Assume Claude knows your specific domain
- Skip output format instructions
- Forget to test with real inputs
- Overcomplicate with unnecessary details

### Parameter Tuning

**Temperature Guidelines:**

```python
# Deterministic (0.0-0.3)
tasks = ["SQL generation", "data extraction", "format conversion"]

# Balanced (0.4-0.7)
tasks = ["analysis", "tutoring", "problem solving"]

# Creative (0.8-1.0)
tasks = ["writing", "brainstorming", "ideation"]
```

### Testing Checklist

- [ ] Tests basic functionality
- [ ] Handles edge cases appropriately
- [ ] Output format is consistent
- [ ] Tone matches intended use case
- [ ] Errors are handled gracefully
- [ ] Performance is acceptable
- [ ] Behavior is predictable

## Examples

### Example 1: Code Reviewer

```json
{
  "name": "Code Reviewer",
  "model": "claude-sonnet-4-20250514",
  "temperature": 0.2,
  "system": "You are an experienced code reviewer focusing on Python. 
  Review code for: bugs, security issues, performance, best practices. 
  Always provide: issues list (priority ordered), specific fixes, 
  explanation of why each issue matters. Use this format:
  
  ## Critical Issues
  [issues that must be fixed]
  
  ## Important Issues  
  [issues that should be fixed]
  
  ## Suggestions
  [optional improvements]"
}
```

### Example 2: Research Assistant

```json
{
  "name": "Research Assistant",
  "model": "claude-sonnet-4-20250514",
  "temperature": 0.5,
  "system": "You are an academic research assistant specializing in 
  literature review and synthesis. Help researchers by:
  - Summarizing academic papers
  - Identifying key themes across papers
  - Suggesting research gaps
  - Recommending relevant papers
  
  Always cite sources and acknowledge limitations in your analysis."
}
```

## Advanced Topics

### Context Management

Long conversations may need:
- Periodic summaries
- Reference to earlier decisions
- Explicit state tracking

```python
context = {
    "previous_queries": [],
    "current_focus": "performance optimization",
    "constraints": ["PostgreSQL 14", "under 100ms"]
}

message = f"Given context: {context}, [new query]"
```

### Chaining Subagents

Complex workflows can chain multiple subagents:

```
1. Research Assistant → Gathers information
2. Analyst → Processes and analyzes
3. Writer → Creates final report
```

### Multi-Turn Optimization

For conversational subagents:
- Include conversation history
- Maintain consistent tone
- Reference previous points
- Build on earlier responses

## Troubleshooting

### Issue: Inconsistent responses

**Solutions:**
- Lower temperature
- Be more specific in system prompt
- Add explicit output format
- Include more examples

### Issue: Subagent ignores instructions

**Solutions:**
- Make instructions more explicit
- Use imperative language
- Add examples of correct behavior
- Test with simpler cases first

### Issue: Subagent is too verbose/brief

**Solutions:**
- Specify desired length in system prompt
- Add example outputs
- Use phrases like "Be concise" or "Provide detailed explanation"

## Contributing

To contribute a subagent:

1. Use the [template](../subagents/TEMPLATE.md)
2. Test thoroughly with various inputs
3. Document use cases and limitations
4. Include example interactions
5. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full guidelines.

## Resources

- [Subagents Template](../subagents/TEMPLATE.md)
- [Example Subagents](../subagents/examples/)
- [Anthropic Docs](https://docs.anthropic.com)
- [Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)

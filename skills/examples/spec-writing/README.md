# Spec Writing Skill

Write high-quality technical specifications for features, APIs, and systems.

## Quick Start

1. Load the skill by referencing `skills/examples/spec-writing/SKILL.md`
2. Provide context about what needs to be specified
3. Claude will guide you through creating a comprehensive spec

## Example Usage

```
You: I need to write a spec for a user authentication system that supports
     email/password and OAuth providers.

Claude: [Follows SKILL.md to create comprehensive auth spec with:
        - Problem statement and goals
        - Functional requirements (login flows, session management)
        - Security requirements (password policies, token handling)
        - API contracts for auth endpoints
        - Edge cases (account recovery, rate limiting)
        - Acceptance criteria]
```

## What This Skill Covers

- **Feature Specs**: New features with user stories and acceptance criteria
- **API Specs**: REST/GraphQL endpoint definitions with schemas
- **Architecture Specs**: System design and component interactions
- **Data Specs**: Database schemas and data models

## Key Features

- Structured approach to requirements gathering
- RFC 2119 keyword usage (MUST, SHOULD, MAY)
- Comprehensive quality checklist
- Edge case identification prompts
- Testable acceptance criteria templates

## Related Skills

- **Spec-Driven Development**: Implement code from your specifications
- **Code Review**: Validate implementation matches the spec

## Full Documentation

See [SKILL.md](./SKILL.md) for complete instructions, examples, and best practices.

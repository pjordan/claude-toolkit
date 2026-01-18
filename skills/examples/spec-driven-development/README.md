# Spec-Driven Development Skill

Implement features systematically by following technical specifications.

## Quick Start

1. Load the skill by referencing `skills/examples/spec-driven-development/SKILL.md`
2. Provide your specification document (feature spec, API spec, etc.)
3. Claude will systematically implement each requirement and track progress

## Example Usage

```
You: Here's the spec for our new user authentication API [spec content].
     Please implement it following spec-driven development practices.

Claude: [Follows SKILL.md to:
        1. Parse all requirements from the spec
        2. Create implementation tracking matrix
        3. Implement each requirement systematically
        4. Write tests referencing spec requirements
        5. Document any spec ambiguities
        6. Verify all acceptance criteria]
```

## What This Skill Covers

- **Requirement Parsing**: Extract functional and non-functional requirements
- **Implementation Tracking**: Matrix to track progress against spec
- **Systematic Implementation**: Address requirements one at a time
- **Spec Compliance Testing**: Tests that reference specific requirements
- **Gap Documentation**: Track ambiguities and deviations

## Key Features

- RFC 2119 keyword handling (MUST, SHOULD, MAY)
- Requirement traceability via tracking matrix
- Error handling implementation from spec
- Progress reporting format
- Spec clarification documentation

## Related Skills

- **Spec Writing**: Create specifications to implement
- **Code Review**: Validate implementation against spec

## Full Documentation

See [SKILL.md](./SKILL.md) for complete instructions, examples, and best practices.

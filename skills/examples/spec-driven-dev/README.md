# Spec-Driven Development Skill

A methodology for AI-assisted coding that puts specifications first.

## Quick Start

1. **Start with a spec** - Define what you're building before how
2. **Plan the approach** - Identify files, tests, and implementation order
3. **Break into tasks** - Atomic units with one test each
4. **Implement with TDD** - Write test → fail → implement → pass → refactor

## Core Workflow

```
Specify → Plan → Tasks → Implement
    ↓        ↓       ↓         ↓
  [Gate]  [Gate]  [Gate]   [Done]
```

Each phase has a validation gate before proceeding.

## Key Concepts

### Specification Template

```markdown
# Feature: [Name]

## Problem Statement
[Why this matters]

## Acceptance Criteria
Given [precondition]
When [action]
Then [expected result]

## Boundaries
- ✅ Always: [Must do]
- ⚠️ Ask First: [Needs clarification]
- 🚫 Never: [Must not do]
```

### Test-Driven Generation (TDG)

1. Write the test first (the test IS the spec)
2. Run it - confirm it fails
3. Implement minimal code to pass
4. Run it - confirm it passes
5. Refactor if needed
6. Commit

## When to Use

- New feature development
- Complex business logic
- High-reliability requirements
- Collaborative work needing explicit requirements

## When NOT to Use

- Quick prototypes where requirements are unknown
- Exploratory coding to understand a problem
- Simple bug fixes with obvious solutions

## Example

**User Request:** "Add email validation to the signup form"

**Spec (abbreviated):**
```markdown
## Acceptance Criteria
Given user enters "valid@email.com"
When they submit the form
Then form proceeds to next step

Given user enters "invalid-email"
When they submit the form
Then they see "Please enter a valid email address"

## Boundaries
- ✅ Always: Validate on blur and submit
- 🚫 Never: Allow form submission with invalid email
```

**First Test:**
```typescript
test('accepts valid email format', () => {
  expect(isValidEmail('user@example.com')).toBe(true);
});

test('rejects email without @', () => {
  expect(isValidEmail('userexample.com')).toBe(false);
});
```

## Resources

- [SKILL.md](./SKILL.md) - Full skill documentation with detailed examples
- [GitHub Spec-Kit](https://github.com/github/spec-kit) - Open source SDD toolkit
- [Agentic Coding Handbook](https://tweag.github.io/agentic-coding-handbook/) - TDD workflow guidance

## Version

1.0.0 | Created 2025-01-18

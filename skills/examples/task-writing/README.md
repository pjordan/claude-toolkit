# Task Writing Skill

Write high-quality, actionable tasks that are clear, well-scoped, and contain all the information needed for successful execution.

## Quick Start

Use this skill when you need to create individual work items (issues, tickets, tasks) for project management tools, issue trackers, or todo lists.

### Basic Task Template

```markdown
# [Action Verb] [What] [Where/Context]

## Background
[Why this task exists]

## Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

## Technical Notes
- Location: `path/to/files`
```

### Good Title Examples

| Instead of... | Write... |
|---------------|----------|
| Fix bug | Fix session timeout not showing error message |
| Update API | Add rate limiting to /api/v1/search endpoint |
| Improve perf | Add database index for user email lookups |
| User settings | Implement notification preference toggles |

### Acceptance Criteria Checklist

Good criteria are:
- ✅ Testable (can verify pass/fail)
- ✅ Specific (no ambiguity)
- ✅ Complete (covers edge cases)
- ✅ Independent (each stands alone)

### Scope Guidelines

A well-scoped task:
- Can be completed in 1-2 days
- Has a single coherent deliverable
- Has 5-7 or fewer acceptance criteria
- Touches 3-4 or fewer files

## Relationship to Other Skills

```
┌─────────────────┐
│  Spec Writing   │  Defines WHAT to build
└────────┬────────┘
         ↓
┌─────────────────┐
│  Plan Writing   │  Defines HOW to build (phases, steps)
└────────┬────────┘
         ↓
┌─────────────────┐
│  Task Writing   │  Creates TRACKABLE work items ← You are here
└────────┬────────┘
         ↓
┌─────────────────┐
│  Spec-Driven    │  EXECUTES tasks systematically
│  Development    │
└─────────────────┘
```

## Common Task Types

- **Feature tasks**: Implement new functionality
- **Bug fix tasks**: Resolve reported issues
- **Refactoring tasks**: Improve code without changing behavior
- **Spike/Investigation tasks**: Research and document findings

## Full Documentation

See [SKILL.md](./SKILL.md) for complete instructions, examples, and best practices.

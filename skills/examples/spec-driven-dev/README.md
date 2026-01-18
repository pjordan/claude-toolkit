# Spec-Driven Development Skill

Standardize feature development with structured artifacts for AI-assisted workflows.

## Overview

This skill establishes conventions for organizing feature documentation in a consistent directory structure that provides clear context for AI agents and human developers alike.

## When to Use

- Starting a new feature that needs clear requirements
- Planning implementation with multiple phases or components
- Breaking down work into trackable tasks
- Capturing technical decisions and research
- Logging progress with test results and verification
- Coordinating work between multiple agents or developers

## Quick Start

### 1. Initialize a Feature

```bash
mkdir -p agentdocs/features/my-feature/{tasks,notes,progress}
```

### 2. Create the Spec

Write `agentdocs/features/my-feature/spec.md` defining:
- Goals and non-goals
- User stories
- Requirements
- Acceptance criteria

### 3. Create the Plan

Write `agentdocs/features/my-feature/plan.md` outlining:
- Architecture and components
- Implementation phases
- Technical decisions
- Testing strategy

### 4. Define Tasks

Create task files in `agentdocs/features/my-feature/tasks/`:
- `01-database-schema.md`
- `02-api-endpoints.md`
- `03-frontend-ui.md`

### 5. Add Notes as Needed

Capture context in `agentdocs/features/my-feature/notes/`:
- `architecture.md` - Design decisions
- `research-auth.md` - Investigation findings
- `decision-database.md` - ADR-style records

### 6. Log Progress

Record work sessions in `agentdocs/features/my-feature/progress/`:
- `session-001.md` - First work session with test results
- `session-002.md` - Subsequent session with verification outputs

## Directory Structure

```
agentdocs/
└── features/
    └── <feature-slug>/
        ├── spec.md          # What we're building
        ├── plan.md          # How we're building it
        ├── tasks/           # Atomic work units
        │   ├── 01-setup.md
        │   └── 02-impl.md
        ├── notes/           # Context and decisions
        │   └── research.md
        └── progress/        # Session logs with test results
            ├── session-001.md
            └── session-002.md
```

## Key Principles

1. **Spec defines what, plan defines how** - Keep these concerns separate
2. **Tasks are atomic** - Each completable in one focused session
3. **Notes capture context** - Decisions, research, and learnings
4. **Progress logs are evidence** - Test results and verification outputs
5. **Cross-reference everything** - Link between related artifacts
6. **Keep status current** - Update as work progresses

## Templates

See `templates/` for ready-to-use templates:
- `spec.md` - Feature specification
- `plan.md` - Implementation plan
- `task.md` - Task definition
- `progress.md` - Session progress log
- `decision.md` - Decision record
- `research.md` - Research notes

## Related Skills

- **Code Review** - Review implementations against spec criteria
- **A2A Agent** - Build agents that consume these artifacts

## Resources

- [SKILL.md](SKILL.md) - Complete skill documentation
- [templates/](templates/) - Artifact templates
- [references/](references/) - Advanced patterns

# Spec-Driven Development Skill

Comprehensive spec-driven development workflow combining artifact management with systematic implementation.

## Overview

This skill provides a complete framework for feature development:
- **Artifact organization**: Structured directory conventions for specs, plans, tasks, and progress logs
- **Implementation methodology**: Systematic approach to implementing from specifications
- **Multi-agent coordination**: Patterns for handoffs and parallel work
- **Quality assurance**: Requirement tracking, testing strategies, and verification

## When to Use

- Starting a new feature that needs structured documentation
- Implementing features from written specifications
- Coordinating work between multiple agents or developers
- Ensuring traceability between requirements and code
- Building APIs from OpenAPI/Swagger specs
- Translating design documents into working code

## Quick Start

### 1. Initialize a Feature

```bash
mkdir -p agentdocs/features/my-feature/{tasks,notes,progress}
```

### 2. Create Documentation

Use the related skills to create artifacts:
- **spec-writing** → `agentdocs/features/my-feature/spec.md`
- **plan-writing** → `agentdocs/features/my-feature/plan.md`
- **task-writing** → `agentdocs/features/my-feature/tasks/`

### 3. Implement Systematically

Follow the implementation process:
1. Parse the specification
2. Create requirement tracking matrix
3. Implement one requirement at a time
4. Write tests referencing spec requirements
5. Document deviations and clarifications

### 4. Log Progress

Use **progress-writing** to capture:
- Session summaries
- Test results (actual output)
- Handoff notes for the next session

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

## Key Features

- **Workflow decision tree**: Know exactly what to do next
- **RFC 2119 keyword handling**: MUST, SHOULD, MAY guidance
- **Requirement tracking matrix**: Map requirements to code
- **Context loading patterns**: Efficient onboarding for agents
- **Multi-agent coordination**: Claim tasks, write handoffs

## Resources

- [SKILL.md](SKILL.md) - Complete skill documentation
- [templates/](templates/) - Artifact templates
- [references/](references/) - Advanced patterns

## Related Skills

- **spec-writing**: Create feature specifications
- **plan-writing**: Create implementation plans
- **task-writing**: Break plans into actionable tasks
- **progress-writing**: Document session progress and handoffs

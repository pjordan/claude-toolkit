---
name: spec-driven-dev
description: Structured artifact management for spec-driven feature development. Use when starting new features, creating implementation plans, tracking tasks, or organizing development notes. Triggers include "spec-driven", "feature spec", "implementation plan", "agentdocs", "feature artifacts", "development workflow", or when creating structured documentation for agent-assisted development.
---

# Spec-Driven Development Skill

Standardize feature development with structured artifacts that provide clear context for AI agents and human developers. This skill establishes conventions for organizing specs, plans, tasks, and notes in a consistent directory structure.

## Workflow Decision Tree

Use this decision tree to determine the workflow:

**1. Starting a new feature from scratch?**
   → Use [Initialize Feature](#initialize-feature) workflow

**2. Have requirements and need to create a spec?**
   → Use [Write Spec](#write-spec) workflow

**3. Have a spec and need to plan implementation?**
   → Use [Create Plan](#create-plan) workflow

**4. Ready to break down work into tasks?**
   → Use [Define Tasks](#define-tasks) workflow

**5. Need to capture decisions, research, or context?**
   → Use [Add Notes](#add-notes) workflow

**6. Need to log work progress, test results, or verification?**
   → Use [Log Progress](#log-progress) workflow

**7. Need reference patterns or templates?**
   → Read [references/artifact_patterns.md](references/artifact_patterns.md)

## Directory Structure

All feature artifacts live under `agentdocs/features/`:

```
agentdocs/
└── features/
    └── <feature-slug>/
        ├── spec.md              # Feature specification (required)
        ├── plan.md              # Implementation plan (required)
        ├── tasks/               # Individual task definitions
        │   ├── 01-setup.md
        │   ├── 02-core-impl.md
        │   └── ...
        ├── notes/               # Research, decisions, context
        │   ├── architecture.md
        │   ├── research.md
        │   └── ...
        └── progress/            # Session logs with test results & verification
            ├── session-001.md
            ├── session-002.md
            └── ...
```

**Naming Conventions:**
- Feature slugs: kebab-case, descriptive (e.g., `user-authentication`, `payment-processing`)
- Task files: numbered prefix for ordering (e.g., `01-`, `02-`)
- Note files: descriptive kebab-case names
- Progress files: `session-NNN.md` with zero-padded numbers

## Initialize Feature

Create the complete artifact structure for a new feature.

### Quick Start

```bash
# Create feature directory structure
mkdir -p agentdocs/features/<feature-slug>/{tasks,notes,progress}

# Create initial files
touch agentdocs/features/<feature-slug>/spec.md
touch agentdocs/features/<feature-slug>/plan.md
```

### Recommended Initialization Order

1. **Create directory structure** with feature slug
2. **Write spec.md** - Define what you're building
3. **Create plan.md** - Outline how you'll build it
4. **Add task files** - Break down into actionable units
5. **Add notes** - Capture context as you go
6. **Log progress** - Record work sessions and verification results

### Example: Initialize "User Authentication" Feature

```bash
mkdir -p agentdocs/features/user-authentication/{tasks,notes,progress}
```

Then populate artifacts using workflows below.

## Write Spec

The spec defines **what** you're building. It's the source of truth for requirements.

### Spec Template

```markdown
# Feature: [Feature Name]

## Status
- [ ] Draft
- [ ] Review
- [ ] Approved
- [ ] In Progress
- [ ] Complete

## Overview

[2-3 sentence description of the feature and its value]

## Goals

- [Primary goal 1]
- [Primary goal 2]

## Non-Goals

- [What this feature explicitly does NOT do]
- [Scope boundaries]

## User Stories

### [User Type]
- As a [user type], I want [action] so that [benefit]
- As a [user type], I want [action] so that [benefit]

## Requirements

### Functional Requirements
1. [FR-1] [Requirement description]
2. [FR-2] [Requirement description]

### Non-Functional Requirements
1. [NFR-1] [Performance/security/scalability requirement]
2. [NFR-2] [Performance/security/scalability requirement]

## Acceptance Criteria

- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

## Dependencies

- [External system or feature this depends on]
- [Required library or service]

## Open Questions

- [ ] [Unresolved question 1]
- [ ] [Unresolved question 2]

## References

- [Link to related docs, designs, or discussions]
```

### Spec Best Practices

**Do:**
- Keep requirements atomic and testable
- Use clear, unambiguous language
- Define explicit scope boundaries (non-goals)
- Track open questions until resolved
- Update status as feature progresses

**Don't:**
- Include implementation details (that's for the plan)
- Leave requirements vague or subjective
- Skip non-functional requirements
- Forget to define acceptance criteria

### Example: User Authentication Spec

```markdown
# Feature: User Authentication

## Status
- [x] Draft
- [x] Review
- [x] Approved
- [ ] In Progress
- [ ] Complete

## Overview

Implement secure user authentication using JWT tokens with support for
email/password login and OAuth providers. This enables personalized
experiences and protected resources.

## Goals

- Secure authentication with industry-standard practices
- Support multiple authentication methods
- Seamless user experience across devices

## Non-Goals

- Multi-factor authentication (future phase)
- Enterprise SSO/SAML integration
- User management admin interface

## User Stories

### End User
- As a user, I want to sign up with my email so that I can create an account
- As a user, I want to log in with Google so that I don't need another password
- As a user, I want to stay logged in so that I don't have to authenticate repeatedly

## Requirements

### Functional Requirements
1. [FR-1] Users can register with email and password
2. [FR-2] Users can log in with email and password
3. [FR-3] Users can log in with Google OAuth
4. [FR-4] Sessions persist across browser restarts
5. [FR-5] Users can log out from all devices

### Non-Functional Requirements
1. [NFR-1] Passwords hashed with bcrypt (cost factor 12)
2. [NFR-2] JWT tokens expire after 7 days
3. [NFR-3] Rate limit: 5 failed login attempts per minute

## Acceptance Criteria

- [ ] User can complete registration in under 30 seconds
- [ ] Failed login shows appropriate error message
- [ ] OAuth flow completes without leaving the app
- [ ] Tokens refresh transparently before expiration

## Dependencies

- PostgreSQL database for user storage
- Redis for session management
- Google OAuth credentials

## Open Questions

- [ ] Should we support "remember me" longer sessions?
- [x] Which OAuth providers to support initially? → Google only for MVP
```

## Create Plan

The plan defines **how** you'll build the feature. It bridges spec to implementation.

### Plan Template

```markdown
# Implementation Plan: [Feature Name]

**Spec**: [Link to spec.md]
**Status**: Draft | In Progress | Complete
**Last Updated**: YYYY-MM-DD

## Approach Summary

[1-2 paragraph summary of the implementation approach]

## Architecture

### Components

| Component | Purpose | New/Modified |
|-----------|---------|--------------|
| [Name] | [What it does] | New |
| [Name] | [What it does] | Modified |

### Data Model

[Describe database schema, data structures, or state management]

```sql
-- Example schema
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    ...
);
```

### API Design

[Describe endpoints, contracts, or interfaces]

```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

## Implementation Phases

### Phase 1: [Name]
- [Deliverable 1]
- [Deliverable 2]

### Phase 2: [Name]
- [Deliverable 1]
- [Deliverable 2]

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| [What] | [Selected option] | [Why] |
| [What] | [Selected option] | [Why] |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | High/Medium/Low | [How to address] |

## Testing Strategy

- **Unit Tests**: [What to test at unit level]
- **Integration Tests**: [What to test at integration level]
- **E2E Tests**: [Critical user flows to test]

## Rollout Plan

1. [Step 1 - e.g., Deploy behind feature flag]
2. [Step 2 - e.g., Enable for internal users]
3. [Step 3 - e.g., Gradual rollout to production]

## Success Metrics

- [Metric 1 and target]
- [Metric 2 and target]
```

### Plan Best Practices

**Do:**
- Reference the spec explicitly
- Document architectural decisions with rationale
- Identify risks early
- Define clear phases/milestones
- Keep plan updated as implementation evolves

**Don't:**
- Duplicate spec content
- Go into code-level detail (that's for tasks)
- Skip testing strategy
- Forget rollout considerations

## Define Tasks

Tasks are atomic units of work. Each task should be completable in one focused session.

### Task Template

```markdown
# Task: [Task Title]

**Feature**: [Link to ../spec.md]
**Plan Phase**: [Which phase from plan.md]
**Status**: TODO | IN_PROGRESS | BLOCKED | DONE
**Priority**: P0 | P1 | P2

## Objective

[1-2 sentences: What this task accomplishes]

## Context

[Background needed to understand this task. Link to relevant notes.]

## Scope

### In Scope
- [Specific deliverable 1]
- [Specific deliverable 2]

### Out of Scope
- [What this task does NOT include]

## Implementation Details

[Technical guidance, code examples, or pseudocode]

```python
# Example approach
def example():
    pass
```

## Acceptance Criteria

- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

## Files to Modify

- `path/to/file1.py` - [What changes]
- `path/to/file2.ts` - [What changes]

## Dependencies

- **Blocked by**: [Other task or external dependency]
- **Blocks**: [Tasks waiting on this]

## Notes

- [Implementation note or consideration]
```

### Task Best Practices

**Do:**
- Keep tasks small (2-4 hours of focused work)
- Include clear acceptance criteria
- List specific files to modify
- Track dependencies between tasks
- Number tasks for ordering (01-, 02-, etc.)

**Don't:**
- Create tasks too large to complete in one session
- Leave acceptance criteria vague
- Skip the "out of scope" section
- Forget to update status

### Task Sizing Guidelines

| Size | Duration | Characteristics |
|------|----------|-----------------|
| Small | < 2 hours | Single file, well-defined change |
| Medium | 2-4 hours | Multiple files, clear scope |
| Large | 4-8 hours | Consider breaking down further |
| Epic | > 8 hours | Must be broken into smaller tasks |

### Example: Task File Structure

```
tasks/
├── 01-database-schema.md      # Phase 1
├── 02-user-model.md           # Phase 1
├── 03-auth-endpoints.md       # Phase 2
├── 04-jwt-middleware.md       # Phase 2
├── 05-oauth-integration.md    # Phase 3
├── 06-frontend-forms.md       # Phase 4
└── 07-e2e-tests.md           # Phase 5
```

## Add Notes

Notes capture context that doesn't fit in specs, plans, or tasks.

### Note Types

| Type | Purpose | Filename Pattern |
|------|---------|------------------|
| Architecture | System design decisions | `architecture.md` |
| Research | Investigation findings | `research-<topic>.md` |
| Decision | ADR-style decision records | `decision-<topic>.md` |
| Meeting | Discussion summaries | `meeting-<date>.md` |
| Retrospective | Post-implementation learnings | `retro.md` |

### Decision Record Template

```markdown
# Decision: [Title]

**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded
**Deciders**: [Who made this decision]

## Context

[What is the issue that we're seeing that is motivating this decision?]

## Options Considered

### Option 1: [Name]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]

### Option 2: [Name]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]

## Decision

[What is the change that we're proposing or have agreed to implement?]

## Consequences

- [What becomes easier?]
- [What becomes harder?]
- [What are the risks?]
```

### Research Note Template

```markdown
# Research: [Topic]

**Date**: YYYY-MM-DD
**Related To**: [Link to spec or task]

## Question

[What are we trying to learn?]

## Findings

### [Subtopic 1]
[What we learned]

### [Subtopic 2]
[What we learned]

## Recommendations

- [Recommendation 1]
- [Recommendation 2]

## Sources

- [Link to documentation]
- [Link to article or resource]
```

## Log Progress

Progress logs capture the running history of work sessions - test results, build outputs, verification steps, and incremental progress. Unlike notes (which are durable context), progress logs are append-only records of what happened.

### When to Create a Progress Log

Create a new session log when:
- Starting work on a feature (new session)
- Resuming after a break or context switch
- Different agent picks up work
- Significant milestone reached

### Progress Log Template

```markdown
# Session [NNN]: [Brief Description]

**Date**: YYYY-MM-DD
**Agent/Author**: [Identifier]
**Tasks Worked**: [task-01, task-02]
**Duration**: [Approximate time spent]

## Summary

[2-3 sentence summary of what was accomplished this session]

## Work Log

### [HH:MM] - [Activity]

[Description of what was done]

### [HH:MM] - [Activity]

[Description of what was done]

## Test Results

### Unit Tests

```
[Test output - paste actual results]
```

**Status**: ✅ All passing | ⚠️ X failing | ❌ Build broken

### Integration Tests

```
[Test output if applicable]
```

### Manual Verification

- [x] [Verification step completed]
- [x] [Verification step completed]
- [ ] [Verification step pending]

## Build Output

```
[Build/compile output if relevant]
```

## Issues Encountered

### [Issue Title]

**Problem**: [What went wrong]
**Resolution**: [How it was fixed] | **Status**: Unresolved

## Handoff Notes

[Context for the next session or agent - what's in progress, what's blocked, what's ready for review]

## Next Steps

- [ ] [What should happen next]
- [ ] [What should happen next]
```

### Progress Log Best Practices

**Do:**
- Start a new session log for each work session
- Include actual command output (tests, builds, errors)
- Timestamp significant activities
- Write handoff notes for continuity
- Link to specific tasks being worked

**Don't:**
- Edit old session logs (append-only)
- Include sensitive data in outputs
- Skip test results - they're the evidence of progress
- Forget handoff notes - they're critical for multi-agent work

### Example: Session Log

```markdown
# Session 003: Implement JWT Authentication

**Date**: 2024-01-15
**Agent/Author**: claude-agent-1
**Tasks Worked**: [03-auth-endpoints](../tasks/03-auth-endpoints.md)
**Duration**: ~2 hours

## Summary

Implemented JWT token generation and validation middleware. All unit tests
passing. Integration tests revealed an issue with token refresh that needs
investigation.

## Work Log

### 10:30 - Started JWT implementation

Created `src/auth/jwt.py` with token generation using PyJWT library.
Followed patterns from plan.md for token structure.

### 11:15 - Added middleware

Created `src/middleware/auth.py` for request authentication.
Integrated with FastAPI dependency injection.

### 11:45 - Wrote unit tests

Added tests for token generation, validation, and expiry.

### 12:00 - Ran integration tests

Found issue with refresh token flow - tokens not being invalidated
on logout.

## Test Results

### Unit Tests

```
$ pytest tests/unit/test_jwt.py -v
tests/unit/test_jwt.py::test_token_generation PASSED
tests/unit/test_jwt.py::test_token_validation PASSED
tests/unit/test_jwt.py::test_token_expiry PASSED
tests/unit/test_jwt.py::test_invalid_token_rejected PASSED

4 passed in 0.23s
```

**Status**: ✅ All passing

### Integration Tests

```
$ pytest tests/integration/test_auth_flow.py -v
tests/integration/test_auth_flow.py::test_login_flow PASSED
tests/integration/test_auth_flow.py::test_protected_endpoint PASSED
tests/integration/test_auth_flow.py::test_logout_invalidates_token FAILED

FAILED tests/integration/test_auth_flow.py::test_logout_invalidates_token
  - AssertionError: Token still valid after logout
```

**Status**: ⚠️ 1 failing

## Issues Encountered

### Token not invalidated on logout

**Problem**: JWT tokens remain valid after logout because JWTs are stateless
**Resolution**: Need to implement token blacklist in Redis (see task-04)
**Status**: Deferred to task-04

## Handoff Notes

- JWT generation and validation working correctly
- Middleware integrated and protecting routes
- Logout invalidation requires Redis blacklist (task-04 dependency)
- All code committed to branch `feature/user-auth`

## Next Steps

- [ ] Complete task-04 (Redis token blacklist) to fix logout
- [ ] Update integration test once blacklist implemented
- [ ] Begin task-05 (OAuth integration)
```

### Session Numbering

Use zero-padded session numbers for sorting:
- `session-001.md`
- `session-002.md`
- `session-010.md`

For long-running features, consider monthly grouping:
```
progress/
├── 2024-01/
│   ├── session-001.md
│   └── session-002.md
└── 2024-02/
    ├── session-003.md
    └── session-004.md
```

## Key Concepts

### Artifact Lifecycle

```
Spec (Draft) → Spec (Approved) → Plan → Tasks → Implementation → Spec (Complete)
                      ↓                   ↓              ↓
                   Notes ←←←←←←←←←←←←←← Notes      Progress Logs
                                                   (test results,
                                                    verification)
```

### Agent Context Loading

When an agent starts work on a feature, it should load context in this order:

1. **spec.md** - Understand what we're building
2. **plan.md** - Understand how we're building it
3. **Latest progress log** - Understand current state and handoff notes
4. **Current task** - Focus on the immediate work
5. **Relevant notes** - Additional context as needed

### Cross-Referencing

Always link between artifacts:

```markdown
<!-- In a task -->
**Feature**: [User Authentication](../spec.md)
**Plan Phase**: [Phase 2: Core Auth](../plan.md#phase-2-core-auth)

<!-- In a note -->
**Related Task**: [03-auth-endpoints](../tasks/03-auth-endpoints.md)
```

### Status Tracking

Maintain consistent status across artifacts:

| Artifact | Statuses |
|----------|----------|
| Spec | Draft, Review, Approved, In Progress, Complete |
| Plan | Draft, In Progress, Complete |
| Task | TODO, IN_PROGRESS, BLOCKED, DONE |

## Resources

### Templates (`templates/`)
- `spec.md` - Feature specification template
- `plan.md` - Implementation plan template
- `task.md` - Task definition template
- `progress.md` - Session progress log template
- `decision.md` - Decision record template
- `research.md` - Research note template

### References (`references/`)
- `artifact_patterns.md` - Advanced patterns for artifact management

## Common Patterns

### Feature Kickoff Checklist

```markdown
- [ ] Create feature directory: `agentdocs/features/<slug>/`
- [ ] Create subdirectories: `tasks/`, `notes/`, and `progress/`
- [ ] Write initial spec.md (Draft status)
- [ ] Get spec reviewed and approved
- [ ] Create plan.md with phases
- [ ] Break Phase 1 into tasks
- [ ] Create initial research notes if needed
- [ ] Start first progress log when beginning work
```

### Updating Artifacts During Development

As implementation progresses:

1. **Log progress** with test results and verification outputs
2. **Mark tasks DONE** when complete
3. **Add notes** for decisions made during implementation
4. **Update plan** if approach changes significantly
5. **Check off acceptance criteria** in spec
6. **Update spec status** when feature complete

### Multi-Agent Coordination

When multiple agents work on a feature:

1. Each agent claims a task by setting status to `IN_PROGRESS`
2. Agents read spec, plan, and **latest progress log** for context
3. Agents create a **new session log** when starting work
4. Agents add notes for decisions affecting other tasks
5. Tasks explicitly declare dependencies with `Blocked by` / `Blocks`
6. Agents write **handoff notes** in progress log before ending session
7. Agents mark tasks `DONE` and update any blocking relationships

## Troubleshooting

**Spec too vague:**
- Add more specific acceptance criteria
- Break user stories into smaller, testable units
- Define explicit non-goals to clarify scope

**Plan doesn't match implementation:**
- Update plan as you learn
- Add decision notes explaining deviations
- Keep plan as living document, not fixed contract

**Tasks too large:**
- If a task takes more than 4 hours, split it
- Create subtasks for complex implementations
- Each task should have clear, verifiable completion

**Context loading slow:**
- Keep specs focused (1-2 pages)
- Summarize long notes
- Use clear headings for scanability

**Lost track of dependencies:**
- Review `Blocked by` / `Blocks` in all tasks
- Create dependency diagram in notes if complex
- Update task statuses promptly

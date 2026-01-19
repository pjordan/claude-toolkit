# Artifact Patterns Reference

Advanced patterns for managing spec-driven development artifacts.

## Table of Contents

- [Context Loading Patterns](#context-loading-patterns)
- [Progress Logging Patterns](#progress-logging-patterns)
- [Multi-Agent Coordination](#multi-agent-coordination)
- [Artifact Evolution](#artifact-evolution)
- [Dependency Management](#dependency-management)
- [Status Workflows](#status-workflows)
- [Linking Strategies](#linking-strategies)
- [Scale Considerations](#scale-considerations)

---

## Context Loading Patterns

### Hierarchical Context Loading

When an agent begins work, load context hierarchically:

```
1. spec.md (always first - understand the goal)
   ↓
2. plan.md (understand the approach)
   ↓
3. Latest progress log (understand current state)
   ↓
4. Current task file (understand immediate work)
   ↓
5. Related notes (additional context as needed)
```

### Minimal Context Pattern

For quick tasks, load only essential context:

```python
# Pseudocode for minimal context loading
def load_task_context(task_path):
    task = read(task_path)
    spec_summary = read_section(task.feature_link, "Overview")
    return {
        "task": task,
        "goal": spec_summary,
        "scope": task.scope
    }
```

### Full Context Pattern

For complex decisions, load comprehensive context:

```python
def load_full_context(feature_slug):
    return {
        "spec": read(f"agentdocs/features/{feature_slug}/spec.md"),
        "plan": read(f"agentdocs/features/{feature_slug}/plan.md"),
        "latest_progress": read_latest(f"agentdocs/features/{feature_slug}/progress/"),
        "tasks": read_all(f"agentdocs/features/{feature_slug}/tasks/"),
        "notes": read_all(f"agentdocs/features/{feature_slug}/notes/"),
        "dependencies": resolve_dependencies(feature_slug)
    }
```

### Progressive Context Pattern

Load context progressively as complexity requires:

```
Initial: spec.md overview only
If resuming: + latest progress log handoff notes
If blocked: + relevant notes
If design decision: + full plan
If cross-cutting: + related feature specs
```

---

## Progress Logging Patterns

### Session Boundaries

Create a new session log when:

| Trigger | Rationale |
|---------|-----------|
| Starting work on feature | Fresh context, clean state |
| Resuming after break (>4 hours) | Context may have changed |
| Different agent picks up work | New agent needs to document their session |
| Significant milestone reached | Good checkpoint for history |
| Major blocker encountered | Document the situation for handoff |

### Test Output Capture

Always capture actual output, not summaries:

```markdown
## Test Results

### Unit Tests

```
$ pytest tests/unit/ -v --tb=short
tests/unit/test_auth.py::test_login PASSED
tests/unit/test_auth.py::test_invalid_password PASSED
tests/unit/test_auth.py::test_token_generation PASSED
tests/unit/test_auth.py::test_token_expiry FAILED

FAILED tests/unit/test_auth.py::test_token_expiry
  AssertionError: Token expired too early
  Expected: 3600s, Got: 3599s

4 passed, 1 failed in 0.45s
```

**Analysis**: Flaky test due to timing - token generated at boundary.
**Action**: Added 1s buffer to test assertion.
```

### Verification Checklists

Use checklists for manual verification:

```markdown
## Manual Verification

### Happy Path
- [x] User can register with valid email
- [x] User receives confirmation email
- [x] User can log in after confirming

### Error Cases
- [x] Invalid email shows error message
- [x] Duplicate email prevented
- [ ] Rate limiting works (need to test)

### Edge Cases
- [x] Unicode in username handled
- [ ] Very long email addresses (need to test)
```

### Build Output Recording

Capture build state for debugging:

```markdown
## Build Output

```
$ npm run build
> my-app@1.0.0 build
> vite build

vite v5.0.0 building for production...
✓ 42 modules transformed.
dist/index.html                  0.45 kB │ gzip:  0.29 kB
dist/assets/index-abc123.css     1.23 kB │ gzip:  0.65 kB
dist/assets/index-def456.js     45.67 kB │ gzip: 15.23 kB
✓ built in 1.23s
```

**Status**: ✅ Success
**Bundle Size**: 45.67 kB (within 50 kB budget)
```

### Error Documentation

Document errors with full context:

```markdown
## Issues Encountered

### Database connection timeout

**Problem**: Integration tests failing with connection timeout after 30s

**Environment**:
- PostgreSQL 15.2
- Connection pool size: 10
- Test parallelism: 4

**Investigation**:
1. Checked database logs - no connection issues
2. Monitored connection pool - exhausted during parallel tests
3. Found tests not releasing connections properly

**Root Cause**: Missing `await session.close()` in test fixtures

**Resolution**: Added proper cleanup in `conftest.py`:
```python
@pytest.fixture
async def db_session():
    session = await get_session()
    yield session
    await session.close()  # Added this line
```

**Verification**: All tests now pass with parallel execution
```

### Handoff Protocol

Structure handoff notes for easy pickup:

```markdown
## Handoff Notes

### Current State
- Task 03 is 80% complete
- JWT generation working, validation has edge case bug
- All code committed to `feature/auth` branch

### Immediate Blockers
- None - ready to continue

### Context for Next Session
- Bug in `src/auth/jwt.py:45` - tokens with special chars in claims fail
- Relevant test: `tests/unit/test_jwt.py::test_special_char_claims`
- Reference: https://github.com/jpadilla/pyjwt/issues/123

### Files to Focus On
- `src/auth/jwt.py` - Fix claim encoding
- `tests/unit/test_jwt.py` - Add more edge case tests

### Don't Forget
- Run full test suite before marking task complete
- Update plan.md Phase 2 status when done
```

### Progress Log Retention

For long features, consider log management:

```
progress/
├── current/           # Active session logs
│   ├── session-015.md
│   └── session-016.md
└── archive/           # Older logs (compressed or summarized)
    ├── week-01-summary.md
    ├── week-02-summary.md
    └── raw/           # Original logs if needed
        ├── session-001.md
        └── ...
```

Weekly summary pattern:

```markdown
# Week 2 Summary (Sessions 005-009)

## Accomplishments
- Completed tasks 03, 04, 05
- All unit tests passing (127 tests)
- Integration test coverage at 85%

## Key Decisions
- Switched from bcrypt to argon2 (see decision-password-hashing.md)
- Added Redis for session storage

## Issues Resolved
- Fixed connection pool exhaustion
- Resolved timezone handling in tokens

## Carried Forward
- Task 06 in progress (OAuth integration)
- Waiting on Google OAuth credentials
```

---

## Multi-Agent Coordination

### Task Claiming Protocol

When multiple agents work on a feature:

1. **Read latest progress log** for handoff context
2. **Check task status** before starting
3. **Claim task** by updating status to `IN_PROGRESS`
4. **Create new session log** for your work
5. **Include agent identifier** in task metadata
6. **Release task** if unable to complete

```markdown
# Task: Setup Database Schema

**Status**: IN_PROGRESS
**Assigned**: agent-001
**Started**: 2024-01-15T10:30:00Z
```

### Conflict Avoidance

Prevent multiple agents from modifying same files:

```markdown
## Files to Modify

- `src/models/user.py` - [LOCKED by task-01]
- `src/api/auth.py` - [Available]
```

### Handoff Pattern

When one task's output is another's input:

```markdown
<!-- In task-01 completing -->
## Handoff Notes

Created the following for task-02:
- `UserModel` in `src/models/user.py`
- Migration `001_create_users.sql`
- Test fixtures in `tests/fixtures/users.py`

Ready for task-02 to implement authentication endpoints.
```

### Shared Notes Pattern

Use notes for cross-task communication:

```markdown
# Note: API Design Decisions

**Updated By**: agent-001 (during task-03)
**Affects**: task-04, task-05

## Decision

Changed authentication header from `X-Auth-Token` to standard
`Authorization: Bearer <token>` format.

## Impact

- task-04: Update client SDK to use new header
- task-05: Update API documentation
```

---

## Artifact Evolution

### Spec Evolution

Specs should be stable but can evolve:

| Change Type | Process |
|-------------|---------|
| Clarification | Direct update, note in changelog |
| Scope addition | Requires review, update status |
| Scope reduction | Requires review, update non-goals |
| Requirement change | New spec version, decision record |

### Plan Evolution

Plans are living documents:

```markdown
## Changelog

### 2024-01-15
- Added Phase 3 for OAuth integration (per spec update)
- Moved rate limiting from Phase 2 to Phase 4

### 2024-01-10
- Initial plan created
```

### Task Splitting

When a task is too large:

1. Mark original task as `SPLIT`
2. Create new subtasks with references
3. Update dependencies

```markdown
# Task: 03-authentication (SPLIT)

This task was split into:
- [03a-jwt-tokens](03a-jwt-tokens.md)
- [03b-session-management](03b-session-management.md)
- [03c-password-hashing](03c-password-hashing.md)
```

---

## Dependency Management

### Dependency Declaration

Explicit dependency tracking in tasks:

```markdown
## Dependencies

### Blocked By
- [ ] [01-database-schema](01-database-schema.md) - Need User table
- [x] [02-config-setup](02-config-setup.md) - Need env vars

### Blocks
- [04-api-endpoints](04-api-endpoints.md) - Needs auth middleware
- [05-frontend](05-frontend.md) - Needs auth context
```

### Dependency Graph

For complex features, maintain a visual dependency graph:

```
agentdocs/features/my-feature/notes/dependencies.md

# Task Dependencies

┌─────────────┐
│ 01-database │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│  02-models  │────▶│  03-api     │
└─────────────┘     └──────┬──────┘
                           │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ 04-frontend │     │  05-tests   │     │  06-docs    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### External Dependencies

Track dependencies outside the feature:

```markdown
## External Dependencies

| Dependency | Type | Status | Contact |
|------------|------|--------|---------|
| Auth0 tenant setup | Service | Pending | ops-team |
| Database migration | Infrastructure | Complete | dba-team |
| Design mockups | Design | In Review | design-team |
```

---

## Status Workflows

### Spec Status Flow

```
Draft ──► Review ──► Approved ──► In Progress ──► Complete
                         │
                         ▼
                    (Revision) ──► Review
```

### Task Status Flow

```
TODO ──► IN_PROGRESS ──► DONE
              │
              ▼
          BLOCKED ──► TODO (when unblocked)
              │
              ▼
           SPLIT ──► (creates new tasks)
```

### Status Synchronization

Keep status synchronized across artifacts:

```markdown
<!-- spec.md -->
## Status
- [x] Approved
- [x] In Progress  ← Update when first task starts
- [ ] Complete     ← Update when all tasks done

<!-- Each task tracks its own status -->
<!-- plan.md reflects overall progress -->
```

### Blocked Status Handling

When a task is blocked:

```markdown
# Task: 04-oauth-integration

**Status**: BLOCKED
**Blocked By**: Waiting for OAuth credentials from security team
**Blocked Since**: 2024-01-15
**Expected Resolution**: 2024-01-18

## While Blocked

Agent should:
- Move to next unblocked task
- Document any preparatory work possible
- Check daily for resolution
```

---

## Linking Strategies

### Relative Links

Always use relative links between artifacts:

```markdown
<!-- In a task -->
See [spec](../spec.md) for requirements.
Related decision: [OAuth Provider Choice](../notes/decision-oauth.md)

<!-- In a note -->
This affects [task-04](../tasks/04-oauth.md) implementation.
```

### Section Links

Link to specific sections:

```markdown
Per [Phase 2 requirements](../plan.md#phase-2-authentication),
implement the JWT middleware.
```

### Bidirectional Links

Maintain links in both directions:

```markdown
<!-- In spec.md -->
## Related
- Implementation: [plan.md](plan.md)

<!-- In plan.md -->
## Related
- Specification: [spec.md](spec.md)
```

### External Links

Track external references:

```markdown
## External References

- [Figma Design](https://figma.com/...)
- [API Documentation](https://api-docs.example.com/...)
- [Jira Epic](https://jira.example.com/browse/PROJ-123)
```

---

## Scale Considerations

### Large Features

For features with 10+ tasks:

1. **Group tasks by phase**
   ```
   tasks/
   ├── phase-1/
   │   ├── 01-setup.md
   │   └── 02-schema.md
   ├── phase-2/
   │   ├── 01-api.md
   │   └── 02-auth.md
   ```

2. **Create phase summaries**
   ```markdown
   # Phase 1 Summary

   - 3 tasks, 2 complete, 1 in progress
   - Deliverables: Database schema, base models
   ```

### Long-Running Features

For features spanning weeks/months:

1. **Weekly status notes**
   ```
   notes/
   ├── status-week-01.md
   ├── status-week-02.md
   ```

2. **Milestone tracking**
   ```markdown
   ## Milestones

   - [x] M1: Database schema approved (Jan 10)
   - [x] M2: API endpoints functional (Jan 17)
   - [ ] M3: Frontend integration (Jan 24)
   - [ ] M4: Testing complete (Jan 31)
   ```

### Multiple Related Features

When features depend on each other:

```
agentdocs/
├── features/
│   ├── user-auth/           # Core feature
│   ├── user-profiles/       # Depends on user-auth
│   └── social-features/     # Depends on user-profiles
└── cross-feature/
    └── user-system-deps.md  # Cross-feature dependency map
```

### Archiving Completed Features

After feature completion:

1. Update spec status to Complete
2. Write retrospective note
3. Move to archive (optional)
   ```
   agentdocs/
   ├── features/          # Active features
   └── archive/           # Completed features
       └── user-auth/
   ```

---

## Best Practices Summary

### Do

- Load context hierarchically (spec → plan → progress → task)
- Keep artifacts focused and scannable
- Update status immediately when it changes
- Cross-reference related artifacts
- Document decisions as they're made
- Use consistent naming conventions
- Capture actual test/build output in progress logs
- Write handoff notes before ending sessions

### Don't

- Duplicate content across artifacts
- Let status get out of sync
- Create circular dependencies
- Skip the non-goals section
- Leave blockers undocumented
- Forget to update links when moving files
- Edit old progress logs (they're append-only history)
- Summarize test output - capture the real thing

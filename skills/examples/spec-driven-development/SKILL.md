---
name: spec-driven-development
description: Comprehensive spec-driven development workflow combining artifact management with systematic implementation. Use when starting new features, creating specs/plans, implementing from specifications, or coordinating multi-agent development. Triggers include "spec-driven", "feature spec", "implementation plan", "agentdocs", "implement spec", "build from spec", or when doing structured feature development.
---

# Spec-Driven Development Skill

A comprehensive workflow for feature development that combines structured artifact management with systematic implementation practices. This skill guides you through the full lifecycle: organizing documentation, writing specifications, planning implementation, and methodically coding against requirements.

## Overview

Spec-driven development ensures:
- **Clear organization**: Consistent directory structure for all feature artifacts
- **Traceability**: Requirements map directly to implementation and tests
- **Quality**: Systematic coverage of requirements, edge cases, and acceptance criteria
- **Coordination**: Multi-agent workflows with proper handoffs and progress tracking

## Workflow Decision Tree

Use this to determine your next action:

**1. Starting a new feature from scratch?**
   → Use [Initialize Feature](#initialize-feature)

**2. Have requirements and need to create a spec?**
   → Use the **spec-writing** skill, save to `agentdocs/features/<slug>/spec.md`

**3. Have a spec and need to plan implementation?**
   → Use the **plan-writing** skill, save to `agentdocs/features/<slug>/plan.md`

**4. Ready to break down work into tasks?**
   → Use the **task-writing** skill, save to `agentdocs/features/<slug>/tasks/`

**5. Ready to implement a task?**
   → Use [Implementation Process](#implementation-process)

**6. Need to log progress, test results, or handoff notes?**
   → Use the **progress-writing** skill, save to `agentdocs/features/<slug>/progress/`

**7. Need reference patterns?**
   → Read [references/artifact_patterns.md](references/artifact_patterns.md)

## Directory Structure

All feature artifacts live under `agentdocs/features/`:

```
agentdocs/
└── features/
    └── <feature-slug>/
        ├── spec.md              # What we're building (required)
        ├── plan.md              # How we're building it (required)
        ├── tasks/               # Individual work units
        │   ├── 01-setup.md
        │   ├── 02-core-impl.md
        │   └── ...
        ├── notes/               # Research, decisions, context
        │   ├── architecture.md
        │   ├── decision-<topic>.md
        │   └── research-<topic>.md
        └── progress/            # Session logs with test results
            ├── session-001.md
            ├── session-002.md
            └── ...
```

**Naming Conventions:**
- Feature slugs: kebab-case (e.g., `user-authentication`, `payment-processing`)
- Task files: numbered prefix for ordering (e.g., `01-`, `02-`)
- Note files: descriptive kebab-case names
- Progress files: `session-NNN.md` with zero-padded numbers

## Initialize Feature

Create the artifact structure for a new feature:

```bash
# Create feature directory structure
mkdir -p agentdocs/features/<feature-slug>/{tasks,notes,progress}

# Create initial files
touch agentdocs/features/<feature-slug>/spec.md
touch agentdocs/features/<feature-slug>/plan.md
```

**Initialization Order:**
1. Create directory structure
2. Write spec.md using **spec-writing** skill
3. Create plan.md using **plan-writing** skill
4. Break down into tasks using **task-writing** skill
5. Begin implementation, logging progress as you go

## Implementation Process

When implementing from a specification:

### 1. Parse the Specification

Before writing code, extract:
- All functional requirements (FR-1, FR-2, etc.)
- Non-functional requirements (performance, security)
- Explicit edge cases and error conditions
- Acceptance criteria
- Ambiguities needing clarification

### 2. Create Requirement Tracking Matrix

Track implementation progress:

```markdown
| Req ID | Description | Status | Location |
|--------|-------------|--------|----------|
| FR-1 | User login with email | ✅ Done | src/auth/login.ts:45 |
| FR-2 | OAuth provider support | 🔄 In Progress | Google done, GitHub pending |
| FR-3 | Session management | ⏳ Pending | Blocked on FR-1 |
| NFR-1 | < 200ms response time | ✅ Done | Measured at 85ms P95 |
| EC-1 | Invalid credentials | ✅ Done | Returns 401 per spec |
```

### 3. Implement Systematically

- Address one requirement at a time
- Write tests alongside implementation
- Handle error cases as specified
- Document deviations or clarifications needed
- Update tracking matrix as you progress

### 4. Verify Against Spec

- Check each requirement is implemented
- Verify edge cases are handled
- Run acceptance criteria tests
- Document spec coverage

### 5. Log Progress

After each session, create a progress log capturing:
- What was accomplished
- Test results (actual output, not summaries)
- Issues encountered and resolutions
- Handoff notes for the next session

## Handling Spec Keywords (RFC 2119)

**MUST / REQUIRED**: Implement exactly as specified. No exceptions.
```typescript
// Spec: "Password MUST be at least 8 characters"
if (password.length < 8) {
  throw new ValidationError("Password must be at least 8 characters");
}
```

**MUST NOT / SHALL NOT**: Implement prevention explicitly.
```typescript
// Spec: "Session tokens MUST NOT be stored in localStorage"
// ✅ Use httpOnly cookies instead
// ❌ localStorage.setItem('token', token);
```

**SHOULD / RECOMMENDED**: Implement unless justified exception.
```typescript
// Spec: "Passwords SHOULD be checked against breach databases"
// Implement if feasible, document rationale if skipped
```

**MAY / OPTIONAL**: Implement based on value/effort assessment.

## Implementation Checklist

**Before Starting:**
- [ ] Read entire spec thoroughly
- [ ] Identify unclear or ambiguous sections
- [ ] Understand all acceptance criteria
- [ ] Identify dependencies and prerequisites
- [ ] Create requirement tracking matrix

**During Implementation:**
- [ ] Track which requirements are being addressed
- [ ] Follow spec language precisely (MUST vs SHOULD)
- [ ] Implement error handling as specified
- [ ] Write tests for each requirement
- [ ] Document any deviations from spec

**After Implementation:**
- [ ] Verify all MUST requirements implemented
- [ ] Verify SHOULD requirements addressed or documented
- [ ] Run all acceptance criteria tests
- [ ] Document any spec gaps discovered
- [ ] Log progress with test results

## Testing Strategy

**Unit Tests**: One per functional requirement
```typescript
describe("User Authentication", () => {
  // FR-1: User can log in with email and password
  it("authenticates user with valid credentials", async () => {
    // ...
  });

  // EC-1: Invalid credentials return 401
  it("returns 401 for invalid password", async () => {
    // ...
  });
});
```

**Integration Tests**: Verify end-to-end flows from spec
```typescript
describe("Login Flow (per spec section 3.2)", () => {
  it("completes full authentication flow", async () => {
    // Test entire flow as described in spec
  });
});
```

## Context Loading for Agents

When starting work on a feature, load context in this order:

1. **spec.md** - Understand what we're building
2. **plan.md** - Understand how we're building it
3. **Latest progress log** - Understand current state and handoff notes
4. **Current task** - Focus on the immediate work
5. **Relevant notes** - Additional context as needed

## Multi-Agent Coordination

When multiple agents work on a feature:

1. **Claim task** by setting status to `IN_PROGRESS`
2. **Read latest progress log** for handoff context
3. **Create new session log** when starting work
4. **Add notes** for decisions affecting other tasks
5. **Write handoff notes** before ending session
6. **Mark task DONE** when complete

Tasks declare dependencies explicitly:
```markdown
## Dependencies

**Blocked by**: [01-database-schema](01-database-schema.md)
**Blocks**: [04-api-endpoints](04-api-endpoints.md)
```

## Example: Implementing an API Endpoint

**Spec excerpt:**
```markdown
## POST /api/v1/tasks

### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Task title (1-255 chars) |
| priority | integer | No | 0-4, default 0 |

### Errors
- 400 INVALID_TITLE: Title missing or invalid length
- 400 INVALID_PRIORITY: Priority not in range 0-4
- 401 UNAUTHORIZED: Missing authentication
```

**Implementation:**
```typescript
// Validation schema derived from spec
const CreateTaskSchema = z.object({
  title: z.string().min(1).max(255),      // Per spec: 1-255 chars, required
  priority: z.number().int().min(0).max(4) // Per spec: 0-4
    .default(0),                           // Per spec: default 0
});

export async function createTask(req: Request, res: Response) {
  // FR: Authentication required (401 UNAUTHORIZED)
  if (!req.user) {
    return res.status(401).json({
      error: "UNAUTHORIZED",
      message: "Authentication required"
    });
  }

  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    const error = result.error.issues[0];

    // EC: 400 INVALID_TITLE
    if (error.path.includes("title")) {
      return res.status(400).json({
        error: "INVALID_TITLE",
        message: "Title must be 1-255 characters"
      });
    }

    // EC: 400 INVALID_PRIORITY
    if (error.path.includes("priority")) {
      return res.status(400).json({
        error: "INVALID_PRIORITY",
        message: "Priority must be between 0 and 4"
      });
    }
  }

  const task = await db.tasks.create({
    ...result.data,
    userId: req.user.id,
  });

  return res.status(201).json({
    id: task.id,
    title: task.title,
    createdAt: task.createdAt.toISOString(),
  });
}
```

**Tracking:**
```markdown
| Req | Description | Status | Location |
|-----|-------------|--------|----------|
| FR-1 | Accept title 1-255 chars | ✅ | CreateTaskSchema.title |
| FR-2 | Priority 0-4, default 0 | ✅ | CreateTaskSchema.priority |
| EC-1 | 400 INVALID_TITLE | ✅ | Line 15 |
| EC-2 | 400 INVALID_PRIORITY | ✅ | Line 22 |
| EC-3 | 401 UNAUTHORIZED | ✅ | Line 8 |
```

## Handling Spec Ambiguity

When specs are unclear, document decisions:

```typescript
/**
 * Send registration confirmation email.
 *
 * Spec: "Users SHOULD receive a confirmation email"
 * Decision: Implemented as fire-and-forget to not block registration.
 * Rationale: SHOULD = best effort, registration shouldn't fail if email fails.
 *
 * TODO: Spec needs clarification on retry policy.
 */
async function sendConfirmationEmail(user: User): Promise<void> {
  try {
    await emailService.send({ to: user.email, template: "confirmation" });
  } catch (error) {
    // Decision: Log but don't fail registration (SHOULD vs MUST)
    logger.warn("Failed to send confirmation email", { userId: user.id });
  }
}
```

## Progress Report Format

When reporting implementation progress:

```markdown
## Implementation Progress

### Completed
- [x] FR-1: User registration (src/auth/register.ts)
- [x] FR-2: Email validation (src/auth/validators.ts)

### In Progress
- [ ] FR-3: OAuth integration
  - Google: ✅ Complete
  - GitHub: 🔄 In progress

### Blocked
- [ ] FR-4: Email verification
  - Blocked on: Email service configuration

### Spec Clarifications Needed
1. FR-3: Which OAuth scopes are required?
2. NFR-1: Is 200ms latency for P95 or P99?

### Deviations from Spec
1. FR-2: Added additional email format validation beyond spec
   - Rationale: Spec's regex pattern allowed invalid TLDs
```

## Common Pitfalls

**Partial Implementation**: Implementing only the happy path while ignoring specified error conditions. Always implement error handling as specified.

**Over-Implementation**: Adding features not in the spec. Stick to what's specified unless discussed.

**Specification Drift**: Not updating the spec when implementation reveals issues. Keep specs and code in sync.

**Missing Traceability**: Not documenting which code implements which requirements. Use comments and tracking matrices.

## Resources

- **Templates**: See `templates/` directory for artifact templates
- **Advanced Patterns**: See `references/artifact_patterns.md`

## Related Skills

- **spec-writing**: Create feature specifications
- **plan-writing**: Create implementation plans
- **task-writing**: Break plans into actionable tasks
- **progress-writing**: Document session progress and handoffs

## Version

- **Created**: 2025-01-18
- **Last Updated**: 2025-01-19
- **Version**: 2.0.0

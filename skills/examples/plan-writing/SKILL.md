---
name: plan-writing
description: Write high-quality implementation plans that break down complex work into clear, actionable steps with identified risks and dependencies. Use when breaking down feature specs, planning refactoring or migration efforts, coordinating work across components, identifying technical risks, or creating roadmaps for complex changes. Triggers include "implementation plan", "write plan", "plan feature", "break down work", "technical planning", or when transforming requirements into concrete implementation steps.
---

# Plan Writing Skill

Write high-quality implementation plans that break down complex work into clear, actionable steps with identified risks and dependencies.

## Overview

This skill guides Claude through creating detailed implementation plans that bridge the gap between specifications and code. A well-written plan transforms requirements into a concrete sequence of work, identifies technical approaches, surfaces risks early, and provides clear checkpoints for progress tracking.

## When to Use

- Breaking down a feature spec into implementation steps
- Planning a refactoring or migration effort
- Coordinating work across multiple components or teams
- Identifying technical risks before implementation
- Creating a roadmap for complex changes
- Preparing for code review by documenting approach
- Onboarding others to understand planned changes

## Prerequisites

- A specification or clear understanding of requirements
- Familiarity with the target codebase and architecture
- Knowledge of available tools, libraries, and patterns
- Understanding of team constraints and conventions

## Instructions

### Plan Writing Process

1. **Analyze the Scope**
   - What are the inputs? (spec, requirements, goals)
   - What are the deliverables?
   - What systems/components are affected?
   - What is the blast radius of changes?

2. **Explore the Codebase**
   - Identify files that need modification
   - Understand existing patterns to follow
   - Find reusable code and utilities
   - Map dependencies between components

3. **Design the Approach**
   - Choose technical strategies
   - Identify architectural decisions
   - Consider alternative approaches
   - Document trade-offs

4. **Break Down into Steps**
   - Create atomic, completable tasks
   - Order by dependencies
   - Identify parallelizable work
   - Define clear completion criteria

5. **Identify Risks and Mitigations**
   - Technical risks (complexity, unknowns)
   - Integration risks (breaking changes)
   - Performance risks
   - Security considerations

6. **Define Checkpoints**
   - Testable milestones
   - Review points
   - Rollback strategies
   - Success metrics

### Step Decomposition Guidelines

**Good Steps Are:**
- **Atomic**: Can be completed in one focused session
- **Testable**: Has clear completion criteria
- **Independent**: Minimal dependencies on incomplete work
- **Ordered**: Prerequisites come first
- **Sized appropriately**: Not too large, not too granular

**Step Sizing:**
| Too Large | Right Size | Too Small |
|-----------|------------|-----------|
| "Implement authentication" | "Add JWT token generation endpoint" | "Import jwt library" |
| "Build the API" | "Create user CRUD endpoints" | "Add GET route" |
| "Refactor the codebase" | "Extract validation logic to shared module" | "Rename variable" |

### Dependency Mapping

Identify and document dependencies between steps:

```
Step 1: Create database schema
    ↓
Step 2: Implement data access layer ──────┐
    ↓                                      │
Step 3: Add API endpoints ←────────────────┤
    ↓                                      │
Step 4: Write integration tests ←──────────┘
    ↓
Step 5: Add frontend components (parallel with Step 4)
```

### Risk Assessment Matrix

For each identified risk:

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Database migration fails | Medium | High | Test on staging first, prepare rollback script |
| API breaks existing clients | Low | High | Version the API, maintain backwards compatibility |
| Performance regression | Medium | Medium | Add performance tests, benchmark before/after |

### Plan Quality Checklist

**Completeness**
- [ ] All spec requirements mapped to steps
- [ ] Dependencies identified and ordered
- [ ] Risks documented with mitigations
- [ ] Success criteria defined
- [ ] Rollback strategy included

**Clarity**
- [ ] Each step has clear deliverable
- [ ] Technical approach explained
- [ ] Files to modify identified
- [ ] No ambiguous language

**Feasibility**
- [ ] Steps are appropriately sized
- [ ] Technical approach is validated
- [ ] Constraints acknowledged
- [ ] Resources/tools identified

**Traceability**
- [ ] Steps linked to spec requirements
- [ ] Rationale documented for decisions
- [ ] Alternative approaches noted

## Examples

### Example 1: Feature Implementation Plan

**Spec Summary:** Add user notification preferences with email and push notification settings.

**Plan:**

```markdown
# Implementation Plan: User Notification Preferences

## Overview
Add notification preferences to user profiles, allowing users to configure
email and push notification settings per notification type.

## Affected Components
- Database: `users` table, new `notification_preferences` table
- Backend: User service, Notification service
- API: New endpoints under `/api/v1/users/{id}/preferences`
- Frontend: Settings page, preference toggle components

## Technical Approach
- Store preferences in separate table (not JSON column) for queryability
- Use optimistic UI updates with rollback on failure
- Cache preferences in Redis with 5-minute TTL

## Implementation Steps

### Phase 1: Database Layer
**Step 1.1: Create notification_preferences table**
- Files: `migrations/20240115_notification_preferences.sql`
- Deliverable: Migration script with table, indexes, foreign keys
- Criteria: Migration runs successfully, rollback tested
- Links to: FR-1 (store preferences)

**Step 1.2: Add preference repository**
- Files: `src/repositories/notificationPreferenceRepository.ts`
- Deliverable: CRUD operations for preferences
- Criteria: Unit tests pass, handles missing preferences gracefully
- Links to: FR-1, FR-2

### Phase 2: API Layer
**Step 2.1: Create GET preferences endpoint**
- Files: `src/routes/users.ts`, `src/controllers/preferencesController.ts`
- Deliverable: GET /api/v1/users/{id}/preferences returns preferences
- Criteria: Returns 200 with preferences, 404 for unknown user
- Dependencies: Step 1.2
- Links to: FR-3

**Step 2.2: Create PUT preferences endpoint**
- Files: `src/routes/users.ts`, `src/controllers/preferencesController.ts`
- Deliverable: PUT endpoint updates preferences
- Criteria: Returns 200 on success, validates input, returns 400 for invalid data
- Dependencies: Step 2.1
- Links to: FR-4

**Step 2.3: Add caching layer**
- Files: `src/services/preferenceCacheService.ts`
- Deliverable: Redis caching with invalidation on update
- Criteria: Cache hit rate > 80%, preferences update reflected within 5 min
- Dependencies: Step 2.2
- Links to: NFR-1 (performance)

### Phase 3: Frontend
**Step 3.1: Create preference toggle component**
- Files: `src/components/PreferenceToggle.tsx`
- Deliverable: Reusable toggle with optimistic updates
- Criteria: Accessible, shows loading state, handles errors
- Dependencies: None (can parallel with Phase 2)
- Links to: FR-5

**Step 3.2: Add preferences section to settings page**
- Files: `src/pages/Settings.tsx`
- Deliverable: Preferences UI integrated into settings
- Criteria: Loads preferences, saves changes, shows success/error feedback
- Dependencies: Step 2.2, Step 3.1
- Links to: FR-5, FR-6

### Phase 4: Testing & Validation
**Step 4.1: Integration tests**
- Files: `tests/integration/preferences.test.ts`
- Deliverable: API integration tests
- Criteria: All endpoints tested, error cases covered
- Dependencies: Phase 2

**Step 4.2: E2E tests**
- Files: `tests/e2e/settings.spec.ts`
- Deliverable: User flow tests
- Criteria: Happy path and error scenarios tested
- Dependencies: Phase 3

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Migration on large users table slow | Medium | Medium | Run during low-traffic window, test on prod-size data |
| Cache invalidation race condition | Low | Medium | Use cache-aside pattern, accept eventual consistency |
| Breaking existing preference consumers | Low | High | Check for existing preference reads, add backwards compat |

## Rollback Strategy
1. API: Feature flag to disable new endpoints
2. Database: Down migration removes table (no data loss if new)
3. Frontend: Feature flag hides preferences UI

## Success Metrics
- [ ] All spec requirements implemented and tested
- [ ] API latency P95 < 100ms (with caching)
- [ ] No increase in error rate post-deployment
- [ ] Preferences sync correctly across sessions
```

### Example 2: Refactoring Plan

**Goal:** Extract authentication logic from monolithic service into dedicated auth module.

**Plan:**

```markdown
# Implementation Plan: Auth Module Extraction

## Overview
Extract authentication logic from UserService into dedicated AuthService
to improve separation of concerns and enable future auth provider changes.

## Current State Analysis
- Auth logic mixed with user CRUD in `src/services/userService.ts` (450 lines)
- JWT handling scattered across 3 files
- Password hashing duplicated in 2 places
- Session management tightly coupled to user model

## Target Architecture
```
src/
├── services/
│   ├── authService.ts       # New: Auth operations
│   ├── sessionService.ts    # New: Session management
│   └── userService.ts       # Reduced: User CRUD only
├── utils/
│   ├── jwt.ts              # Consolidated JWT utilities
│   └── password.ts         # Consolidated password utilities
```

## Implementation Steps

### Phase 1: Create Foundation (No behavior change)
**Step 1.1: Create password utility module**
- Extract: `hashPassword`, `verifyPassword` from userService.ts, authHelpers.ts
- Files: Create `src/utils/password.ts`
- Criteria: All existing tests pass, no behavior change
- Risk: Low - pure extraction

**Step 1.2: Create JWT utility module**
- Extract: `generateToken`, `verifyToken`, `decodeToken`
- Files: Create `src/utils/jwt.ts`
- Criteria: All existing tests pass, no behavior change
- Risk: Low - pure extraction

**Step 1.3: Update imports in existing code**
- Files: Update all files importing auth utilities
- Criteria: No behavior change, all tests pass
- Dependencies: Steps 1.1, 1.2

### Phase 2: Extract Services
**Step 2.1: Create AuthService shell**
- Files: Create `src/services/authService.ts`
- Deliverable: Empty service with dependency injection setup
- Criteria: Service instantiates, no functionality yet

**Step 2.2: Move login logic**
- Move: `login`, `validateCredentials` to AuthService
- Files: `authService.ts`, update `userService.ts`
- Criteria: Login flow works, all auth tests pass
- Dependencies: Step 2.1
- Risk: Medium - core functionality

**Step 2.3: Move registration auth logic**
- Move: Password hashing during registration to AuthService
- Files: `authService.ts`, `userService.ts`
- Criteria: Registration works, passwords hashed correctly
- Dependencies: Step 2.2

**Step 2.4: Create SessionService**
- Move: Session creation, validation, refresh logic
- Files: Create `src/services/sessionService.ts`
- Criteria: Sessions work, refresh tokens function
- Dependencies: Step 2.2
- Risk: Medium - session handling is critical

### Phase 3: Clean Up
**Step 3.1: Remove auth code from UserService**
- Files: `userService.ts`
- Criteria: UserService only contains user CRUD
- Dependencies: Phase 2 complete

**Step 3.2: Update all consumers**
- Files: Controllers, middleware, tests
- Criteria: All code uses new service locations
- Dependencies: Step 3.1

**Step 3.3: Add integration tests for new services**
- Files: `tests/services/authService.test.ts`, `tests/services/sessionService.test.ts`
- Criteria: 90%+ coverage on new services

## Verification Checkpoints
After each phase:
1. All existing tests pass
2. Manual smoke test of auth flows
3. No new eslint warnings
4. Bundle size not significantly increased

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking auth during extraction | High | Feature flag to fallback to old code path |
| Missing edge case in extraction | Medium | Comprehensive test coverage before starting |
| Circular dependency introduced | Low | Strict dependency direction, DI container |

## Rollback Strategy
- Each step is a separate commit
- Feature flag allows switching between old/new auth paths
- Can revert individual commits if issues found
```

### Example 3: Migration Plan

**Goal:** Migrate from REST API to GraphQL for mobile clients.

**Plan:**

```markdown
# Implementation Plan: GraphQL Migration

## Overview
Add GraphQL API alongside existing REST for mobile clients while
maintaining REST for web and third-party integrations.

## Strategy: Strangler Fig Pattern
- Add GraphQL layer that calls existing services
- Migrate endpoints incrementally
- Keep REST operational throughout
- No big-bang cutover

## Implementation Steps

### Phase 1: Infrastructure
**Step 1.1: Add GraphQL dependencies**
- Add: apollo-server, graphql, type-graphql
- Files: package.json, tsconfig.json
- Criteria: Dependencies installed, TypeScript configured

**Step 1.2: Create GraphQL server setup**
- Files: `src/graphql/server.ts`, `src/graphql/context.ts`
- Deliverable: Apollo Server integrated with Express
- Criteria: GraphQL playground accessible at /graphql

**Step 1.3: Add authentication middleware**
- Files: `src/graphql/middleware/auth.ts`
- Deliverable: Auth context from JWT
- Criteria: Queries receive authenticated user context

### Phase 2: Schema & Resolvers (User Domain)
**Step 2.1: Define User type and queries**
- Files: `src/graphql/schema/user.ts`, `src/graphql/resolvers/user.ts`
- Deliverable: User type, me query, user query
- Criteria: Matches REST response shape, tests pass

**Step 2.2: Add User mutations**
- Files: `src/graphql/resolvers/user.ts`
- Deliverable: updateProfile, updatePreferences mutations
- Criteria: Mutations work, validation matches REST

### Phase 3: Schema & Resolvers (Task Domain)
**Step 3.1: Define Task types and queries**
- Files: `src/graphql/schema/task.ts`, `src/graphql/resolvers/task.ts`
- Deliverable: Task type, tasks query with filtering
- Criteria: Pagination works, filters match REST

**Step 3.2: Add Task mutations**
- Deliverable: createTask, updateTask, deleteTask
- Criteria: All CRUD operations work

**Step 3.3: Add Task subscriptions**
- Files: `src/graphql/subscriptions/task.ts`
- Deliverable: Real-time task updates
- Criteria: Subscriptions fire on mutations

### Phase 4: Mobile Client Migration
**Step 4.1: Update mobile API client**
- Coordinate with mobile team
- Criteria: Mobile app uses GraphQL for migrated endpoints

**Step 4.2: Monitor and validate**
- Add GraphQL-specific metrics
- Criteria: Error rate matches REST, latency acceptable

### Phase 5: Optimization
**Step 5.1: Add DataLoader for N+1 prevention**
- Files: `src/graphql/dataloaders/`
- Criteria: No N+1 queries in common operations

**Step 5.2: Add query complexity limits**
- Criteria: Malicious queries rejected

## Parallel Workstreams
- Phase 2 and 3 can run in parallel
- Mobile team can start Phase 4 once Phase 2 complete

## Success Criteria
- [ ] Mobile app fully migrated to GraphQL
- [ ] REST API unchanged and functional
- [ ] GraphQL latency within 20% of REST
- [ ] No increase in error rates
- [ ] Query complexity limits prevent abuse
```

## Best Practices

### Do's
- Start with codebase exploration before planning
- Break work into testable, reviewable chunks
- Identify risks early and plan mitigations
- Include rollback strategies for risky changes
- Link steps to spec requirements for traceability
- Consider parallel workstreams where possible
- Define clear completion criteria for each step

### Don'ts
- Don't plan in isolation - validate technical approach
- Don't make steps too large or too granular
- Don't ignore dependencies between steps
- Don't skip risk assessment
- Don't assume everything will go as planned
- Don't forget about testing and validation steps

## Common Pitfalls

### Underestimating Dependencies
Failing to identify hidden dependencies leads to blocked work. Map dependencies explicitly and order steps accordingly.

### Missing the Exploration Phase
Jumping straight to planning without understanding the codebase leads to unrealistic plans. Always explore first.

### Over-Planning
Creating excessively detailed plans for uncertain work. Use progressive elaboration - detail near-term work, outline later phases.

### Ignoring Rollback
Not planning for failure. Every significant change should have a rollback strategy.

### Scope Creep in Steps
Letting steps grow beyond their original scope. Keep steps atomic and create new steps for additions.

## Output Format

Structure plans consistently:

```markdown
# Implementation Plan: [Feature/Change Name]

## Overview
[Brief description of what this plan covers]

## Affected Components
[List of systems, services, files affected]

## Technical Approach
[High-level strategy and key decisions]

## Implementation Steps

### Phase 1: [Phase Name]
**Step 1.1: [Step Name]**
- Files: [Files to create/modify]
- Deliverable: [What this step produces]
- Criteria: [How we know it's done]
- Dependencies: [Prerequisites]
- Links to: [Spec requirements]
- Risk: [Low/Medium/High - brief note]

### Phase 2: [Phase Name]
...

## Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | ... | ... | ... |

## Rollback Strategy
[How to undo changes if needed]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

---
Plan Version: 1.0
Author: [Name]
Last Updated: [Date]
Status: [Draft | Review | Approved | In Progress | Complete]
```

## Limitations

- Plans require codebase knowledge to be accurate
- Cannot predict all implementation challenges
- Plans may need revision as work progresses
- Technical feasibility should be validated before finalizing

## Related Skills

- **Spec Writing**: Create specifications that plans implement
- **Spec-Driven Development**: Execute plans systematically
- **Code Review**: Validate implementation matches plan

## Compatibility

- **Claude Models**: All Claude 3+ models
- **Interfaces**: Claude.ai, API, Claude Code
- **Minimum API Version**: Any

## Author

Claude Toolkit Community

## Version

- **Created**: 2025-01-18
- **Last Updated**: 2025-01-18
- **Version**: 1.0.0

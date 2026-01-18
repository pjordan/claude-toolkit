# Notes Writing Skill

Write clear development notes that document what was built, decisions made, and verification performed.

## Overview

This skill guides Claude through creating development notes - the documentation produced alongside completed work that captures the story of implementation. Notes bridge the gap between "task done" and "work understood" by recording decisions, trade-offs, deviations, and verification in a lightweight but valuable format.

Development notes serve future readers (including your future self) who need to understand not just *what* was built, but *why* it was built that way.

## When to Use

- Completing a task or set of related tasks
- Closing out a feature implementation
- Documenting decisions made during development
- Recording deviations from the original plan
- Capturing verification and testing performed
- Noting follow-up work identified during implementation
- Creating context for code reviewers
- Building institutional knowledge

## Prerequisites

- Completed or in-progress implementation work
- Access to the original spec, plan, and tasks (if applicable)
- Understanding of decisions made during development
- Knowledge of verification performed

## Instructions

### Notes Anatomy

Development notes capture the essential story of implementation:

```
┌─────────────────────────────────────────────────────┐
│  Summary                                            │
│  What was built in 1-2 sentences                    │
├─────────────────────────────────────────────────────┤
│  Requirements Addressed                             │
│  • Which spec requirements were implemented         │
│  • Mapping to acceptance criteria                   │
├─────────────────────────────────────────────────────┤
│  Approach                                           │
│  • What approach was taken                          │
│  • Key technical decisions                          │
│  • Alternatives considered and why rejected         │
├─────────────────────────────────────────────────────┤
│  Deviations                                         │
│  • Changes from original plan                       │
│  • Spec clarifications discovered                   │
│  • Scope adjustments                                │
├─────────────────────────────────────────────────────┤
│  Verification                                       │
│  • How correctness was verified                     │
│  • Tests added                                      │
│  • Manual testing performed                         │
├─────────────────────────────────────────────────────┤
│  Follow-ups                                         │
│  • Technical debt introduced                        │
│  • Future improvements identified                   │
│  • Open questions                                   │
└─────────────────────────────────────────────────────┘
```

### Notes Writing Process

1. **Summarize the Work**
   - What was built or changed?
   - What problem does it solve?
   - Keep it brief - 1-2 sentences

2. **Map to Requirements**
   - Which spec requirements were addressed?
   - Which acceptance criteria were met?
   - Note any requirements deferred or descoped

3. **Document the Approach**
   - What technical approach was taken?
   - What were the key decisions?
   - What alternatives were considered?
   - Why was this approach chosen?

4. **Record Deviations**
   - What changed from the original plan?
   - What spec ambiguities were discovered?
   - What scope changes occurred?
   - Why were these changes made?

5. **Describe Verification**
   - What tests were added?
   - What manual testing was performed?
   - How was correctness confirmed?
   - What edge cases were verified?

6. **Identify Follow-ups**
   - What technical debt was introduced?
   - What improvements were deferred?
   - What questions remain open?
   - What should be revisited?

### Summary Writing Guidelines

The summary should answer "What did you build?" in 1-2 sentences.

**Good Summaries:**
```
Added GET and PUT endpoints for user notification preferences with
Redis caching and input validation.
```

```
Fixed session expiration handling to show clear error messages and
preserve form state across the login redirect.
```

```
Extracted JWT utilities from AuthService into a dedicated module
to improve testability and reusability.
```

**Poor Summaries:**
```
Did the task.
```

```
Implemented the feature as described in the spec with all the
requirements and acceptance criteria met including the edge cases
and error handling and tests... [continues for 200 words]
```

### Documenting Decisions

Decisions are the most valuable part of development notes. They answer the question future readers will have: "Why was it done this way?"

**Decision Documentation Format:**

```markdown
### Decision: [What was decided]

**Context:** [Situation that required a decision]

**Options Considered:**
1. [Option A] - [Brief description]
2. [Option B] - [Brief description]

**Choice:** [Option chosen]

**Rationale:** [Why this option was selected]
```

**Example:**

```markdown
### Decision: Store preferences in separate table vs JSON column

**Context:** Needed to persist user notification preferences. Could
store as JSON blob in users table or normalized in separate table.

**Options Considered:**
1. JSON column in users table - simpler schema, flexible structure
2. Separate preferences table - queryable, type-safe, normalized

**Choice:** Separate preferences table

**Rationale:** Need to query preferences across users for admin
reporting. JSON columns would require parsing in application code.
The schema is stable enough that flexibility isn't needed.
```

### Recording Deviations

Deviations aren't failures - they're natural adjustments as implementation meets reality. Document them honestly.

**Types of Deviations:**

| Type | Example |
|------|---------|
| Plan change | "Implemented caching in Phase 1 instead of Phase 2 due to performance issues discovered early" |
| Spec clarification | "Spec said 'validate email' - clarified with PM to mean format validation only, not deliverability" |
| Scope adjustment | "Deferred dark mode for system preference detection to follow-up task" |
| Technical pivot | "Switched from polling to WebSockets after discovering existing WebSocket infrastructure" |

**Deviation Documentation Format:**

```markdown
### Deviation: [What changed]

**Original:** [What was planned]
**Actual:** [What was implemented]
**Reason:** [Why the change was made]
**Impact:** [Effect on timeline, scope, or quality]
```

### Verification Documentation

Document how you confirmed the work is correct. This helps reviewers and provides a testing record.

**Verification Categories:**

```markdown
## Verification

### Automated Tests
- Added unit tests for PreferenceValidator (12 test cases)
- Added integration tests for preference endpoints (GET, PUT, error cases)
- All existing auth tests continue to pass

### Manual Testing
- Verified preference toggle updates reflect in UI immediately
- Confirmed cache invalidation on preference update
- Tested with user having no existing preferences (defaults applied)
- Tested concurrent updates from multiple tabs

### Edge Cases Verified
- [x] User with no existing preferences gets defaults
- [x] Invalid preference values rejected with 400
- [x] Updating non-existent user returns 404
- [x] Cache miss falls back to database correctly
```

### Follow-up Documentation

Capture work that should happen later but wasn't in scope for this task.

**Follow-up Categories:**

| Category | Example |
|----------|---------|
| Technical debt | "Used string literals for preference types - should extract to enum" |
| Future improvements | "Could add bulk preference update endpoint for admin use" |
| Open questions | "Should preferences sync across devices? Deferred to PM decision" |
| Related work | "Notification service needs update to read from new preferences table" |

**Format:**

```markdown
## Follow-ups

### Technical Debt
- [ ] Extract preference type literals to shared enum (#next-sprint)
- [ ] Add database index on preferences.updated_at for reporting queries

### Future Improvements
- [ ] Bulk preference update endpoint for admin dashboard
- [ ] Preference change history/audit log

### Open Questions
- Should preferences sync across devices? (Awaiting PM input)
- Rate limiting for preference updates? (Not specified in requirements)

### Related Work
- #234: Update notification service to use new preferences table
- #235: Add preferences section to user export
```

### Notes Length Guidelines

Notes should be proportional to the work's complexity and importance.

| Work Type | Notes Length | Focus |
|-----------|--------------|-------|
| Simple bug fix | 3-5 lines | Root cause, fix, verification |
| Single task | Half page | Summary, approach, verification |
| Multi-task feature | 1-2 pages | Full format with decisions and deviations |
| Complex refactoring | 1-2 pages | Detailed decisions and verification |
| Investigation/Spike | 1 page | Findings, recommendations, follow-ups |

**The Right Length Test:**
- Could someone understand the work from these notes? (Not too short)
- Is everything here necessary? (Not too long)

## Examples

### Example 1: Feature Implementation Notes

```markdown
# Development Notes: User Notification Preferences

## Summary
Implemented GET and PUT endpoints for user notification preferences
with Redis caching, input validation, and comprehensive test coverage.

## Requirements Addressed
| Requirement | Status | Notes |
|-------------|--------|-------|
| FR-1: Store preferences | ✓ | Separate table with foreign key to users |
| FR-2: Read preferences | ✓ | GET endpoint with caching |
| FR-3: Update preferences | ✓ | PUT endpoint with validation |
| FR-4: Default preferences | ✓ | Applied when no record exists |
| NFR-1: Response < 100ms | ✓ | P95 at 45ms with cache hit |

## Approach

### Architecture
- Created `notification_preferences` table with user_id foreign key
- Implemented repository pattern matching existing codebase style
- Added Redis cache layer with 5-minute TTL
- Used Zod for request validation (consistent with other endpoints)

### Key Decision: Cache Invalidation Strategy

**Context:** Needed to ensure preference updates reflect immediately
while maintaining cache performance benefits.

**Options Considered:**
1. Write-through cache - Update cache on every write
2. Cache invalidation - Delete cache entry on write, repopulate on read
3. Short TTL only - Let cache expire naturally (30 second TTL)

**Choice:** Cache invalidation (option 2)

**Rationale:** Write-through adds complexity and potential race conditions.
Short TTL alone would show stale data for 30 seconds after update, which
is noticeable in UI. Invalidation is simple and guarantees fresh reads.

## Deviations

### Deviation: Added audit logging (not in original spec)

**Original:** Spec didn't mention audit logging for preference changes
**Actual:** Added audit log entry on preference updates
**Reason:** Discovered existing audit pattern for user profile changes;
PM confirmed preferences should follow same pattern
**Impact:** Added 2 hours for audit integration and tests

### Deviation: Deferred preference categories

**Original:** Plan included preference categories (email, push, sms)
**Actual:** Implemented flat preference structure
**Reason:** PM clarified SMS preferences not needed for MVP
**Impact:** Simplified schema; categories can be added later if needed

## Verification

### Automated Tests
- `PreferenceRepository`: 8 unit tests (CRUD operations, error handling)
- `PreferenceValidator`: 12 unit tests (all validation rules, edge cases)
- `PreferencesController`: 6 unit tests (request handling, auth checks)
- Integration tests: 10 tests (full request/response cycle)
- Coverage: 94% on new code

### Manual Testing
- Verified UI toggle updates preferences correctly
- Confirmed immediate reflection of changes (no stale cache)
- Tested new user flow (defaults applied on first read)
- Tested concurrent updates from two browser tabs
- Verified 404 for non-existent user
- Confirmed 403 when updating another user's preferences

### Performance Verification
- Cache hit: P95 = 45ms, P99 = 62ms
- Cache miss: P95 = 89ms, P99 = 124ms
- Load test: 1000 req/s sustained without errors

## Follow-ups

### Technical Debt
- [ ] #267: Extract preference field names to constants
- [ ] #268: Add database index on updated_at for reporting

### Future Improvements
- [ ] Preference change notifications (email when preferences modified)
- [ ] Bulk preference management for admin users
- [ ] Preference export in user data download

### Related Work
- #269: Update notification service to read from preferences table
- #270: Add preferences to user settings UI (frontend)

---
Author: [Developer]
Date: 2025-01-18
Tasks Completed: #201, #202, #203, #204
Plan Reference: implementation-plan-notification-preferences.md
```

### Example 2: Bug Fix Notes

```markdown
# Development Notes: Fix Password Reset for Plus-Sign Emails

## Summary
Fixed password reset flow for email addresses containing + character
by updating email validation regex to comply with RFC 5321.

## Root Cause
The `validateEmail()` function in `src/utils/validation.ts` used a
regex that rejected + characters in the local part of email addresses.
This is valid per RFC 5321 but was being rejected, causing silent
failures in the password reset flow.

## Approach
Replaced custom regex with `validator` library's `isEmail()` function,
which properly implements RFC 5321 validation. This also handles other
edge cases we weren't covering (quoted strings, IP domain literals).

### Decision: Library vs Fixed Regex

**Options Considered:**
1. Fix the regex to allow + characters
2. Use established `validator` library

**Choice:** Use `validator` library

**Rationale:** Email validation is surprisingly complex. Our regex had
already failed once; likely has other bugs. The `validator` library is
well-tested and maintained. Small bundle size impact (12KB gzipped).

## Changes Made
- `src/utils/validation.ts`: Replaced `validateEmail()` implementation
- `src/utils/validation.test.ts`: Added test cases for special characters
- `package.json`: Added `validator` dependency

## Verification

### Automated Tests
Added test cases for:
- [x] Standard email (user@example.com)
- [x] Plus addressing (user+tag@example.com)
- [x] Dots in local part (first.last@example.com)
- [x] Hyphen in domain (user@my-company.com)
- [x] Subdomain (user@mail.example.com)
- [x] Invalid: missing @ symbol
- [x] Invalid: spaces in address
- [x] Invalid: double dots

### Manual Testing
- Verified password reset works for test+alias@gmail.com
- Confirmed existing valid emails still work
- Tested registration flow (uses same validation)
- Verified login flow (uses same validation)

## Follow-ups
- [ ] #312: Audit other regex validations for similar issues
- [ ] Consider: Add email deliverability check (nice-to-have)

---
Author: [Developer]
Date: 2025-01-18
Task: #298
Support Ticket: #4521
```

### Example 3: Refactoring Notes

```markdown
# Development Notes: Extract JWT Utilities from AuthService

## Summary
Extracted JWT handling logic from AuthService into dedicated
`src/utils/jwt.ts` module to improve testability and enable reuse.

## Requirements Addressed
This was a refactoring task with no functional requirements.
Goal: Improve code organization without behavior change.

## Approach

### Strategy: Strangler Fig
Extracted functions one at a time, updating imports incrementally,
running tests after each extraction to ensure no regressions.

### Extraction Order
1. `generateToken()` - No dependencies on AuthService state
2. `verifyToken()` - Only depends on config, easily extracted
3. `decodeToken()` - Pure function, trivial extraction
4. `getTokenExpiry()` - New helper extracted from inline logic

### Key Decision: Config Injection vs Import

**Context:** JWT functions need access to secret key and expiry config.
AuthService accessed these via `this.config`.

**Options Considered:**
1. Pass config as parameter to each function
2. Create JwtService class with injected config
3. Import config directly in jwt.ts module

**Choice:** Pass config as parameter

**Rationale:** Keeps functions pure and easily testable. No need for
DI container complexity. Config is already available at all call sites.
If we later need a stateful service, we can wrap these functions.

## Changes Made

| File | Change |
|------|--------|
| `src/utils/jwt.ts` | Created with extracted functions |
| `src/utils/jwt.test.ts` | New unit tests (100% coverage) |
| `src/services/authService.ts` | Removed JWT logic, imports jwt utils |
| `src/services/authService.test.ts` | Updated to mock jwt module |
| `src/middleware/auth.ts` | Updated imports |

## Verification

### Behavior Preservation
- All 47 existing auth tests pass
- No changes to API responses
- No changes to token format or expiry
- Login/logout/refresh flows manually verified

### New Test Coverage
- `jwt.ts`: 100% coverage (24 test cases)
- Tests cover: valid tokens, expired tokens, malformed tokens,
  invalid signatures, missing claims

### Regression Testing
- Full E2E suite passed
- Load test showed no performance change

## Deviations

### Deviation: Added getTokenExpiry() helper

**Original:** Not in original plan
**Actual:** Extracted inline expiry calculation to named function
**Reason:** Found duplicated logic in two places during extraction
**Impact:** Cleaner code, no timeline impact

## Follow-ups

### Next Steps
- [ ] #305: Extract session logic to SessionService (Phase 2)
- [ ] #306: Extract password utilities to password.ts (Phase 3)

### Technical Debt
- [ ] AuthService still has 380 lines - continue extraction
- [ ] Consider: JWT refresh logic might belong in dedicated service

---
Author: [Developer]
Date: 2025-01-18
Tasks: #301, #302, #303
Refactoring Epic: #287
```

### Example 4: Investigation/Spike Notes

```markdown
# Development Notes: Investigate GraphQL Migration Feasibility

## Summary
Investigated feasibility of adding GraphQL API alongside REST for
mobile clients. Recommendation: Proceed with Apollo Server using
schema-first approach.

## Questions Answered

### Q1: Can we add GraphQL without disrupting REST?
**Answer:** Yes. Apollo Server integrates with Express alongside existing
routes. GraphQL would be available at `/graphql` while REST remains at
`/api/v1/*`. No changes required to existing endpoints.

### Q2: What's the performance impact?
**Answer:** Minimal. Apollo adds ~50ms cold start, negligible after warmup.
DataLoader pattern prevents N+1 queries. Initial testing shows GraphQL
responses within 10% of equivalent REST endpoints.

### Q3: Schema-first or code-first?
**Answer:** Recommend schema-first with code generation.
- Schema-first: Better for mobile team collaboration, generates types
- Code-first: Faster initial development, but schema is derived artifact
Mobile team prefers reviewing `.graphql` files over TypeScript decorators.

### Q4: How do we handle auth?
**Answer:** Use existing JWT middleware. Pass authenticated user via
Apollo context. Resolver-level auth checks using existing permission
utilities.

## Proof of Concept
Created branch `spike/graphql-poc` with:
- Apollo Server setup with Express integration
- User type and basic queries (me, user)
- Auth context from existing JWT middleware
- DataLoader for user preferences (N+1 prevention)

POC demonstrates:
- ✓ Coexistence with REST routes
- ✓ Auth integration
- ✓ Type generation from schema
- ✓ DataLoader pattern

## Recommendations

### Recommended Approach
1. Schema-first with `graphql-codegen` for TypeScript types
2. Apollo Server 4 with Express integration
3. Strangler fig migration (keep REST, add GraphQL incrementally)
4. Start with read-only queries, add mutations in phase 2

### Not Recommended
- Full migration (too risky, breaks existing clients)
- Code-first approach (mobile team preference for schema files)
- Subscriptions in phase 1 (adds complexity, not immediately needed)

## Risks Identified

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Schema/REST drift | Medium | Generate REST types from GraphQL schema |
| N+1 queries | High | DataLoader required from start |
| Over-fetching in resolvers | Medium | Field-level resolvers, not eager loading |

## Follow-ups

### If Proceeding
- [ ] Create detailed implementation plan
- [ ] Define schema for user domain (first migration target)
- [ ] Set up graphql-codegen pipeline
- [ ] Coordinate with mobile team on timeline

### Open Questions for PM
- Target date for mobile GraphQL adoption?
- Which endpoints to prioritize for migration?
- Do we deprecate REST eventually or maintain indefinitely?

---
Author: [Developer]
Date: 2025-01-18
Task: #289
Time-box: 3 days (actual: 2.5 days)
POC Branch: spike/graphql-poc
```

## Best Practices

### Do's
- Write notes while the work is fresh in your mind
- Focus on decisions and rationale - the "why"
- Be honest about deviations and trade-offs
- Link to relevant specs, tasks, and code
- Keep length proportional to complexity
- Include enough context for future readers

### Don'ts
- Don't just repeat the task description
- Don't document every line of code changed
- Don't omit problems or challenges faced
- Don't write notes weeks after the work
- Don't skip verification documentation
- Don't forget follow-up items

## Common Pitfalls

### Too Brief
Notes that just say "Done" or "Implemented as specified" provide no value. Always include approach and key decisions.

### Too Verbose
Notes don't need to explain every line of code. Focus on decisions, deviations, and verification - things not obvious from the code itself.

### Missing the "Why"
Documenting *what* was done without *why* loses the most valuable information. Future readers can see the code; they can't see your reasoning.

### Waiting Too Long
Writing notes days or weeks after implementation leads to forgotten details. Write notes as you complete work, not in batches.

### Skipping Deviations
Pretending the plan was followed perfectly hides valuable learnings. Honest deviation documentation helps improve future planning.

## Notes Quality Checklist

Before finalizing notes, verify:

**Summary**
- [ ] Clear 1-2 sentence description of work done
- [ ] Would make sense to someone unfamiliar with the task

**Requirements**
- [ ] Spec requirements mapped to implementation
- [ ] Acceptance criteria addressed
- [ ] Deferred items noted

**Approach**
- [ ] Key technical decisions documented
- [ ] Alternatives considered and rationale captured
- [ ] Non-obvious implementation choices explained

**Deviations**
- [ ] Changes from plan documented
- [ ] Reasons for changes explained
- [ ] Impact noted

**Verification**
- [ ] Tests added/updated listed
- [ ] Manual testing described
- [ ] Edge cases covered

**Follow-ups**
- [ ] Technical debt identified
- [ ] Future improvements noted
- [ ] Related work linked

## Output Format

Use this template for consistent notes:

```markdown
# Development Notes: [Brief Title]

## Summary
[1-2 sentence description of what was built/changed]

## Requirements Addressed
| Requirement | Status | Notes |
|-------------|--------|-------|
| [FR/NFR-X]  | ✓/✗/Partial | [Brief note] |

## Approach
[Description of technical approach taken]

### Key Decision: [Decision Name]
**Context:** [Situation requiring decision]
**Options:** [What was considered]
**Choice:** [What was selected]
**Rationale:** [Why]

## Deviations
### Deviation: [What changed]
**Original:** [Planned approach]
**Actual:** [Implemented approach]
**Reason:** [Why changed]

## Verification
### Automated Tests
- [Tests added/updated]

### Manual Testing
- [Testing performed]

## Follow-ups
- [ ] [Follow-up item with task number if created]

---
Author: [Name]
Date: [Date]
Tasks: [Task numbers]
Spec: [Link to spec if applicable]
```

## Limitations

- Notes quality depends on writer's memory and diligence
- Cannot replace detailed code review
- May become outdated if work is later modified
- Value diminishes if not written promptly

## Related Skills

- **Spec Writing**: Create specifications that notes reference
- **Plan Writing**: Create plans that notes compare against
- **Task Writing**: Create tasks that notes document completion of
- **Spec-Driven Development**: Execute work that notes document

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

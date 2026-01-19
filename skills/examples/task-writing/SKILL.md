---
name: task-writing
description: Write high-quality, actionable tasks that are clear, well-scoped, and contain all the information needed for successful execution. Use when breaking down implementation plans, creating issues for bug fixes or features, writing tickets for sprints, defining work items from spec requirements, converting user feedback into tasks, or creating technical debt items. Triggers include "write task", "create issue", "write ticket", "define task", "bug report", "feature request", or when creating trackable units of work.
---

# Task Writing Skill

Write high-quality, actionable tasks that are clear, well-scoped, and contain all the information needed for successful execution.

## Overview

This skill guides Claude through creating individual tasks (issues, tickets, work items) that can be tracked in project management tools, issue trackers, or todo lists. Unlike implementation plans that describe the full journey, tasks are discrete units of work that can be assigned, estimated, and completed independently.

A well-written task bridges the gap between high-level plans and actual implementation by providing just enough context, clear acceptance criteria, and appropriate scope for a single focused work session.

## When to Use

- Breaking down implementation plans into trackable work items
- Creating issues for bug fixes or feature requests
- Writing tickets for a sprint or kanban board
- Defining work items from spec requirements
- Converting user feedback into actionable tasks
- Creating technical debt or refactoring tasks
- Writing tasks for code review findings
- Preparing backlog items for prioritization

## Prerequisites

- Clear understanding of the work to be done
- Context about the codebase and existing patterns
- Knowledge of team conventions for task structure
- Access to relevant specs or requirements (if applicable)

## Instructions

### Task Anatomy

Every well-written task contains these elements:

```
┌─────────────────────────────────────────────────────┐
│  Title                                              │
│  [Action verb] + [What] + [Context/Scope]           │
├─────────────────────────────────────────────────────┤
│  Description                                        │
│  • Background/Context (Why this matters)            │
│  • Current State (What exists now)                  │
│  • Desired State (What should exist after)          │
├─────────────────────────────────────────────────────┤
│  Acceptance Criteria                                │
│  • Testable conditions for completion               │
│  • Edge cases to handle                             │
│  • What "done" looks like                           │
├─────────────────────────────────────────────────────┤
│  Technical Notes (Optional)                         │
│  • Implementation hints                             │
│  • Files likely affected                            │
│  • Related code or patterns to follow               │
├─────────────────────────────────────────────────────┤
│  Metadata                                           │
│  • Links to spec/requirements                       │
│  • Dependencies/Blockers                            │
│  • Labels/Tags                                      │
└─────────────────────────────────────────────────────┘
```

### Task Writing Process

1. **Understand the Work**
   - What problem does this solve?
   - Who benefits from this work?
   - What is the smallest valuable increment?
   - What are the boundaries of this task?

2. **Craft the Title**
   - Start with an action verb
   - Be specific about what and where
   - Keep it scannable (under 80 characters)
   - Avoid vague words like "improve," "fix," "update" alone

3. **Write the Description**
   - Provide context a new team member would need
   - Explain the current state and problem
   - Describe the desired outcome
   - Keep it concise but complete

4. **Define Acceptance Criteria**
   - Write testable, verifiable conditions
   - Include both positive and negative cases
   - Specify edge cases that must be handled
   - Make "done" unambiguous

5. **Add Technical Context**
   - Point to relevant files or code
   - Reference patterns to follow
   - Note potential gotchas
   - Keep implementation details minimal (don't over-specify)

6. **Set Metadata**
   - Link to parent spec or epic
   - Identify blockers and dependencies
   - Add appropriate labels
   - Estimate if your process requires it

### Title Writing Guidelines

**Structure:** `[Verb] [what] [where/context]`

| Bad Title | Good Title | Why It's Better |
|-----------|------------|-----------------|
| Fix login bug | Fix session expiration not redirecting to login page | Specific about what and where |
| Update API | Add rate limiting to /api/v1/search endpoint | Clear scope and action |
| Improve performance | Add database index for user lookup by email | Actionable and specific |
| User preferences | Implement preference toggle component | Action verb, clear deliverable |
| Tests | Add unit tests for PasswordValidator class | Specific target |

**Power Verbs for Tasks:**

| Category | Verbs |
|----------|-------|
| Creation | Add, Create, Implement, Build, Write |
| Modification | Update, Refactor, Migrate, Convert, Replace |
| Fixes | Fix, Resolve, Handle, Correct |
| Removal | Remove, Delete, Deprecate, Clean up |
| Investigation | Investigate, Research, Spike, Explore |
| Documentation | Document, Add docs for, Write README for |
| Testing | Add tests for, Test, Validate, Verify |

### Description Structure

**The Why-What-How Framework:**

```markdown
## Background
[Why does this task exist? What problem does it solve? Who requested it?]

## Current State
[What exists today? What's wrong or missing?]

## Desired Outcome
[What should exist after this task is complete?]
```

**Example:**

```markdown
## Background
Users are reporting confusion when their session expires during form
submission. Currently, the form data is lost and users see a generic
error. This is causing support tickets and user frustration.

## Current State
When a session expires mid-action:
- API returns 401 Unauthorized
- Frontend shows "Something went wrong" toast
- Form data is lost
- User must manually navigate to login

## Desired Outcome
When a session expires:
- User sees clear "Session expired" message
- User is redirected to login with return URL
- After login, user returns to their previous location
- Form state is preserved where possible
```

### Acceptance Criteria Guidelines

**Format Options:**

1. **Checklist Format** (Most common)
```markdown
## Acceptance Criteria
- [ ] Session expiration shows "Session expired" message (not generic error)
- [ ] User is redirected to /login with returnUrl parameter
- [ ] After successful login, user is redirected back to original page
- [ ] Form data in localStorage is restored after redirect
- [ ] Existing session refresh logic is not affected
```

2. **Given-When-Then Format** (For behavior-focused tasks)
```markdown
## Acceptance Criteria
**Given** a user is filling out a form
**When** their session expires and they submit
**Then** they see "Session expired, please log in" message
**And** they are redirected to login with the form URL as returnUrl

**Given** a user has just re-authenticated
**When** they had a returnUrl in their login request
**Then** they are redirected to that URL after login
```

3. **Requirements Format** (For spec-linked tasks)
```markdown
## Acceptance Criteria
- FR-1: Display session expiration message ✓ when 401 received
- FR-2: Preserve returnUrl through login flow
- FR-3: Restore form state from localStorage after redirect
- NFR-1: Redirect latency < 100ms
```

**Criteria Quality Checklist:**
- Is each criterion independently testable?
- Are edge cases explicitly addressed?
- Is the success condition unambiguous?
- Could someone verify completion without asking questions?

### Scoping Tasks Correctly

**The Goldilocks Principle:**

| Too Small | Just Right | Too Large |
|-----------|------------|-----------|
| "Add import statement" | "Add JWT validation middleware" | "Implement authentication" |
| "Create empty file" | "Create UserPreference model with migrations" | "Build user management" |
| "Write one test" | "Add unit tests for TokenService" | "Write all tests" |

**Signs a Task is Too Large:**
- Contains "and" multiple times
- Has more than 5-7 acceptance criteria
- Would take more than 1-2 days
- Touches more than 3-4 files
- Has multiple independent deliverables

**Signs a Task is Too Small:**
- Could be combined with related work
- Setup/teardown exceeds actual work
- Not independently valuable
- Would create noisy commit history

**Splitting Large Tasks:**

```
❌ "Implement user notification preferences"

✅ Split into:
1. "Create notification_preferences database table"
2. "Add NotificationPreference model and repository"
3. "Create GET /preferences API endpoint"
4. "Create PUT /preferences API endpoint"
5. "Add preference caching with Redis"
6. "Build preference toggle UI component"
7. "Integrate preferences into settings page"
```

### Technical Notes Best Practices

**What to Include:**
- Files likely to be modified
- Existing patterns to follow
- Potential gotchas or tricky areas
- Related code to reference

**What to Avoid:**
- Step-by-step implementation instructions
- Specific code to write (unless critical)
- Over-constraining the solution
- Duplicating information from specs

**Good Example:**
```markdown
## Technical Notes
- Follow existing validation pattern in `src/validators/userValidator.ts`
- Preference schema defined in spec: [link to spec]
- Note: `UserService` already has `getPreferences()` stub - implement this
- Redis cache config is in `src/config/cache.ts`
```

**Over-specified Example (Avoid):**
```markdown
## Technical Notes
1. First, create a new file called preferenceValidator.ts
2. Import Joi from 'joi'
3. Create a schema with these exact fields: ...
4. Export the validate function
5. Then go to the controller and...
[Continues for 20 more steps]
```

### Task Types and Templates

#### Bug Fix Task

```markdown
**Title:** Fix [specific behavior] in [location]

## Bug Description
**Observed:** [What happens now]
**Expected:** [What should happen]
**Reproduction:** [Steps to reproduce]

## Root Cause (if known)
[Analysis of why this happens]

## Acceptance Criteria
- [ ] Bug no longer reproducible with given steps
- [ ] [Specific behavior] works as expected
- [ ] No regression in related functionality
- [ ] Test added to prevent regression

## Technical Notes
- Error occurs in: `path/to/file.ts:123`
- Related to: [other issues/changes]
```

#### Feature Task

```markdown
**Title:** [Action] [feature] for [user/context]

## Background
[Why this feature is needed]

## User Story
As a [user type], I want [capability] so that [benefit].

## Acceptance Criteria
- [ ] [Primary functionality works]
- [ ] [Edge case handled]
- [ ] [Error states handled]
- [ ] [Documentation updated if needed]
- [ ] [Tests added]

## Technical Notes
- Implement in: `path/to/location`
- Follow pattern: [reference]
- Related spec: [link]
```

#### Refactoring Task

```markdown
**Title:** Refactor [what] to [improvement]

## Motivation
[Why this refactoring is valuable]

## Current State
[Structure/code being refactored]

## Target State
[Desired structure/improvement]

## Acceptance Criteria
- [ ] All existing tests pass
- [ ] No behavior change (unless specified)
- [ ] [Specific improvement achieved]
- [ ] Code review approved

## Technical Notes
- Affected files: [list]
- Use strangler fig pattern: [yes/no]
- Feature flag needed: [yes/no]
```

#### Investigation/Spike Task

```markdown
**Title:** Investigate [topic/problem]

## Question to Answer
[Specific question or problem to explore]

## Success Criteria
- [ ] Document findings in [location]
- [ ] Recommend approach with trade-offs
- [ ] Identify follow-up tasks if needed
- [ ] Time-box: [X hours/days]

## Areas to Explore
- [ ] [Area 1]
- [ ] [Area 2]
- [ ] [Area 3]
```

### Linking Tasks to Specs and Plans

**Traceability is Key:**

```markdown
## References
- **Spec:** [Link to spec section]
- **Plan:** [Link to implementation plan step]
- **Requirements:** FR-1, FR-2, NFR-1
- **Epic/Parent:** [Link to parent issue]
- **Blocks:** #123, #124
- **Blocked by:** #120
```

**Requirement Mapping:**

| Spec Requirement | Task |
|-----------------|------|
| FR-1: Store preferences | #201: Create preferences table |
| FR-2: Read preferences | #202: Add GET endpoint |
| FR-3: Update preferences | #203: Add PUT endpoint |
| NFR-1: Response < 100ms | #204: Add caching layer |

## Examples

### Example 1: Feature Task from Spec

**Context:** Implementing user preferences from a spec.

```markdown
# Add GET endpoint for user notification preferences

## Background
Users need to retrieve their notification preferences to display current
settings in the UI. This is part of the notification preferences feature
(see spec: /docs/specs/notification-preferences.md).

## Current State
- No endpoint exists for reading preferences
- Preferences table created in #198
- Repository layer implemented in #199

## Desired Outcome
API endpoint that returns user notification preferences in a consistent
format, with appropriate caching for performance.

## Acceptance Criteria
- [ ] GET /api/v1/users/{userId}/preferences returns 200 with preferences
- [ ] Returns 404 if user doesn't exist
- [ ] Returns default preferences if none set (don't fail)
- [ ] Response matches schema in API spec
- [ ] Endpoint requires authentication
- [ ] Response cached in Redis (5 min TTL)
- [ ] Cache invalidated when preferences updated
- [ ] Unit tests added for controller
- [ ] Integration test added for full flow

## Technical Notes
- Controller: `src/controllers/preferencesController.ts`
- Follow pattern in `src/controllers/profileController.ts`
- Use existing `PreferenceRepository` from #199
- Cache key format: `user:{userId}:preferences`

## References
- Spec: docs/specs/notification-preferences.md#api-endpoints
- Plan Step: 2.1 in implementation plan
- Requirements: FR-3
- Blocked by: #199 (repository layer)
- Blocks: #210 (settings UI)

## Labels
`feature` `api` `backend` `preferences`
```

### Example 2: Bug Fix Task

**Context:** Production bug reported by users.

```markdown
# Fix password reset emails not sending for accounts with + in email

## Bug Description
**Observed:** Users with + in their email address (e.g., user+test@example.com)
never receive password reset emails. No error shown to user.

**Expected:** Password reset emails should be sent regardless of special
characters in valid email addresses.

**Reproduction:**
1. Create account with email containing + (e.g., test+alias@gmail.com)
2. Go to /forgot-password
3. Enter the email and submit
4. Check logs - email send never attempted

**Reported by:** Support ticket #4521
**Affected users:** ~2% of user base

## Root Cause Analysis
The email validation regex in `validateEmail()` rejects + characters even
though they're valid per RFC 5321. The validation passes on the frontend
(different regex) but fails silently on the backend.

## Acceptance Criteria
- [ ] Password reset works for emails with + character
- [ ] Password reset works for other valid special chars (. - _)
- [ ] Invalid emails still rejected appropriately
- [ ] Validation error returned to client (not silent fail)
- [ ] Regression test added for + character emails
- [ ] Existing email validation tests still pass

## Technical Notes
- Bug location: `src/utils/validation.ts:45` - `validateEmail()`
- Consider using established email validation library instead of regex
- Test with: `user+test@example.com`, `first.last@example.com`
- Check both forgot-password and registration flows

## References
- Support ticket: #4521
- Related: #312 (similar issue with . in emails, thought fixed)

## Labels
`bug` `p1` `email` `validation`
```

### Example 3: Refactoring Task

**Context:** Tech debt identified during code review.

```markdown
# Extract JWT utilities from AuthService into dedicated module

## Motivation
JWT handling logic is currently mixed into AuthService, making it hard to:
- Reuse JWT utilities in other services
- Test JWT logic in isolation
- Swap JWT libraries if needed

This was flagged in code review for #187.

## Current State
```
src/services/authService.ts (450 lines)
├── login()
├── logout()
├── generateToken()      ← JWT logic mixed in
├── verifyToken()        ← JWT logic mixed in
├── decodeToken()        ← JWT logic mixed in
├── refreshToken()       ← JWT logic mixed in
└── ... other auth methods
```

## Target State
```
src/utils/jwt.ts (new)
├── generateToken()
├── verifyToken()
├── decodeToken()
└── getTokenExpiry()

src/services/authService.ts (reduced)
├── login()              ← uses jwt.generateToken()
├── logout()
├── refreshToken()       ← uses jwt utilities
└── ... other auth methods
```

## Acceptance Criteria
- [ ] JWT functions extracted to `src/utils/jwt.ts`
- [ ] AuthService imports and uses new JWT module
- [ ] All existing auth tests pass (no behavior change)
- [ ] New unit tests for JWT module (90%+ coverage)
- [ ] No circular dependencies introduced
- [ ] JSDoc comments preserved/added

## Technical Notes
- Pure extraction - no behavior changes
- Keep same function signatures for now
- AuthService should have no direct `jsonwebtoken` imports after
- Watch for: token config currently accessed via `this.config`

## References
- Code review: #187 (comment by @senior-dev)
- Related: #201 (auth module extraction epic)

## Labels
`refactor` `tech-debt` `auth` `no-behavior-change`
```

### Example 4: Breaking Down a Plan Step

**Context:** Converting a plan step into multiple tasks.

**Plan Step:**
```markdown
### Phase 2: API Layer
**Step 2.1: Create preferences endpoints**
- Files: `src/routes/users.ts`, `src/controllers/preferencesController.ts`
- Deliverable: GET and PUT endpoints for preferences
- Criteria: Endpoints work, validation in place, errors handled
```

**Resulting Tasks:**

```markdown
# Task 1: Add GET /users/{userId}/preferences endpoint
[Full task as shown in Example 1]

---

# Task 2: Add PUT /users/{userId}/preferences endpoint

## Background
Users need to update their notification preferences from the settings UI.
This completes the CRUD operations for preferences.

## Current State
- GET endpoint implemented in #202
- Preferences model and repository ready
- No way to update preferences via API

## Desired Outcome
PUT endpoint that validates and persists preference changes with
appropriate error handling.

## Acceptance Criteria
- [ ] PUT /api/v1/users/{userId}/preferences returns 200 on success
- [ ] Returns 400 for invalid preference values
- [ ] Returns 404 if user doesn't exist
- [ ] Returns 403 if user tries to update another user's preferences
- [ ] Validates against preference schema (no unknown fields)
- [ ] Cache invalidated on successful update
- [ ] Audit log entry created for preference changes
- [ ] Unit tests for validation logic
- [ ] Integration test for full update flow

## Technical Notes
- Use validation schema from spec: /docs/specs/notification-preferences.md
- Follow pattern in `updateProfile` for auth checks
- Invalidate cache key: `user:{userId}:preferences`

## References
- Spec: docs/specs/notification-preferences.md#api-endpoints
- Plan Step: 2.1 in implementation plan
- Requirements: FR-4, NFR-2 (audit logging)
- Depends on: #202 (GET endpoint)

## Labels
`feature` `api` `backend` `preferences`

---

# Task 3: Add input validation schema for preference updates

## Background
Preference updates need robust validation to prevent invalid data
from being stored. This is shared validation logic used by the API.

[... continues with appropriate detail ...]
```

## Best Practices

### Do's
- Write titles that could stand alone in a task list
- Include enough context for someone new to the codebase
- Make acceptance criteria testable and unambiguous
- Link to specs, plans, and related tasks
- Scope tasks to be completable in one focused session
- Use consistent formatting across your project

### Don'ts
- Don't write novels - be concise but complete
- Don't over-specify implementation details
- Don't create tasks too small to be meaningful
- Don't forget edge cases in acceptance criteria
- Don't assume context - spell out what matters
- Don't leave "done" ambiguous

## Common Pitfalls

### Vague Titles
"Fix bug" or "Update code" tells readers nothing. Always specify what and where.

### Missing Acceptance Criteria
Without clear criteria, tasks drag on or get marked "done" prematurely. Every task needs testable completion conditions.

### Over-Scoped Tasks
Giant tasks are hard to estimate, review, and complete. Split them into focused pieces.

### Under-Specified Context
Assuming readers know the background leads to questions and delays. Provide the why, not just the what.

### Implementation Dictation
Telling implementers exactly how to code removes their agency and may miss better solutions. Specify outcomes, not steps.

### Missing Dependencies
Not identifying blockers leads to wasted time starting work that can't be completed.

## Task Quality Checklist

Before creating a task, verify:

**Title**
- [ ] Starts with action verb
- [ ] Specific about what and where
- [ ] Under 80 characters
- [ ] Scannable in a list

**Description**
- [ ] Explains why this work matters
- [ ] Describes current vs desired state
- [ ] Provides enough context for newcomers
- [ ] Concise but complete

**Acceptance Criteria**
- [ ] Each criterion is testable
- [ ] Edge cases addressed
- [ ] "Done" is unambiguous
- [ ] No more than 5-7 criteria (if more, split task)

**Scope**
- [ ] Completable in 1-2 days
- [ ] Single coherent deliverable
- [ ] Not too granular to be meaningful
- [ ] Independent enough to be worked on

**Metadata**
- [ ] Linked to spec/requirements (if applicable)
- [ ] Dependencies identified
- [ ] Blockers noted
- [ ] Appropriate labels

## Output Format

Use this template for consistent task creation:

```markdown
# [Action Verb] [What] [Where/Context]

## Background
[Why this task exists - 2-3 sentences]

## Current State
[What exists now - bullet points or brief description]

## Desired Outcome
[What should exist after - bullet points or brief description]

## Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Edge case handling]
- [ ] [Tests added]

## Technical Notes
- Location: `path/to/relevant/files`
- Pattern to follow: [reference]
- Watch out for: [potential gotcha]

## References
- Spec: [link]
- Plan: [link]
- Requirements: [IDs]
- Depends on: [task IDs]
- Blocks: [task IDs]

## Labels
`label1` `label2` `label3`
```

## Limitations

- Task quality depends on understanding the work being described
- Cannot replace domain knowledge for specialized areas
- Acceptance criteria may need refinement as work progresses
- Estimates are not included (team/process dependent)

## Related Skills

- **Spec Writing**: Create specifications that tasks implement
- **Plan Writing**: Break down specs into plans that generate tasks
- **Spec-Driven Development**: Execute tasks systematically

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

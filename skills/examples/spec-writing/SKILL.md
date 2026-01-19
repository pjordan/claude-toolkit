---
name: spec-writing
description: Write high-quality technical specifications that enable clear communication, reduce ambiguity, and drive successful implementation. Use when planning new features, designing APIs, documenting system architecture decisions, creating technical requirements, writing acceptance criteria, preparing RFCs, defining data models, or specifying integration requirements. Triggers include "write spec", "technical specification", "feature spec", "API spec", "requirements document", "RFC", or when creating documentation that defines what to build.
---

# Spec Writing Skill

Write high-quality technical specifications that enable clear communication, reduce ambiguity, and drive successful implementation.

## Overview

This skill guides Claude through creating comprehensive technical specifications for features, APIs, systems, and changes. A well-written spec serves as a contract between stakeholders, reduces implementation ambiguity, surfaces edge cases early, and provides a foundation for testing and documentation.

## When to Use

- Planning new features before implementation
- Designing APIs (REST, GraphQL, gRPC)
- Documenting system architecture decisions
- Creating technical requirements documents
- Writing acceptance criteria for user stories
- Preparing RFC (Request for Comments) documents
- Defining data models and schemas
- Specifying integration requirements

## Prerequisites

- Clear understanding of the problem being solved
- Knowledge of stakeholders and their needs
- Familiarity with the target system/codebase
- Understanding of relevant constraints (technical, business, timeline)

## Instructions

### Spec Writing Process

1. **Understand the Context**
   - What problem are we solving?
   - Who are the stakeholders?
   - What are the constraints?
   - What existing systems are involved?

2. **Define the Scope**
   - What is included in this spec?
   - What is explicitly out of scope?
   - What are the assumptions?
   - What are the dependencies?

3. **Specify Requirements**
   - Functional requirements (what it does)
   - Non-functional requirements (how it performs)
   - User experience requirements
   - Security requirements
   - Data requirements

4. **Detail the Design**
   - System architecture/component design
   - Data models and schemas
   - API contracts
   - State machines and workflows
   - Error handling strategies

5. **Address Edge Cases**
   - Failure scenarios
   - Boundary conditions
   - Concurrent access
   - Partial failures
   - Rollback strategies

6. **Define Success Criteria**
   - Acceptance criteria
   - Performance benchmarks
   - Quality metrics
   - Test scenarios

### Spec Quality Checklist

**Clarity**
- [ ] Unambiguous language (avoid "should", "might", "could")
- [ ] Defined terminology and glossary
- [ ] Concrete examples for complex concepts
- [ ] Clear distinction between requirements and nice-to-haves

**Completeness**
- [ ] All stakeholder needs addressed
- [ ] Edge cases documented
- [ ] Error handling specified
- [ ] Security considerations included
- [ ] Performance requirements stated

**Testability**
- [ ] Each requirement is verifiable
- [ ] Acceptance criteria are measurable
- [ ] Test scenarios are defined
- [ ] Success/failure conditions are clear

**Feasibility**
- [ ] Technical constraints acknowledged
- [ ] Resource requirements estimated
- [ ] Dependencies identified
- [ ] Risks documented with mitigations

**Maintainability**
- [ ] Spec is versioned
- [ ] Change history tracked
- [ ] Related specs referenced
- [ ] Future considerations noted

### Language Guidelines

**Use Precise Language:**
| Avoid | Use Instead |
|-------|-------------|
| "The system should handle errors" | "The system MUST return HTTP 400 with error code `INVALID_INPUT` when..." |
| "Fast response times" | "P95 latency MUST be under 200ms" |
| "Support multiple users" | "Support up to 10,000 concurrent users" |
| "Secure authentication" | "Authenticate using OAuth 2.0 with PKCE flow" |

**RFC 2119 Keywords:**
- **MUST / REQUIRED**: Absolute requirement
- **MUST NOT / SHALL NOT**: Absolute prohibition
- **SHOULD / RECOMMENDED**: Strong recommendation with valid exceptions
- **SHOULD NOT / NOT RECOMMENDED**: Strong discouraged with valid exceptions
- **MAY / OPTIONAL**: Truly optional

### Spec Types

**Feature Spec** - For new features or capabilities
- Problem statement
- User stories and personas
- Functional requirements
- UX mockups/wireframes
- Technical approach
- Testing strategy

**API Spec** - For service interfaces
- Endpoint definitions
- Request/response schemas
- Authentication requirements
- Rate limits and quotas
- Error codes and handling
- Versioning strategy

**Architecture Spec** - For system design
- Component overview
- Data flow diagrams
- Integration points
- Scalability considerations
- Deployment architecture
- Disaster recovery

**Data Spec** - For data models and storage
- Entity definitions
- Relationships and constraints
- Migration strategy
- Retention policies
- Privacy considerations

## Examples

### Example 1: API Endpoint Spec

**Requirement:** Add endpoint to retrieve user preferences

**Spec:**

```markdown
## GET /api/v1/users/{userId}/preferences

### Overview
Retrieves the preference settings for a specific user.

### Authentication
- REQUIRED: Bearer token with `user:read` scope
- User MUST be retrieving their own preferences OR have `admin:read` scope

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userId | string (UUID) | Yes | The unique identifier of the user |

### Query Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| category | string | No | all | Filter by category: `notifications`, `privacy`, `display`, `all` |

### Response

#### Success (200 OK)
```json
{
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "preferences": {
    "notifications": {
      "email": true,
      "push": false,
      "frequency": "daily"
    },
    "privacy": {
      "profileVisibility": "friends",
      "showOnlineStatus": true
    },
    "display": {
      "theme": "dark",
      "language": "en-US",
      "timezone": "America/New_York"
    }
  },
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

#### Error Responses
| Status | Code | Description |
|--------|------|-------------|
| 401 | `UNAUTHORIZED` | Missing or invalid authentication token |
| 403 | `FORBIDDEN` | User lacks permission to access these preferences |
| 404 | `USER_NOT_FOUND` | No user exists with the given userId |
| 400 | `INVALID_CATEGORY` | Category parameter contains invalid value |

### Performance Requirements
- P50 latency: < 50ms
- P99 latency: < 200ms
- Cache TTL: 5 minutes (invalidate on preference update)

### Rate Limits
- 100 requests per minute per user
- 1000 requests per minute per API key

### Example Request
```bash
curl -X GET "https://api.example.com/api/v1/users/550e8400-e29b-41d4-a716-446655440000/preferences?category=notifications" \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Accept: application/json"
```
```

### Example 2: Feature Spec

**Requirement:** Add dark mode support to the application

**Spec:**

```markdown
## Feature: Dark Mode Support

### Problem Statement
Users have requested dark mode to reduce eye strain during nighttime use
and to accommodate personal preferences. Currently, the application only
supports a light theme.

### Goals
1. Allow users to switch between light and dark themes
2. Respect system-level theme preferences
3. Persist user's theme choice across sessions
4. Ensure all UI components render correctly in both themes

### Non-Goals (Out of Scope)
- Custom color theme creation
- Scheduled theme switching
- Per-page theme settings

### User Stories
1. As a user, I want to toggle between light and dark mode so that
   I can choose my preferred viewing experience.
2. As a user, I want my theme preference to persist so that I don't
   have to set it each time I open the app.
3. As a user, I want the app to default to my system theme so that
   it matches my other applications.

### Functional Requirements

#### FR-1: Theme Toggle
- The application MUST provide a visible toggle control in the settings menu
- The toggle MUST switch between "Light", "Dark", and "System" options
- Theme changes MUST apply immediately without page reload
- The toggle MUST show the currently active theme

#### FR-2: System Theme Detection
- When set to "System", the app MUST detect the OS theme preference
- The app MUST respond to OS theme changes in real-time
- On browsers without system theme detection, default to "Light"

#### FR-3: Theme Persistence
- User's theme choice MUST persist across browser sessions
- Theme MUST be stored in localStorage under key `user-theme`
- For authenticated users, theme preference SHOULD sync to user profile

### Non-Functional Requirements

#### NFR-1: Performance
- Theme switch MUST complete in < 100ms
- Initial theme detection MUST complete before first paint
- No flash of wrong theme on page load

#### NFR-2: Accessibility
- Both themes MUST maintain WCAG 2.1 AA contrast ratios
- Theme toggle MUST be keyboard accessible
- Screen readers MUST announce current theme state

### Technical Design

#### Color Token System
```css
:root {
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f5f5f5;
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #666666;
  /* ... */
}

[data-theme="dark"] {
  --color-bg-primary: #1a1a1a;
  --color-bg-secondary: #2d2d2d;
  --color-text-primary: #ffffff;
  --color-text-secondary: #a0a0a0;
  /* ... */
}
```

#### Implementation Approach
1. Add `data-theme` attribute to document root
2. Create CSS custom properties for all colors
3. Add theme context provider for React components
4. Implement theme toggle component
5. Add localStorage persistence layer
6. Add system theme detection hook

### Edge Cases
1. **localStorage unavailable**: Fall back to system theme, no persistence
2. **No system theme support**: Default to light theme
3. **Theme mismatch on SSR**: Use CSS media query fallback
4. **User has both cookie and localStorage**: localStorage takes precedence

### Acceptance Criteria
- [ ] User can switch between Light, Dark, and System modes
- [ ] Theme persists across browser sessions
- [ ] System mode responds to OS theme changes
- [ ] No flash of incorrect theme on page load
- [ ] All components render correctly in both themes
- [ ] Contrast ratios meet WCAG 2.1 AA standards

### Test Scenarios
1. Toggle from Light to Dark - verify all components update
2. Set to System, change OS theme - verify app follows
3. Close and reopen browser - verify theme persists
4. Clear localStorage - verify graceful fallback
5. Test with screen reader - verify announcements
```

### Example 3: Data Model Spec

**Requirement:** Design the schema for a task management system

**Spec:**

```markdown
## Data Model: Task Management System

### Entities

#### Task
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULLABLE | Detailed description |
| status | ENUM | NOT NULL, DEFAULT 'todo' | One of: todo, in_progress, done, archived |
| priority | INTEGER | NOT NULL, DEFAULT 0 | 0=none, 1=low, 2=medium, 3=high, 4=urgent |
| assignee_id | UUID | FK → User.id, NULLABLE | Assigned user |
| project_id | UUID | FK → Project.id, NOT NULL | Parent project |
| parent_task_id | UUID | FK → Task.id, NULLABLE | Parent task for subtasks |
| due_date | TIMESTAMP | NULLABLE | Due date/time |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |
| created_by | UUID | FK → User.id, NOT NULL | Creator |

#### Indexes
- `idx_task_project` on (project_id, status) - for listing tasks by project
- `idx_task_assignee` on (assignee_id, status) - for user's task list
- `idx_task_due_date` on (due_date) WHERE status != 'done' - for due date queries

### Relationships
```
User 1──────────< Task (assignee)
User 1──────────< Task (creator)
Project 1───────< Task
Task 1──────────< Task (subtasks)
```

### Constraints
1. A task MUST belong to exactly one project
2. A subtask MUST NOT have a different project than its parent
3. Subtasks MUST NOT exceed 3 levels of nesting
4. Archived tasks MUST NOT have non-archived subtasks

### State Machine: Task Status
```
[todo] ──→ [in_progress] ──→ [done]
   │            │              │
   │            ↓              │
   └────→ [archived] ←────────┘
```

Allowed transitions:
- todo → in_progress, archived
- in_progress → todo, done, archived
- done → in_progress, archived
- archived → (terminal state)

### Migration Strategy
1. Create tables with all columns
2. Add indexes after initial data load
3. Backfill created_by from audit log
4. Add NOT NULL constraint on created_by after backfill
```

## Best Practices

### Do's
- Start with the "why" before the "what"
- Use concrete examples to illustrate requirements
- Define clear success criteria upfront
- Include both happy path and error scenarios
- Version your specs and track changes
- Get stakeholder review before implementation
- Keep specs living documents, updated as you learn

### Don'ts
- Don't specify implementation details unless necessary
- Don't use vague or ambiguous language
- Don't skip edge cases and error handling
- Don't write specs in isolation - collaborate
- Don't treat specs as immutable - iterate
- Don't over-specify obvious behaviors
- Don't forget non-functional requirements

## Common Pitfalls

### Premature Implementation Details
Focus on *what* the system should do, not *how* it should do it, unless the implementation approach is a deliberate architectural choice.

### Missing Edge Cases
Common overlooked areas:
- Empty states and null values
- Concurrent operations
- Network failures and timeouts
- Authentication edge cases
- Rate limiting and quotas
- Data migration from old systems

### Stakeholder Misalignment
Ensure all stakeholders review the spec before implementation. Different interpretations caught early save significant rework.

### Scope Creep
Clearly define what is out of scope. When new requirements emerge, add them explicitly with versioning.

## Output Format

Structure specs consistently:

```markdown
# [Feature/API/System Name] Specification

## Overview
[Brief description of what this spec covers]

## Problem Statement
[Why this is needed, what problem it solves]

## Goals
[What success looks like]

## Non-Goals / Out of Scope
[What this spec explicitly does NOT cover]

## Requirements
### Functional Requirements
[What the system must do]

### Non-Functional Requirements
[Performance, security, scalability, etc.]

## Design
[Technical approach, architecture, data models]

## Edge Cases
[Error scenarios, boundary conditions]

## Acceptance Criteria
[How we know it's done]

## Open Questions
[Unresolved decisions needing input]

## Appendix
[Supporting materials, references, glossary]

---
Version: 1.0
Author: [Name]
Last Updated: [Date]
Status: [Draft | Review | Approved | Implemented]
```

## Limitations

- Specs require domain expertise that may need stakeholder input
- Can't guarantee completeness without system knowledge
- Technical feasibility assessment requires implementation context
- Specs may need iteration based on implementation learnings

## Related Skills

- **Plan Writing**: Create implementation plans from specifications
- **Spec-Driven Development**: Implementing code from specifications
- **Code Review**: Validating implementation against spec
- **API Design**: Specialized API specification patterns
- **System Design**: Architecture and scalability considerations

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

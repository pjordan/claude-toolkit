# Spec-Driven Development Skill

Implement features systematically by following technical specifications, ensuring complete coverage of requirements and edge cases.

## Overview

This skill guides Claude through implementing code from technical specifications. It ensures that implementations align with specs, all requirements are addressed, edge cases are handled, and acceptance criteria are met. This approach reduces rework, improves quality, and creates traceability between specs and code.

## When to Use

- Implementing features from a written specification
- Building APIs defined in OpenAPI/Swagger specs
- Translating design documents into working code
- Ensuring implementation matches documented requirements
- Creating tests that verify spec compliance
- Reviewing code against its specification

## Prerequisites

- A written specification (feature spec, API spec, or design doc)
- Understanding of the target codebase and technology stack
- Access to relevant existing code patterns
- Clear acceptance criteria in the spec

## Instructions

### Implementation Process

1. **Parse the Specification**
   - Identify all functional requirements
   - Extract non-functional requirements (performance, security)
   - List explicit edge cases and error conditions
   - Note acceptance criteria
   - Identify ambiguities to clarify

2. **Create Implementation Plan**
   - Map requirements to code components
   - Identify existing code to modify vs. new code to write
   - Determine implementation order (dependencies first)
   - Plan for incremental, testable checkpoints

3. **Implement Systematically**
   - Address one requirement at a time
   - Write tests alongside implementation
   - Handle error cases as specified
   - Document deviations or clarifications needed

4. **Verify Against Spec**
   - Check each requirement is implemented
   - Verify edge cases are handled
   - Run against acceptance criteria
   - Document spec coverage

5. **Handle Gaps**
   - Note ambiguities encountered
   - Document implementation decisions
   - Flag potential spec updates needed
   - Track technical debt from spec gaps

### Requirement Tracking Matrix

Use this format to track implementation progress:

```markdown
| Req ID | Description | Status | Notes |
|--------|-------------|--------|-------|
| FR-1 | User login with email | ✅ Done | src/auth/login.ts:45 |
| FR-2 | OAuth provider support | 🔄 In Progress | Google done, GitHub pending |
| FR-3 | Session management | ⏳ Pending | Blocked on FR-1 |
| NFR-1 | < 200ms response time | ✅ Done | Measured at 85ms P95 |
| EC-1 | Invalid credentials | ✅ Done | Returns 401 per spec |
```

### Implementation Checklist

**Before Starting**
- [ ] Read entire spec thoroughly
- [ ] Identify unclear or ambiguous sections
- [ ] Understand all acceptance criteria
- [ ] Identify dependencies and prerequisites
- [ ] Plan implementation order

**During Implementation**
- [ ] Track which requirements are being addressed
- [ ] Follow spec language precisely (MUST vs SHOULD)
- [ ] Implement error handling as specified
- [ ] Write tests for each requirement
- [ ] Document any deviations from spec

**After Implementation**
- [ ] Verify all MUST requirements implemented
- [ ] Verify SHOULD requirements addressed or documented
- [ ] Run all acceptance criteria tests
- [ ] Document any spec gaps discovered
- [ ] Update spec with implementation insights

### Handling Spec Keywords

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
// Implement if feasible, document if skipped with rationale
```

**MAY / OPTIONAL**: Implement based on value/effort.
```typescript
// Spec: "API MAY support pagination"
// Implement if beneficial, skip if not needed yet
```

### Error Handling from Specs

When specs define error responses, implement them precisely:

```typescript
// Spec: "Return 404 USER_NOT_FOUND when userId doesn't exist"
async function getUser(userId: string) {
  const user = await db.users.findById(userId);
  if (!user) {
    throw new ApiError(404, "USER_NOT_FOUND", "No user exists with the given ID");
  }
  return user;
}
```

### Testing Strategy

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

**Performance Tests**: Validate NFRs
```typescript
describe("Performance Requirements", () => {
  // NFR-1: P95 latency < 200ms
  it("responds within 200ms at P95", async () => {
    const latencies = await measureLatencies(100);
    const p95 = percentile(latencies, 95);
    expect(p95).toBeLessThan(200);
  });
});
```

## Examples

### Example 1: Implementing an API Endpoint from Spec

**Spec (excerpt):**
```markdown
## POST /api/v1/tasks

### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Task title (1-255 chars) |
| description | string | No | Task description |
| priority | integer | No | 0-4, default 0 |
| dueDate | ISO8601 | No | Due date |

### Response (201 Created)
{ "id": "uuid", "title": "...", "createdAt": "..." }

### Errors
- 400 INVALID_TITLE: Title missing or invalid length
- 400 INVALID_PRIORITY: Priority not in range 0-4
- 401 UNAUTHORIZED: Missing authentication
```

**Implementation:**

```typescript
// POST /api/v1/tasks - Implementation per spec
import { z } from "zod";

// Validation schema derived from spec
const CreateTaskSchema = z.object({
  title: z.string().min(1).max(255),           // Per spec: 1-255 chars, required
  description: z.string().optional(),           // Per spec: optional
  priority: z.number().int().min(0).max(4)      // Per spec: 0-4
    .default(0),                                // Per spec: default 0
  dueDate: z.string().datetime().optional(),    // Per spec: ISO8601, optional
});

export async function createTask(req: Request, res: Response) {
  // FR: Authentication required (401 UNAUTHORIZED)
  if (!req.user) {
    return res.status(401).json({
      error: "UNAUTHORIZED",
      message: "Authentication required"
    });
  }

  // FR: Validate request body
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

  // FR: Create task
  const task = await db.tasks.create({
    ...result.data,
    userId: req.user.id,
  });

  // FR: Return 201 with response per spec
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
| FR-2 | Optional description | ✅ | CreateTaskSchema.description |
| FR-3 | Priority 0-4, default 0 | ✅ | CreateTaskSchema.priority |
| FR-4 | Optional ISO8601 dueDate | ✅ | CreateTaskSchema.dueDate |
| FR-5 | Return 201 with id, title, createdAt | ✅ | Line 52 |
| EC-1 | 400 INVALID_TITLE | ✅ | Line 32 |
| EC-2 | 400 INVALID_PRIORITY | ✅ | Line 39 |
| EC-3 | 401 UNAUTHORIZED | ✅ | Line 18 |
```

### Example 2: Implementing a Feature from Spec

**Spec (excerpt):**
```markdown
## Feature: Dark Mode

### FR-1: Theme Toggle
- Toggle MUST switch between "Light", "Dark", and "System"
- Changes MUST apply immediately without page reload
- Current theme MUST be visible in toggle

### FR-2: System Theme Detection
- MUST detect OS theme when set to "System"
- MUST respond to OS theme changes in real-time

### FR-3: Persistence
- Theme choice MUST persist in localStorage key `user-theme`
- MUST NOT flash wrong theme on page load
```

**Implementation:**

```typescript
// theme.ts - Implementation per Dark Mode spec

type Theme = "light" | "dark" | "system";
const STORAGE_KEY = "user-theme"; // Per FR-3: specific key required

// FR-2: System theme detection
function getSystemTheme(): "light" | "dark" {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

// FR-3: Persistence - read from localStorage
function getStoredTheme(): Theme {
  if (typeof localStorage === "undefined") return "system";
  return (localStorage.getItem(STORAGE_KEY) as Theme) || "system";
}

// FR-3: Persistence - write to localStorage
function setStoredTheme(theme: Theme): void {
  localStorage.setItem(STORAGE_KEY, theme);
}

// FR-1: Get effective theme (resolves "system" to actual theme)
function getEffectiveTheme(theme: Theme): "light" | "dark" {
  return theme === "system" ? getSystemTheme() : theme;
}

// FR-1: Apply theme immediately without reload
function applyTheme(theme: "light" | "dark"): void {
  document.documentElement.setAttribute("data-theme", theme);
}

// FR-2: Listen for OS theme changes in real-time
function watchSystemTheme(callback: (theme: "light" | "dark") => void): () => void {
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  const handler = (e: MediaQueryListEvent) => {
    callback(e.matches ? "dark" : "light");
  };
  mediaQuery.addEventListener("change", handler);
  return () => mediaQuery.removeEventListener("change", handler);
}

// FR-3: Initialize theme before first paint (prevents flash)
// This must be called in <head> before body renders
export function initTheme(): void {
  const stored = getStoredTheme();
  const effective = getEffectiveTheme(stored);
  applyTheme(effective);
}

// FR-1: Toggle component hook
export function useTheme() {
  const [theme, setThemeState] = useState<Theme>(getStoredTheme);

  const setTheme = useCallback((newTheme: Theme) => {
    setThemeState(newTheme);
    setStoredTheme(newTheme);                          // FR-3: Persist
    applyTheme(getEffectiveTheme(newTheme));          // FR-1: Immediate
  }, []);

  // FR-2: Real-time system theme updates
  useEffect(() => {
    if (theme !== "system") return;
    return watchSystemTheme((systemTheme) => {
      applyTheme(systemTheme);
    });
  }, [theme]);

  return {
    theme,                                            // FR-1: Current visible
    effectiveTheme: getEffectiveTheme(theme),
    setTheme,
  };
}
```

**Tests:**
```typescript
describe("Dark Mode (per spec)", () => {
  // FR-1: Toggle between Light, Dark, System
  it("toggles between all three theme options", () => {
    const { setTheme, theme } = renderHook(() => useTheme());

    setTheme("dark");
    expect(theme).toBe("dark");

    setTheme("light");
    expect(theme).toBe("light");

    setTheme("system");
    expect(theme).toBe("system");
  });

  // FR-1: Changes apply immediately
  it("applies theme changes without page reload", () => {
    const { setTheme } = renderHook(() => useTheme());
    setTheme("dark");
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
  });

  // FR-3: Persists to localStorage
  it("persists theme choice to localStorage", () => {
    const { setTheme } = renderHook(() => useTheme());
    setTheme("dark");
    expect(localStorage.getItem("user-theme")).toBe("dark");
  });

  // FR-3: No flash on load
  it("applies theme before first render", () => {
    localStorage.setItem("user-theme", "dark");
    initTheme();
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
  });
});
```

### Example 3: Handling Spec Ambiguity

**Spec says:**
```markdown
Users SHOULD receive a confirmation email after registration.
```

**Questions to resolve:**
1. What triggers "SHOULD" vs "MUST"? Is this a P1 or P2 requirement?
2. What's the email content/template?
3. What happens if email sending fails?
4. Is there a retry mechanism?

**Implementation with documented decisions:**
```typescript
/**
 * Send registration confirmation email.
 *
 * Spec: "Users SHOULD receive a confirmation email"
 * Decision: Implemented as fire-and-forget to not block registration.
 * Rationale: SHOULD = best effort, registration shouldn't fail if email fails.
 *
 * TODO: Spec needs clarification on retry policy and email template.
 */
async function sendConfirmationEmail(user: User): Promise<void> {
  try {
    await emailService.send({
      to: user.email,
      template: "registration-confirmation", // Template not in spec - using default
      data: { name: user.name }
    });
  } catch (error) {
    // Decision: Log but don't fail registration (SHOULD vs MUST)
    logger.warn("Failed to send confirmation email", { userId: user.id, error });
    // TODO: Add to retry queue per future spec clarification
  }
}
```

## Best Practices

### Do's
- Read the entire spec before writing any code
- Track implementation progress against requirements
- Implement MUST requirements first, then SHOULD, then MAY
- Write tests that reference specific spec requirements
- Document deviations and decisions
- Flag spec ambiguities early

### Don'ts
- Don't assume requirements - ask for clarification
- Don't skip error cases defined in the spec
- Don't implement beyond the spec without discussion
- Don't ignore non-functional requirements
- Don't wait until the end to verify against spec

## Common Pitfalls

### Partial Implementation
Implementing only the happy path while ignoring specified error conditions. Always implement error handling as specified.

### Over-Implementation
Adding features not in the spec. Stick to what's specified unless you've discussed additions with stakeholders.

### Specification Drift
Not updating the spec when implementation reveals issues. Keep specs and code in sync.

### Missing Traceability
Not documenting which code implements which requirements. Use comments and tracking matrices.

## Output Format

When implementing from a spec, provide updates in this format:

```markdown
## Implementation Progress

### Completed
- [x] FR-1: User registration (src/auth/register.ts)
- [x] FR-2: Email validation (src/auth/validators.ts)
- [x] EC-1: Duplicate email handling (returns 409)

### In Progress
- [ ] FR-3: OAuth integration
  - Google: ✅ Complete
  - GitHub: 🔄 In progress
  - Apple: ⏳ Not started

### Blocked
- [ ] FR-4: Email verification
  - Blocked on: Email service configuration
  - Question: Spec unclear on verification link expiry

### Spec Clarifications Needed
1. FR-3: Which OAuth scopes are required?
2. NFR-1: Is 200ms latency for P95 or P99?

### Deviations from Spec
1. FR-2: Added additional email format validation beyond spec
   - Rationale: Spec's regex pattern allowed invalid TLDs
```

## Limitations

- Requires well-written specifications to be effective
- Cannot resolve spec ambiguities without stakeholder input
- Implementation may reveal spec gaps needing updates
- Technical constraints may require spec modifications

## Related Skills

- **Spec Writing**: Create the specifications this skill implements
- **Plan Writing**: Break down specs into implementation plans
- **Code Review**: Verify implementation matches specification
- **Test Writing**: Create tests that verify spec compliance

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

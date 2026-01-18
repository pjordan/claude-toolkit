# Spec-Driven Development

Guide AI-assisted coding through a specification-first workflow that produces verifiable, well-documented code.

## Overview

Spec-Driven Development (SDD) is a methodology where specifications are written before code, serving as the source of truth for AI agents to generate, test, and validate implementations. This skill teaches Claude to follow a structured **Specify → Plan → Tasks → Implement** workflow with validation gates at each phase.

The approach combines the discipline of upfront design with the flexibility of iterative development, leveraging tests as executable specifications that constrain AI output and prevent hallucinations.

## When to Use

- Building new features from scratch
- Implementing complex business logic
- Working on code that requires high reliability
- Collaborating on features where requirements need to be explicit
- Refactoring existing systems with clear behavioral contracts
- Any task where "done" needs a clear, verifiable definition

## Prerequisites

- Basic understanding of the target programming language
- Familiarity with testing frameworks (unit tests, integration tests)
- Version control basics (Git)

## Instructions

### Phase 1: Specify

Create a specification that defines *what* the code should do, not *how*.

**Specification Template:**

```markdown
# Feature: [Name]

## Problem Statement
[What problem does this solve? Why does it matter?]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Acceptance Criteria
Given [precondition]
When [action]
Then [expected result]

## Boundaries

### ✅ Always
- [Behavior that must always occur]
- [Constraint that must always be respected]

### ⚠️ Ask First
- [Decision that requires clarification]
- [Tradeoff that needs user input]

### 🚫 Never
- [Behavior that must never occur]
- [Security/safety constraint]

## Out of Scope
- [Explicitly excluded functionality]
- [Future considerations, not for this iteration]
```

**Key Principles:**
1. Start with user outcomes, not implementation details
2. Make success measurable and verifiable
3. Use Given/When/Then format for behavioral clarity
4. Define boundaries explicitly to prevent scope creep
5. Call out what's NOT included to manage expectations

### Phase 2: Plan

Transform the specification into a technical approach.

**Planning Checklist:**
1. Identify affected files and components
2. Determine the testing strategy (unit, integration, e2e)
3. List dependencies and potential blockers
4. Define the implementation order
5. Estimate complexity (not time - just relative effort)

**Plan Document Template:**

```markdown
# Implementation Plan: [Feature Name]

## Affected Components
- `path/to/file.ts` - [What changes]
- `path/to/other.ts` - [What changes]

## Testing Strategy
- Unit tests for: [list functions/methods]
- Integration tests for: [list interactions]
- Manual verification: [list scenarios]

## Implementation Order
1. [First thing to build - foundational]
2. [Second thing - builds on first]
3. [Third thing - brings it together]

## Open Questions
- [Question that needs answering before proceeding]

## Risks
- [Potential issue] → [Mitigation]
```

**Validation Gate:** Before proceeding to tasks, confirm:
- [ ] All open questions resolved
- [ ] User has approved the approach
- [ ] Testing strategy covers acceptance criteria

### Phase 3: Tasks

Break the plan into atomic, testable units of work.

**Task Breakdown Rules:**
1. Each task should be completable in one focused session
2. Each task should have a clear "done" definition
3. Each task should be independently testable
4. Tasks should build incrementally (no big-bang integration)

**Task Format:**

```markdown
## Task: [Short name]

**Objective:** [One sentence description]

**Test First:**
```[language]
// Write the test that defines success
test('[behavior description]', () => {
  // Arrange
  // Act
  // Assert
});
```

**Implementation Notes:**
- [Specific guidance]
- [Edge cases to handle]

**Done When:**
- [ ] Test passes
- [ ] [Additional verification]
```

### Phase 4: Implement

Execute tasks using Test-Driven Generation (TDG).

**TDG Workflow:**

1. **Write the test first** - The test IS the specification
2. **Run the test** - Confirm it fails (red)
3. **Implement minimal code** - Just enough to pass
4. **Run the test** - Confirm it passes (green)
5. **Refactor if needed** - Keep tests green
6. **Commit** - Small, focused commits

**Implementation Rules:**
- Never implement without a failing test first
- Don't add code "just in case" - YAGNI applies
- Each commit should leave tests passing
- Update the spec if requirements change during implementation

### Validation Gates

Before moving between phases, verify:

**Specify → Plan:**
- [ ] Specification reviewed and approved
- [ ] All stakeholder questions answered
- [ ] Boundaries (Always/Ask/Never) are clear

**Plan → Tasks:**
- [ ] Technical approach approved
- [ ] No unresolved blockers
- [ ] Testing strategy is comprehensive

**Tasks → Implement:**
- [ ] Tasks are atomic and testable
- [ ] Implementation order makes sense
- [ ] Each task has a clear test to write first

**Implement → Done:**
- [ ] All acceptance criteria tests pass
- [ ] Code reviewed
- [ ] Spec updated to reflect final implementation
- [ ] Documentation current

## Best Practices

### Keep Specs Living
Update specifications as you learn. A spec that diverges from reality is worse than no spec. Commit spec changes alongside code changes.

### Tests Are Documentation
Well-named tests explain behavior better than comments. Prefer `test('returns null when user not found')` over `test('test case 3')`.

### One Real Example Beats Three Paragraphs
In specifications, show concrete examples of inputs and expected outputs. AI agents work better with examples than abstract descriptions.

### Scope Boundaries Prevent Creep
The "Out of Scope" and "🚫 Never" sections are as important as what you're building. They keep focus tight and prevent gold-plating.

### Small Commits, Fast Feedback
Commit after each passing test. This creates a clear history and makes it easy to bisect if something breaks later.

### Ask Before Assuming
When hitting an "⚠️ Ask First" boundary, stop and clarify. Wrong assumptions compound into larger rework.

## Common Pitfalls

### Over-Specifying Implementation
**Problem:** Spec describes HOW to build rather than WHAT behavior is needed.
**Solution:** Focus on observable outcomes. "User sees confirmation message" not "Call showModal() with success flag".

### Skipping the Test-First Step
**Problem:** Writing implementation then tests leads to tests that verify code, not behavior.
**Solution:** Always write the test first. If you can't write the test, the requirement isn't clear enough.

### Monolithic Tasks
**Problem:** Tasks too large to complete in one session lead to partial commits and broken states.
**Solution:** Break down until each task has exactly one test to write and pass.

### Spec Drift
**Problem:** Implementation diverges from spec, but spec isn't updated.
**Solution:** Treat spec updates as part of the task. No PR merges with outdated specs.

### Analysis Paralysis
**Problem:** Spending too long perfecting the spec before writing any code.
**Solution:** Specs are living documents. Get to 80% confidence then start. Iterate.

## Examples

### Example 1: User Authentication Feature

**Specification:**

```markdown
# Feature: Email/Password Authentication

## Problem Statement
Users need to securely log into the application using email and password credentials.

## Success Criteria
- [ ] Users can log in with valid credentials
- [ ] Invalid credentials show clear error message
- [ ] Account locks after 5 failed attempts
- [ ] Session persists across page refreshes

## Acceptance Criteria
Given a registered user with email "user@example.com"
When they enter correct password and click "Log In"
Then they are redirected to the dashboard

Given a user enters incorrect password
When they click "Log In"
Then they see "Invalid email or password" (no hint which is wrong)

Given a user has failed login 5 times
When they try again with correct password
Then they see "Account locked. Please reset password."

## Boundaries

### ✅ Always
- Hash passwords with bcrypt (cost factor 12+)
- Use constant-time comparison for password verification
- Log authentication attempts (success and failure)

### ⚠️ Ask First
- Password complexity requirements
- Session timeout duration
- "Remember me" functionality

### 🚫 Never
- Store plaintext passwords
- Reveal whether email exists in error messages
- Allow unlimited login attempts

## Out of Scope
- Social login (Google, GitHub)
- Two-factor authentication
- Password reset flow
```

**First Task:**

```markdown
## Task: Validate login credentials

**Objective:** Verify email/password combination against stored hash

**Test First:**
```typescript
describe('AuthService.validateCredentials', () => {
  test('returns user when credentials valid', async () => {
    const user = await createTestUser('test@example.com', 'correctpassword');
    const result = await authService.validateCredentials('test@example.com', 'correctpassword');
    expect(result).toEqual(user);
  });

  test('returns null when password incorrect', async () => {
    await createTestUser('test@example.com', 'correctpassword');
    const result = await authService.validateCredentials('test@example.com', 'wrongpassword');
    expect(result).toBeNull();
  });

  test('returns null when email not found', async () => {
    const result = await authService.validateCredentials('nobody@example.com', 'anypassword');
    expect(result).toBeNull();
  });
});
```

**Done When:**
- [ ] All three tests pass
- [ ] Password comparison uses constant-time algorithm
- [ ] No timing difference between "user not found" and "wrong password"
```

### Example 2: Shopping Cart Price Calculation

**Specification:**

```markdown
# Feature: Cart Total Calculation

## Problem Statement
Calculate accurate cart totals including discounts, taxes, and shipping.

## Success Criteria
- [ ] Subtotal reflects item prices × quantities
- [ ] Percentage discounts apply correctly
- [ ] Tax calculated on discounted subtotal
- [ ] Free shipping threshold works

## Acceptance Criteria
Given cart has 2x Widget ($10) and 1x Gadget ($25)
When calculating total
Then subtotal is $45.00

Given cart subtotal is $100 with 10% discount code
When calculating total
Then discount is $10.00 and new subtotal is $90.00

Given cart is in California (7.25% tax)
When calculating total
Then tax is calculated on post-discount subtotal

Given cart subtotal exceeds $50
When calculating shipping
Then shipping is $0.00 (free shipping applied)

## Boundaries

### ✅ Always
- Round currency to 2 decimal places
- Apply discounts before tax
- Show line-item breakdown

### ⚠️ Ask First
- How to handle multiple discount codes
- Tax-exempt items handling
- International shipping rates

### 🚫 Never
- Allow negative totals
- Apply tax to shipping
- Stack percentage discounts

## Out of Scope
- Gift cards
- Loyalty points
- Subscription discounts
```

**Task Breakdown:**

1. Calculate subtotal from line items
2. Apply percentage discount to subtotal
3. Calculate tax on discounted amount
4. Determine shipping cost with free threshold
5. Combine into final total with breakdown

**First Task Test:**

```typescript
describe('CartCalculator.subtotal', () => {
  test('sums price × quantity for all items', () => {
    const cart = new Cart([
      { name: 'Widget', price: 10.00, quantity: 2 },
      { name: 'Gadget', price: 25.00, quantity: 1 }
    ]);
    expect(cart.subtotal()).toBe(45.00);
  });

  test('returns 0 for empty cart', () => {
    const cart = new Cart([]);
    expect(cart.subtotal()).toBe(0.00);
  });

  test('handles fractional prices correctly', () => {
    const cart = new Cart([
      { name: 'Item', price: 10.99, quantity: 3 }
    ]);
    expect(cart.subtotal()).toBe(32.97);
  });
});
```

## Tools and Resources

- **GitHub Spec-Kit**: Open source toolkit for spec-driven development workflows
- **Gherkin/Cucumber**: Given/When/Then syntax for acceptance criteria
- **Jest/Vitest/pytest**: Testing frameworks for TDG workflow
- **Agentic Coding Handbook**: Community resource for AI-assisted TDD

## Limitations

- Requires discipline to maintain specs alongside code
- Initial overhead higher than "just coding" (pays off in reduced rework)
- Not ideal for exploratory/prototype work where requirements are genuinely unknown
- Specs can become stale if team doesn't commit to updates

## Related Skills

- **Code Review**: Review implementations against specifications
- **Test-Driven Development**: Deep dive into TDD mechanics
- **API Design**: Designing contract-first APIs

## Compatibility

- **Claude Models**: All Claude 3+ models, Sonnet 4 or Opus 4 recommended
- **Interfaces**: Claude.ai, API, Claude Code
- **Minimum API Version**: Any

## Author

Claude Toolkit Community

## Version

- **Created**: 2025-01-18
- **Last Updated**: 2025-01-18
- **Version**: 1.0.0

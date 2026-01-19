---
name: progress-writing
description: Write effective progress files that enable continuity across sessions and agent handoffs in spec-driven development. Use when starting work sessions, resuming after breaks, completing tasks or milestones, encountering blockers, handing off work, recording test results, or documenting issues and resolutions. Triggers include "progress log", "session log", "write progress", "handoff notes", "work log", or when capturing session-by-session work history for continuity.
---

# Progress Writing Skill

Write effective progress files that enable continuity across sessions and agent handoffs in spec-driven development.

## Overview

This skill guides Claude through creating progress files - the session-by-session work logs that capture what happened, what was verified, and what comes next. Progress files are the critical handoff mechanism that enables work to continue seamlessly across context windows, between agents, or after breaks.

Unlike notes (which capture durable context like decisions and research), progress files are append-only records of sessions. They answer: "What happened in this work session, and where should the next session pick up?"

## When to Use

- Starting a work session on a spec-driven feature
- Resuming work after a context switch or break
- Completing a task or reaching a milestone
- Encountering blockers that need documentation
- Handing off work to another agent or developer
- Recording test results and verification outputs
- Documenting issues and their resolutions

## Prerequisites

- A feature with the spec-driven-dev artifact structure
- Access to the feature's spec.md and plan.md
- Previous progress logs (if resuming work)
- Ability to run tests and capture outputs

## Instructions

### Progress File Anatomy

A progress file captures a complete work session:

```
┌─────────────────────────────────────────────────────────┐
│  Header                                                 │
│  Session number, date, author, tasks worked, duration   │
├─────────────────────────────────────────────────────────┤
│  Summary                                                │
│  2-3 sentences: What was accomplished, key outcomes     │
├─────────────────────────────────────────────────────────┤
│  Work Log                                               │
│  Timestamped activities with descriptions               │
├─────────────────────────────────────────────────────────┤
│  Test Results                                           │
│  Actual test output (not summaries)                     │
├─────────────────────────────────────────────────────────┤
│  Build Output                                           │
│  Compilation/build results if relevant                  │
├─────────────────────────────────────────────────────────┤
│  Code Changes                                           │
│  Files modified with brief descriptions                 │
├─────────────────────────────────────────────────────────┤
│  Issues Encountered                                     │
│  Problems, investigations, resolutions                  │
├─────────────────────────────────────────────────────────┤
│  Handoff Notes                                          │
│  CRITICAL: Context for the next session                 │
├─────────────────────────────────────────────────────────┤
│  Next Steps                                             │
│  Specific actions for continuation                      │
└─────────────────────────────────────────────────────────┘
```

### When to Create a New Progress File

Create a new session log when:

| Trigger | Rationale |
|---------|-----------|
| Starting work on a feature | Fresh context, clean state |
| Resuming after a break (>2-4 hours) | Context may have changed |
| Different agent picks up work | New agent documents their session |
| Significant milestone reached | Good checkpoint for history |
| Major blocker encountered | Document the situation for handoff |
| Context window limit approaching | Ensure work is captured before reset |

**The golden rule**: When in doubt, create a new session log. It's better to have more granular history than to lose context.

### Session Numbering

Use zero-padded session numbers for consistent sorting:
- `session-001.md`
- `session-002.md`
- `session-010.md`

For long-running features (months), consider monthly grouping:
```
progress/
├── 2025-01/
│   ├── session-001.md
│   └── session-002.md
└── 2025-02/
    ├── session-003.md
    └── session-004.md
```

### Writing the Header

The header provides quick context for anyone scanning progress files:

```markdown
# Session 003: Implement JWT Authentication

**Date**: 2025-01-18
**Agent/Author**: claude-opus-4 (or developer name)
**Tasks Worked**: [03-auth-endpoints](../tasks/03-auth-endpoints.md)
**Duration**: ~2 hours
```

**Header Guidelines:**
- Session number matches the filename number
- Brief description captures the session's focus
- Link to actual task files (relative paths)
- Duration is approximate - helps estimate future work

### Writing the Summary

The summary is for quick scanning. Keep it to 2-3 sentences covering:
1. What was accomplished
2. Key outcome or state
3. Any blockers (if applicable)

**Good Summaries:**

```markdown
## Summary

Implemented JWT token generation and validation middleware. All unit tests
passing (12 tests). Integration tests revealed a token refresh edge case
that needs investigation next session.
```

```markdown
## Summary

Fixed the database connection pool exhaustion issue identified last session.
Root cause was missing connection cleanup in test fixtures. All integration
tests now pass with parallel execution enabled.
```

```markdown
## Summary

Blocked on OAuth integration - waiting for credentials from security team.
Used the time to improve test coverage for existing auth endpoints (coverage
up from 78% to 94%). Documented the OAuth flow for when credentials arrive.
```

**Poor Summaries:**

```markdown
## Summary

Did some work on authentication.
```
(Too vague - what specifically?)

```markdown
## Summary

Today I started by reading through the spec and plan files to understand the
requirements, then I looked at the existing codebase to see how similar features
were implemented, after which I began implementing the JWT token generation
functionality using the jsonwebtoken library which I chose because...
```
(Too verbose - this belongs in the work log)

### Writing the Work Log

The work log provides a timeline of activities. Use timestamps and descriptive titles.

```markdown
## Work Log

### 10:30 - Started JWT implementation

Created `src/auth/jwt.ts` with token generation using jose library.
Followed the signing pattern from plan.md. Token includes:
- user_id claim
- email claim
- 7-day expiry per spec requirement NFR-2

### 11:15 - Added authentication middleware

Created `src/middleware/auth.ts` for request authentication.
Integrated with existing request context pattern.

### 11:45 - Wrote unit tests

Added tests for:
- Token generation with valid claims
- Token validation (happy path)
- Expired token rejection
- Invalid signature rejection
- Malformed token handling

### 12:15 - Ran integration tests, found issue

Integration test `test_logout_invalidates_token` fails.
Issue: JWT tokens remain valid after logout because JWTs are stateless.
This was anticipated in the plan - needs Redis token blacklist (task-04).
```

**Work Log Guidelines:**
- Timestamps don't need to be exact - approximate is fine
- Focus on what was done, not process narration
- Include file paths for code changes
- Note decisions made and their rationale
- Flag issues discovered for the Issues section

### Capturing Test Results

**This is critical**: Include actual test output, not summaries. Test output is evidence of state and invaluable for debugging.

```markdown
## Test Results

### Unit Tests

```
$ npm test -- --grep "auth"

  auth/jwt.ts
    ✓ generates valid token with required claims (12ms)
    ✓ validates token with correct signature (8ms)
    ✓ rejects expired token (5ms)
    ✓ rejects token with invalid signature (4ms)
    ✓ rejects malformed token (3ms)

  auth/middleware.ts
    ✓ extracts user from valid token (15ms)
    ✓ returns 401 for missing token (4ms)
    ✓ returns 401 for invalid token (5ms)

  8 passing (51ms)
```

**Status**: ✅ All passing
```

### Integration Tests

```
$ npm run test:integration -- --grep "auth"

  Auth Flow
    ✓ user can register with valid email (234ms)
    ✓ user can login with correct password (189ms)
    ✓ protected endpoint rejects unauthenticated request (45ms)
    ✓ protected endpoint accepts valid token (67ms)
    ✗ logout invalidates token
      AssertionError: Expected 401 but got 200
      Token still accepted after logout

  4 passing, 1 failing (623ms)
```

**Status**: ⚠️ 1 failing

**Notes**: Logout test failure is expected - JWT statelessness issue.
Requires token blacklist implementation in task-04.
```

**Test Result Guidelines:**
- Paste actual command and output
- Include failing test details with error messages
- Note whether failures are expected or unexpected
- Link to related tasks or issues

### Capturing Build Output

For compiled languages or build steps, capture the output:

```markdown
## Build Output

```
$ npm run build

> my-app@1.0.0 build
> tsc && vite build

vite v5.0.0 building for production...
✓ 156 modules transformed.
dist/index.html                   0.45 kB │ gzip:  0.29 kB
dist/assets/index-a1b2c3.css      8.23 kB │ gzip:  2.14 kB
dist/assets/index-d4e5f6.js     127.45 kB │ gzip: 41.23 kB
✓ built in 3.21s
```

**Status**: ✅ Success
**Bundle Size**: 127.45 kB (within 150 kB budget)
```

### Documenting Code Changes

Track what files were touched:

```markdown
## Code Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `src/auth/jwt.ts` | Added | Token generation and validation |
| `src/middleware/auth.ts` | Added | Request authentication middleware |
| `src/routes/protected.ts` | Modified | Added auth middleware to routes |
| `tests/unit/auth.test.ts` | Added | Unit tests for auth module |
| `tests/integration/auth.test.ts` | Modified | Added login flow tests |
```

### Documenting Issues Encountered

Issues are learning opportunities. Document them thoroughly:

```markdown
## Issues Encountered

### Token validation timing issue

**Problem**: Unit test `rejects expired token` was flaky - sometimes passing,
sometimes failing.

**Investigation**:
1. Added logging - saw token expiry was exactly at test time
2. Realized test was generating token with 1-second expiry
3. Test execution sometimes crossed the boundary

**Resolution**: Changed test to use 0-second expiry with explicit time mocking:
```typescript
jest.useFakeTimers();
const token = generateToken({ expiresIn: '1s' });
jest.advanceTimersByTime(2000);
expect(() => validateToken(token)).toThrow('Token expired');
```

### Database connection pool exhaustion

**Problem**: Integration tests failing with "connection pool exhausted" after
running 15+ tests.

**Investigation**:
1. Checked pool settings - max 10 connections
2. Added connection monitoring - saw connections not being released
3. Found test fixtures creating sessions but not closing them

**Resolution**: Added proper cleanup to test fixtures (see commit abc123)

**Status**: Resolved
```

For unresolved issues:

```markdown
### OAuth callback URL mismatch

**Problem**: Google OAuth returning "redirect_uri_mismatch" error in staging.

**Investigation**:
1. Verified callback URL in code matches Google Console
2. Checked environment variables - they look correct
3. Noticed staging uses different subdomain than configured

**Status**: Unresolved - need access to Google Console to add staging URL.
Blocked until security team updates OAuth config.

**Workaround**: Can test OAuth flow locally where URLs match.
```

### Writing Handoff Notes

**Handoff notes are the most important section for continuity**. They tell the next session exactly where to pick up.

```markdown
## Handoff Notes

### Current State
- JWT authentication is implemented and unit tested
- Middleware integrated with protected routes
- One integration test failing (expected - needs token blacklist)
- All code committed to branch `feature/user-auth`

### Blockers
- None - ready to continue with task-04

### Context for Next Session
- Token blacklist design is in `notes/decision-token-blacklist.md`
- Plan specifies Redis for blacklist storage (see plan.md Phase 2)
- Consider using SET with TTL matching token expiry

### Files to Focus On
- `src/auth/blacklist.ts` - Create this for token blacklist
- `tests/integration/auth.test.ts` - Uncomment blacklist tests
- `src/auth/jwt.ts` - Add blacklist check to validateToken

### Environment Notes
- Redis running locally on default port
- Test Redis database is index 1 (to avoid conflicts)

### Don't Forget
- Run full test suite before marking task-03 complete
- Update task-03 status to DONE when integration test passes
```

**Handoff Note Sections:**

| Section | Purpose |
|---------|---------|
| Current State | Where things stand right now |
| Blockers | What's preventing progress (if anything) |
| Context for Next Session | Background needed to continue |
| Files to Focus On | Where to look first |
| Environment Notes | Setup or config reminders |
| Don't Forget | Important items easy to overlook |

### Writing Next Steps

Next steps are specific, actionable items:

```markdown
## Next Steps

- [ ] Implement Redis token blacklist (task-04)
- [ ] Add blacklist check to validateToken function
- [ ] Update logout endpoint to blacklist token
- [ ] Fix failing integration test
- [ ] Consider: Add token rotation for long-lived sessions
```

**Next Steps Guidelines:**
- Be specific - "implement X" not "continue work"
- Use checkbox format for trackability
- Distinguish required vs optional items
- Link to task files when relevant

## Examples

### Example 1: Feature Implementation Session

```markdown
# Session 005: Complete User Registration API

**Date**: 2025-01-18
**Agent/Author**: claude-opus-4
**Tasks Worked**: [02-user-registration](../tasks/02-user-registration.md)
**Duration**: ~3 hours

## Summary

Completed the user registration API endpoint with email validation, password
hashing, and duplicate detection. All 24 tests passing. Ready for code review.

## Work Log

### 09:00 - Reviewed spec requirements

Checked spec.md for registration requirements:
- FR-1: Register with email/password
- NFR-1: bcrypt with cost factor 12
- NFR-3: Rate limiting (5 attempts/minute)

### 09:30 - Implemented registration endpoint

Created `POST /api/auth/register` in `src/routes/auth.ts`:
- Email format validation using validator library
- Password strength check (min 8 chars, 1 number, 1 special)
- bcrypt hashing with cost factor 12
- Duplicate email check with proper error response

### 10:15 - Added rate limiting

Implemented rate limiting middleware:
- Used sliding window with Redis
- 5 registration attempts per IP per minute
- Returns 429 with Retry-After header

### 10:45 - Wrote comprehensive tests

Added unit and integration tests:
- Valid registration flow
- Invalid email formats (12 variants)
- Weak password rejection
- Duplicate email handling
- Rate limiting behavior

### 11:30 - Fixed edge case with unicode emails

Discovered validator library rejects some valid unicode emails.
Switched to more permissive regex per RFC 6531.
Added test cases for unicode local parts.

## Test Results

### Unit Tests

```
$ npm test src/routes/auth.test.ts

  POST /api/auth/register
    ✓ registers user with valid email and password (45ms)
    ✓ returns 400 for invalid email format (12ms)
    ✓ returns 400 for weak password (8ms)
    ✓ returns 409 for duplicate email (23ms)
    ✓ hashes password with bcrypt (156ms)
    ✓ accepts unicode in email local part (15ms)

  Email validation
    ✓ accepts standard email (3ms)
    ✓ accepts email with plus addressing (2ms)
    ✓ accepts email with dots (2ms)
    ✓ accepts unicode local part (3ms)
    ✓ rejects email without @ (2ms)
    ✓ rejects email with spaces (2ms)
    ✓ rejects email with invalid TLD (2ms)

  Password validation
    ✓ accepts strong password (2ms)
    ✓ rejects password under 8 chars (2ms)
    ✓ rejects password without number (2ms)
    ✓ rejects password without special char (2ms)

  17 passing (285ms)
```

**Status**: ✅ All passing

### Integration Tests

```
$ npm run test:integration -- --grep "registration"

  Registration Flow
    ✓ complete registration creates user in database (234ms)
    ✓ registered user can login (189ms)
    ✓ duplicate registration returns 409 (45ms)
    ✓ rate limiting kicks in after 5 attempts (1203ms)
    ✓ rate limit resets after window expires (2045ms)
    ✓ returns proper validation errors (67ms)
    ✓ sends welcome email on successful registration (312ms)

  7 passing (4.1s)
```

**Status**: ✅ All passing

## Build Output

```
$ npm run build

✓ Built in 2.1s
No type errors
Bundle size: 132 kB (within budget)
```

**Status**: ✅ Success

## Code Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `src/routes/auth.ts` | Modified | Added register endpoint |
| `src/middleware/rateLimit.ts` | Added | Sliding window rate limiter |
| `src/validators/email.ts` | Added | RFC 6531 compliant validation |
| `src/validators/password.ts` | Added | Password strength checker |
| `tests/unit/auth.test.ts` | Modified | Added registration tests |
| `tests/integration/registration.test.ts` | Added | E2E registration tests |

## Issues Encountered

### Unicode email validation

**Problem**: validator library's isEmail() rejects valid unicode emails
like `用户@example.com` which are valid per RFC 6531.

**Investigation**:
1. Tested with various unicode emails
2. Found validator uses older RFC 5321 which doesn't support unicode
3. Checked codebase - we explicitly want to support international users

**Resolution**: Created custom email validator using RFC 6531 compliant regex.
Added specific test cases for unicode emails.

## Handoff Notes

### Current State
- User registration fully implemented and tested
- Rate limiting working correctly
- All 24 tests passing
- Code committed to `feature/user-auth` branch
- Ready for code review

### Next Task
- Task-03: Login endpoint (depends on this task)
- Login can begin immediately - User model is complete

### Files Modified This Session
- All changes in single commit: `abc123f`
- PR ready: #42

### Verification Performed
- [x] Unit tests passing
- [x] Integration tests passing
- [x] Manual testing via Postman
- [x] Rate limiting verified
- [x] Build succeeds
- [x] No type errors

## Next Steps

- [ ] Create PR for code review
- [ ] Address review feedback
- [ ] Begin task-03 (login endpoint) after merge
- [ ] Consider: Add CAPTCHA for registration (noted in spec as future)
```

### Example 2: Debugging Session

```markdown
# Session 008: Debug Payment Processing Timeout

**Date**: 2025-01-18
**Agent/Author**: claude-opus-4
**Tasks Worked**: [BUG-payment-timeout](../tasks/BUG-payment-timeout.md)
**Duration**: ~2.5 hours

## Summary

Investigated and fixed payment processing timeout issue. Root cause was
missing database index on `transactions.user_id`. Query time reduced from
45 seconds to 12ms. Deployed fix to staging for validation.

## Work Log

### 14:00 - Reproduced the issue

Confirmed timeout in staging:
- Payment requests timing out after 30 seconds
- Error: "Payment processing failed - please try again"
- Affects ~15% of users (those with 100+ transactions)

### 14:30 - Added instrumentation

Added timing logs to payment flow:
```
[14:32:15] Payment initiated for user_123
[14:32:15] Fetching user transactions...
[14:33:00] Transaction fetch complete (45.2s) ← BOTTLENECK
[14:33:00] Request timed out
```

### 15:00 - Analyzed slow query

Found the problematic query:
```sql
SELECT * FROM transactions
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT 10
```

EXPLAIN ANALYZE showed full table scan:
```
Seq Scan on transactions (cost=0.00..125432.00)
  Filter: (user_id = 'user_123')
  Rows Removed by Filter: 2847293
  Actual Time: 45234.123ms
```

### 15:30 - Identified missing index

Table has 2.8M rows but no index on user_id:
```sql
\d transactions
-- No index on user_id column
```

### 15:45 - Applied fix

Created index:
```sql
CREATE INDEX CONCURRENTLY idx_transactions_user_id
ON transactions(user_id);
```

Used CONCURRENTLY to avoid locking production.

### 16:15 - Verified fix

After index creation:
```
Index Scan using idx_transactions_user_id (cost=0.42..8.44)
  Index Cond: (user_id = 'user_123')
  Actual Time: 0.012ms
```

Query time: 45,234ms → 0.012ms (3.7 million times faster)

## Test Results

### Load Test (Staging)

```
$ artillery run payment-load-test.yml

All virtual users finished
Summary report @ 16:25:00

  Scenarios launched:  100
  Scenarios completed: 100
  Requests completed:  100

  Response time (msec):
    min: 45
    max: 234
    median: 89
    p95: 156
    p99: 201

  Codes:
    200: 100
```

**Status**: ✅ All requests successful (previously 15% timeout)

### Regression Tests

```
$ npm run test:integration -- --grep "payment"

  Payment Processing
    ✓ processes payment for new user (234ms)
    ✓ processes payment for user with history (189ms)
    ✓ handles payment for user with 1000+ transactions (201ms)
    ✓ maintains ACID properties (445ms)

  4 passing (1.1s)
```

**Status**: ✅ All passing

## Code Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `migrations/027_add_transaction_user_index.sql` | Added | Index migration |
| `src/services/payment.ts` | Modified | Added query timing logs |
| `tests/load/payment-load-test.yml` | Added | Load test config |

## Issues Encountered

### Why wasn't this caught earlier?

**Investigation**:
1. Local dev only had ~100 transactions per user
2. Staging was refreshed from prod 6 months ago (before growth)
3. No load tests covering high-transaction users

**Resolution**:
1. Added load test to CI pipeline
2. Created ticket to refresh staging data monthly
3. Added query performance monitoring alerts

## Handoff Notes

### Current State
- Fix deployed to staging, verified working
- Migration ready for production deployment
- Load test added to prevent regression

### Production Deployment
- Migration uses CONCURRENTLY - safe for prod
- Estimated index creation time: ~5 minutes
- No downtime required
- Monitor `pg_stat_user_indexes` after deployment

### Monitoring Added
- Datadog alert: Query time > 1s on transactions table
- Will catch similar issues before they become outages

### Remaining Risk
- Other tables may have similar issues
- Created ticket #567 for database index audit

## Next Steps

- [ ] Deploy migration to production (scheduled: tonight 2am)
- [ ] Monitor index creation progress
- [ ] Verify production query times post-deployment
- [ ] Close bug ticket after production verification
- [ ] Complete database index audit (ticket #567)

## References

- [PostgreSQL EXPLAIN documentation](https://www.postgresql.org/docs/current/using-explain.html)
- [Index creation best practices](https://wiki.postgresql.org/wiki/Index_Maintenance)
- Bug ticket: JIRA-1234
```

### Example 3: Blocked Session

```markdown
# Session 012: OAuth Integration (Blocked)

**Date**: 2025-01-18
**Agent/Author**: claude-opus-4
**Tasks Worked**: [05-oauth-integration](../tasks/05-oauth-integration.md)
**Duration**: ~1.5 hours

## Summary

Attempted to implement Google OAuth integration but blocked on missing
credentials. Used session time productively to document OAuth flow,
prepare implementation, and improve test coverage for existing auth code.

## Work Log

### 10:00 - Started OAuth implementation

Read through OAuth flow in plan.md. Implementation approach:
1. Add Google OAuth strategy to passport.js
2. Create callback handler
3. Link or create user on successful auth
4. Issue JWT for session

### 10:30 - Discovered missing credentials

Checked environment for Google OAuth credentials:
```bash
$ echo $GOOGLE_CLIENT_ID
(empty)
$ echo $GOOGLE_CLIENT_SECRET
(empty)
```

Checked 1Password vault - no Google OAuth credentials found.
Messaged security team in Slack.

### 10:45 - Documented OAuth flow while waiting

Created `notes/oauth-flow.md` documenting:
- Full OAuth authorization code flow
- User linking strategy (email match)
- Account creation for new users
- Token exchange process

### 11:15 - Improved existing auth test coverage

While blocked, improved test coverage:
- Added edge case tests for JWT validation
- Added tests for token refresh scenarios
- Coverage increased from 87% to 94%

## Test Results

### Auth Module Coverage (Improved)

```
$ npm test -- --coverage src/auth/

--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |   94.23 |    91.45 |   95.00 |   94.23 |
 jwt.ts             |   96.00 |    94.00 |  100.00 |   96.00 |
 middleware.ts      |   92.00 |    88.00 |   90.00 |   92.00 |
 password.ts        |   95.00 |    92.00 |  100.00 |   95.00 |
--------------------|---------|----------|---------|---------|
```

**Status**: ✅ Coverage improved (was 87%)

## Code Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `notes/oauth-flow.md` | Added | OAuth implementation documentation |
| `tests/unit/jwt.test.ts` | Modified | Added edge case tests |
| `src/auth/oauth.ts` | Added | Skeleton for OAuth (blocked) |

## Issues Encountered

### Missing OAuth credentials

**Problem**: Cannot proceed with OAuth integration without Google credentials.

**Investigation**:
1. Checked all environment files and vaults
2. Found no existing Google OAuth application
3. Security team needs to create Google Cloud project

**Status**: BLOCKED
**Blocker**: Waiting for security team to provision credentials
**Expected Resolution**: ~2 business days per security team

**Workaround**: None for actual OAuth testing. Can test with mocked
OAuth responses for unit tests.

## Handoff Notes

### Current State
- Task-05 is BLOCKED
- OAuth flow documented in `notes/oauth-flow.md`
- Skeleton code ready in `src/auth/oauth.ts`
- Test coverage improved while waiting

### Blocker Details
- Need: Google OAuth Client ID and Secret
- Contact: @security-team in #security Slack channel
- Ticket: SEC-456
- ETA: Tuesday Jan 21

### What Can Be Done While Blocked
- Task-06 (frontend auth) can proceed with mock OAuth
- Task-07 (password reset) has no OAuth dependency
- Continue improving test coverage

### When Unblocked
1. Get credentials from 1Password (security will add)
2. Add to `.env.local` and deployment secrets
3. Complete OAuth implementation (~2-3 hours remaining)
4. Test with real Google account

### Files Ready for OAuth
- `src/auth/oauth.ts` - Skeleton ready, just needs credentials
- `tests/integration/oauth.test.ts` - Test structure ready
- `notes/oauth-flow.md` - Implementation guide

## Next Steps

- [ ] Wait for security team (ticket SEC-456)
- [ ] Proceed with task-06 or task-07 while blocked
- [ ] Once credentials available, complete OAuth implementation
- [ ] Consider: Add mock OAuth provider for local development
```

## Best Practices

### Do's

- **Create new session for each work period** - Don't append to old sessions
- **Capture actual command output** - Copy/paste real terminal output
- **Write handoff notes immediately** - Before context is lost
- **Be specific in next steps** - Actionable items, not vague goals
- **Document issues thoroughly** - Future sessions will thank you
- **Link to related artifacts** - Tasks, notes, decisions
- **Include timestamps** - Helps reconstruct the session timeline
- **Note environment details** - Commands, versions, configs

### Don'ts

- **Don't edit old progress files** - They're append-only history
- **Don't summarize test output** - Paste the actual results
- **Don't skip handoff notes** - They're the most critical section
- **Don't wait to write progress** - Document as you go
- **Don't include sensitive data** - Redact credentials, tokens
- **Don't duplicate notes content** - Reference notes, don't copy
- **Don't leave status ambiguous** - Clear passing/failing/blocked

## Common Pitfalls

### Missing Test Output

Don't write:
```markdown
## Test Results
All tests passing.
```

Do write:
```markdown
## Test Results

```
$ npm test
  45 passing (2.3s)
```

**Status**: ✅ All passing
```

### Vague Handoff Notes

Don't write:
```markdown
## Handoff Notes
Continue working on the feature.
```

Do write:
```markdown
## Handoff Notes

### Current State
- Task-03 is 60% complete
- Token generation works, validation has edge case bug

### Context for Next Session
- Bug: tokens with colons in claims fail validation
- Relevant test: `test_special_chars_in_claims`
- Likely fix: URL-encode claims before signing

### Files to Focus On
- `src/auth/jwt.ts:45` - validateToken function
- `tests/unit/jwt.test.ts` - failing test case
```

### Forgetting the Why

Don't write:
```markdown
### 11:00 - Changed email validation
Modified email regex.
```

Do write:
```markdown
### 11:00 - Fixed unicode email validation
Changed from validator.isEmail() to custom RFC 6531 regex.
Validator library only supports ASCII emails per RFC 5321,
but we need to support international users with unicode addresses.
```

### Skipping Issues Section

Even successful sessions often have learnings. Document them:

```markdown
## Issues Encountered

### No major issues

This session went smoothly. Minor learnings:
- Database seeding takes 30s - consider parallel seeding
- TypeScript strict mode caught 3 potential null issues
- Integration tests require Redis - added to README
```

## Quality Checklist

Before ending a session, verify:

**Header**
- [ ] Session number matches filename
- [ ] Date is accurate
- [ ] Tasks worked are linked
- [ ] Duration is estimated

**Summary**
- [ ] 2-3 sentences covering key outcomes
- [ ] Mentions blockers if any
- [ ] Would make sense to someone scanning

**Work Log**
- [ ] Timestamps for major activities
- [ ] Specific file paths mentioned
- [ ] Decisions and rationale included

**Test Results**
- [ ] Actual command output included
- [ ] Clear passing/failing/blocked status
- [ ] Notes explaining any failures

**Handoff Notes** (CRITICAL)
- [ ] Current state clearly described
- [ ] Blockers documented with details
- [ ] Context for next session provided
- [ ] Specific files to focus on listed
- [ ] Nothing important left unsaid

**Next Steps**
- [ ] Specific, actionable items
- [ ] Checkbox format for tracking
- [ ] Links to tasks where relevant

## Output Format

Use this template for consistent progress files:

```markdown
# Session [NNN]: [Brief Description]

**Date**: YYYY-MM-DD
**Agent/Author**: [Identifier]
**Tasks Worked**: [Links to task files]
**Duration**: [Approximate time]

## Summary

[2-3 sentences: What was accomplished, key outcomes, any blockers]

## Work Log

### [HH:MM] - [Activity Title]

[Description with specific details, file paths, decisions]

### [HH:MM] - [Activity Title]

[Description]

## Test Results

### Unit Tests

```
[Actual test output]
```

**Status**: ✅ All passing | ⚠️ X failing | ❌ Build broken

### Integration Tests

```
[Actual test output]
```

**Status**: [Status with notes]

## Build Output

```
[Build/compile output if relevant]
```

**Status**: [Status]

## Code Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `path/to/file` | Added/Modified/Deleted | [Brief description] |

## Issues Encountered

### [Issue Title]

**Problem**: [Clear description]
**Investigation**: [Steps taken]
**Resolution**: [How fixed] | **Status**: Unresolved - [what's needed]

## Handoff Notes

### Current State
[Where things stand]

### Blockers
[What's preventing progress, or "None"]

### Context for Next Session
[Background needed to continue]

### Files to Focus On
[Where to look first]

## Next Steps

- [ ] [Specific action]
- [ ] [Specific action]

## References

- [Links to relevant resources]
```

## Limitations

- Progress quality depends on discipline to write during/after sessions
- Cannot replace real-time collaboration for complex issues
- Test output can become verbose for large test suites
- May become stale if work continues without logging

## Related Skills

- **Spec-Driven Development**: Creates the artifact structure progress files live in
- **Notes Writing**: For durable context (decisions, research) vs session logs
- **Task Writing**: Defines the work that progress files track
- **Code Review**: Review implementations with progress file context

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

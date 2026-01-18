# Progress Writing Skill

Write effective progress files that enable continuity across sessions and agent handoffs.

## Overview

Progress files are the session-by-session work logs that capture what happened, what was verified, and what comes next. They're the critical handoff mechanism that enables work to continue seamlessly across context windows, between agents, or after breaks.

## When to Use

- Starting or completing a work session on a spec-driven feature
- Encountering blockers that need documentation
- Handing off work to another agent or developer
- Recording test results and verification outputs
- Documenting issues and their resolutions

## Quick Start

### 1. Create a New Session File

```bash
# In your feature's progress directory
touch agentdocs/features/my-feature/progress/session-001.md
```

### 2. Write the Header

```markdown
# Session 001: [Brief Description]

**Date**: 2025-01-18
**Agent/Author**: [Your identifier]
**Tasks Worked**: [Links to task files]
**Duration**: ~2 hours
```

### 3. Write the Summary

2-3 sentences covering what was accomplished and any blockers.

### 4. Log Your Work

Timestamped activities with specific details.

### 5. Capture Test Results

**Critical**: Paste actual command output, not summaries.

### 6. Write Handoff Notes

The most important section - context for the next session.

### 7. List Next Steps

Specific, actionable items for continuation.

## Key Sections

| Section | Purpose | Priority |
|---------|---------|----------|
| Summary | Quick overview of session | High |
| Work Log | Timestamped activities | Medium |
| Test Results | Evidence of state | High |
| Issues | Problems and resolutions | High |
| Handoff Notes | Context for continuation | **Critical** |
| Next Steps | What to do next | High |

## Golden Rules

1. **Create new session for each work period** - Don't append to old files
2. **Capture actual output** - Paste real terminal results
3. **Write handoff notes immediately** - Before context is lost
4. **Be specific** - File paths, line numbers, exact errors

## Example Summary

```markdown
## Summary

Implemented JWT token generation and validation middleware. All 12 unit
tests passing. Integration tests revealed a token refresh edge case that
needs investigation next session.
```

## Example Handoff Notes

```markdown
## Handoff Notes

### Current State
- Task-03 is 80% complete
- Token generation works, validation has edge case bug

### Context for Next Session
- Bug in `src/auth/jwt.ts:45` - tokens with colons fail
- Relevant test: `tests/unit/jwt.test.ts::test_special_chars`

### Files to Focus On
- `src/auth/jwt.ts` - Fix claim encoding
- `tests/unit/jwt.test.ts` - Add more edge cases
```

## Related Skills

- **Spec-Driven Development**: Creates the artifact structure
- **Notes Writing**: For durable context (decisions, research)
- **Task Writing**: Defines work that progress files track

## Resources

- [SKILL.md](SKILL.md) - Complete skill documentation with examples

# Notes Writing Skill

Write clear development notes that document what was built, decisions made, and verification performed.

## Quick Start

Use this skill when you complete work and need to document what was done, why decisions were made, and how it was verified.

### Basic Notes Template

```markdown
# Development Notes: [Brief Title]

## Summary
[1-2 sentences: what was built/changed]

## Approach
[Technical approach and key decisions]

## Verification
[Tests added, manual testing performed]

## Follow-ups
- [ ] [Items for future work]
```

### The Complete Workflow

```
Spec → Plan → Task → Notes
(what)  (how)  (track) (done)
```

Notes are the final artifact - documenting the completed work.

### What to Include

| Section | Purpose |
|---------|---------|
| Summary | Quick overview of work done |
| Requirements | Map to spec requirements addressed |
| Approach | Technical decisions and rationale |
| Deviations | What changed from the plan and why |
| Verification | How correctness was confirmed |
| Follow-ups | Technical debt and future work |

### Notes Length Guide

| Work Type | Length |
|-----------|--------|
| Simple bug fix | 3-5 lines |
| Single task | Half page |
| Multi-task feature | 1-2 pages |
| Complex refactoring | 1-2 pages |

### The Most Important Part

**Document the "why" not just the "what."**

Future readers can see the code. They can't see your reasoning.

## Full Documentation

See [SKILL.md](./SKILL.md) for complete instructions, examples, and best practices.

# Plan Writing Skill

Write high-quality implementation plans that break down complex work into actionable steps.

## Quick Start

1. Load the skill by referencing `skills/examples/plan-writing/SKILL.md`
2. Provide a specification or description of the work to be done
3. Claude will create a detailed implementation plan with steps, risks, and checkpoints

## Example Usage

```
You: I have a spec for adding user notification preferences. Create an
     implementation plan for this feature.

Claude: [Follows SKILL.md to create comprehensive plan with:
        - Affected components analysis
        - Technical approach decisions
        - Phased implementation steps with dependencies
        - Risk assessment and mitigations
        - Rollback strategy
        - Success criteria]
```

## What This Skill Covers

- **Feature Plans**: Breaking down specs into implementation steps
- **Refactoring Plans**: Safe extraction and restructuring
- **Migration Plans**: Incremental transitions between systems
- **Risk Assessment**: Identifying and mitigating technical risks

## Key Features

- Step decomposition guidelines (atomic, testable, ordered)
- Dependency mapping between steps
- Risk assessment matrix
- Rollback strategy templates
- Traceability to spec requirements

## Workflow Integration

```
Spec Writing     →    Plan Writing       →    Spec-Driven Dev
────────────────────────────────────────────────────────────
Define WHAT         Define HOW to           Execute the plan
to build            approach it             systematically
```

## Related Skills

- **Spec Writing**: Create specifications that plans implement
- **Spec-Driven Development**: Execute plans systematically

## Full Documentation

See [SKILL.md](./SKILL.md) for complete instructions, examples, and best practices.

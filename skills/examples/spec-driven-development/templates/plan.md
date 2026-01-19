# Implementation Plan: [Feature Name]

**Spec**: [spec.md](spec.md)
**Status**: Draft | In Progress | Complete
**Last Updated**: YYYY-MM-DD

## Approach Summary

[1-2 paragraph summary of the overall implementation approach. Explain the key architectural decisions and why this approach was chosen.]

## Architecture

### Components

| Component | Purpose | New/Modified |
|-----------|---------|--------------|
| [Component Name] | [What it does] | New |
| [Component Name] | [What it does] | Modified |
| [Component Name] | [What it does] | New |

### Data Model

[Describe the data structures, database schema, or state management approach]

```sql
-- Example schema (adjust language as needed)
CREATE TABLE example (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### API Design

[Describe the API endpoints, interfaces, or contracts]

```
METHOD /api/endpoint
METHOD /api/endpoint/:id
METHOD /api/endpoint/:id/action
```

### System Diagram

[Optional: ASCII diagram or link to diagram showing component relationships]

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Client  │────▶│   API   │────▶│   DB    │
└─────────┘     └─────────┘     └─────────┘
```

## Implementation Phases

### Phase 1: [Phase Name]

**Goal**: [What this phase accomplishes]

- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

### Phase 2: [Phase Name]

**Goal**: [What this phase accomplishes]

- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

### Phase 3: [Phase Name]

**Goal**: [What this phase accomplishes]

- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| [What needed deciding] | [Selected option] | [Why this was chosen] |
| [What needed deciding] | [Selected option] | [Why this was chosen] |
| [What needed deciding] | [Selected option] | [Why this was chosen] |

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| [Potential risk] | High/Medium/Low | High/Medium/Low | [How to address] |
| [Potential risk] | High/Medium/Low | High/Medium/Low | [How to address] |

## Testing Strategy

### Unit Tests

- [What to test at the unit level]
- [Key functions or components to cover]

### Integration Tests

- [What to test at the integration level]
- [System boundaries to verify]

### End-to-End Tests

- [Critical user flows to test]
- [Happy path and error scenarios]

## Rollout Plan

1. **[Stage 1]**: [Description, e.g., Deploy behind feature flag]
2. **[Stage 2]**: [Description, e.g., Enable for internal users]
3. **[Stage 3]**: [Description, e.g., Gradual rollout 10% → 50% → 100%]

## Success Metrics

- [Metric 1]: [Target value or threshold]
- [Metric 2]: [Target value or threshold]
- [Metric 3]: [Target value or threshold]

## Changelog

### YYYY-MM-DD

- Initial plan created

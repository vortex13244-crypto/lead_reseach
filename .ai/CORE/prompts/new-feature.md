# Prompt: New Feature

> **Purpose:** Design and implement a new feature following best practices from requirements through testing.
> **Use When:** Building a new feature from a specification, user story, or product request.

---

## Prompt Template

```
You are a Senior Software Engineer implementing a new feature. Follow a structured approach from understanding requirements through verified implementation.

## Feature Specification

- **Feature Name:** [name]
- **Feature ID:** [FEAT-XXX, if tracked]
- **Description:** [2-3 sentences describing what this feature does]
- **User Story:** As a [persona], I want to [action], so that [benefit].
- **Acceptance Criteria:**
  - [ ] Given [context], when [action], then [expected result]
  - [ ] Given [context], when [action], then [expected result]
- **Non-Goals:** [What this feature explicitly does NOT do]
- **Design Mockup:** [Link or description, if available]

## Implementation Process

### Phase 1: Analysis

Before writing any code:

1. **Identify affected modules** — Which parts of the system will this feature touch?
2. **Check for existing patterns** — Is there a similar feature already implemented? Follow the same patterns.
3. **Identify dependencies** — What other features, APIs, or libraries does this depend on?
4. **Define the data model** — What new data entities or schema changes are needed?
5. **Define the API contract** — What endpoints will be added/modified? Specify request/response shapes.
6. **Identify edge cases** — What happens with:
   - Empty input
   - Invalid input
   - Concurrent access
   - Network failures
   - Permission boundaries
   - Maximum scale (1000x normal)

### Phase 2: Implementation Plan

Provide a detailed implementation plan:

1. **Database changes** — Migrations, new tables/columns, indexes
2. **Backend changes** — Services, controllers, validators, repositories
3. **API changes** — New/modified endpoints with request/response schemas
4. **Frontend changes** — Components, state, routing, data fetching
5. **Integration points** — External APIs, events, notifications
6. **Configuration** — New env vars, feature flags

### Phase 3: Implementation

For each component:

1. Write the implementation following project standards:
   - [standards/code-style.md](../standards/code-style.md)
   - [standards/naming.md](../standards/naming.md)
   - [standards/folder-structure.md](../standards/folder-structure.md)
2. Handle all error paths explicitly.
3. Add input validation at system boundaries.
4. Include structured logging for significant operations.
5. Use existing abstractions — do not reinvent patterns.

### Phase 4: Testing

1. **Unit tests** for all business logic:
   - Test the primary success path
   - Test at least 2 failure/edge cases per function
   - Test boundary conditions
2. **Integration tests** for API endpoints:
   - Test the complete request/response cycle
   - Test authentication/authorization
   - Test validation errors
3. **Frontend tests** (if applicable):
   - Test component rendering and interactions
   - Test loading, error, and empty states

### Phase 5: Documentation

1. Update API documentation (OpenAPI / inline docs)
2. Update [docs/features.md](../docs/features.md) with the feature entry
3. Add inline code comments for non-obvious logic

## Output Format

Structure your response as:

### Analysis
[Dependencies, affected modules, data model, API contract]

### Implementation Plan
[Ordered list of changes with file paths]

### Code
[Implementation with explanations for non-obvious decisions]

### Tests
[Test code with clear test names describing behavior]

### Documentation Updates
[API docs, feature entry, inline comments]

### Checklist
- [ ] All acceptance criteria met
- [ ] Edge cases handled
- [ ] Input validation implemented
- [ ] Error handling is explicit
- [ ] Tests cover happy path and failure modes
- [ ] No hardcoded values
- [ ] API documentation updated
- [ ] Feature entry added to features.md
```

---

## Usage Notes

- Reference [roles/backend.md](../roles/backend.md) and [roles/frontend.md](../roles/frontend.md) for role-specific guidance.
- Check [docs/architecture.md](../docs/architecture.md) to ensure the feature respects module boundaries.
- Update [docs/roadmap.md](../docs/roadmap.md) if the feature affects milestones.

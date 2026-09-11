# Role: Backend Developer

> **Scope:** Server-side logic, APIs, data access, background processing, and service integrations.
> **Activate When:** Implementing business logic, building APIs, designing data models, writing migrations, or integrating external services.
> **Related Roles:** [architect.md](./architect.md) · [frontend.md](./frontend.md) · [debugger.md](./debugger.md)

---

## Purpose

Build reliable, performant, and secure server-side systems. Transform business requirements into clean, testable backend code that other developers and AI agents can understand and extend.

---

## Responsibilities

1. **Implement business logic** — Translate product requirements into domain services with clear inputs, outputs, and error handling.
2. **Design and build APIs** — Create well-documented, versioned, and consistent API endpoints.
3. **Manage data** — Design schemas, write migrations, optimize queries, and enforce data integrity.
4. **Handle integrations** — Connect to external APIs, message queues, and third-party services with proper error handling and circuit breaking.
5. **Ensure security** — Implement authentication, authorization, input validation, and data protection.
6. **Write tests** — Maintain comprehensive unit and integration test coverage for all business-critical paths.
7. **Optimize performance** — Profile, measure, and improve response times, throughput, and resource utilization.

---

## Workflow

```
1. Understand the Task
   ├── Read the feature spec or bug report
   ├── Identify affected modules and data models
   ├── Check for existing patterns in the codebase
   └── Clarify edge cases before writing code

2. Design the Solution
   ├── Define API contract (endpoints, request/response schemas)
   ├── Plan data model changes (schema, migrations)
   ├── Identify side effects (emails, events, webhooks)
   └── Consider failure modes and rollback strategies

3. Implement
   ├── Write code following standards/code-style.md
   ├── Use existing abstractions — do not reinvent
   ├── Handle all error paths explicitly
   ├── Add input validation at the boundary
   └── Log meaningful events with structured data

4. Test
   ├── Unit test all business logic (pure functions first)
   ├── Integration test API endpoints
   ├── Test failure scenarios (network, DB, auth)
   └── Verify idempotency for mutating operations

5. Review & Ship
   ├── Self-review against the checklist below
   ├── Ensure migrations are backward-compatible
   ├── Update API documentation
   └── Monitor deployment for errors
```

---

## Principles

1. **Validate at the boundary, trust internally.** All external input is untrusted. Validate once at the API layer, then pass validated data through the system.
2. **Fail fast, fail loudly.** Do not swallow errors. Log them with context and propagate them to callers with meaningful messages.
3. **Idempotency by default.** Design mutating operations so they can be safely retried without unintended side effects.
4. **No business logic in controllers.** Controllers handle HTTP concerns (parsing, status codes). Business logic lives in services.
5. **Database is an implementation detail.** Use repository/data-access patterns. Business logic should not contain raw SQL or ORM-specific syntax.
6. **Prefer composition over inheritance.** Build behavior by composing small, focused functions and modules.

---

## Decision Making

### When to Create a New Service / Module

- The logic represents a distinct domain concept with its own lifecycle.
- Multiple consumers need the same business logic.
- The existing module exceeds ~500 lines and contains multiple responsibilities.

### When to Add Caching

- The data is read far more frequently than it is written (10:1+ ratio).
- The source query is expensive (> 100ms or joins multiple tables).
- Stale data is acceptable for the defined TTL window.
- **Always** define a cache invalidation strategy before adding a cache.

### When to Use Background Jobs vs. Synchronous Processing

| Factor              | Synchronous                     | Background Job                    |
| ------------------- | ------------------------------- | --------------------------------- |
| Response time target| < 500ms                         | > 500ms or unbounded              |
| User expects result | Immediately                     | Eventually (with notification)    |
| Failure handling    | Return error to caller          | Retry with dead-letter queue      |
| Side effects        | None or trivial                 | Email, webhook, file processing   |

---

## Best Practices

- Use environment variables for configuration. Never hardcode secrets, URLs, or feature flags.
- Implement structured logging with correlation IDs. Every log entry should be traceable to a request.
- Use database transactions for operations that modify multiple records atomically.
- Write migrations that are forward-only and backward-compatible. Never modify a deployed migration.
- Version APIs from day one. Use URL prefixing (`/api/v1/`) or header-based versioning.
- Set timeouts on all external calls (HTTP, database, cache). No call should block indefinitely.
- Use pagination for all list endpoints. Default to cursor-based pagination for large datasets.
- Return consistent error response shapes across all endpoints.

---

## Common Mistakes

| Mistake                                  | Why It Happens                       | Correction                                  |
| ---------------------------------------- | ------------------------------------ | ------------------------------------------- |
| Business logic in controllers            | Expedience, "it's just one line"     | Move to a service layer immediately          |
| Missing input validation                 | "The frontend validates it"          | Never trust the client — validate server-side|
| N+1 queries                              | Lazy loading without awareness       | Use eager loading or batch queries           |
| Swallowing exceptions                    | Empty catch blocks                   | Log, wrap, and re-throw with context         |
| Hardcoded configuration                  | "Just for now"                       | Use env vars from the start                  |
| No request logging                       | Overlooked during development        | Add middleware for all incoming requests      |
| Unbounded list responses                 | "We only have 10 records"            | Always paginate — data grows                 |
| Missing database indexes                 | Schema-first, queries-later thinking | Add indexes based on query patterns          |

---

## Checklist

Before submitting backend code:

- [ ] Input validation is implemented at the API boundary.
- [ ] All error paths return meaningful error messages and appropriate HTTP status codes.
- [ ] Database queries are optimized (no N+1, proper indexes, pagination).
- [ ] Sensitive data is not logged or exposed in API responses.
- [ ] Unit tests cover the primary success path and at least 2 failure paths.
- [ ] Integration tests verify the API contract.
- [ ] Database migrations are backward-compatible.
- [ ] API documentation is updated (OpenAPI / inline docs).
- [ ] Environment-specific values use configuration, not hardcoded strings.
- [ ] Timeouts are set on all external calls.

---

## References

- [standards/code-style.md](../standards/code-style.md) — Coding conventions and formatting.
- [standards/naming.md](../standards/naming.md) — Naming conventions.
- [docs/architecture.md](../docs/architecture.md) — System architecture and module boundaries.
- [docs/tech-stack.md](../docs/tech-stack.md) — Backend technology inventory.

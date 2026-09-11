# Checklist: Backend

> **Purpose:** Backend quality verification for APIs, services, and infrastructure code.
> **Related:** [roles/backend.md](../roles/backend.md) · [docs/api.md](../docs/api.md) · [docs/database.md](../docs/database.md)

---

## API Design

- [ ] Endpoints follow REST conventions (noun resources, proper HTTP methods)
- [ ] HTTP status codes are correct (200 OK, 201 Created, 204 No Content, 400, 401, 403, 404, 422, 500)
- [ ] Error responses follow standard format: `{ error: { code, message, details } }`
- [ ] List endpoints are paginated (no unbounded responses)
- [ ] API versioned if breaking changes possible (`/api/v1/`)
- [ ] OpenAPI/Swagger documented (or types generate the spec)

---

## Input Validation

- [ ] All request bodies validated with Zod/Pydantic schema
- [ ] All URL parameters validated and typed
- [ ] Validation errors return 422 with field-level error details
- [ ] File upload size and MIME type validated
- [ ] Maximum string lengths enforced

---

## Authentication & Authorization

- [ ] Authentication middleware applied to all protected routes
- [ ] Authorization checks verify resource ownership (not just auth)
- [ ] Admin operations require admin role check
- [ ] Token expiry handled gracefully (401 with clear message)

---

## Error Handling

- [ ] All async operations wrapped in try/catch
- [ ] No unhandled promise rejections
- [ ] Expected errors (404, 403, 422) thrown explicitly
- [ ] Unexpected errors logged with full context
- [ ] Stack traces not exposed to users in production

---

## Database

- [ ] No raw SQL with string interpolation (use ORM or parameterized)
- [ ] N+1 queries avoided (batch queries with `include` / `joinedload`)
- [ ] Transactions used for multi-table writes
- [ ] Large queries paginated
- [ ] Sensitive fields (`password`, `token`) never returned in responses
- [ ] `select` used to return only needed fields (not `SELECT *`)

---

## Performance

- [ ] No blocking I/O in request handlers (all I/O is async)
- [ ] Expensive operations cached in Redis
- [ ] Background jobs for non-critical operations (emails, analytics)
- [ ] Responses compressed
- [ ] Database queries optimized (EXPLAIN ANALYZE checked)

---

## Logging

- [ ] Request/response logged at INFO level (method, path, status, duration)
- [ ] Errors logged at ERROR level with full context
- [ ] No passwords, tokens, or PII in logs
- [ ] Structured logging (JSON format in production)
- [ ] Request IDs added to logs for tracing

---

## Testing

- [ ] Unit tests for service/business logic
- [ ] Integration tests for API endpoints
- [ ] Error cases tested (404, 403, 422, 500)
- [ ] Database integration tests use transactions (rolled back after test)

---

## Code Quality

- [ ] Service layer has no HTTP knowledge (no `req`/`res` in services)
- [ ] Repository pattern for database access (no ORM calls in controllers)
- [ ] Dependency injection for testability
- [ ] No circular imports
- [ ] Files ≤ 500 lines

---

*Related: [roles/backend.md](../roles/backend.md) · [docs/api.md](../docs/api.md) · [docs/security.md](../docs/security.md)*

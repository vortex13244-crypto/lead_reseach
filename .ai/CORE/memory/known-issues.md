# Known Issues

> **Purpose:** Catalog of known bugs, limitations, and workarounds. Read before debugging to avoid re-investigating resolved issues.
> **Related:** [active-context.md](active-context.md) · [../workflows/fix-bug.md](../workflows/fix-bug.md)

---

## Active Issues

### Critical

<!-- Issues that block features or cause data loss -->

| ID | Title | Symptom | Workaround | Assigned | Created |
|----|-------|---------|-----------|----------|---------|
| BUG-001 | <!-- title --> | <!-- symptom --> | <!-- workaround --> | <!-- owner --> | <!-- date --> |

### High

<!-- Issues that degrade UX or performance significantly -->

| ID | Title | Symptom | Workaround | Assigned | Created |
|----|-------|---------|-----------|----------|---------|

### Low

<!-- Minor issues, cosmetic bugs, minor UX issues -->

| ID | Title | Symptom | Workaround | Assigned | Created |
|----|-------|---------|-----------|----------|---------|

---

## Resolved Issues (Notable)

<!-- Only record bugs that reveal systemic problems or non-obvious behaviors -->

### [YYYY-MM-DD] Example: N+1 Query in User Dashboard

**Category:** Performance Bug
**Severity:** High
**Affected Files:** `src/api/users/route.ts`, `src/infrastructure/db/user-repository.ts`

**Symptom:** Dashboard page took 4+ seconds to load with 100+ users.

**Root Cause:** The user list query was fetching users, then making individual queries for each user's subscription status inside a loop — classic N+1 problem.

**Fix:** Joined the subscriptions table in the initial query and used `include` in Prisma to batch-load related data.

**Lesson:** Always check generated SQL queries in development mode. Use `prisma.$on('query', ...)` to log all DB queries during development.

---

## Known Limitations

<!-- System limitations that are by design or cannot be fixed currently -->

| Limitation | Impact | Reason | Mitigation |
|-----------|--------|--------|-----------|
| <!-- Limitation --> | <!-- Impact --> | <!-- Why it exists --> | <!-- How to work around it --> |

---

## Environment-Specific Issues

### Local Development
- <!-- e.g., Hot reload doesn't work with WebSocket connections — restart server manually -->

### Staging
- <!-- e.g., Email sending is disabled in staging — use Mailtrap -->

### Production
- <!-- e.g., File uploads limited to 10MB by Vercel proxy -->

---

## Issue Template

When adding a new issue:

```markdown
### [YYYY-MM-DD] Issue Title

**Category:** Bug | Performance | Security | UX | Infrastructure
**Severity:** Critical | High | Medium | Low
**Status:** Active | In Progress | Resolved
**Affected Files:** [file paths]

**Symptom:** What the user or system observes.
**Root Cause:** Why it happens (if known).
**Workaround:** How to work around it until fixed.
**Fix:** What needs to change (if known).
**Lesson:** What this teaches about the system.
```

---

*Last Updated: <!-- YYYY-MM-DD --> | Add issues as discovered, resolve them when fixed*

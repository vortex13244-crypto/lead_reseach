# Architecture Decisions

> **Purpose:** Log of all significant architectural decisions. Every ADR must document the context, options considered, and rationale. Never delete entries — mark superseded ones.
> **Related:** [../docs/architecture.md](../docs/architecture.md)

---

## Decision Log

| ID | Title | Status | Date | Impact |
|----|-------|--------|------|--------|
| ADR-001 | Separate reusable guidance from product context | Accepted | 2026-08-17 | High |

---

## ADR Format

```markdown
### ADR-NNN: Title

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNN
**Impact:** High | Medium | Low
**Deciders:** <!-- roles or names -->

#### Context
Why was this decision necessary? What problem does it solve?

#### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| Option A | ... | ... |
| Option B | ... | ... |

#### Decision
What was decided and why.

#### Consequences
- **Positive:** ...
- **Negative:** ...
- **Risks:** ...

#### Migration Path
How to migrate if this decision is reversed.
```

---

## Active Decisions

### ADR-001: Separate reusable guidance from product context

**Date:** 2026-08-17
**Status:** Accepted
**Impact:** High

#### Context
Carrying a completed product's context into another product causes incorrect assumptions and can expose stale or sensitive information.

#### Options Considered

| Option | Pros | Cons |
| --- | --- | --- |
| Copy the entire workspace to each project | Fast to start | Mixes product history and creates drift |
| Shared library plus a small project-local context | Reusable rules with clean product memory | Requires a short setup step |

#### Decision
Keep reusable guidance in this workspace. Copy `templates/project-context/` into every product repository as `.ai/` and retain that context with its code.

#### Consequences
- **Positive:** New products inherit quality standards without inheriting irrelevant history.
- **Negative:** Every new project needs its small context filled in before implementation.
- **Risks:** The shared library may drift; maintain `START-HERE.md` and `INDEX.md` when changing it.

### ADR-EXAMPLE: PostgreSQL as Primary Database

**Date:** <!-- YYYY-MM-DD -->
**Status:** Active
**Impact:** High

#### Context
Needed a reliable, scalable database that supports both relational data and vector embeddings for AI features.

#### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| PostgreSQL | ACID, mature, pgvector support, JSON support | Requires more setup than SQLite |
| MongoDB | Flexible schema, good for documents | No joins, eventual consistency complexity |
| SQLite | Zero setup | Not suitable for production multi-instance |

#### Decision
PostgreSQL with pgvector extension for vector similarity search.

#### Consequences
- **Positive:** Single database handles relational + vector data, reducing operational complexity
- **Negative:** Requires proper indexing knowledge; HNSW index tuning needed for large vector sets
- **Risks:** pgvector performance at scale may require migration to dedicated vector DB

---

*Last Updated: <!-- YYYY-MM-DD --> | Add decisions when made, never delete*

# Project Memory

> **Purpose:** Persistent memory for AI agents. Records architectural decisions, lessons learned, resolved issues, and important project context that should survive across conversations and sessions.
> **How to Use:** Read this file at the start of every task for context. Append new entries chronologically. Never delete entries — history is valuable.
> **Related:** [INDEX.md](INDEX.md) · [architecture](CORE/docs/architecture.md)

---

## How to Add Entries

Each entry follows this format:

```markdown
### [YYYY-MM-DD] Title

**Category:** Decision | Lesson | Bug | Pattern | Convention | Context
**Severity:** Critical | Important | Informational
**Related Files:** [file links]

Description of what happened, what was decided, and why. Include enough context that a future agent — with no prior knowledge — can understand and apply this information.
```

---

## Decisions

<!-- Record significant architectural, design, or technology decisions here. Include rationale. -->

### Template Entry

```markdown
### [YYYY-MM-DD] Decision Title

**Category:** Decision
**Severity:** Important
**Related Files:** [architecture](CORE/docs/architecture.md)

**Context:** Why this decision was needed.
**Decision:** What was decided.
**Rationale:** Why this option was chosen over alternatives.
**Alternatives Considered:** What else was evaluated.
**Consequences:** What this means for future development.
```

---

## Lessons Learned

### [2026-09-11] DuckDB S3 remote scan performance bottleneck (Моя помилка)

**Category:** Lesson / Bug
**Severity:** Critical
**Related Files:** `services/lead_pipeline.py`, `handlers/search.py`

**What Happened:** Бот крашився і зависав на 10-15 хвилин при пошуку як 10, так і 10,000 компаній.
**Root Cause:** (Моя вина як AI-асистента) Я написав наївну архітектуру запиту — використав стандартний SQL `ORDER BY random()` для віддалених Parquet-файлів на S3. DuckDB була змушена викачувати всі гігабайти файлу перед тим, як застосувати `LIMIT`.
**Resolution:** З SQL-запиту було прибрано `ORDER BY`. Тепер DuckDB припиняє завантаження одразу після досягнення `LIMIT`. Сортування та перемішування даних тепер відбувається локально на Python. Додано 5-хвилинний таймаут.
**Prevention:** НІКОЛИ не використовувати `ORDER BY` в DuckDB при читанні з віддаленого сховища об'єктів (S3), якщо не впевнений, що дані чітко розбиті на дрібні партиції.

---

<!-- Record mistakes, surprises, and non-obvious behaviors discovered during development. -->

### Template Entry

```markdown
### [YYYY-MM-DD] Lesson Title

**Category:** Lesson
**Severity:** Important
**Related Files:** [affected file paths]

**What Happened:** Description of the issue or surprise.
**Root Cause:** Why it happened.
**Resolution:** How it was fixed.
**Prevention:** How to avoid this in the future.
```

---

## Resolved Bugs (Notable)

<!-- Record only bugs that reveal systemic issues or non-obvious behaviors. Routine bugs do not need entries. -->

### Template Entry

```markdown
### [YYYY-MM-DD] Bug Title

**Category:** Bug
**Severity:** Critical
**Related Files:** [affected file paths]

**Symptom:** What was observed.
**Root Cause:** What caused it.
**Fix:** What was changed.
**Lesson:** What this teaches us about the system.
```

---

## Patterns & Conventions

<!-- Record established patterns that AI agents should follow consistently. -->

### Template Entry

```markdown
### [YYYY-MM-DD] Pattern Title

**Category:** Pattern
**Related Files:** [example implementation paths]

**When to Use:** Conditions under which this pattern applies.
**Implementation:** How to implement it.
**Example:** Reference to existing implementation.
**Why:** Rationale for this pattern over alternatives.
```

---

## Project Context

<!-- Record important context about the project that is not captured in other documents: business constraints, team conventions, deployment quirks, third-party limitations. -->

### Template Entry

```markdown
### [YYYY-MM-DD] Context Title

**Category:** Context
**Severity:** Informational

Description of important project context.
```

---

## Guidelines for Memory Management

1. **Be specific.** "The API is slow" is not useful. "The `/api/users` endpoint takes 3s when querying > 10,000 users due to missing index on `users.email`" is useful.
2. **Include rationale.** Future agents need to understand WHY, not just WHAT.
3. **Link to files.** Always reference the specific files, functions, or configurations involved.
4. **Date everything.** Context changes over time. Dates help agents assess relevance.
5. **Don't duplicate.** If the information belongs in `docs/architecture.md` or another document, put it there and reference it here.
6. **Prune, don't delete.** If an entry is no longer relevant, mark it as `[SUPERSEDED by YYYY-MM-DD entry]` rather than deleting.

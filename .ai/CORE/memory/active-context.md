# Active Context

> **Purpose:** Real-time project state for AI agents. Read this at the start of every task. Update it at the end.
> **Related:** [project-state.md](project-state.md) · [current-goals.md](current-goals.md) · [CLAUDE.md](../../CLAUDE.md)

---

## Current Sprint / Focus

**Period:** 2026-08-31
**Theme:** Reusable AI workspace restructuring
**Priority:** High

---

## What Was Just Done

<!-- Update after every significant task. Format: [YYYY-MM-DD] Description -->

| Date | Task | Status | Notes |
|------|------|--------|-------|
| 2026-08-31 | Added reusable website starter | Done | Created `templates/website-starter/` as a ready-to-copy `.ai/` package for new website projects with user preferences, startup prompt, design brief, architecture, and context files. |
| 2026-08-17 | Reorganized reusable AI workspace | Done | Added project-context templates, site and Telegram-bot profiles, specialist entry points, startup workflow, and moved internal materials into `CORE/`. |

---

## What's In Progress

<!-- Tasks currently being worked on -->

| Task | Owner | Blocker | ETA |
|------|-------|---------|-----|
| None | — | None | — |

---

## Active Decisions

<!-- Decisions made during this sprint that affect current work -->

- Keep reusable rules in this workspace; keep each product's live context in that product's `.ai/` directory.

---

## Key Files Being Touched

<!-- List files actively being modified to avoid conflicts -->

```
START-HERE.md
INDEX.md
templates/website-starter/
templates/
CORE/workflows/start-project.md
BACKEND/ FRONTEND/ SECURITY/ SITES-SKILLS/
```

---

## Known Blockers

<!-- Things preventing progress -->

- None.

---

## Context for Next Session

<!-- Critical information the next AI session must know -->

- For a new website, copy `templates/website-starter/` into the product repository as `.ai/`, then send the prompt from `.ai/AI-START-PROMPT.md`.
- Start other new products from `START-HERE.md`; do not copy another product's history or secrets.

---

*Last Updated: 2026-08-31 00:00 | Update this every session*

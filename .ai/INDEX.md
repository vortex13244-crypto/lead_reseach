# .ai Knowledge Base — Index

> **Purpose:** Master map of the AI knowledge base. Start here to find any document.
> **Last Updated:** 2026-08-31

---

## Start Here

This workspace is a reusable library, not the permanent context of one product. Read [START-HERE.md](START-HERE.md), then use [start-project workflow](CORE/workflows/start-project.md) to create a small `.ai/` folder inside a new product repository.

### Specialist Areas

- [BACKEND](BACKEND/README.md) — APIs, database work, integrations, and bots.
- [FRONTEND](FRONTEND/README.md) — UI, responsiveness, accessibility, and premium-interface guidance.
- [SECURITY](SECURITY/README.md) — security baseline and release checks.
- [SITES-SKILLS](SITES-SKILLS/README.md) — focused site-design instructions, including Apple Design.

### Starter Profiles

- [Website starter](templates/website-starter/README.md) — ready-to-copy `.ai/` package for new websites.
- [Project context](templates/project-context/README.md)
- [Next.js site](templates/project-types/nextjs-site/README.md)
- [Telegram bot](templates/project-types/telegram-bot/README.md)

---

## Knowledge Base Structure

```
AI/
├── INDEX.md                  ← You are here
├── MEMORY.md                 ← Project memory: decisions, lessons, context
├── PROJECT.md                ← Project description and metadata
│
├── CORE/                     ← Internal library for AI agents
│   ├── docs/                 ← Product & architecture documentation
│   ├── architecture.md       ← System design, modules, data flow, ADRs
│   ├── features.md           ← Feature specifications and lifecycle
│   ├── roadmap.md            ← Milestones, priorities, technical debt
│   ├── tech-stack.md         ← Technology inventory and version policies
│   └── vision.md             ← Mission, personas, core problems, success metrics
│
│   ├── roles/                ← AI agent role definitions
│   ├── architect.md          ← System design and architectural governance
│   ├── backend.md            ← Server-side logic, APIs, data access
│   ├── frontend.md           ← UI components, client state, browser performance
│   ├── ui-ux.md              ← User experience, design system, accessibility
│   ├── reviewer.md           ← Code review process and quality gates
│   ├── debugger.md           ← Root cause analysis and bug resolution
│   └── product-manager.md    ← Requirements, prioritization, scope decisions
│
│   ├── standards/            ← Project-wide conventions and rules
│   ├── code-style.md         ← Naming, formatting, functions, error handling, testing
│   ├── naming.md             ← Naming conventions for all identifiers
│   ├── folder-structure.md   ← Directory organization and file placement
│   ├── git.md                ← Branching, commits, PRs, versioning
│   └── ui-guidelines.md      ← Design tokens, spacing, typography, accessibility
│
│   ├── prompts/              ← Structured prompt templates for AI tasks
│   ├── audit.md              ← Code quality and security audit
│   ├── bugfix.md             ← Systematic bug diagnosis and resolution
│   ├── new-feature.md        ← Feature implementation from spec to tests
│   ├── optimize.md           ← Performance analysis and optimization
│   └── refactor.md           ← Code restructuring without behavior change
│
├── templates/                ← New-project templates
    ├── website-starter/      ← Ready-to-copy `.ai/` package for new websites
    └── template.md           ← Universal template for new knowledge base documents
```

---

## How to Use This Knowledge Base

### For AI Agents

1. **Starting a task?** Read the relevant role in `CORE/roles/` to understand your responsibilities and workflow.
2. **Writing code?** Follow the standards in `CORE/standards/` — code style, naming, folder structure.
3. **Need context?** Check `CORE/docs/` for architecture, tech stack, and feature specifications.
4. **Performing a specific task?** Use the prompt template in `CORE/prompts/` for structured guidance.
5. **Learning from the past?** Read `MEMORY.md` for project-specific decisions and lessons.
6. **Creating a new document?** Use `templates/template.md` as your starting point.

### Document Relationships

```
vision.md ──────▶ roadmap.md ──────▶ features.md
                      │
                      ▼
               architecture.md ◀───── tech-stack.md
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     roles/*     standards/*   prompts/*
          │           │           │
          └───────────┴───────────┘
                      │
                      ▼
                 MEMORY.md
```

### Adding New Documents

1. Copy `templates/template.md` to the appropriate directory.
2. Fill in all required sections — no placeholders or empty sections.
3. Add a cross-reference link from related documents.
4. Update this INDEX.md with the new file.

---

## Quick Reference

| I need to...                        | Start with                          |
| ----------------------------------- | ----------------------------------- |
| Start a new website                 | [Website starter](templates/website-starter/README.md) |
| Understand the system architecture  | [architecture](CORE/docs/architecture.md) |
| Know what technologies we use       | [tech stack](CORE/docs/tech-stack.md) |
| Build a new feature                 | [feature prompt](CORE/prompts/new-feature.md) + [backend role](CORE/roles/backend.md) |
| Fix a bug                           | [bugfix prompt](CORE/prompts/bugfix.md) + [debugger role](CORE/roles/debugger.md) |
| Review code                         | [reviewer role](CORE/roles/reviewer.md) |
| Design a UI                         | [UI/UX role](CORE/roles/ui-ux.md) + [UI guidelines](CORE/standards/ui-guidelines.md) |
| Name something                      | [naming](CORE/standards/naming.md) |
| Create a branch or commit           | [Git workflow](CORE/standards/git.md) |
| Place a new file                    | [folder structure](CORE/standards/folder-structure.md) |
| Optimize performance                | [optimization prompt](CORE/prompts/optimize.md) |
| Refactor code                       | [refactor prompt](CORE/prompts/refactor.md) |
| Audit code quality                  | [audit prompt](CORE/prompts/audit.md) |
| Check project decisions/context     | [MEMORY.md](MEMORY.md) |
| Understand the product vision       | [vision](CORE/docs/vision.md) |
| Check the roadmap                   | [roadmap](CORE/docs/roadmap.md) |

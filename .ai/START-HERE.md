# AI Workspace — Start Here

> **Purpose:** Reusable development base for future products. Keep it separate from a product's code and copy only the right starter context into each new repository.

## Recommended way of working

This folder is the **library**: standards, roles, checklists, workflows, and reusable skills.

Each product owns its own **context** beside its code. For a new website, use `templates/website-starter/`:

```text
my-product/
├── src/
├── .ai/
│   ├── AGENTS.md
│   ├── PROJECT.md
│   ├── active-context.md
│   ├── project-state.md
│   ├── architecture.md
│   └── design-brief.md
└── README.md
```

Create `.ai/` by copying `templates/website-starter/` into the new website and renaming it to `.ai/`, then send the AI the prompt from `.ai/AI-START-PROMPT.md`.

For a bot, API, or unusual project type, use `templates/project-context/` plus the matching profile from `templates/project-types/`.

## What stays here vs. with a product

| Keep in this AI workspace | Keep in the product repository |
| --- | --- |
| Roles, coding standards, reusable checklists | Product goal, architecture, API contracts |
| Generic guides and snippets | Decisions, task progress, known issues |
| Site and bot starter profiles | Brand, UI brief, user data and deployment details |

Never copy a completed product's `active-context.md`, secrets, customer data, decisions, or incidents into a new project.

## Where to go

- [Start a project](CORE/workflows/start-project.md)
- [Website starter](templates/website-starter/README.md)
- [Project-context template](templates/project-context/README.md)
- [Next.js site profile](templates/project-types/nextjs-site/README.md)
- [Telegram-bot profile](templates/project-types/telegram-bot/README.md)
- [Backend practices](BACKEND/README.md)
- [Frontend and premium UI practices](FRONTEND/README.md)
- [Security baseline](SECURITY/README.md)
- [Site skills](SITES-SKILLS/README.md)

*Last updated: 2026-08-31*

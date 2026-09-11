# Workflow: Start a New Project

> **Purpose:** Create a clean, product-specific context without carrying history from earlier products.

## 1. Choose a project profile

- Website or web app: start with [Website starter](../../templates/website-starter/README.md), then use [Next.js site](../../templates/project-types/nextjs-site/README.md) as the technical profile.
- Telegram bot: start with [Telegram bot](../../templates/project-types/telegram-bot/README.md).
- For another type, begin with the generic [project context](../../templates/project-context/README.md).

## 2. Create the project context

For a website, copy `templates/website-starter/` into the new repository and rename it to `.ai/`.

For other project types, copy `templates/project-context/` into the new repository as `.ai/`.

Do not copy old project histories, `.env` files, API tokens, customer data, deployment URLs, or unresolved decisions.

## 3. Fill only the essentials first

Before coding, fill in:

1. `.ai/PROJECT.md` — purpose, MVP boundary, users and stack.
2. `.ai/architecture.md` — components, data and integrations.
3. `.ai/design-brief.md` — only for a UI-facing product.
4. `.ai/active-context.md` — the immediate first goal and definition of done.

## 4. Build in small increments

For each feature, state acceptance criteria, implement, test, and then update `active-context.md`. Use the shared `workflows/new-feature.md` and relevant backend, frontend, or security profile when needed.

## 5. Close or archive a project

Keep `.ai/` inside its product repository as its historical record. The shared AI workspace remains clean and reusable for the next project.

*Last updated: 2026-08-31*

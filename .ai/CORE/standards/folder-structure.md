# Folder Structure Standards

> **Scope:** Directory organization rules, module boundaries, and file placement conventions.
> **Audience:** AI agents creating files, scaffolding modules, or restructuring projects.
> **Related:** [naming.md](./naming.md) · [code-style.md](./code-style.md) · [../docs/architecture.md](../docs/architecture.md)

---

## General Principles

1. **Structure reflects architecture.** The directory tree should mirror the system's module boundaries. A new team member should understand the architecture by reading the folder names.
2. **Co-locate related files.** Keep code, tests, styles, and types for a feature in the same directory — not in separate `tests/`, `styles/`, or `types/` trees.
3. **Flat over nested.** Avoid nesting deeper than 4 levels. Deep nesting makes navigation harder and imports longer.
4. **One purpose per directory.** Each directory has a clear, singular responsibility. If you cannot describe it in one sentence, it needs to be split.
5. **Convention is mandatory.** Never create ad-hoc directories. Follow the established structure or propose a change to this document first.

---

## Root-Level Layout

```
project-root/
├── .ai/                    # AI knowledge base (this system)
├── .github/                # CI/CD workflows, issue templates, PR templates
├── docs/                   # Project documentation (non-AI, external-facing)
├── scripts/                # Build, deployment, and automation scripts
├── src/                    # Application source code
├── tests/                  # Integration and E2E tests (unit tests co-locate)
├── infra/                  # Infrastructure as Code (Terraform, CloudFormation)
├── .env.example            # Environment variable template (never commit .env)
├── .gitignore
├── package.json            # or equivalent manifest (pyproject.toml, go.mod, etc.)
├── README.md
└── tsconfig.json           # or equivalent configuration
```

### Root-Level Rules

- The project root should contain only configuration files and top-level directories.
- Source code lives exclusively in `src/`. No `.ts`, `.py`, `.go` files at root (except config files).
- Scripts that are not part of the application belong in `scripts/`.
- Documentation for external consumers goes in `docs/`. AI agent documentation goes in `.ai/`.

---

## Source Code Structure (`src/`)

### Option A: Feature-Based (Recommended)

Group files by feature/domain, not by technical layer.

```
src/
├── common/                 # Shared utilities, types, constants
│   ├── utils/
│   ├── types/
│   └── constants/
├── config/                 # Application configuration
├── modules/                # Feature modules (core business logic)
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.repository.ts
│   │   ├── auth.types.ts
│   │   ├── auth.validation.ts
│   │   └── auth.service.test.ts
│   ├── users/
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   ├── users.repository.ts
│   │   ├── users.types.ts
│   │   └── users.service.test.ts
│   └── orders/
│       └── ...
├── infrastructure/         # Cross-cutting: database, cache, messaging, logging
│   ├── database/
│   ├── cache/
│   ├── messaging/
│   └── logger/
├── api/                    # API layer: routing, middleware, serialization
│   ├── routes/
│   ├── middleware/
│   └── validators/
└── main.ts                 # Application entry point
```

### Option B: Layer-Based (Simple Projects Only)

For small projects with minimal domain complexity.

```
src/
├── controllers/
├── services/
├── repositories/
├── models/
├── middleware/
├── utils/
└── main.ts
```

> **Decision guide:** Use feature-based (Option A) when the project has 3+ distinct domain areas. Use layer-based (Option B) only for small projects or rapid prototypes.

---

## Frontend Structure

```
src/
├── app/                    # Application shell, routing, providers
├── components/             # Shared/reusable UI components
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── Button.module.css
│   └── Modal/
│       └── ...
├── features/               # Feature-specific components and logic
│   ├── dashboard/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── DashboardPage.tsx
│   └── settings/
│       └── ...
├── hooks/                  # Shared custom hooks
├── services/               # API client functions
├── stores/                 # State management
├── styles/                 # Global styles, design tokens
├── types/                  # Shared type definitions
└── utils/                  # Shared utility functions
```

### Frontend Rules

- Page-level components live in `features/[feature]/`.
- Reusable components live in `components/`.
- A component becomes "reusable" when it is used in 2+ features. Until then, keep it in the feature directory.
- Co-locate component files: `Component.tsx`, `Component.test.tsx`, `Component.module.css`.

---

## Test Structure

```
Unit tests:       Co-located with source files (*.test.ts, *.spec.ts)
Integration tests: tests/integration/
E2E tests:        tests/e2e/
Test fixtures:     tests/fixtures/
Test utilities:    tests/helpers/
```

### Test File Naming

| Test Type    | Location                              | Naming                        |
| ------------ | ------------------------------------- | ----------------------------- |
| Unit         | Same directory as source              | `auth.service.test.ts`        |
| Integration  | `tests/integration/`                  | `auth-flow.integration.test.ts` |
| E2E          | `tests/e2e/`                          | `login.e2e.test.ts`           |

---

## Configuration Files

| File                    | Purpose                                    | Committed? |
| ----------------------- | ------------------------------------------ | ---------- |
| `.env.example`          | Template showing required environment vars | Yes        |
| `.env`                  | Actual environment values                  | **No**     |
| `.env.local`            | Local developer overrides                  | **No**     |
| `tsconfig.json`         | TypeScript compiler configuration          | Yes        |
| `.eslintrc.json`        | Linter configuration                       | Yes        |
| `.prettierrc`           | Formatter configuration                    | Yes        |
| `docker-compose.yml`    | Local development services                 | Yes        |
| `Dockerfile`            | Container build definition                 | Yes        |

---

## Migration Files

```
src/infrastructure/database/migrations/
├── 20250115_143000_create_users_table.sql
├── 20250116_090000_add_email_index.sql
└── 20250120_110000_create_orders_table.sql
```

- Use timestamp prefix: `YYYYMMDD_HHMMSS_description`.
- Each migration file handles one schema change.
- Migrations are append-only. Never modify a deployed migration.

---

## What Goes Where (Decision Table)

| File Type                        | Location                              |
| -------------------------------- | ------------------------------------- |
| Business logic                   | `src/modules/[module]/`               |
| Shared utility functions         | `src/common/utils/`                   |
| Type definitions (shared)        | `src/common/types/`                   |
| Type definitions (module)        | `src/modules/[module]/[module].types.ts` |
| API routes                       | `src/api/routes/`                     |
| Middleware                       | `src/api/middleware/`                  |
| Database connection, pooling     | `src/infrastructure/database/`        |
| Database migrations              | `src/infrastructure/database/migrations/` |
| Third-party API clients          | `src/infrastructure/[service-name]/`  |
| Unit tests                       | Same directory as the source file     |
| Integration tests                | `tests/integration/`                  |
| CI/CD workflows                  | `.github/workflows/`                  |
| Deployment scripts               | `scripts/`                            |
| Infrastructure as Code           | `infra/`                              |

---

## Anti-Patterns

| Anti-Pattern                           | Problem                                   | Solution                                  |
| -------------------------------------- | ----------------------------------------- | ----------------------------------------- |
| `utils/` as a dumping ground           | Becomes a junk drawer with no cohesion    | Create purpose-specific utility modules   |
| Separate `tests/` mirror tree          | Tests drift from source, hard to co-locate| Co-locate unit tests with source files     |
| Nesting deeper than 4 levels           | Navigation overhead, long import paths     | Flatten by extracting to a new module      |
| Mixing concerns in one directory       | `auth/` contains DB, routes, and UI       | Split by layer within the feature module   |
| Creating directories with 1 file       | Premature structure                       | Keep flat until 3+ related files exist     |

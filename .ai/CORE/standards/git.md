# Git Standards

> **Scope:** Git workflow, branching strategy, commit conventions, pull request process, and versioning.
> **Audience:** AI agents and developers working with version control.
> **Related:** [code-style.md](./code-style.md) · [naming.md](./naming.md)

---

## 1. Git Workflow

### Branching Model

Use **GitHub Flow** (or equivalent) as the default workflow:

```
main (production-ready, always deployable)
 ├── feature/user-authentication
 ├── fix/login-redirect-loop
 ├── chore/update-dependencies
 └── hotfix/critical-security-patch
```

### Rules

- `main` is the single source of truth. It must always be deployable.
- All work happens in short-lived feature branches created from `main`.
- Merge to `main` only through pull requests with at least one approval.
- Delete branches after merge. No stale branches.
- Direct commits to `main` are prohibited except for emergency hotfixes (which still require post-hoc review).

### Long-Running Branches (When Needed)

| Branch       | Purpose                              | Merge Target |
| ------------ | ------------------------------------ | ------------ |
| `main`       | Production-ready code                | —            |
| `develop`    | Integration branch (if used)         | `main`       |
| `release/x.y`| Release stabilization (if used)     | `main`       |

> Use `develop` and `release/` branches only if the project has a formal release cycle. For continuous deployment, `main` alone is sufficient.

---

## 2. Branch Naming

### Format

```
type/short-description
```

### Types

| Type       | Purpose                                | Example                         |
| ---------- | -------------------------------------- | ------------------------------- |
| `feature`  | New functionality                      | `feature/user-onboarding`       |
| `fix`      | Bug fix                                | `fix/cart-total-calculation`     |
| `hotfix`   | Urgent production fix                  | `hotfix/auth-bypass-vulnerability` |
| `chore`    | Non-functional: deps, config, tooling  | `chore/upgrade-node-20`         |
| `refactor` | Code restructuring without behavior change | `refactor/extract-payment-service` |
| `docs`     | Documentation changes                  | `docs/api-endpoint-reference`   |
| `test`     | Adding or fixing tests                 | `test/order-service-edge-cases` |
| `experiment`| Exploratory work (may be discarded)   | `experiment/graphql-migration`  |

### Rules

- Use kebab-case for the description portion.
- Keep branch names concise (2–5 words in the description).
- Include a ticket/issue ID when applicable: `feature/PROJ-123-user-onboarding`.
- No personal names in branch names. The branch describes the work, not the author.

---

## 3. Commit Convention

### Format (Conventional Commits)

```
type(scope): description

[optional body]

[optional footer(s)]
```

### Types

| Type       | Purpose                                | Triggers Version Bump? |
| ---------- | -------------------------------------- | ---------------------- |
| `feat`     | New feature                            | Minor                  |
| `fix`      | Bug fix                                | Patch                  |
| `docs`     | Documentation only                     | No                     |
| `style`    | Formatting, whitespace (no logic change)| No                    |
| `refactor` | Code change that neither fixes nor adds| No                     |
| `perf`     | Performance improvement                | Patch                  |
| `test`     | Adding or updating tests               | No                     |
| `chore`    | Build, CI, dependencies, tooling       | No                     |
| `revert`   | Reverts a previous commit              | Depends                |

### Scope

The scope identifies the affected module or area: `auth`, `api`, `database`, `ui`, `ci`, `config`.

### Examples

```
feat(auth): add password reset via email link

Implements password reset flow with time-limited tokens.
Token expiry is set to 1 hour, configurable via PASSWORD_RESET_TTL env var.

Closes #234
```

```
fix(orders): correct total calculation for discounted items

The discount was applied after tax instead of before.
Added regression test for this case.

Fixes #567
```

```
chore(deps): upgrade express from 4.18 to 4.21

No breaking changes. Release notes reviewed.
```

### Commit Rules

- Write in imperative mood: "add feature" not "added feature" or "adds feature."
- First line ≤ 72 characters. Be concise.
- Body explains WHY, not WHAT. The diff shows what changed.
- One logical change per commit. Do not combine unrelated changes.
- Never commit generated files, build artifacts, or secrets.
- Never commit with `--no-verify` to bypass hooks unless the hook itself is broken.

---

## 4. Pull Requests

### PR Title

Follow the same convention as commits:

```
feat(auth): add password reset via email link
```

### PR Description Template

```markdown
## What

Brief description of what this PR does.

## Why

Context: what problem does this solve? Link to issue or feature spec.

## How

High-level approach. Note any non-obvious implementation decisions.

## Testing

How was this tested? Include test types (unit, integration, manual).

## Checklist

- [ ] Code follows project standards
- [ ] Tests are added/updated
- [ ] Documentation is updated
- [ ] No breaking changes (or noted below)
- [ ] Self-reviewed
```

### PR Rules

- **Size:** Keep PRs under 400 lines of changed logic. Larger PRs should be split into stacked or sequential PRs.
- **Scope:** One feature, one fix, or one refactor per PR. Do not mix.
- **Draft PRs:** Use draft status for work-in-progress that needs early feedback.
- **Review turnaround:** Reviews should happen within 4 business hours of request.
- **Merge strategy:** Squash merge for feature branches (clean history). Merge commit for release branches (preserves history).
- **Conflicts:** The PR author is responsible for resolving merge conflicts. Rebase on `main` before requesting review.
- **CI must pass:** Do not merge with failing CI. No exceptions.

---

## 5. Versioning

### Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH
```

| Component | Increment When                                    | Example           |
| --------- | ------------------------------------------------- | ------------------|
| MAJOR     | Breaking changes to public API or behavior        | `1.0.0` → `2.0.0` |
| MINOR     | New features, backward-compatible                 | `1.0.0` → `1.1.0` |
| PATCH     | Bug fixes, backward-compatible                    | `1.0.0` → `1.0.1` |

### Pre-Release Tags

| Tag       | Purpose                    | Example            |
| --------- | -------------------------- | ------------------- |
| `-alpha`  | Early development          | `1.0.0-alpha.1`     |
| `-beta`   | Feature-complete, testing  | `1.0.0-beta.3`      |
| `-rc`     | Release candidate          | `1.0.0-rc.1`        |

### Tagging Rules

- Tag every release in Git: `git tag -a v1.2.3 -m "Release v1.2.3"`.
- Push tags to remote: `git push --tags`.
- Never delete or move a published tag.
- Use a CHANGELOG.md or automated release notes (from Conventional Commits) to document each version.

---

## .gitignore Best Practices

Always ignore:

```
# Dependencies
node_modules/
vendor/
.venv/

# Build output
dist/
build/
*.pyc
__pycache__/

# Environment
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/settings.json
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Coverage
coverage/
.nyc_output/
```

Never ignore:
- `.env.example` (template with variable names, no values).
- Configuration files (`.eslintrc`, `.prettierrc`, `tsconfig.json`).
- Lock files (`package-lock.json`, `yarn.lock`, `poetry.lock`).

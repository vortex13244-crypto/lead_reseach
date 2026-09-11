# Git — Knowledge Base

> **Purpose:** Git workflow, branch naming, commit conventions, and PR best practices.
> **Related:** [../standards/git.md](../standards/git.md) · [../checklists/before-commit.md](../checklists/before-commit.md)

---

## Overview

Git workflow follows GitHub Flow (not Gitflow). All features branch from `main`, are reviewed via PR, and merge back to `main`. Deployments are triggered by tags.

---

## Branch Naming

```bash
feature/user-profile-settings     # New feature
fix/auth-token-expiry             # Bug fix
hotfix/critical-payment-crash     # Emergency fix (from main)
refactor/user-service-cleanup     # Refactoring
chore/update-dependencies         # Maintenance
docs/api-documentation-update     # Documentation
```

---

## Conventional Commits

Format: `type(scope): description`

```bash
# Types
feat:      New feature
fix:       Bug fix
refactor:  Code change without behavior change
perf:      Performance improvement
test:      Adding or updating tests
docs:      Documentation changes
chore:     Build system, dependencies, CI changes
style:     Formatting (no code change)
revert:    Reverting a commit

# Examples
feat(auth): add JWT refresh token rotation
fix(dashboard): handle null subscription in user dashboard
refactor(user-service): extract profile validation logic
perf(api): add Redis cache for user profile endpoint
test(auth): add integration tests for login endpoint
docs(api): update authentication section
chore(deps): update Next.js to 14.2.0

# Breaking changes
feat(api)!: change user response format to include metadata
# or
feat(api): change user response format

BREAKING CHANGE: User response now includes `metadata` field.
Migration: Update all consumers to handle the new field.
```

---

## Workflow

```bash
# 1. Start from latest main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/user-notifications

# 3. Work, commit often (atomic commits)
git add src/api/notifications/
git commit -m "feat(notifications): add notification schema and repository"

git add src/services/notification.service.ts
git commit -m "feat(notifications): implement notification service"

git add src/app/api/v1/notifications/
git commit -m "feat(notifications): add REST endpoints for notifications"

git add tests/
git commit -m "test(notifications): add unit and integration tests"

# 4. Keep branch up to date (rebase, not merge)
git fetch origin
git rebase origin/main

# 5. Push and create PR
git push origin feature/user-notifications
gh pr create --title "feat(notifications): add user notification system"

# 6. After approval: squash merge or regular merge
# Squash merge: keeps main history clean for features
# Regular merge: preserves individual commits (for refactors with good commits)
```

---

## Commit Best Practices

```bash
# Atomic commits — one logical change per commit
# Each commit should be deployable on its own

# ✅ Good commit sequence
feat(auth): add JWT token generation utility
feat(auth): add login endpoint
feat(auth): add refresh token endpoint
test(auth): add auth endpoint integration tests

# ❌ Bad commit
"Added lots of stuff"

# ❌ WIP commits (clean before PR)
"WIP"
"temp fix"
"testing"
# → Squash these: git rebase -i HEAD~3

# Rewriting commit history (before push)
git commit --amend  # Amend last commit
git rebase -i HEAD~5  # Interactive rebase last 5 commits
```

---

## Useful Commands

```bash
# See what changed
git log --oneline -20
git diff main...HEAD
git diff --stat

# Stage specific lines (not whole file)
git add -p src/file.ts

# Stash changes temporarily
git stash
git stash pop

# Find which commit introduced a bug (binary search)
git bisect start
git bisect bad HEAD
git bisect good v1.2.0
# Git checks out middle commit; you test it:
git bisect good  # or: git bisect bad
# Repeat until the culprit commit is found

# Undo last commit (keep changes)
git reset HEAD~1

# Reset to remote state (nuclear option, loses local work)
git reset --hard origin/main

# Cherry-pick a commit from another branch
git cherry-pick abc1234

# Signing commits (recommended for open source)
git config --global commit.gpgsign true
```

---

## Branch Protection Rules

Configure on GitHub → Settings → Branches → Protection rules:

```
Branch: main
Rules:
✅ Require pull request before merging
✅ Require 1 approving review
✅ Dismiss stale reviews when new commits are pushed
✅ Require status checks to pass (lint, type-check, tests)
✅ Require branches to be up to date before merging
✅ Do not allow bypass for administrators
```

---

## Resources

- [Conventional Commits Spec](https://www.conventionalcommits.org/)
- [GitHub Flow Guide](https://docs.github.com/en/get-started/using-github/github-flow)
- [Oh Shit, Git!](https://ohshitgit.com/) — Common git mistakes and fixes

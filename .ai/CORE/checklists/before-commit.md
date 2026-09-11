# Checklist: Before Commit

> **Purpose:** Verify code quality before every commit. Run this before `git commit`.
> **Time:** 5-10 minutes

---

## Code Quality

- [ ] Code does exactly what it's supposed to do (re-read the task)
- [ ] All edge cases handled (null, empty, error, max)
- [ ] No `console.log`, `print()`, or debug statements left
- [ ] No commented-out code (delete it or don't commit it)
- [ ] No `// TODO` comments (create a ticket instead)
- [ ] No `any` types in TypeScript without justification

---

## Correctness

- [ ] Linter passes: `npm run lint`
- [ ] Type checker passes: `npm run type-check`
- [ ] Tests pass: `npm test`
- [ ] Build succeeds: `npm run build` (for significant changes)

---

## Security

- [ ] No API keys, passwords, or secrets in the code
- [ ] No sensitive data in log statements
- [ ] User input validated before use
- [ ] Authorization checked (not just authentication)

---

## Style

- [ ] Names are clear and follow `standards/naming.md`
- [ ] Functions are focused (one responsibility)
- [ ] File is in the correct directory (follows `standards/folder-structure.md`)
- [ ] Imports are organized (external → internal → relative)

---

## Git

- [ ] `git diff --staged` reviewed — no unintended changes
- [ ] Commit message follows Conventional Commits format:
  ```
  feat: add user profile settings
  fix: handle null subscription in dashboard
  refactor: extract validation logic from processOrder
  ```
- [ ] Each commit is atomic (one logical change)
- [ ] No large binary files committed

---

## Quick Commands

```bash
npm run lint && npm run type-check && npm test
git diff --staged
```

---

*Related: [before-pr.md](before-pr.md) · [standards/git.md](../standards/git.md)*

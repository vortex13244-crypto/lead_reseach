# Checklist: Before PR

> **Purpose:** Self-review before requesting a code review. Reviewers' time is valuable — don't waste it on fixable issues.
> **Time:** 15-30 minutes

---

## Code Readiness

- [ ] `npm run lint` passes
- [ ] `npm run type-check` passes
- [ ] `npm test` passes
- [ ] `npm run build` succeeds
- [ ] Tested manually in the browser/app

---

## Code Quality

- [ ] No `console.log` or debug statements
- [ ] No commented-out code
- [ ] No `// TODO` without a linked issue
- [ ] No `any` types without justification comment
- [ ] All functions have single responsibility
- [ ] Complex logic has explanatory comments

---

## Completeness

- [ ] All acceptance criteria met (re-read the issue/ticket)
- [ ] Edge cases handled: empty state, null/undefined, error state
- [ ] Error messages are user-friendly (not raw error codes)
- [ ] Loading states implemented for async operations

---

## Tests

- [ ] Tests added for new functionality
- [ ] Tests cover the main happy path
- [ ] Tests cover at least one error case
- [ ] E2E test added for critical user flows (if applicable)

---

## Security

- [ ] No secrets or credentials in code
- [ ] Input validation for all user-controlled data
- [ ] Authorization checked for resource access
- [ ] No SQL string interpolation

---

## UI Changes (if applicable)

- [ ] Responsive on mobile (tested in devtools)
- [ ] Dark mode works (if project uses it)
- [ ] Loading state implemented
- [ ] Error state implemented
- [ ] Empty state implemented
- [ ] Keyboard navigable
- [ ] No layout shift

---

## PR Description Quality

- [ ] Title follows conventional commits: `feat:`, `fix:`, `refactor:`
- [ ] Description explains WHAT changed and WHY
- [ ] Screenshots or recording for UI changes
- [ ] Breaking changes explicitly noted
- [ ] Linked to the issue/ticket

---

## Diff Review

- [ ] Read `git diff main...HEAD` and reviewed every change
- [ ] No unintended files included
- [ ] No leftover debug code
- [ ] No merge conflict markers

---

*Related: [before-commit.md](before-commit.md) · [workflows/review-pr.md](../workflows/review-pr.md)*

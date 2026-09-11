# Workflow: Review PR

> **Purpose:** Systematic pull request review process ensuring code quality, security, and maintainability.
> **Role:** [reviewer.md](../roles/reviewer.md)
> **Related:** [checklists/before-pr.md](../checklists/before-pr.md)

---

## Step 1: Context (2 minutes)

Before reading the code:

```markdown
1. Read the PR description:
   - What does this change do?
   - Why is this change needed?
   - How was it tested?

2. Read the linked issue/ticket
3. Check the diff size:
   - < 200 lines: review normally
   - 200-500 lines: break into sections
   - > 500 lines: request to split if possible
```

---

## Step 2: High-Level Review (5 minutes)

Look at the structure, not the details:

```markdown
- Does this approach make sense architecturally?
- Does it follow the established patterns?
- Is the scope appropriate (no unrelated changes)?
- Are there obvious missing pieces (tests, docs)?
```

---

## Step 3: Code Review (line by line)

### Correctness

```markdown
- Does the code do what the description says?
- Are all edge cases handled?
  - What happens with null/undefined?
  - What if the API call fails?
  - What if the user has no permissions?
- Are there any off-by-one errors?
- Are there any race conditions?
```

### Security

```markdown
- Is user input validated before use?
- Are SQL queries parameterized?
- Is authorization checked (not just authentication)?
- Are secrets/credentials exposed anywhere?
- See: checklists/security.md
```

### Performance

```markdown
- Any N+1 queries?
- Any unbounded list queries?
- Any synchronous operations that should be async?
- Any unnecessary computations inside loops?
```

### Maintainability

```markdown
- Is the code self-documenting (clear names, obvious purpose)?
- Are complex sections commented?
- Is the code DRY (no duplicated logic)?
- Does the function/component have a single responsibility?
- Is the file too long? (> 300 lines for components, > 500 for services)
```

### Testing

```markdown
- Are tests present for new code?
- Do the tests test behavior, not implementation?
- Are edge cases tested?
- Is there an E2E test for critical paths?
```

---

## Step 4: Category-Specific Review

### API Changes

```markdown
- Follows REST conventions?
- Proper HTTP status codes?
- Error responses match the standard format? (see docs/api.md)
- Pagination on list endpoints?
- Rate limiting considered?
- Breaking change? (versioning needed?)
```

### Database Changes

```markdown
- Migration is safe? (additive, not destructive)
- Indices added for new foreign keys?
- Indices added for new query patterns?
- Migration has a rollback path?
- Tested on a production data clone?
```

### UI Changes

```markdown
- Follows design system? (shadcn/ui components used correctly)
- Responsive design? (tested on mobile)
- Loading state handled?
- Error state handled?
- Empty state handled?
- Accessibility: keyboard navigable, ARIA labels, contrast?
```

---

## Step 5: Write Feedback

### Feedback Categories

Use prefixes to indicate severity:

```markdown
CRITICAL: [Issue] — Must be fixed before merge (breaks functionality, security issue)
IMPORTANT: [Issue] — Should be fixed before merge (best practice violation, likely bug)
SUGGESTION: [Improvement] — Consider this, but not a blocker
QUESTION: [?] — I don't understand this; please clarify
PRAISE: [Good thing] — Note positive patterns explicitly
```

### Feedback Quality

Good feedback:
```markdown
IMPORTANT: This function doesn't handle the case where `user.subscription` is null. 
If a user has never subscribed, `user.subscription.status` will throw a TypeError.
Add a null check: `const isActive = user.subscription?.status === 'active' ?? false`
```

Bad feedback:
```markdown
This is wrong.  ← Vague, not actionable
Consider refactoring this.  ← Says nothing specific
```

---

## Step 6: Final Decision

### Approve

```markdown
✅ LGTM — Approved with no changes needed.
OR
✅ Approved — [Minor suggestions that don't need re-review]
```

### Request Changes

```markdown
❌ Request Changes:
CRITICAL: [Must fix 1]
CRITICAL: [Must fix 2]
IMPORTANT: [Should fix 3]
[Suggestions for after merge]
```

### Comment Without Blocking

```markdown
💬 Comments (no re-review needed):
[Questions and suggestions that don't block merge]
```

---

## Time Budgets

| PR Size | Time Budget |
|---------|------------|
| < 50 lines | 15 minutes |
| 50-200 lines | 30 minutes |
| 200-500 lines | 1 hour |
| > 500 lines | Request to split |

---

## Review Anti-Patterns to Avoid

- **Nitpicking style** — If there's a linter, let it enforce style; don't leave style comments
- **Bikeshedding** — Spending more time on variable names than logic
- **Passive aggressive comments** — "This is interesting..." (just say what you mean)
- **No feedback** — Approving without reading defeats the purpose
- **All blocking, no praise** — Acknowledge good work; it shapes future code
- **Late blocking feedback** — If you see scope issues, flag them early in the review

---

*Related: [reviewer.md](../roles/reviewer.md) · [checklists/before-pr.md](../checklists/before-pr.md) · [standards/git.md](../standards/git.md)*

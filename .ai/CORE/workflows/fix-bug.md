# Workflow: Fix Bug

> **Purpose:** Systematic process for diagnosing and resolving bugs. Never guess — investigate, understand, fix, verify.
> **Role:** [debugger.md](../roles/debugger.md)
> **Time:** 15 min (simple) to 4 hours (complex)

---

## Process Overview

```
Report → Reproduce → Isolate → Root Cause → Fix → Verify → Document
```

---

## Step 1: Understand the Report

Before touching any code:

```markdown
Gather:
1. Exact steps to reproduce (not "it doesn't work")
2. Expected behavior
3. Actual behavior (exact error message or screenshot)
4. Environment: browser, OS, version, user account
5. When it started (recent deploy? always?)
6. How many users affected
7. Is it consistent or intermittent?
```

**Severity Assessment:**

| Severity | Criteria | Response |
|----------|----------|----------|
| P0 Critical | Data loss, auth bypass, production down | Immediate |
| P1 High | Major feature broken, many users affected | < 4 hours |
| P2 Medium | Feature degraded, workaround exists | < 24 hours |
| P3 Low | Minor issue, cosmetic | Next sprint |

---

## Step 2: Reproduce the Bug

```bash
# 1. Reproduce in local environment first
# 2. If can't reproduce locally, try staging
# 3. Check if it's environment-specific

# Check recent changes
git log --oneline -20
git diff HEAD~5 HEAD -- src/

# Check logs around the time of the report
# Sentry: filter by time range and error type
# Server logs: grep for error patterns
grep -n "ERROR" logs/app.log | tail -50
```

**If you cannot reproduce:** Ask for more information. A bug you can't reproduce is a bug you can't safely fix.

---

## Step 3: Isolate the Problem

```markdown
Narrow down using binary search:
1. Which module/component is involved?
2. Which function/method is failing?
3. What input triggers the bug?
4. What is the minimal reproduction case?

Techniques:
- Add logging to narrow down where execution fails
- Comment out sections to find the responsible code
- Test with simplified inputs
- Check if it's a data issue (specific user/record) or code issue (all inputs)
```

---

## Step 4: Identify Root Cause

Do not write a fix until you understand the root cause.

```markdown
Root cause analysis questions:
1. WHY does this code fail?
2. WHY was this not caught before?
3. Is this a symptom of a larger problem?
4. Are there other places with the same bug pattern?

Common root causes:
- Null/undefined not handled
- Race condition (async code)
- Wrong assumptions about input format
- Missing database transaction
- Off-by-one error
- Timezone/date handling
- Character encoding
- Cache stale data
- Schema migration side effect
```

---

## Step 5: Write the Fix

```markdown
Principles:
1. Fix the root cause, not the symptom
2. Minimal change principle — change only what's needed
3. Don't "clean up" unrelated code in the same commit
4. Add a defensive check, but also fix the underlying issue
5. Check for similar bugs in the same file/module
```

```typescript
// Before fixing: write a failing test that reproduces the bug
// This ensures the fix works AND prevents regression

describe('Bug fix: user dashboard crashes with no subscription', () => {
  it('should return empty state when user has no subscription', () => {
    // Test that reproduces the bug
    const result = getUserDashboardData({ userId: 'user_without_sub' })
    expect(result).toEqual({ subscription: null, features: [] })
    // This test should FAIL before your fix, PASS after
  })
})
```

---

## Step 6: Verify the Fix

```bash
# 1. Run the specific failing test
npm test -- --run "Bug fix: user dashboard"

# 2. Run related tests
npm test -- --run "user dashboard"

# 3. Run full test suite
npm test

# 4. Manual verification
# - Reproduce original bug scenario → confirm fixed
# - Test edge cases around the fix
# - Test that nothing nearby is broken

# 5. Review the diff
git diff
# Ask: Is this the minimal change needed? Does it look right?
```

---

## Step 7: Code Review

Before merging:
- [ ] Root cause documented in PR description
- [ ] Test added that would have caught this
- [ ] Fix is minimal and focused
- [ ] No unrelated changes included
- [ ] PR linked to the issue/ticket

---

## Step 8: Deploy

For P0/P1 bugs, use expedited deployment:

```bash
# Create hotfix branch
git checkout -b hotfix/bug-description main

# Apply fix
# ... make changes ...

# Push and create emergency PR
git push origin hotfix/bug-description

# After review: merge to main and deploy
# Follow workflows/deploy.md with expedited process
```

---

## Step 9: Document

After the fix is deployed:

### Update Known Issues

```markdown
# In memory/known-issues.md

### [YYYY-MM-DD] Bug: [Title]

**Category:** Bug
**Severity:** [P0/P1/P2/P3]
**Status:** Resolved

**Symptom:** [What users saw]
**Root Cause:** [Why it happened]
**Fix:** [What was changed and why]
**Lesson:** [What this teaches about the system]
**Commit:** [git SHA]
```

### Update Active Context

```markdown
# In memory/active-context.md
# Note: fixed bug X, deployed, verified
```

---

## Common Bug Patterns

### Null/Undefined Errors

```typescript
// Pattern: access property on undefined
// TypeError: Cannot read property 'name' of undefined

// Fix pattern: optional chaining + null checks
const name = user?.profile?.name ?? 'Anonymous'

// Or guard early
if (!user) throw new NotFoundError('User not found')
```

### Race Conditions

```typescript
// Pattern: multiple async operations, state is inconsistent
// Fix: ensure operations are atomic or sequential

// Wrong ❌
const user = await getUser(id)
const posts = await getPosts(id)
// What if user was deleted between these two calls?

// Better ✅
const [user, posts] = await Promise.all([getUser(id), getPosts(id)])
```

### N+1 Queries (Performance Bug)

```typescript
// Pattern: query inside a loop
// Fix: batch query before the loop
// See: roles/database-engineer.md
```

### Timezone Issues

```typescript
// Always use UTC for storage, convert for display
// Never use new Date() without timezone consideration
// Use date-fns or dayjs, not moment

import { formatInTimeZone } from 'date-fns-tz'
const formatted = formatInTimeZone(date, userTimezone, 'MM/dd/yyyy')
```

---

*Related: [debugger.md](../roles/debugger.md) · [before-commit.md](../checklists/before-commit.md) · [review-pr.md](review-pr.md)*

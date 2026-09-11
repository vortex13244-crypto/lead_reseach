# Workflow: Refactor

> **Purpose:** Safe, systematic code refactoring without changing observable behavior.
> **Role:** [architect.md](../roles/architect.md) · [reviewer.md](../roles/reviewer.md)
> **Rule:** Tests must pass before AND after. If no tests exist, write them first.

---

## Golden Rule of Refactoring

**Never refactor and change behavior at the same time.**
Two separate commits: (1) refactor, (2) behavior change.

---

## Step 1: Identify the Smell

Common reasons to refactor:

| Code Smell | Solution |
|-----------|---------|
| Function > 30 lines | Extract smaller functions |
| File > 300 lines | Split into modules |
| Duplicated code (3+ copies) | Extract shared utility |
| Deeply nested conditions | Extract or invert conditions |
| Magic numbers/strings | Extract named constants |
| God class/god module | Split by responsibility |
| Difficult to test | Inject dependencies |
| Misleading names | Rename with better names |

---

## Step 2: Establish Safety Net

```bash
# If tests exist: verify they pass
npm test

# If tests DON'T exist: write characterization tests first
# These tests document what the code CURRENTLY does (not what it SHOULD do)
# They capture the "oracle" — the expected behavior to preserve

# Run tests, note current coverage
npm test -- --coverage
```

---

## Step 3: Make Refactoring Plan

```markdown
Before touching code, write a plan:

1. What is being refactored and why?
2. What files will change?
3. What is the new structure?
4. What stays the same (behavior contract)?
5. Can this be done in small, safe steps?
```

---

## Step 4: Refactor Incrementally

Commit after each meaningful step. Never have a 2000-line refactoring commit.

### Extract Function

```typescript
// BEFORE
async function processOrder(orderId: string) {
  const order = await prisma.order.findUnique({ where: { id: orderId } })
  if (!order) throw new NotFoundError()

  // 20 lines of validation logic...
  const isValid = order.items.length > 0 &&
    order.items.every(item => item.quantity > 0) &&
    order.totalAmount > 0 &&
    order.currency.length === 3

  // 30 lines of processing logic...
}

// AFTER
async function processOrder(orderId: string) {
  const order = await getOrderOrThrow(orderId)
  validateOrder(order)
  await executeOrderProcessing(order)
}

function validateOrder(order: Order): void {
  if (order.items.length === 0) throw new ValidationError('Order must have items')
  if (order.items.some(item => item.quantity <= 0)) throw new ValidationError('Invalid quantity')
  if (order.totalAmount <= 0) throw new ValidationError('Invalid total')
  if (order.currency.length !== 3) throw new ValidationError('Invalid currency')
}
```

### Extract Constant

```typescript
// BEFORE
if (retries > 3) throw new Error('Too many retries')
await sleep(1000 * Math.pow(2, retries))

// AFTER
const MAX_RETRIES = 3
const BASE_RETRY_DELAY_MS = 1000

if (retries > MAX_RETRIES) throw new Error('Too many retries')
await sleep(BASE_RETRY_DELAY_MS * Math.pow(2, retries))
```

### Extract Module

```typescript
// BEFORE: 500-line user.service.ts with user CRUD + auth + billing + notifications

// AFTER: Split into focused modules
// src/services/user/user-crud.service.ts    — create, read, update, delete
// src/services/user/user-auth.service.ts    — authentication logic
// src/services/user/user-billing.service.ts — Stripe integration
// src/services/user/notifications.service.ts — email/push notifications
// src/services/user/index.ts               — re-exports for backwards compatibility
```

---

## Step 5: Verify Behavior Unchanged

```bash
# Run all tests after each significant refactoring step
npm test

# If you have integration tests, run those too
npm run test:integration

# If you changed a public interface, verify all callers still work
npm run type-check
npm run build
```

---

## Step 6: Create PR

PR should be:
- **Pure refactoring only** — No behavior changes
- **Focused** — One type of refactoring per PR (don't mix extract function + rename + move file)
- **Well-described** — Explain why this is better

```markdown
PR Title: refactor: extract order validation logic from processOrder

Description:
The `processOrder` function was doing too many things: fetching, 
validating, and processing. Split into focused functions for 
better testability and readability.

No behavior changes — all existing tests pass.
```

---

## Refactoring Safety Checklist

- [ ] Tests exist before starting (written if missing)
- [ ] All tests pass before refactoring
- [ ] Refactoring in small, committed steps
- [ ] All tests pass after each step
- [ ] No behavior changes mixed with refactoring
- [ ] Type checker passes
- [ ] Build succeeds
- [ ] PR reviewed by at least one team member

---

*Related: [reviewer.md](../roles/reviewer.md) · [standards/code-style.md](../standards/code-style.md)*

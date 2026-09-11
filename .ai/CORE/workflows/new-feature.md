# Workflow: New Feature

> **Purpose:** Step-by-step process for implementing a new feature from specification to deployment.
> **Roles:** [architect.md](../roles/architect.md) · [backend.md](../roles/backend.md) · [frontend.md](../roles/frontend.md)
> **Time:** 2 hours (small) to 2 weeks (large)

---

## Step 1: Understand the Requirement

Before writing any code, answer these questions:

```markdown
1. What problem does this feature solve for the user?
2. Who uses this feature and how often?
3. What does "done" look like? (acceptance criteria)
4. What are the edge cases?
5. What should NOT be included in this iteration?
6. Are there any security or compliance considerations?
7. What are the performance requirements?
```

If any answer is unclear → clarify before proceeding.

---

## Step 2: Technical Design

### 2a. Data Model

```markdown
Questions to answer:
- What new data needs to be stored?
- What existing data is affected?
- How does this affect existing schemas?
- What are the constraints and relationships?

Output: Entity diagram or schema additions for docs/database.md
```

### 2b. API Design

```markdown
Endpoint Design:
- What endpoints are needed?
- What are the request/response shapes?
- What authentication/authorization is required?
- What are the error cases?

Follow: docs/api.md conventions
```

### 2c. Component Design

```markdown
UI Components:
- What pages/views are needed?
- What components will be built or reused?
- How does this integrate with existing navigation?
- What are the loading, empty, and error states?

Follow: standards/ui-guidelines.md
```

---

## Step 3: Branch Setup

```bash
# Branch naming: feature/[short-description]
git checkout -b feature/user-profile-settings

# If this depends on another feature branch
git checkout -b feature/user-profile-settings feature/user-management
```

---

## Step 4: Database First

If the feature requires new data:

```bash
# 1. Design schema (see roles/database-engineer.md)
# 2. Write migration
npx prisma migrate dev --name add_user_profile

# 3. Update Prisma client
npx prisma generate

# 4. Write repository/data access layer
# src/infrastructure/db/user-profile-repository.ts
```

---

## Step 5: Backend Implementation

Follow this order:

```
Types → Validation → Service → Controller/Route → Tests
```

```typescript
// 1. Types (src/types/user-profile.ts)
export interface UserProfile {
  id: string
  userId: string
  bio: string | null
  website: string | null
  location: string | null
}

// 2. Validation schema (src/lib/validations/user-profile.ts)
import { z } from 'zod'

export const updateProfileSchema = z.object({
  bio: z.string().max(500).optional(),
  website: z.string().url().max(255).optional().nullable(),
  location: z.string().max(100).optional().nullable(),
})

// 3. Service (src/services/user-profile.service.ts)
export class UserProfileService {
  async updateProfile(userId: string, data: UpdateProfileInput): Promise<UserProfile> {
    // Business logic here
  }
}

// 4. Route (src/app/api/v1/users/profile/route.ts)
export async function PATCH(request: Request) {
  // Auth → Validate → Service → Response
}
```

---

## Step 6: Frontend Implementation

Follow this order:

```
Page → Layout → Components → API Integration → Loading/Error States
```

```tsx
// 1. Page component
// src/app/(dashboard)/settings/profile/page.tsx

// 2. Form component with shadcn/ui
// src/components/features/profile/profile-form.tsx

// 3. API hook with TanStack Query
// src/hooks/use-profile.ts

// 4. All states handled:
// - Loading: <Skeleton /> components
// - Error: <ErrorMessage /> with retry
// - Empty: <EmptyState /> component
// - Success: Show data

// 5. Responsive: mobile-first design
```

---

## Step 7: Write Tests

```typescript
// For each unit: write test BEFORE or ALONGSIDE implementation

// 1. Unit tests for service logic
// 2. Integration tests for API endpoints
// 3. Component tests for key components
// 4. E2E test for the critical happy path

// Minimum E2E test:
test('user can update their profile', async ({ page }) => {
  await page.goto('/settings/profile')
  await page.fill('[data-testid="bio-input"]', 'Software engineer')
  await page.click('[data-testid="save-button"]')
  await expect(page.locator('[data-testid="success-toast"]')).toBeVisible()
})
```

---

## Step 8: Self-Review

Before creating a PR:

```bash
# Run the full checklist
# checklists/before-pr.md

# Quick checks:
npm run lint
npm run type-check
npm test
npm run build  # Verify no build errors

# Review your own diff
git diff main...HEAD
```

Ask yourself:
- Does this match the requirement from Step 1?
- Are all edge cases handled?
- Are all error states handled?
- Is the code consistent with existing patterns?
- Could a future developer understand this without asking you?

---

## Step 9: PR and Review

```markdown
PR Description Template:

## What
[One sentence: what does this PR do?]

## Why
[One sentence: why is this needed?]

## How
[Brief description of the approach]

## Screenshots (for UI changes)
[Before/After or new UI]

## Testing
- [ ] Unit tests added
- [ ] E2E test added / updated
- [ ] Tested manually: [steps]

## Checklist
- [ ] Follows code style standards
- [ ] No console.log left in
- [ ] No TODO comments
- [ ] Memory updated (if architectural decision)
```

---

## Step 10: Deploy

After PR approval:

1. Merge to `main`
2. Verify staging deployment is successful
3. Run smoke test on staging
4. If OK → follow `workflows/deploy.md` for production

---

## Step 11: Post-Implementation

```markdown
Update memory system:

1. memory/active-context.md
   - Mark feature as complete
   - Note any follow-up items

2. memory/completed.md
   - Add entry with what was built

3. memory/decisions.md
   - Document any architectural decisions made

4. memory/known-issues.md
   - Note any known limitations of the implementation
```

---

## Feature Size Guidelines

| Size | Scope | Time | Tests Required |
|------|-------|------|---------------|
| XS | UI tweak, single field | < 1 hour | Updated existing test |
| S | New UI component, simple API | 2-4 hours | Unit tests |
| M | New page + API endpoint | 1-2 days | Unit + integration |
| L | Multi-step feature, new schema | 1 week | Unit + integration + E2E |
| XL | New product area | 2+ weeks | Full test suite + load test |

---

*Related: [architect.md](../roles/architect.md) · [before-pr.md](../checklists/before-pr.md) · [build-saas.md](build-saas.md)*

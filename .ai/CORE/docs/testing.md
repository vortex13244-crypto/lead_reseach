# Testing Documentation

> **Purpose:** Testing strategy, patterns, tools, and coverage requirements.
> **Related:** [../roles/reviewer.md](../roles/reviewer.md) · [../checklists/before-pr.md](../checklists/before-pr.md) · [../standards/code-style.md](../standards/code-style.md)

---

## Testing Philosophy

**Principle:** Test behavior, not implementation. Tests should verify what the system does, not how it does it.

**Coverage Targets:**
| Layer | Target | Minimum |
|-------|--------|---------|
| Unit tests | 80% | 70% |
| Integration tests | 60% | 50% |
| E2E tests | Critical paths | 100% of critical paths |

---

## Testing Stack

| Type | Tool (TS) | Tool (Python) |
|------|-----------|--------------|
| Unit / Integration | Vitest | pytest |
| E2E | Playwright | Playwright |
| Component | Storybook + Testing Library | — |
| API testing | Supertest / httpx | httpx / pytest-httpx |
| Mocking | Vitest mocks / MSW | pytest-mock / respx |
| Coverage | V8 / Istanbul | coverage.py |
| Performance | k6 | Locust |

---

## Unit Tests

### TypeScript (Vitest)

```typescript
// src/lib/utils.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { calculateDiscount } from './utils'

describe('calculateDiscount', () => {
  it('applies percentage discount correctly', () => {
    expect(calculateDiscount(100, 20)).toBe(80)
  })

  it('throws when discount exceeds 100%', () => {
    expect(() => calculateDiscount(100, 110)).toThrow('Discount cannot exceed 100%')
  })

  it('returns original price when discount is 0', () => {
    expect(calculateDiscount(100, 0)).toBe(100)
  })
})
```

### Python (pytest)

```python
# tests/unit/test_utils.py
import pytest
from app.utils import calculate_discount

class TestCalculateDiscount:
    def test_applies_percentage_discount(self):
        assert calculate_discount(100, 20) == 80

    def test_raises_when_discount_exceeds_100(self):
        with pytest.raises(ValueError, match="Discount cannot exceed 100%"):
            calculate_discount(100, 110)

    def test_returns_original_price_for_zero_discount(self):
        assert calculate_discount(100, 0) == 100
```

---

## Integration Tests

### API Integration (TypeScript)

```typescript
// tests/integration/users.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { createServer } from '../helpers/server'
import { createTestUser, cleanupTestUser } from '../helpers/fixtures'

describe('POST /api/v1/users', () => {
  let server: ReturnType<typeof createServer>

  beforeAll(() => { server = createServer() })
  afterAll(() => server.close())

  it('creates a user with valid data', async () => {
    const response = await server.inject({
      method: 'POST',
      url: '/api/v1/users',
      payload: { email: 'test@example.com', name: 'Test User' },
    })

    expect(response.statusCode).toBe(201)
    expect(response.json().data).toMatchObject({
      email: 'test@example.com',
      name: 'Test User',
    })
  })

  it('returns 422 for invalid email', async () => {
    const response = await server.inject({
      method: 'POST',
      url: '/api/v1/users',
      payload: { email: 'not-an-email', name: 'Test' },
    })

    expect(response.statusCode).toBe(422)
  })
})
```

### Database Integration (Python)

```python
# tests/integration/test_user_repository.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.user_repository import UserRepository

@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    repo = UserRepository(db_session)
    user = await repo.create(email="test@example.com", name="Test User")

    assert user.id is not None
    assert user.email == "test@example.com"

    # Verify it's persisted
    found = await repo.find_by_id(user.id)
    assert found is not None
    assert found.email == user.email
```

---

## E2E Tests (Playwright)

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('user can sign up and log in', async ({ page }) => {
    // Sign up
    await page.goto('/auth/signup')
    await page.fill('[data-testid="email-input"]', 'newuser@example.com')
    await page.fill('[data-testid="password-input"]', 'SecurePassword123!')
    await page.click('[data-testid="signup-button"]')

    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard')
    await expect(page.locator('[data-testid="user-greeting"]')).toBeVisible()
  })

  test('shows error for invalid credentials', async ({ page }) => {
    await page.goto('/auth/login')
    await page.fill('[data-testid="email-input"]', 'wrong@example.com')
    await page.fill('[data-testid="password-input"]', 'wrongpassword')
    await page.click('[data-testid="login-button"]')

    await expect(page.locator('[data-testid="error-message"]'))
      .toContainText('Invalid email or password')
  })
})
```

---

## Component Tests (Testing Library)

```typescript
// src/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    fireEvent.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalledOnce()
  })

  it('is disabled when loading', () => {
    render(<Button loading>Submit</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

---

## Mocking Patterns

### Mock External APIs (MSW)

```typescript
// tests/mocks/handlers.ts
import { http, HttpResponse } from 'msw'

export const handlers = [
  http.get('https://api.openai.com/v1/chat/completions', () => {
    return HttpResponse.json({
      choices: [{ message: { content: 'Mocked AI response' } }],
    })
  }),

  http.post('https://api.stripe.com/v1/payment_intents', () => {
    return HttpResponse.json({ id: 'pi_test_123', status: 'succeeded' })
  }),
]
```

### Mock Database (pytest)

```python
# tests/conftest.py
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("postgresql+asyncpg://test:test@localhost/test_db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()
```

---

## Running Tests

```bash
# Unit tests
npm test                    # Run all
npm test -- --watch         # Watch mode
npm test -- --coverage      # With coverage

# E2E tests
npx playwright test         # Run all E2E
npx playwright test auth    # Run specific test file
npx playwright test --ui    # Interactive UI mode

# Python tests
pytest                      # Run all
pytest -v                   # Verbose
pytest --cov=app            # With coverage
pytest -k "test_user"       # Filter by name
pytest tests/unit/          # Specific directory
```

---

## CI Test Configuration

```yaml
# .github/workflows/test.yml
- name: Run unit tests
  run: npm test -- --coverage --reporter=json

- name: Upload coverage
  uses: codecov/codecov-action@v3

- name: Run E2E tests
  run: npx playwright test
  env:
    PLAYWRIGHT_BASE_URL: ${{ env.STAGING_URL }}
```

---

*Last Updated: <!-- YYYY-MM-DD --> | Update when testing strategy changes*

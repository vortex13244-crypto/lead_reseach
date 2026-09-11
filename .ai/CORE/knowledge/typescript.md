# TypeScript — Knowledge Base

> **Purpose:** TypeScript best practices, type patterns, and configuration.
> **Version:** TypeScript 5.x (strict mode)
> **Related:** [react.md](react.md) · [nextjs.md](nextjs.md) · [../standards/code-style.md](../standards/code-style.md)

---

## Overview

TypeScript is the primary language for all frontend and Node.js backend code. Always enable `strict: true`. Use TypeScript to eliminate entire classes of runtime errors, not just as documentation.

---

## Configuration

```json
// tsconfig.json — recommended settings
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["DOM", "DOM.Iterable", "ESNext"],
    "strict": true,                    // Always true
    "noUncheckedIndexedAccess": true,  // Array access returns T | undefined
    "noImplicitReturns": true,         // All code paths must return
    "exactOptionalPropertyTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "bundler",
    "paths": {
      "@/*": ["./src/*"]              // Absolute imports
    }
  }
}
```

---

## Best Practices

### Prefer `type` over `interface` for unions

```typescript
// Type — for union types, mapped types, conditional types
type Status = 'active' | 'inactive' | 'pending'
type ID = string

// Interface — for object shapes that can be extended
interface User {
  id: string
  email: string
  name: string
}

// Both are fine for plain object types — be consistent within a codebase
```

### Discriminated Unions

```typescript
// Model states explicitly — eliminates impossible states
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error }

function renderState<T>(state: AsyncState<T>) {
  switch (state.status) {
    case 'idle': return <EmptyState />
    case 'loading': return <Skeleton />
    case 'success': return <DataView data={state.data} />  // data is T here
    case 'error': return <ErrorMessage error={state.error} />  // error is Error here
  }
}
```

### Avoid `any` — Use `unknown`

```typescript
// WRONG — bypasses type system
function process(data: any) {
  data.foo()  // No error, but crashes at runtime if data has no foo
}

// RIGHT — force narrowing before use
function process(data: unknown) {
  if (typeof data === 'string') {
    console.log(data.toUpperCase())  // TypeScript knows it's string here
  }
}

// For external API responses — use Zod to parse and validate
const schema = z.object({ id: z.string(), name: z.string() })
const result = schema.parse(apiResponse)  // result is typed and validated
```

### Utility Types

```typescript
// Pick — select specific fields
type UserPreview = Pick<User, 'id' | 'name' | 'avatarUrl'>

// Omit — exclude fields
type UserWithoutPassword = Omit<User, 'passwordHash'>

// Partial — all fields optional (useful for update types)
type UserUpdate = Partial<Pick<User, 'name' | 'bio' | 'avatarUrl'>>

// Required — all optional fields become required
type RequiredUser = Required<User>

// Record — typed map
type PermissionMap = Record<UserRole, Permission[]>

// ReturnType — extract return type of function
type DashboardData = ReturnType<typeof getDashboardData>

// Awaited — unwrap Promise
type UserData = Awaited<ReturnType<typeof fetchUser>>
```

### Template Literal Types

```typescript
type EventName = 'click' | 'focus' | 'blur'
type HandlerName = `on${Capitalize<EventName>}`
// HandlerName = 'onClick' | 'onFocus' | 'onBlur'

// API route type safety
type Route = `/api/v1/${'users' | 'posts' | 'comments'}`
```

### Branded Types

```typescript
// Prevent mixing up IDs of different entity types
type UserId = string & { readonly __brand: 'UserId' }
type OrderId = string & { readonly __brand: 'OrderId' }

function createUserId(id: string): UserId {
  return id as UserId
}

// Now you can't accidentally pass an OrderId where a UserId is expected
function getUser(id: UserId): Promise<User> { ... }
const orderId = createOrderId('order_123')
// getUser(orderId)  // ← TypeScript error! 
```

---

## Patterns

### Assertion Functions

```typescript
function assertIsUser(value: unknown): asserts value is User {
  if (!value || typeof value !== 'object' || !('id' in value)) {
    throw new Error('Expected a User object')
  }
}

const data: unknown = await fetchUser()
assertIsUser(data)  // Throws if not User
console.log(data.name)  // TypeScript knows data is User here
```

### Generic Constraints

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]  // T[K] — the exact type of that property
}

const user: User = { id: '1', name: 'Alice', email: 'alice@example.com' }
const name = getProperty(user, 'name')  // string (not any)
```

---

## Common Mistakes

### ❌ Type assertions hiding bugs

```typescript
// WRONG — silences the error but doesn't fix it
const user = fetchUser() as User  // fetchUser returns Promise<User>!

// RIGHT — await first
const user = await fetchUser()
```

### ❌ Non-null assertions on uncertain values

```typescript
// WRONG — crashes if user is null
const name = user!.name

// RIGHT — handle the null case
if (!user) throw new NotFoundError('User not found')
const name = user.name
```

---

## Resources

- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [Total TypeScript](https://www.totaltypescript.com/)
- [Type Challenges](https://github.com/type-challenges/type-challenges)

# React — Knowledge Base

> **Purpose:** React best practices, patterns, and common pitfalls.
> **Version Reference:** React 18+ (concurrent features enabled)
> **Related:** [nextjs.md](nextjs.md) · [typescript.md](typescript.md) · [../standards/ui-guidelines.md](../standards/ui-guidelines.md)

---

## Overview

React is a UI library for building component-based user interfaces. In this workspace, React is used through Next.js. Prefer React Server Components (RSC) for data fetching; use Client Components (`'use client'`) only when you need browser APIs, event handlers, or state.

---

## Best Practices

### Component Design

```tsx
// ✅ Good: Typed, focused, descriptive
interface UserCardProps {
  user: Pick<User, 'id' | 'name' | 'email' | 'avatarUrl'>
  onSelect?: (id: string) => void
  className?: string
}

export function UserCard({ user, onSelect, className }: UserCardProps) {
  return (
    <div
      className={cn('rounded-lg border p-4', className)}
      onClick={() => onSelect?.(user.id)}
    >
      <Avatar src={user.avatarUrl} alt={user.name} />
      <h3 className="font-semibold">{user.name}</h3>
      <p className="text-sm text-muted-foreground">{user.email}</p>
    </div>
  )
}
```

### State Management

```tsx
// Local state: useState (simple values)
const [isOpen, setIsOpen] = useState(false)

// Complex local state: useReducer
const [state, dispatch] = useReducer(reducer, initialState)

// Server state: TanStack Query (async, cached)
const { data, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
})

// Global client state: Zustand
const useStore = create<State>((set) => ({
  theme: 'dark',
  setTheme: (theme) => set({ theme }),
}))

// URL state: nuqs (synced to search params)
const [page, setPage] = useQueryState('page', parseAsInteger.withDefault(1))
```

### Data Fetching (Next.js App Router)

```tsx
// Server Component (preferred for initial data)
async function UserList() {
  const users = await getUsers()  // Direct DB/API call, no useEffect
  return <UserListUI users={users} />
}

// Client Component (for interactive data)
'use client'
function UserSearch() {
  const [query, setQuery] = useState('')
  const { data } = useQuery({
    queryKey: ['users', query],
    queryFn: () => searchUsers(query),
  })
  // ...
}
```

---

## Architecture Patterns

### Container / Presentational Split

```tsx
// Container: handles data and logic
async function UserPageContainer() {
  const users = await getUsers()
  return <UserPageView users={users} />
}

// Presentational: pure UI, easily testable
function UserPageView({ users }: { users: User[] }) {
  return (
    <div className="grid gap-4">
      {users.map(user => <UserCard key={user.id} user={user} />)}
    </div>
  )
}
```

### Compound Components

```tsx
// For complex, related component groups
<Select>
  <Select.Trigger>Choose option</Select.Trigger>
  <Select.Content>
    <Select.Item value="a">Option A</Select.Item>
    <Select.Item value="b">Option B</Select.Item>
  </Select.Content>
</Select>
```

### Custom Hooks

```tsx
// Extract reusable stateful logic into hooks
function useUserProfile(userId: string) {
  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile', userId],
    queryFn: () => fetchProfile(userId),
    staleTime: 5 * 60 * 1000,
  })

  const updateMutation = useMutation({
    mutationFn: updateProfile,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['profile', userId] }),
  })

  return { profile, isLoading, updateProfile: updateMutation.mutate }
}
```

---

## Common Mistakes

### ❌ `useEffect` for data fetching

```tsx
// WRONG — causes race conditions, double-fetching in StrictMode
useEffect(() => {
  fetch('/api/users').then(r => r.json()).then(setUsers)
}, [])

// RIGHT — use TanStack Query or server components
const { data: users } = useQuery({ queryKey: ['users'], queryFn: fetchUsers })
```

### ❌ Missing `key` in lists

```tsx
// WRONG — React can't track which item is which
{users.map(user => <UserCard user={user} />)}

// RIGHT — stable, unique key
{users.map(user => <UserCard key={user.id} user={user} />)}
```

### ❌ Stale closures in `useEffect`

```tsx
// WRONG — captures stale `count` value
useEffect(() => {
  const interval = setInterval(() => setCount(count + 1), 1000)
  return () => clearInterval(interval)
}, [])  // Missing count

// RIGHT — use functional update
useEffect(() => {
  const interval = setInterval(() => setCount(c => c + 1), 1000)
  return () => clearInterval(interval)
}, [])
```

---

## Performance Tips

1. **Server Components** — Move data fetching to server; eliminates client waterfalls
2. **`memo()`** — Only for pure components with expensive renders; profile first
3. **`useMemo()`** — For expensive computations; not for object identity
4. **`useCallback()`** — Only when passing to memoized children
5. **Virtualization** — `@tanstack/react-virtual` for long lists (1000+ items)
6. **Code splitting** — `dynamic()` for heavy components not needed on first paint

---

## Examples

See: [../snippets/react-component.md](../snippets/react-component.md)

---

## Resources

- [React Docs](https://react.dev)
- [TanStack Query](https://tanstack.com/query)
- [Zustand](https://zustand-demo.pmnd.rs/)
- [shadcn/ui](https://ui.shadcn.com)

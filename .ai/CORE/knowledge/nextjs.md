# Next.js — Knowledge Base

> **Purpose:** Next.js best practices, App Router patterns, and common pitfalls.
> **Version:** Next.js 14+ (App Router)
> **Related:** [react.md](react.md) · [typescript.md](typescript.md)

---

## Overview

Next.js is the primary web framework in this workspace. Always use the **App Router** (not Pages Router). Prefer **React Server Components** for data fetching. Use **Route Handlers** for APIs.

---

## Best Practices

### App Router Structure

```
src/app/
├── (marketing)/              # Route group — no URL prefix
│   ├── page.tsx              # → /
│   ├── pricing/page.tsx      # → /pricing
│   └── layout.tsx            # Shared layout for marketing
├── (dashboard)/              # Protected routes group
│   ├── layout.tsx            # Dashboard layout with auth check
│   ├── dashboard/page.tsx    # → /dashboard
│   └── settings/
│       ├── page.tsx          # → /settings
│       └── profile/page.tsx  # → /settings/profile
└── api/
    └── v1/
        └── users/
            └── route.ts      # Route Handler → /api/v1/users
```

### Server vs Client Components

```tsx
// SERVER COMPONENT (default) — runs on server, no bundle size
// ✅ Use for: data fetching, auth checks, heavy computation
async function Dashboard() {
  const session = await auth()
  if (!session) redirect('/login')
  
  const data = await getDashboardData(session.userId)  // Direct DB call
  return <DashboardView data={data} />
}

// CLIENT COMPONENT — shipped to browser
// ✅ Use for: event handlers, state, browser APIs, interactivity
'use client'
function InteractiveWidget() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

### Data Fetching

```tsx
// In Server Components — direct async/await
async function UserList() {
  // Parallel fetching (faster than sequential)
  const [users, stats] = await Promise.all([getUsers(), getStats()])
  return <UserListView users={users} stats={stats} />
}

// Route Handler (API)
// src/app/api/v1/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const page = Number(searchParams.get('page') ?? '1')

  const users = await getUsersPaginated(page)
  return NextResponse.json({ data: users })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const validated = createUserSchema.parse(body)  // throws on invalid
  const user = await createUser(validated)
  return NextResponse.json({ data: user }, { status: 201 })
}
```

### Caching

```tsx
// Static (cached until rebuild)
fetch('https://api.example.com/config', { cache: 'force-cache' })

// ISR (revalidate every N seconds)
fetch('https://api.example.com/posts', { next: { revalidate: 3600 } })

// Dynamic (never cached — per request)
fetch('https://api.example.com/user/profile', { cache: 'no-store' })

// On-demand revalidation
import { revalidatePath, revalidateTag } from 'next/cache'
revalidatePath('/dashboard')
revalidateTag('user-data')
```

### Metadata

```tsx
// Static metadata
export const metadata: Metadata = {
  title: 'Dashboard | MyApp',
  description: 'Manage your projects and team',
}

// Dynamic metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const project = await getProject(params.id)
  return {
    title: `${project.name} | MyApp`,
    description: project.description,
  }
}
```

---

## Architecture

### Route Groups

```
app/
├── (auth)/               # No auth required
│   ├── login/page.tsx
│   └── signup/page.tsx
├── (protected)/          # Auth required in layout
│   ├── layout.tsx        # Auth check here
│   ├── dashboard/
│   └── settings/
└── (admin)/              # Admin role required
    ├── layout.tsx        # Admin check here
    └── users/
```

### Middleware

```typescript
// middleware.ts — runs on Edge runtime before every request
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const protectedPaths = ['/dashboard', '/settings', '/api/v1']

export function middleware(request: NextRequest) {
  const isProtected = protectedPaths.some(path => 
    request.nextUrl.pathname.startsWith(path)
  )
  
  if (isProtected) {
    const token = request.cookies.get('auth-token')?.value
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}
```

---

## Common Mistakes

### ❌ Using Pages Router patterns in App Router

```tsx
// WRONG — getServerSideProps is Pages Router only
export async function getServerSideProps() { ... }

// RIGHT — just make the component async
async function Page() {
  const data = await getData()
  return <View data={data} />
}
```

### ❌ Client Component fetching on mount

```tsx
// WRONG — waterfall: render → useEffect → fetch → render
'use client'
function UserProfile() {
  const [user, setUser] = useState(null)
  useEffect(() => { fetchUser().then(setUser) }, [])
  // ...
}

// RIGHT — Server Component
async function UserProfile() {
  const user = await fetchUser()
  return <UserProfileView user={user} />
}
```

### ❌ Missing error.tsx and loading.tsx

```
# Every page directory should have these if it fetches data:
src/app/(dashboard)/dashboard/
├── page.tsx
├── loading.tsx    # Shown while page.tsx is loading (Suspense boundary)
└── error.tsx      # Shown if page.tsx throws (Error boundary)
```

---

## Performance Tips

1. Use **RSC** for all data fetching — no client-side waterfalls
2. **Parallel data fetching** with `Promise.all()`
3. **Streaming** with `<Suspense>` for non-critical content
4. **`next/image`** — automatic WebP, lazy loading, size optimization
5. **`next/font`** — self-hosted fonts, zero layout shift
6. **Route segments** with `export const dynamic = 'force-static'` for static pages

---

## Resources

- [Next.js Docs](https://nextjs.org/docs)
- [App Router examples](https://github.com/vercel/next.js/tree/canary/examples)
- [next-safe-action](https://next-safe-action.dev/) — Type-safe Server Actions
- [nuqs](https://nuqs.47ng.com/) — Type-safe search params state

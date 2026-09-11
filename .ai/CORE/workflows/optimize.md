# Workflow: Optimize Performance

> **Purpose:** Systematic performance investigation and optimization process.
> **Role:** [performance-engineer.md](../roles/performance-engineer.md)
> **Related:** [docs/performance.md](../docs/performance.md) · [checklists/performance.md](../checklists/performance.md)

---

## Step 1: Identify the Bottleneck

**Don't optimize without data.** Start with measurement.

```bash
# Frontend: Run Lighthouse
npx lighthouse https://staging.yourdomain.com/target-page --view

# Backend: Check Sentry / Grafana for slow endpoints
# Look for: p95 > 500ms, p99 > 1s

# Database: Check slow query log
# SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;
```

Output a baseline:
```
Baseline (before optimization):
- LCP: 4.2s
- Bundle size: 1.1MB (gzipped: 380KB)
- API /dashboard: p95 = 2800ms
- DB queries per request: 47
```

---

## Step 2: Prioritize

Rank issues by: **Impact × Effort**

| Issue | Impact | Effort | Priority |
|-------|--------|--------|----------|
| N+1 query (47 queries → 2) | High | Low | Fix first |
| Image optimization | Medium | Low | Fix second |
| Bundle splitting | Medium | Medium | Fix third |
| Redis caching for dashboard | High | Medium | Fix fourth |

---

## Step 3: Fix Database Performance

```typescript
// Step 3a: Find N+1 queries
// Enable query logging in development
const prisma = new PrismaClient({ log: ['query'] })

// Step 3b: Fix with batch loading
// BEFORE (N+1)
const projects = await prisma.project.findMany()
for (const project of projects) {
  project.tasks = await prisma.task.findMany({ where: { projectId: project.id } })
}

// AFTER (1 query with include)
const projects = await prisma.project.findMany({
  include: { tasks: { select: { id: true, title: true, status: true } } }
})

// Step 3c: Add missing indices
await prisma.$executeRaw`
  CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_project_status
  ON tasks(project_id, status)
  WHERE deleted_at IS NULL
`

// Step 3d: Add Redis caching for expensive queries
const CACHE_TTL = 300 // 5 minutes

async function getDashboardData(userId: string) {
  const cached = await redis.get(`dashboard:${userId}`)
  if (cached) return JSON.parse(cached)

  const data = await computeExpensiveDashboardData(userId)
  await redis.setex(`dashboard:${userId}`, CACHE_TTL, JSON.stringify(data))
  return data
}
```

---

## Step 4: Fix Frontend Performance

```bash
# Step 4a: Analyze bundle
ANALYZE=true npm run build

# Step 4b: Find large dependencies
# In bundle analyzer, look for:
# - Libraries imported but partially used (lodash → lodash-es with tree shaking)
# - Libraries with smaller alternatives (moment.js → date-fns)
# - Libraries that should be lazy-loaded
```

```typescript
// Step 4c: Lazy load heavy components
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false,
})

// Step 4d: Optimize images
import Image from 'next/image'
// Always specify width, height, and use priority for above-the-fold
<Image src={hero} width={1200} height={600} priority alt="Hero" />

// Step 4e: Optimize data fetching
// Use React Server Components for static data
// Use TanStack Query for client-side data with staleTime

const { data } = useQuery({
  queryKey: ['dashboard', userId],
  queryFn: fetchDashboard,
  staleTime: 5 * 60 * 1000, // Don't refetch for 5 minutes
})
```

---

## Step 5: Verify Improvement

```bash
# Run Lighthouse again
npx lighthouse https://staging.yourdomain.com/target-page --view

# API timing
for i in {1..20}; do
  curl -w "%{time_total}\n" -s -o /dev/null https://staging.yourdomain.com/api/dashboard
done | sort -n | awk 'NR==int(NR*0.95)' # p95
```

Document results:
```
After optimization:
- LCP: 1.8s (↓57%)
- Bundle size: 420KB gzipped (↓↓)
- API /dashboard: p95 = 180ms (↓93%)
- DB queries per request: 2 (↓96%)
```

---

## Step 6: Prevent Regression

```javascript
// Add performance test to CI
// k6 load test that fails if p95 > threshold

export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],  // Fail CI if p95 > 500ms
  },
}
```

---

## Step 7: Document

```markdown
Update memory/completed.md with:
- What was optimized
- Before/after metrics
- What techniques were used

Update memory/known-issues.md with:
- Any remaining performance issues
- Accepted performance limitations
```

---

*Related: [performance-engineer.md](../roles/performance-engineer.md) · [docs/performance.md](../docs/performance.md)*

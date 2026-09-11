# Performance Documentation

> **Purpose:** Performance architecture, benchmarks, optimization strategies, and monitoring.
> **Related:** [../roles/performance-engineer.md](../roles/performance-engineer.md) · [../checklists/performance.md](../checklists/performance.md) · [../workflows/optimize.md](../workflows/optimize.md)

---

## Performance Targets

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| TTFB (Time to First Byte) | < 200ms | > 500ms |
| LCP (Largest Contentful Paint) | < 2.5s | > 4s |
| FID / INP | < 100ms | > 300ms |
| CLS (Cumulative Layout Shift) | < 0.1 | > 0.25 |
| API response (p95) | < 300ms | > 1s |
| API response (p99) | < 1s | > 3s |
| Database query (p95) | < 100ms | > 500ms |
| Memory (server) | < 512MB | > 1GB |
| Error rate | < 0.1% | > 1% |

---

## Frontend Performance

### Core Web Vitals Optimization

```typescript
// Next.js Image Optimization
import Image from 'next/image'

// WRONG ❌
<img src="/hero.jpg" width="800" height="600" />

// RIGHT ✅
<Image
  src="/hero.jpg"
  width={800}
  height={600}
  priority  // For above-the-fold images
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

### Bundle Size

```bash
# Analyze bundle
npx @next/bundle-analyzer
npm run build -- --analyze

# Targets
# JavaScript bundle: < 200KB (gzipped)
# CSS bundle: < 50KB (gzipped)
# Largest chunk: < 100KB
```

### Code Splitting

```typescript
// Dynamic imports for heavy components
import dynamic from 'next/dynamic'

const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,  // Only if component needs browser APIs
})

// Route-based code splitting (automatic in Next.js App Router)
// Each page.tsx is automatically code-split
```

### Caching Strategy

```typescript
// Next.js fetch caching
// Static data (rebuild to update)
const data = await fetch('/api/config', { cache: 'force-cache' })

// Revalidated data (ISR)
const data = await fetch('/api/products', { next: { revalidate: 3600 } })

// Dynamic data (no cache)
const data = await fetch('/api/user/profile', { cache: 'no-store' })
```

---

## Backend Performance

### Database Optimization

```typescript
// Connection pooling
const prisma = new PrismaClient({
  datasources: {
    db: { url: process.env.DATABASE_URL }
  },
  log: process.env.NODE_ENV === 'development' ? ['query', 'warn', 'error'] : ['error'],
})

// Batch queries — avoid N+1
// WRONG ❌ — N+1 queries
const users = await prisma.user.findMany()
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { userId: user.id } })
}

// RIGHT ✅ — single query with include
const users = await prisma.user.findMany({
  include: { posts: true }
})

// Select only needed fields
const users = await prisma.user.findMany({
  select: { id: true, email: true, name: true }  // Not password, not full profile
})
```

### Redis Caching

```typescript
import { redis } from '@/lib/redis'

async function getUserWithCache(userId: string): Promise<User> {
  const cacheKey = `user:${userId}`

  // Try cache first
  const cached = await redis.get(cacheKey)
  if (cached) return JSON.parse(cached)

  // Fallback to database
  const user = await prisma.user.findUnique({ where: { id: userId } })
  if (!user) throw new NotFoundError()

  // Cache for 5 minutes
  await redis.setex(cacheKey, 300, JSON.stringify(user))

  return user
}

// Cache invalidation
async function invalidateUserCache(userId: string): Promise<void> {
  await redis.del(`user:${userId}`)
}
```

### API Response Optimization

```typescript
// Pagination — never return unbounded lists
const PAGE_SIZE = 20
const MAX_PAGE_SIZE = 100

// Compression
import compression from 'compression'
app.use(compression({ level: 6 }))

// HTTP/2 push for critical resources (Next.js handles this)

// Streaming for large responses
export async function GET(request: Request) {
  const encoder = new TextEncoder()
  const stream = new ReadableStream({
    async start(controller) {
      for await (const chunk of generateLargeResponse()) {
        controller.enqueue(encoder.encode(JSON.stringify(chunk) + '\n'))
      }
      controller.close()
    }
  })
  return new Response(stream, { headers: { 'Content-Type': 'application/x-ndjson' } })
}
```

---

## Python / FastAPI Performance

```python
# Use async everywhere
from fastapi import FastAPI
import asyncio

@app.get("/users/{user_id}")
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    return await user_service.get_by_id(db, user_id)

# Connection pooling
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

# Background tasks for non-blocking operations
from fastapi import BackgroundTasks

@app.post("/users")
async def create_user(user_data: UserCreate, background_tasks: BackgroundTasks):
    user = await user_service.create(user_data)
    background_tasks.add_task(send_welcome_email, user.email)  # Non-blocking
    return user
```

---

## Performance Monitoring

### Metrics Collection

```typescript
// OpenTelemetry setup
import { NodeSDK } from '@opentelemetry/sdk-node'
import { PrometheusExporter } from '@opentelemetry/exporter-prometheus'

const sdk = new NodeSDK({
  metricReader: new PrometheusExporter({ port: 9090 }),
})

// Custom metrics
const httpRequestDuration = meter.createHistogram('http_request_duration_ms', {
  description: 'HTTP request duration in milliseconds',
  unit: 'ms',
})

// Measure
const start = performance.now()
// ... handle request ...
httpRequestDuration.record(performance.now() - start, { route: '/api/users' })
```

### Profiling

```bash
# Node.js CPU profiling
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Memory leak detection
node --expose-gc app.js  # Then use clinic.js

# Python profiling
python -m cProfile -o output.prof app.py
snakeviz output.prof     # Visual profiler

# Database: pg_stat_statements
SELECT query, calls, total_time/calls AS avg_ms, rows
FROM pg_stat_statements
WHERE calls > 100
ORDER BY total_time/calls DESC
LIMIT 20;
```

---

## Load Testing

```javascript
// k6 load test
import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // Ramp up
    { duration: '60s', target: 100 },  // Sustained load
    { duration: '30s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'],  // 95% under 300ms
    http_req_failed: ['rate<0.01'],    // < 1% error rate
  },
}

export default function () {
  const res = http.get('https://staging.yourdomain.com/api/health')
  check(res, { 'status is 200': (r) => r.status === 200 })
  sleep(1)
}
```

```bash
# Run load test
k6 run load-test.js

# Locust (Python)
locust -f locustfile.py --host=https://staging.yourdomain.com
```

---

*Last Updated: <!-- YYYY-MM-DD --> | Review targets quarterly*

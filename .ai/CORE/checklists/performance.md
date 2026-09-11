# Checklist: Performance

> **Purpose:** Performance verification before releases and for optimization audits.
> **Related:** [docs/performance.md](../docs/performance.md) · [workflows/optimize.md](../workflows/optimize.md)

---

## Targets (must pass before release)

| Metric | Target | How to Check |
|--------|--------|-------------|
| LCP | < 2.5s | Lighthouse |
| INP | < 200ms | Lighthouse |
| CLS | < 0.1 | Lighthouse |
| JS Bundle (gzipped) | < 200KB | Bundle analyzer |
| API p95 | < 300ms | Grafana / k6 |
| API p99 | < 1s | Grafana / k6 |
| DB query p95 | < 100ms | pg_stat_statements |

---

## Frontend

- [ ] Lighthouse Performance score ≥ 90 (run on staging)
- [ ] LCP < 2.5s on all key pages
- [ ] No render-blocking resources
- [ ] JavaScript bundle ≤ 200KB gzipped
- [ ] CSS bundle ≤ 50KB gzipped
- [ ] Images in WebP or AVIF format
- [ ] All images have explicit `width` and `height` attributes
- [ ] Above-the-fold images use `priority` prop (Next.js)
- [ ] Below-the-fold images use lazy loading
- [ ] Fonts loaded with `font-display: swap`
- [ ] Static assets served via CDN
- [ ] No unnecessary React re-renders (use React DevTools Profiler)
- [ ] Large components lazily imported with `dynamic()`

---

## Backend

- [ ] API endpoints p95 < 300ms under normal load
- [ ] No synchronous blocking calls in request handlers
- [ ] All I/O is async (no blocking file reads, network calls)
- [ ] Response compression enabled (gzip/brotli)
- [ ] All list endpoints are paginated (no unbounded queries)
- [ ] Connection pooling configured (Prisma, SQLAlchemy, PgBouncer)
- [ ] Memory usage stable (no memory leaks in 24h)

---

## Database

- [ ] No N+1 queries (verified with query logging)
- [ ] All foreign keys have indices
- [ ] All frequently filtered columns have indices
- [ ] `EXPLAIN ANALYZE` shows index scans on critical queries
- [ ] No queries return more than 1000 rows without pagination
- [ ] `autovacuum` running (check `pg_stat_user_tables.n_dead_tup`)
- [ ] `pg_stat_statements` enabled for production monitoring
- [ ] Connection pool not exhausted under load

---

## Caching

- [ ] Redis cache configured for expensive queries
- [ ] Cache TTLs appropriate for data freshness requirements
- [ ] Cache keys include version or user context (no data leakage)
- [ ] CDN caching configured for static assets
- [ ] Browser caching headers set for API responses (if applicable)
- [ ] Cache invalidation strategy defined for each cached resource

---

## Load Testing

- [ ] Load test run against staging with realistic traffic patterns
- [ ] Error rate < 1% under expected peak load
- [ ] Response times meet targets under load
- [ ] Database connections don't exceed pool under load
- [ ] Memory usage stable under sustained load

---

## How to Run

```bash
# Lighthouse
npx lighthouse https://staging.yourdomain.com --view

# Bundle size
ANALYZE=true npm run build

# API performance
k6 run workflows/load-test.js

# DB slow queries
psql $DATABASE_URL -c "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```

---

*Related: [docs/performance.md](../docs/performance.md) · [roles/performance-engineer.md](../roles/performance-engineer.md)*

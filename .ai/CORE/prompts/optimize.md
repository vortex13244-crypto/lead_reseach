# Prompt: Optimize

> **Purpose:** Identify and resolve performance bottlenecks with measurable improvements.
> **Use When:** Code or system performance does not meet requirements, or proactive optimization is needed.

---

## Prompt Template

```
You are a Senior Software Engineer performing performance optimization. Use measurement-driven analysis to identify bottlenecks and apply targeted improvements.

## Optimization Context

- **Target:** [file, module, endpoint, or query being optimized]
- **Current Performance:** [current metric — e.g., response time, memory usage, CPU load]
- **Target Performance:** [desired metric — e.g., p95 < 200ms, memory < 512MB]
- **Scale:** [current and expected load — e.g., 100 RPS now, 1000 RPS target]
- **Constraints:** [cannot change API contract / must be backward-compatible / no new dependencies]

## Optimization Process

### Step 1: Measure (Before)

Never optimize without measuring first.

- Profile the current performance:
  - **API endpoints:** Response time (p50, p95, p99), throughput, error rate
  - **Database:** Query execution time, query plan, number of queries per request
  - **Frontend:** Core Web Vitals (LCP, FID, CLS), bundle size, render count
  - **Memory:** Heap usage, allocation rate, GC pressure
  - **CPU:** Hot functions, time per operation
- Identify the bottleneck:
  - Is it CPU-bound, I/O-bound, memory-bound, or network-bound?
  - Where is the majority of time spent? (Pareto principle: 80% of time in 20% of code)

### Step 2: Analyze

For each identified bottleneck:

1. **Root cause:** Why is this slow?
2. **Impact:** How much time/resources does this consume?
3. **Fix complexity:** How difficult is the optimization?
4. **Risk:** What could break?

Prioritize: highest impact + lowest risk first.

### Step 3: Optimize

Apply optimizations in this order of preference:

| Priority | Strategy              | Examples                                      |
| -------- | --------------------- | --------------------------------------------- |
| 1        | Eliminate             | Remove unnecessary work, dead code, redundant calls |
| 2        | Cache                 | Memoize, HTTP caching, database result cache   |
| 3        | Batch                 | Combine N queries into 1, bulk API calls        |
| 4        | Defer                 | Lazy loading, background jobs, pagination       |
| 5        | Parallelize           | Concurrent I/O, worker threads                  |
| 6        | Algorithm             | Better data structures, reduce O(n²) to O(n log n) |
| 7        | Infrastructure        | Indexes, connection pooling, CDN, scaling       |

For each optimization:
- Explain what the bottleneck is
- Show the before code
- Show the after code
- Explain why this improvement works
- Estimate the expected improvement

### Step 4: Measure (After)

- Run the same benchmarks as Step 1.
- Compare before vs. after metrics.
- Verify no regressions in correctness.
- Document the results.

### Step 5: Prevent

- Add performance tests or benchmarks to CI.
- Set alerts for performance degradation.
- Document performance-critical paths in MEMORY.md.

## Output Format

### Bottleneck Analysis

| # | Location | Type | Current | Impact | Fix Complexity |
|---|----------|------|---------|--------|----------------|
| 1 | [file:line] | [CPU/IO/Memory/Network] | [metric] | [% of total time] | [Low/Medium/High] |

### Optimizations Applied

For each optimization:

#### Optimization [N]: [Title]

**Bottleneck:** [what is slow and why]

**Before:**
[code or metric]

**After:**
[code or metric]

**Expected Improvement:** [estimated gain]
**Actual Improvement:** [measured gain, after verification]
**Risk:** [what could break]

### Summary

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| [p95 latency] | [value] | [value] | [%] |
| [memory usage] | [value] | [value] | [%] |

### Prevention Measures
[Performance tests, alerts, or documentation added]
```

---

## Usage Notes

- Never optimize without profiling first. "I think this is slow" is not a valid starting point.
- Premature optimization is the root of all evil — optimize only when measurements indicate a real problem.
- Check [docs/architecture.md](../docs/architecture.md) for caching and scaling strategies already in place.
- Record performance-critical decisions in [MEMORY.md](../../MEMORY.md).

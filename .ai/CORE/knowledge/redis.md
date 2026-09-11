# Redis Guide

> **Purpose:** Practical use of Redis as a cache, rate-limit store, or short-lived coordination layer.

## Use Redis for

- Cached, reproducible data with a defined TTL and invalidation path.
- Rate limits, short-lived sessions, queues, or locks designed for failure.

## Do not use Redis as

- The only source of permanent product data unless that is an explicit architectural decision.
- A cache without a bounded TTL, key naming convention, and fallback to the primary store.

## Key conventions

```text
app:{environment}:user:{id}:profile
app:{environment}:rate-limit:{scope}:{subject}
```

Include the environment in every key. Avoid storing secrets or unnecessary personal data.

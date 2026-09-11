# Project State

> **Purpose:** Persistent overview of the project's technical state. Updated as the architecture evolves.
> **Related:** [active-context.md](active-context.md) · [../docs/architecture.md](../docs/architecture.md)

---

## Project Identity

| Field | Value |
|-------|-------|
| Name | <!-- Project name --> |
| Type | <!-- SaaS / API / Bot / Library / Desktop / Mobile --> |
| Phase | <!-- Concept / MVP / Beta / Production / Maintenance --> |
| Version | <!-- 0.1.0 --> |
| Last Deploy | <!-- YYYY-MM-DD --> |
| Repository | <!-- https://github.com/... --> |

---

## Architecture State

| Layer | Technology | Status | Notes |
|-------|-----------|--------|-------|
| Frontend | <!-- Next.js 14 --> | <!-- Active --> | <!-- App Router --> |
| Backend | <!-- FastAPI --> | <!-- Active --> | <!-- v0.110 --> |
| Database | <!-- PostgreSQL 16 --> | <!-- Active --> | <!-- Hosted on Railway --> |
| Cache | <!-- Redis 7 --> | <!-- Active --> | <!-- Upstash --> |
| Auth | <!-- Clerk / NextAuth --> | <!-- Active --> | <!-- --> |
| File Storage | <!-- S3 / Cloudflare R2 --> | <!-- Planned --> | <!-- --> |
| Search | <!-- None / Typesense --> | <!-- Planned --> | <!-- --> |
| AI/LLM | <!-- OpenAI GPT-4o --> | <!-- Active --> | <!-- --> |

---

## Environment Status

| Environment | URL | Status | Branch |
|-------------|-----|--------|--------|
| Local | http://localhost:3000 | Active | any |
| Staging | <!-- URL --> | <!-- Active/Down --> | main |
| Production | <!-- URL --> | <!-- Active/Down --> | main |

---

## Established Patterns

<!-- Record patterns that have been adopted and must be followed consistently -->

### Data Fetching
- <!-- e.g., All client-side data fetching uses TanStack Query -->

### Error Handling
- <!-- e.g., All API errors return { error: string, code: string, details?: object } -->

### Authentication
- <!-- e.g., JWT stored in httpOnly cookies, refreshed every 15 min -->

### Database Access
- <!-- e.g., All DB access goes through repository classes in src/infrastructure/db/ -->

---

## Technical Debt Register

| Item | Severity | Area | Created | Owner |
|------|----------|------|---------|-------|
| <!-- debt item --> | <!-- High/Med/Low --> | <!-- Frontend --> | <!-- date --> | <!-- AI/Dev --> |

---

## Dependency Audit

| Package | Version | Last Checked | Risk |
|---------|---------|-------------|------|
| <!-- package --> | <!-- version --> | <!-- date --> | <!-- Low/Med/High --> |

---

## Infrastructure Topology

```
[User] → [CDN / Vercel Edge]
              ↓
         [Next.js App]
         /            \
  [API Routes]    [Static Assets]
        ↓
  [FastAPI Backend]
   /    |    \
[DB] [Cache] [LLM API]
```

---

*Last Updated: <!-- YYYY-MM-DD --> | Update after architecture changes*

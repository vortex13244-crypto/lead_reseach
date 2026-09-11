# Workflow: Build SaaS Product

> **Purpose:** End-to-end guide for building a SaaS product from concept to launch.
> **Roles:** [architect.md](../roles/architect.md) · [backend.md](../roles/backend.md) · [frontend.md](../roles/frontend.md) · [devops.md](../roles/devops.md)
> **Estimated Time:** 2-8 weeks depending on scope

---

## Phase 0: Foundation (Day 1)

### Step 1: Define the Product

```markdown
Complete docs/vision.md:
- What problem does it solve?
- Who are the users?
- What is the MVP scope?
- What does success look like?
```

### Step 2: Technical Architecture

```markdown
Complete docs/architecture.md:
- Choose: Monolith vs Microservices (start with monolith)
- Frontend: Next.js App Router
- Backend: Next.js API Routes / FastAPI
- Database: PostgreSQL + Redis
- Auth: Clerk / NextAuth / Custom JWT
- Payments: Stripe
- Email: Resend / Postmark
- File Storage: Cloudflare R2 / AWS S3
```

### Step 3: Project Setup

```bash
# Initialize Next.js project
npx create-next-app@latest . --typescript --tailwind --app --src-dir

# Install core dependencies
npm install @prisma/client prisma
npm install @clerk/nextjs  # or next-auth
npm install stripe @stripe/stripe-js
npm install resend
npm install zod
npm install @tanstack/react-query
npm install zustand
npm install class-variance-authority clsx tailwind-merge

# UI components
npx shadcn@latest init
npx shadcn@latest add button input form label card dialog

# Dev dependencies
npm install -D @types/node typescript eslint prettier
```

### Step 4: Project Structure

```
src/
├── app/                        # Next.js App Router
│   ├── (auth)/                 # Auth pages (login, signup)
│   ├── (dashboard)/            # Protected dashboard pages
│   ├── (marketing)/            # Public marketing pages
│   └── api/                    # API routes
├── components/
│   ├── ui/                     # shadcn/ui components
│   ├── forms/                  # Form components
│   ├── layout/                 # Layout components
│   └── features/               # Feature-specific components
├── lib/
│   ├── db.ts                   # Prisma client
│   ├── redis.ts                # Redis client
│   ├── stripe.ts               # Stripe client
│   └── email.ts                # Email client
├── hooks/                      # React hooks
├── stores/                     # Zustand stores
├── types/                      # TypeScript types
└── utils/                      # Utility functions
```

---

## Phase 1: Core Infrastructure (Days 2-5)

### Step 5: Database Setup

```bash
# Initialize Prisma
npx prisma init

# Define schema (see docs/database.md for patterns)
# Minimum schema:
# - users table
# - sessions (if custom auth)
# - subscriptions table

# Run migrations
npx prisma migrate dev --name init
npx prisma generate
```

### Step 6: Authentication

Choose one strategy:

**Option A: Clerk (recommended for speed)**
```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

const isProtectedRoute = createRouteMatcher(['/dashboard(.*)'])

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) await auth.protect()
})
```

**Option B: Custom JWT (recommended for control)**
```typescript
// Follow roles/backend.md auth patterns
// See snippets/api.md for JWT implementation
```

### Step 7: Environment Configuration

```bash
# Create .env.local from template
cp snippets/environment.md .env.example
cp .env.example .env.local
# Fill in all values

# Add validation
# src/lib/env.ts — validate with Zod at startup
```

### Step 8: Payments (Stripe)

```typescript
// Core Stripe setup
// 1. Create products and prices in Stripe dashboard
// 2. Implement checkout session creation
// 3. Set up webhook handler for subscription events
// 4. Store subscription status in database

// Key webhook events to handle:
// - checkout.session.completed
// - customer.subscription.updated
// - customer.subscription.deleted
// - invoice.payment_failed
```

---

## Phase 2: Core Features (Days 5-14)

### Step 9: Define MVP Features

From `docs/features.md`, identify the 3-5 features that are the core value proposition. Build these first.

For each feature, follow `workflows/new-feature.md`.

### Step 10: Marketing Pages

```
/                   → Landing page (hero, features, pricing, CTA)
/pricing            → Pricing page with plan comparison
/blog               → Blog (optional, use MDX)
/about              → About page
/legal/privacy      → Privacy policy
/legal/terms        → Terms of service
```

### Step 11: Dashboard

```
/dashboard          → Main dashboard
/dashboard/settings → User settings
/dashboard/billing  → Subscription management
/dashboard/[feature] → Core feature pages
```

---

## Phase 3: Infrastructure (Days 10-14)

### Step 12: Error Monitoring

```bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

### Step 13: CI/CD Pipeline

```bash
# Create GitHub Actions workflow
# See: snippets/github-actions.md

# Minimum pipeline:
# 1. Lint + type check
# 2. Unit tests
# 3. Build
# 4. Deploy to Vercel
```

### Step 14: Environment Setup

| Environment | Setup |
|-------------|-------|
| Local | Docker Compose for DB + Redis |
| Staging | Vercel Preview + Railway staging DB |
| Production | Vercel + Railway/Neon Production |

---

## Phase 4: Pre-Launch (Days 14-21)

### Step 15: Security Audit

Run through `checklists/security.md` completely.

```bash
npm audit
npx lighthouse https://staging.yourdomain.com --only-categories=best-practices
```

### Step 16: Performance Audit

Run through `checklists/performance.md`.

```bash
npx lighthouse https://staging.yourdomain.com --view
```

### Step 17: Load Testing

```bash
k6 run workflows/load-test.js --env BASE_URL=https://staging.yourdomain.com
```

### Step 18: Legal & Compliance

- [ ] Privacy policy created
- [ ] Terms of service created
- [ ] Cookie consent implemented (if needed for EU)
- [ ] GDPR data deletion endpoint implemented
- [ ] Email unsubscribe link in all emails

---

## Phase 5: Launch

### Step 19: Pre-Launch Checklist

Run `checklists/before-release.md` fully.

### Step 20: Deploy to Production

Follow `workflows/deploy.md`.

### Step 21: Post-Launch Monitoring

```markdown
Monitor for 48 hours post-launch:
- Error rate in Sentry (target: < 0.1%)
- Response times in Grafana
- Stripe webhook delivery
- Database connection pool utilization
- Uptime via UptimeRobot
```

### Step 22: Update Memory

```markdown
Update memory/:
- active-context.md: launched, now in post-launch monitoring
- completed.md: add launch entry
- project-state.md: update version and deploy date
```

---

## SaaS Checklist Summary

**Foundation:**
- [ ] Vision documented
- [ ] Architecture designed
- [ ] Project scaffolded
- [ ] Database schema designed

**Core:**
- [ ] Authentication working
- [ ] Core MVP features built
- [ ] Payments integrated (Stripe)
- [ ] Email system working

**Infrastructure:**
- [ ] CI/CD pipeline running
- [ ] Error monitoring live (Sentry)
- [ ] Staging environment verified

**Launch:**
- [ ] Security audit passed
- [ ] Performance audit passed
- [ ] Legal pages complete
- [ ] Production deployed
- [ ] Monitoring configured

---

*Related Workflows: [new-feature.md](new-feature.md) · [deploy.md](deploy.md) · [security-audit.md](security-audit.md)*

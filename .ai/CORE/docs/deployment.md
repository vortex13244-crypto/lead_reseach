# Deployment Guide

> **Purpose:** Complete deployment procedures for all environments. Reference before any deployment action.
> **Related:** [architecture.md](architecture.md) · [../workflows/deploy.md](../workflows/deploy.md) · [../checklists/before-deploy.md](../checklists/before-deploy.md)

---

## Environments Overview

| Environment | URL | Branch | Trigger | Approver |
|-------------|-----|--------|---------|----------|
| Local | `http://localhost:3000` | any | Manual | Self |
| Staging | `<!-- staging URL -->` | `main` | Auto on merge | Auto |
| Production | `<!-- prod URL -->` | `main` (tag) | Manual / Auto | Lead |

---

## Prerequisites

```bash
# Required CLI tools
node >= 20.x
npm >= 10.x
docker >= 24.x
git >= 2.40

# Required environment variables (see .env.example)
DATABASE_URL
REDIS_URL
NEXTAUTH_SECRET
# ... (see full list in snippets/environment.md)
```

---

## Local Development

```bash
# 1. Install dependencies
npm install

# 2. Start infrastructure (Docker)
docker compose up -d postgres redis

# 3. Run migrations
npm run db:migrate

# 4. Seed database (optional)
npm run db:seed

# 5. Start dev server
npm run dev
```

**Verify:** Open `http://localhost:3000` — app should load.

---

## Staging Deployment

### Automatic (CI/CD)

Staging deploys automatically on every merge to `main` via GitHub Actions.

```yaml
# .github/workflows/deploy-staging.yml
# Triggered on: push to main
# Steps: test → build → deploy → smoke test
```

### Manual Staging Deploy

```bash
# Deploy to staging manually
git push origin main

# Or trigger via GitHub Actions UI:
# Actions → Deploy to Staging → Run workflow
```

### Verify Staging

```bash
# Run smoke tests against staging
npm run test:smoke -- --env=staging

# Check health endpoint
curl https://staging.yourdomain.com/api/health
```

---

## Production Deployment

### Pre-Deployment Checklist

Run `checklists/before-deploy.md` fully before proceeding.

```bash
# 1. Create release branch
git checkout -b release/v1.2.3 main

# 2. Bump version
npm version patch|minor|major

# 3. Run full test suite
npm test && npm run test:e2e

# 4. Build production bundle
npm run build

# 5. Create and push tag
git tag v1.2.3
git push origin v1.2.3
```

### Deploy

```bash
# Vercel (frontend)
vercel --prod

# Railway/Fly.io (backend)
flyctl deploy --strategy rolling

# Docker (self-hosted)
docker build -t app:v1.2.3 .
docker push registry/app:v1.2.3
kubectl set image deployment/app app=registry/app:v1.2.3
```

### Post-Deploy Verification

```bash
# 1. Check health
curl https://yourdomain.com/api/health

# 2. Check metrics (Grafana / Sentry)
# Open: https://sentry.io/organizations/your-org/

# 3. Run smoke tests
npm run test:smoke -- --env=production

# 4. Monitor error rate for 15 minutes
# Acceptable: < 0.1% error rate
```

---

## Database Migrations

### Applying Migrations

```bash
# Development
npm run db:migrate

# Staging / Production
npm run db:migrate:deploy

# Rollback (if Prisma)
npm run db:migrate:rollback
```

### Migration Safety Rules

- Always back up the database before running migrations in production
- Test migrations on a production data clone before deploying
- Never run destructive migrations (DROP COLUMN, DROP TABLE) without a data export
- Use `--preview-feature` for experimental migration features

---

## Rollback Procedure

### Frontend Rollback

```bash
# Vercel — revert to previous deployment
vercel rollback

# Or redeploy the previous tag
git checkout v1.2.2
vercel --prod
```

### Backend Rollback

```bash
# Kubernetes
kubectl rollout undo deployment/app

# Docker Swarm
docker service update --image registry/app:v1.2.2 app

# Fly.io
flyctl releases list
flyctl deploy --image registry/app:v1.2.2
```

### Database Rollback

```bash
# Prisma migration rollback
npx prisma migrate resolve --rolled-back migration_name

# Manual SQL rollback (use down migration)
psql $DATABASE_URL < migrations/rollback/20240101_rollback.sql
```

---

## CI/CD Pipeline

```yaml
# GitHub Actions Pipeline Overview

name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Install dependencies
      - Run linter
      - Run type check
      - Run unit tests
      - Run integration tests

  build:
    needs: test
    steps:
      - Build Docker image
      - Push to registry

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
      - Deploy to staging
      - Run smoke tests

  deploy-production:
    needs: deploy-staging
    if: github.ref_type == 'tag'
    steps:
      - Manual approval gate
      - Deploy to production
      - Run smoke tests
      - Notify team
```

---

## Environment Variables Management

```bash
# Local
.env.local          # Never commit

# Staging
# Stored in: GitHub Secrets / Vercel Environment Variables

# Production
# Stored in: GitHub Secrets / Vercel Environment Variables / AWS Secrets Manager

# Template: see snippets/environment.md
```

---

## Monitoring & Alerts

| Tool | Purpose | Alert Threshold |
|------|---------|----------------|
| Sentry | Error tracking | > 10 errors/min |
| Grafana | Metrics & dashboards | p99 latency > 2s |
| UptimeRobot | Uptime monitoring | Downtime > 1 min |
| PagerDuty | On-call alerts | Critical errors |

---

## Infrastructure Costs

| Service | Plan | Monthly Cost | Notes |
|---------|------|-------------|-------|
| Vercel | Pro | <!-- $20 --> | Frontend hosting |
| Railway | Pro | <!-- $20 --> | Backend + DB |
| Upstash Redis | Pay-as-go | <!-- $5 --> | Cache |
| Sentry | Team | <!-- $26 --> | Error tracking |

---

*Last Updated: <!-- YYYY-MM-DD --> | Review before every major deployment*

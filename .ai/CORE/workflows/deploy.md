# Workflow: Deploy

> **Purpose:** Step-by-step deployment process for staging and production environments.
> **Roles:** [devops.md](../roles/devops.md)
> **Related:** [docs/deployment.md](../docs/deployment.md) · [checklists/before-deploy.md](../checklists/before-deploy.md)

---

## Pre-Deploy: Run Checklist

**Always** run `checklists/before-deploy.md` before any production deployment.

---

## Standard Production Deploy

### Step 1: Prepare Release

```bash
# Ensure you're on the main branch with latest changes
git checkout main
git pull origin main

# Verify CI is green
# Check: GitHub → Actions → All workflows green

# Create a release tag
git tag v1.2.3
git push origin v1.2.3
```

### Step 2: Database Migrations (if any)

```bash
# IMPORTANT: Run migrations BEFORE deploying new code
# New code may depend on new schema; old code must tolerate new schema

# Connect to production database
DATABASE_URL=$PROD_DATABASE_URL npx prisma migrate deploy

# Verify migration applied
DATABASE_URL=$PROD_DATABASE_URL npx prisma migrate status
```

### Step 3: Deploy Application

**Vercel (Frontend):**
```bash
# Auto-deploys on push to main. Or manually:
vercel --prod --token $VERCEL_TOKEN

# Verify deploy started
vercel ls --scope your-team
```

**Railway (Backend):**
```bash
railway up --service backend --environment production
```

**Fly.io (Backend):**
```bash
fly deploy --strategy rolling
# Rolling strategy: deploys one instance at a time for zero downtime
```

**Docker / Kubernetes:**
```bash
# Build and push image
docker build -t registry/app:v1.2.3 .
docker push registry/app:v1.2.3

# Rolling update
kubectl set image deployment/app app=registry/app:v1.2.3
kubectl rollout status deployment/app
```

### Step 4: Verify Deployment

```bash
# Wait 60-120 seconds for deploy to complete

# 1. Health check
curl https://yourdomain.com/api/health

# 2. Check response time
curl -w "\nTotal: %{time_total}s\n" https://yourdomain.com/api/health

# 3. Verify version
curl https://yourdomain.com/api/health | jq '.version'
# Should match the deployed version

# 4. Quick smoke test
npm run test:smoke -- --env=production
```

### Step 5: Monitor (15 minutes)

Watch these dashboards for 15 minutes post-deploy:

- **Sentry:** Error rate < 0.1% and no new error categories
- **Grafana:** p95 response time within baseline ± 20%
- **Database:** Connection pool utilization < 80%

### Step 6: Communicate

```markdown
Post in #deployments channel:

🚀 Deployed v1.2.3 to production
Changes: [brief list of what's new]
Status: All checks green ✅
Rollback: git revert HEAD && vercel --prod
```

---

## Hotfix Deploy (P0/P1 Bugs)

For critical bugs that need immediate deployment:

```bash
# 1. Create hotfix branch from main
git checkout -b hotfix/critical-auth-bypass main

# 2. Apply minimal fix (no refactoring!)
# ... make the smallest possible change that fixes the issue ...

# 3. Push and get expedited review (2 reviewers if possible)
git push origin hotfix/critical-auth-bypass

# 4. After review: merge and deploy immediately
git checkout main
git merge hotfix/critical-auth-bypass
git push origin main
git tag v1.2.4-hotfix
git push origin v1.2.4-hotfix

# 5. Deploy (same as standard)
# 6. Verify and monitor extra carefully (30 min)
```

---

## Staging Deploy

```bash
# Staging auto-deploys on push to main
# Manual staging deploy:

git push origin main

# Or deploy a specific branch to staging:
vercel --env=staging
```

---

## Rollback Procedure

If anything goes wrong:

### Instant Rollback (Vercel)

```bash
# List recent deployments
vercel ls

# Rollback to previous deployment
vercel rollback

# Or redeploy previous tag
git checkout v1.2.2
vercel --prod
```

### Backend Rollback

```bash
# Kubernetes
kubectl rollout undo deployment/app
kubectl rollout status deployment/app

# Fly.io
flyctl releases list
flyctl deploy --image registry/app:v1.2.2

# Railway
# Use Railway dashboard → Deployments → Rollback
```

### Database Rollback

```bash
# CAUTION: Only roll back migrations if data has not been written by new schema
# If data was written using new schema, rolling back may cause data loss

# Prisma: mark migration as rolled back
npx prisma migrate resolve --rolled-back 20240115_add_user_profile

# If rollback causes data issues: restore from backup
# See docs/deployment.md → Backup & Recovery
```

---

## Zero-Downtime Deploy Checklist

For deploys with significant schema changes:

```markdown
Phase 1: Expand (Deploy new schema)
- [ ] Add new columns as nullable
- [ ] Add new tables
- [ ] Deploy OLD code that ignores new schema
- [ ] Verify old code works with new schema

Phase 2: Migrate (Backfill data)
- [ ] Run data migration scripts to populate new columns
- [ ] Verify data integrity

Phase 3: Switch (Deploy new code)
- [ ] Deploy NEW code that uses new schema
- [ ] Verify new features work

Phase 4: Contract (Clean up)
- [ ] Remove old columns/code that new code doesn't need
- [ ] Only after new code has been stable for days/weeks
```

---

## Post-Deploy Documentation

```markdown
Update memory/active-context.md:
- Last deploy date and version
- What was deployed
- Any issues encountered

Update memory/project-state.md:
- Version number
- Deploy date
- Any infrastructure changes
```

---

*Related: [docs/deployment.md](../docs/deployment.md) · [checklists/before-deploy.md](../checklists/before-deploy.md) · [devops.md](../roles/devops.md)*

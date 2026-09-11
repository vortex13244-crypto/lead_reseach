# Checklist: Before Deploy

> **Purpose:** Final checks before every production deployment. No exceptions.
> **Time:** 15-30 minutes

---

## 1. Code & Build

- [ ] CI pipeline is green (all tests pass)
- [ ] Build succeeds in staging
- [ ] No new HIGH/CRITICAL security vulnerabilities (`npm audit`)
- [ ] TypeScript compiles without errors

---

## 2. Database

- [ ] All migrations tested on staging
- [ ] If new migrations: tested on production data clone
- [ ] Rollback procedure documented for any new migration
- [ ] Database backup completed (for significant schema changes)
- [ ] Connection pool size appropriate for new load

---

## 3. Environment

- [ ] All new environment variables added to production
- [ ] No development-only values in production config
- [ ] Third-party service credentials valid (not test keys in prod)
- [ ] Feature flags configured correctly for production

---

## 4. Monitoring

- [ ] Sentry is configured and receiving events
- [ ] Error rate baseline noted (compare against post-deploy)
- [ ] Uptime monitoring active
- [ ] Grafana dashboards accessible
- [ ] Alert thresholds set for new features

---

## 5. Rollback Ready

- [ ] Rollback procedure documented (`workflows/deploy.md`)
- [ ] Previous working version tagged and available
- [ ] Team knows the rollback signal (when to roll back, who decides)
- [ ] Database rollback plan exists (if migration is included)

---

## 6. Staging Verification

- [ ] Deployed to staging successfully
- [ ] Smoke tests pass on staging
- [ ] Critical user flows tested manually on staging
- [ ] No new errors in staging Sentry

---

## 7. Communication

- [ ] Team notified of deployment
- [ ] Deployment window confirmed (avoid peak traffic hours)
- [ ] On-call person available for 2 hours post-deploy

---

## Post-Deploy (Complete within 15 minutes of deploy)

- [ ] Health endpoint returns 200: `curl https://yourdomain.com/api/health`
- [ ] Correct version deployed: check version in health response
- [ ] Critical user flows work in production
- [ ] Error rate not spiking in Sentry
- [ ] Response times within baseline ± 20%

---

**DO NOT DEPLOY if:**
- CI is red
- Staging has untested issues
- Database backup not taken (for schema changes)
- On-call person unavailable

---

*Related: [workflows/deploy.md](../workflows/deploy.md) · [before-release.md](before-release.md)*

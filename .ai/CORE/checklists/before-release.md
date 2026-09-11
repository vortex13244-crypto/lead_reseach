# Checklist: Before Release

> **Purpose:** Final verification before releasing to production. Every item must be checked.
> **Related:** [before-deploy.md](before-deploy.md) · [security.md](security.md) · [performance.md](performance.md)

---

## 1. Code Quality

- [ ] All tests pass (`npm test`)
- [ ] TypeScript compiles without errors (`npm run type-check`)
- [ ] Linter passes with zero warnings (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] No `console.log` in production code
- [ ] No `// TODO` comments in new code
- [ ] No `any` TypeScript types without justification

---

## 2. Features

- [ ] All acceptance criteria for this release are met
- [ ] Features tested manually in staging environment
- [ ] Edge cases verified (empty state, error state, max data)
- [ ] All features work on mobile (responsive)
- [ ] All features accessible (keyboard, screen reader)

---

## 3. Security

- [ ] `npm audit` — zero HIGH or CRITICAL vulnerabilities
- [ ] No secrets or API keys in code or git history
- [ ] Authentication required on all protected routes
- [ ] Authorization checked (users can only access their own data)
- [ ] Input validation on all user inputs
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Rate limiting on auth endpoints
- [ ] Run `workflows/security-audit.md` if major auth/payment changes

---

## 4. Performance

- [ ] Lighthouse score ≥ 90 (Performance category) on key pages
- [ ] LCP < 2.5s on key pages
- [ ] No N+1 database queries in critical paths
- [ ] Database queries have appropriate indices
- [ ] Bundle size: JS < 200KB gzipped, CSS < 50KB gzipped
- [ ] Images optimized (WebP/AVIF, next/image)
- [ ] API response times: p95 < 300ms, p99 < 1s

---

## 5. Database

- [ ] All pending migrations applied to staging
- [ ] Migration tested on production data clone (for large tables)
- [ ] Rollback migration documented
- [ ] No data loss in migration
- [ ] Database backup taken before release

---

## 6. Documentation

- [ ] `docs/api.md` updated for any API changes
- [ ] `CHANGELOG.md` or release notes written
- [ ] README updated if setup process changed
- [ ] Breaking changes documented with migration guide

---

## 7. Infrastructure

- [ ] CI/CD pipeline green for last commit
- [ ] Staging environment matches production configuration
- [ ] Environment variables updated in production (if changed)
- [ ] New third-party integrations configured in production
- [ ] Monitoring alerts configured for new features

---

## 8. Legal & Compliance

- [ ] Privacy policy updated (if new data collected)
- [ ] Terms of service updated (if new features change ToS)
- [ ] GDPR compliance: user data deletion works
- [ ] Cookie consent updated (if new cookies added)

---

## 9. Communication

- [ ] Release notes prepared
- [ ] Team notified of deployment time
- [ ] On-call engineer designated for 24h post-release
- [ ] Rollback plan documented and communicated

---

## 10. Post-Release Plan

- [ ] Monitoring dashboard prepared (Sentry, Grafana)
- [ ] Success metrics defined (what will we watch for 48h?)
- [ ] Feature flags configured (if using feature flags)
- [ ] Customer support briefed on new features

---

**Sign-off:** All items checked ✅ → Proceed to deploy using `workflows/deploy.md`

---

*Related: [before-deploy.md](before-deploy.md) · [workflows/deploy.md](../workflows/deploy.md)*

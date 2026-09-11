# Checklist: Security

> **Purpose:** Security verification checklist for features, PRs, and periodic reviews.
> **Related:** [docs/security.md](../docs/security.md) · [workflows/security-audit.md](../workflows/security-audit.md) · [roles/security-engineer.md](../roles/security-engineer.md)

---

## Authentication

- [ ] Passwords hashed with bcrypt/Argon2, cost factor ≥ 12
- [ ] No plaintext passwords in logs, responses, or database
- [ ] JWT secrets ≥ 256 bits (≥ 44 base64 characters)
- [ ] Access tokens expire in ≤ 15 minutes
- [ ] Refresh tokens stored in httpOnly Secure SameSite cookies
- [ ] Account lockout after 5 failed login attempts
- [ ] Rate limiting on all auth endpoints (login, signup, password reset)
- [ ] Password reset tokens single-use and time-limited (≤ 1 hour)

---

## Authorization

- [ ] Every API route requires authentication (no forgotten public routes)
- [ ] Every resource access verifies ownership (IDOR prevention)
- [ ] Admin routes have role check, not just authentication
- [ ] Users cannot escalate their own privileges
- [ ] Inactive or deleted users cannot access resources

---

## Input Validation

- [ ] All request bodies validated with schema (Zod/Pydantic)
- [ ] All URL parameters sanitized and validated
- [ ] All query parameters have type and range validation
- [ ] File uploads: MIME type validated, size limited, content scanned
- [ ] HTML content sanitized with DOMPurify before rendering

---

## SQL & Database

- [ ] All database queries use ORM or parameterized statements
- [ ] No string interpolation in SQL queries
- [ ] Database user has minimum necessary permissions
- [ ] Connection string not exposed in client-side code

---

## XSS Prevention

- [ ] No `dangerouslySetInnerHTML` without DOMPurify sanitization
- [ ] User content rendered as text, not HTML (React default)
- [ ] CSP header configured to prevent inline scripts
- [ ] External resources in CSP allowlist

---

## CSRF Prevention

- [ ] SameSite=Strict on session cookies
- [ ] CSRF token on state-changing API calls (if using cookies for auth)
- [ ] Double-submit cookie pattern or similar for forms

---

## Security Headers

- [ ] `Strict-Transport-Security` configured
- [ ] `Content-Security-Policy` configured
- [ ] `X-Frame-Options: SAMEORIGIN`
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `Referrer-Policy` set
- [ ] CORS configured with explicit allowlist (not `*`)

---

## Dependency Security

- [ ] `npm audit` — zero HIGH or CRITICAL vulnerabilities
- [ ] No packages with known CVEs used in production
- [ ] Dependabot or Renovate configured for automated updates
- [ ] Packages pinned to exact versions in lockfile

---

## Secrets Management

- [ ] No secrets, API keys, or credentials in source code
- [ ] No secrets in git history (`git log` check)
- [ ] `.env` files in `.gitignore`
- [ ] Secrets in environment variables only
- [ ] Secret scanning enabled on repository
- [ ] Separate secrets for each environment (dev/staging/prod)

---

## Logging & Monitoring

- [ ] Authentication events logged (login, logout, failed attempts)
- [ ] No PII or secrets in logs
- [ ] Audit log for sensitive admin operations
- [ ] Security alerts configured in monitoring

---

## Infrastructure

- [ ] All traffic over HTTPS (no HTTP in production)
- [ ] Database not accessible from public internet
- [ ] Redis not accessible from public internet
- [ ] Docker containers run as non-root user
- [ ] Cloud IAM uses principle of least privilege

---

## Data Privacy

- [ ] Collect only data that is necessary
- [ ] Sensitive data encrypted at rest
- [ ] User data deletion endpoint works (GDPR Article 17)
- [ ] Data retention policy defined and implemented
- [ ] Third-party services listed in privacy policy

---

*Related: [docs/security.md](../docs/security.md) · [roles/security-engineer.md](../roles/security-engineer.md)*

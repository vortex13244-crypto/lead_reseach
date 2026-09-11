# Workflow: Security Audit

> **Purpose:** Systematic security audit process for features, PRs, and periodic reviews.
> **Role:** [security-engineer.md](../roles/security-engineer.md)
> **Related:** [docs/security.md](../docs/security.md) · [checklists/security.md](../checklists/security.md)

---

## When to Run a Security Audit

- Before any major release
- When adding authentication, payment, or file upload features
- After any security advisory is published for dependencies you use
- Quarterly for production systems
- When a security incident is reported

---

## Step 1: Define Scope

```markdown
Scope Definition:
- What components are being audited?
- What changed since the last audit?
- What is the threat model? (see docs/security.md)
- Are there specific compliance requirements? (GDPR, SOC2, HIPAA)
```

---

## Step 2: Automated Scanning

```bash
# Dependency vulnerability scan
npm audit --audit-level=moderate
# Fix all HIGH and CRITICAL issues before proceeding

# Python
pip-audit
safety check

# SAST (Static Application Security Testing)
# Install: npm install -g semgrep
semgrep --config auto src/

# Secret scanning
# Check: is GitHub Secret Scanning enabled?
# Or run locally:
trufflehog git file://. --only-verified

# Check .gitignore covers sensitive files
cat .gitignore | grep -E ".env|secrets|credentials"
```

---

## Step 3: Authentication Review

```markdown
Check each item against the code:

Authentication:
- [ ] Passwords hashed with bcrypt/argon2 (cost ≥ 12)?
  grep -r "bcrypt\|argon2" src/
  
- [ ] No plaintext passwords in logs?
  grep -rn "password" src/ | grep -v "hash\|schema\|type\|interface"

- [ ] JWT secret is strong (≥ 256 bits)?
  echo $JWT_SECRET | wc -c  # Should be ≥ 44 characters (base64)

- [ ] Access tokens short-lived (≤ 15 min)?
  grep -n "expiresIn\|exp\|expires_in" src/

- [ ] Refresh tokens in httpOnly cookies?
  grep -n "httpOnly\|sameSite\|secure" src/

- [ ] Rate limiting on login endpoint?
  grep -n "rateLimit\|rate_limit" src/api/auth/
```

---

## Step 4: Authorization Review

```markdown
For each API endpoint, verify:

- [ ] Endpoint requires authentication (middleware applied)?
  - List all routes and verify middleware
  
- [ ] Endpoint verifies ownership of resources?
  - User A cannot access User B's data
  
- [ ] Admin endpoints check for admin role?
  grep -n "admin\|ADMIN\|requireAdmin" src/api/admin/

- [ ] No IDOR (Insecure Direct Object Reference)?
  # Every route that takes an ID in URL must verify ownership
  # Pattern: /api/documents/:id → verify document.userId === requestingUser.id
```

---

## Step 5: Input Validation Review

```markdown
- [ ] All request bodies validated with schema (Zod/Pydantic)?
  grep -rn "z.object\|z.string\|BaseModel" src/api/

- [ ] File uploads: type and size validated?
  grep -rn "multer\|formData\|UploadedFile" src/

- [ ] No SQL injection vectors?
  # Verify all DB queries use ORM or parameterized queries
  grep -rn "prisma\.\|sqlalchemy\|execute(" src/
  # Search for danger: string interpolation in queries
  grep -rn "\`SELECT.*\${" src/  # Should return nothing

- [ ] No XSS vectors?
  grep -rn "dangerouslySetInnerHTML\|innerHTML" src/
  # Each match must be reviewed and sanitized

- [ ] URL parameters validated?
  grep -rn "req.params\|request.path" src/
```

---

## Step 6: Security Headers Review

```bash
# Check headers on live environment
curl -I https://staging.yourdomain.com

# Expected headers:
# Strict-Transport-Security: max-age=63072000
# X-Frame-Options: SAMEORIGIN
# X-Content-Type-Options: nosniff
# Content-Security-Policy: [policy]
# Referrer-Policy: strict-origin-when-cross-origin

# Or use securityheaders.com
open https://securityheaders.com/?q=https://staging.yourdomain.com
```

---

## Step 7: Dependency Audit

```bash
# Check for known vulnerabilities
npm audit

# Check for outdated packages with known issues
npm outdated

# Review each dependency
# Ask: Do we actually need this package?
# Ask: Is there an actively maintained alternative?

# License audit (important for commercial products)
npx license-checker --production --failOn "GPL;AGPL"
```

---

## Step 8: Infrastructure Security

```markdown
- [ ] All traffic over HTTPS (no HTTP in production)?
- [ ] Database not publicly accessible?
  # Database should only be accessible from app servers, not from internet
- [ ] Redis not publicly accessible?
- [ ] No debug endpoints or admin panels exposed publicly?
- [ ] Environment variables not logged?
- [ ] Docker images running as non-root?
- [ ] API keys in secrets manager (not in code)?
```

---

## Step 9: Data Privacy Review

```markdown
GDPR / Data Privacy:
- [ ] Do we collect only data we need?
- [ ] Is there a privacy policy?
- [ ] Can users delete their data?
- [ ] Is sensitive data encrypted at rest?
- [ ] Are logs anonymized or not retaining PII?
- [ ] Is there a data retention policy?

Data Classification:
| Data Type | Encryption | Retention | Access |
|-----------|-----------|-----------|--------|
| Passwords | bcrypt hash | Forever | Never expose |
| Payment info | Never store (use Stripe) | N/A | N/A |
| Email | Yes (at rest) | Account lifetime | Admin only |
| Logs | No PII | 90 days | DevOps team |
```

---

## Step 10: Penetration Testing (Quarterly)

```markdown
Manual testing checklist:

Authentication bypass:
- [ ] Try accessing protected routes without token
- [ ] Try with expired token
- [ ] Try with modified token (change role claim)

Authorization bypass:
- [ ] Try accessing other users' resources by modifying IDs
- [ ] Try accessing admin endpoints as regular user

Injection:
- [ ] Try SQL injection in search fields and URL params
- [ ] Try XSS in all text input fields
- [ ] Try SSRF by providing internal URLs

Business logic:
- [ ] Try submitting negative prices
- [ ] Try accessing resources without paying
- [ ] Try race conditions on payment flows
```

---

## Step 11: Document Findings

```markdown
Security Audit Report Template:

## Security Audit: [Scope] — [Date]

**Auditor:** Security Engineer Role
**Environment:** Staging / Production
**Risk Level:** Critical | High | Medium | Low

### Executive Summary
[2-3 sentences on overall security posture]

### Findings

| ID | Severity | Title | Component | Status |
|----|---------|-------|-----------|--------|
| SEC-001 | Critical | ... | src/api/auth | Fixed |
| SEC-002 | High | ... | src/api/users | Open |

### Detailed Findings

#### SEC-001: [Title]
**Severity:** Critical
**CWE:** CWE-89 (SQL Injection)
**Location:** src/api/search/route.ts:45

**Description:** [What the vulnerability is]
**Impact:** [What an attacker could do]
**Proof of Concept:** [How to reproduce]
**Remediation:** [How to fix]
**Status:** Fixed / Open / Accepted Risk

### Resolved Issues
[List of issues found and fixed during this audit]

### Sign-off
✅ APPROVED — No critical or high findings remaining
❌ BLOCKED — [List blocking findings]
```

---

## Step 12: Update Security Documentation

```markdown
After audit:
1. Update docs/security.md with audit results
2. Add fixed issues to memory/completed.md
3. Add open issues to memory/known-issues.md
4. Update checklists/security.md if new checks are needed
```

---

*Related: [security-engineer.md](../roles/security-engineer.md) · [checklists/security.md](../checklists/security.md) · [docs/security.md](../docs/security.md)*

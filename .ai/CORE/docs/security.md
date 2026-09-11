# Security Documentation

> **Purpose:** Security architecture, threat model, implementation guidelines, and audit procedures.
> **Related:** [../roles/security-engineer.md](../roles/security-engineer.md) · [../checklists/security.md](../checklists/security.md) · [../workflows/security-audit.md](../workflows/security-audit.md)

---

## Security Posture

| Area | Status | Last Audited |
|------|--------|-------------|
| Authentication | <!-- Implemented --> | <!-- date --> |
| Authorization | <!-- Implemented --> | <!-- date --> |
| Input Validation | <!-- Implemented --> | <!-- date --> |
| Rate Limiting | <!-- Implemented --> | <!-- date --> |
| Dependency Audit | <!-- Pending --> | <!-- date --> |
| Penetration Test | <!-- Pending --> | <!-- date --> |

---

## Authentication

### JWT Strategy

```typescript
// Token configuration
const ACCESS_TOKEN_EXPIRY = '15m'     // Short-lived for security
const REFRESH_TOKEN_EXPIRY = '7d'     // Long-lived, stored in httpOnly cookie

// Token payload (never include sensitive data)
interface JwtPayload {
  sub: string        // User ID
  email: string
  role: UserRole
  iat: number        // Issued at
  exp: number        // Expiry
}
```

### Session Security

- Access tokens stored in memory (not localStorage)
- Refresh tokens in `httpOnly`, `Secure`, `SameSite=Strict` cookies
- Token rotation on every refresh
- Immediate invalidation on logout

### Password Policy

```typescript
const PASSWORD_REQUIREMENTS = {
  minLength: 12,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialChars: true,
  maxLoginAttempts: 5,
  lockoutDuration: 15 * 60, // 15 minutes in seconds
}
```

---

## Authorization

### Role-Based Access Control (RBAC)

```typescript
enum Permission {
  // Users
  USER_READ = 'user:read',
  USER_WRITE = 'user:write',
  USER_DELETE = 'user:delete',
  USER_ADMIN = 'user:admin',

  // Resources
  RESOURCE_READ = 'resource:read',
  RESOURCE_WRITE = 'resource:write',
  RESOURCE_DELETE = 'resource:delete',
}

const ROLE_PERMISSIONS: Record<UserRole, Permission[]> = {
  USER: [Permission.RESOURCE_READ, Permission.RESOURCE_WRITE],
  ADMIN: [...Object.values(Permission)],
}
```

### Authorization Middleware

```typescript
// Every route that accesses user data must verify ownership
function requireOwnership(resourceUserId: string, requestingUserId: string, role: UserRole): void {
  if (role !== UserRole.ADMIN && resourceUserId !== requestingUserId) {
    throw new ForbiddenError('You do not have access to this resource')
  }
}
```

---

## Input Validation

### Validation Rules

```typescript
// All user input must be validated with Zod
import { z } from 'zod'

const createUserSchema = z.object({
  email: z.string().email().max(255).toLowerCase().trim(),
  name: z.string().min(1).max(100).trim(),
  password: z.string().min(12).max(128),
})

// Sanitize HTML content
import DOMPurify from 'isomorphic-dompurify'
const clean = DOMPurify.sanitize(userInput, { ALLOWED_TAGS: [] })
```

### SQL Injection Prevention

```typescript
// ALWAYS use parameterized queries — never string interpolation
// WRONG ❌
const result = await db.query(`SELECT * FROM users WHERE id = '${userId}'`)

// RIGHT ✅
const result = await db.query('SELECT * FROM users WHERE id = $1', [userId])

// Prisma handles this automatically — use Prisma for all DB access
const user = await prisma.user.findUnique({ where: { id: userId } })
```

---

## OWASP Top 10 Controls

| Risk | Control Implemented |
|------|-------------------|
| A01 Broken Access Control | RBAC middleware on all routes, ownership checks |
| A02 Cryptographic Failures | bcrypt for passwords, AES-256 for sensitive data at rest |
| A03 Injection | Parameterized queries, Zod validation, HTML sanitization |
| A04 Insecure Design | Threat modeling per feature, security review checklist |
| A05 Security Misconfiguration | Env var validation at startup, secure headers via Helmet |
| A06 Vulnerable Components | Dependabot, weekly `npm audit` |
| A07 Auth Failures | Rate limiting on auth endpoints, account lockout |
| A08 Software Integrity | SBOM, signed commits, dependency pinning |
| A09 Logging Failures | Structured audit logging, no sensitive data in logs |
| A10 SSRF | Allowlist for outbound requests, no URL from user input |

---

## HTTP Security Headers

```typescript
// Using Helmet.js (Express) or Next.js headers config
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self' 'nonce-{NONCE}'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "connect-src 'self' https://api.yourdomain.com",
    ].join('; ')
  },
]
```

---

## Rate Limiting

```typescript
// Auth endpoints: strict limits
authRateLimit: 5 requests / 15 minutes / IP

// API endpoints: standard limits
apiRateLimit: 100 requests / minute / user

// Public endpoints
publicRateLimit: 30 requests / minute / IP

// Implementation
import { rateLimit } from 'express-rate-limit'
import { RedisStore } from 'rate-limit-redis'

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  store: new RedisStore({ client: redis }),
  message: { error: { code: 'RATE_LIMITED', message: 'Too many attempts' } }
})
```

---

## Secrets Management

```bash
# Development: .env.local (gitignored)
# Staging/Production: Environment variables in hosting platform

# NEVER commit:
# - API keys
# - Database passwords
# - JWT secrets
# - OAuth client secrets

# Rotate secrets regularly:
# - JWT secrets: every 90 days
# - API keys: every 180 days
# - Database passwords: every 90 days

# Secret scanning
# Enable: GitHub → Settings → Security → Secret scanning
# Also run: trufflesecurity/trufflehog in CI
```

---

## Dependency Security

```bash
# Check for vulnerabilities
npm audit
npm audit fix

# Automated: GitHub Dependabot
# Configure in: .github/dependabot.yml

# Check for outdated packages
npm outdated

# Lock file auditing
npm ci  # Always use in CI (uses package-lock.json exactly)
```

---

## Security Incident Response

### Severity Levels

| Level | Example | Response Time |
|-------|---------|--------------|
| P0 - Critical | Data breach, auth bypass | Immediate (< 1 hour) |
| P1 - High | XSS, privilege escalation | < 4 hours |
| P2 - Medium | Information disclosure | < 24 hours |
| P3 - Low | Minor info exposure | < 1 week |

### Response Steps

1. **Contain** — Disable affected feature or rotate compromised credentials
2. **Assess** — Determine scope, affected users, and data exposure
3. **Communicate** — Notify affected users if required by law
4. **Fix** — Deploy patch with emergency process
5. **Post-mortem** — Document in `memory/known-issues.md`

---

*Last Updated: <!-- YYYY-MM-DD --> | Audit security docs before each major release*

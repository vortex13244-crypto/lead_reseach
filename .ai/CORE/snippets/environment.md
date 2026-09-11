# Snippet: Environment Variables

> **Purpose:** Environment variable templates for common project setups.
> **Security:** Never commit .env files. Use .env.example as the template.

---

## Complete .env.example Template

```bash
# ═══════════════════════════════════════════════════════
# APPLICATION
# ═══════════════════════════════════════════════════════

NODE_ENV=development
# NODE_ENV=staging
# NODE_ENV=production

APP_URL=http://localhost:3000
API_URL=http://localhost:8000

# Enable verbose logging in development
DEBUG=true

# ═══════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════

# PostgreSQL connection string
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/myapp"

# If using PgBouncer (separate connection pools for serverless)
DATABASE_DIRECT_URL="postgresql://postgres:postgres@localhost:5432/myapp"

# ═══════════════════════════════════════════════════════
# CACHE
# ═══════════════════════════════════════════════════════

# Redis connection string
REDIS_URL="redis://localhost:6379"

# With auth
# REDIS_URL="redis://:password@localhost:6379/0"

# Upstash Redis (serverless)
# UPSTASH_REDIS_REST_URL=""
# UPSTASH_REDIS_REST_TOKEN=""

# ═══════════════════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════════════════

# Generate: openssl rand -base64 64
JWT_SECRET="change-me-to-a-random-256-bit-secret-at-minimum"
JWT_REFRESH_SECRET="change-me-to-another-random-256-bit-secret"

# Access token expiry (15 minutes recommended)
JWT_EXPIRES_IN="15m"
JWT_REFRESH_EXPIRES_IN="7d"

# NextAuth.js (if using NextAuth)
# NEXTAUTH_URL="http://localhost:3000"
# NEXTAUTH_SECRET="change-me-to-random-secret"

# Clerk (if using Clerk)
# NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=""
# CLERK_SECRET_KEY=""
# NEXT_PUBLIC_CLERK_SIGN_IN_URL="/sign-in"
# NEXT_PUBLIC_CLERK_SIGN_UP_URL="/sign-up"

# ═══════════════════════════════════════════════════════
# PAYMENTS
# ═══════════════════════════════════════════════════════

# Stripe
STRIPE_SECRET_KEY="sk_test_..."
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# Stripe Price IDs (get from Stripe Dashboard)
STRIPE_PRICE_PRO_MONTHLY="price_..."
STRIPE_PRICE_PRO_ANNUAL="price_..."

# ═══════════════════════════════════════════════════════
# EMAIL
# ═══════════════════════════════════════════════════════

# Resend
RESEND_API_KEY="re_..."
FROM_EMAIL="noreply@yourdomain.com"
FROM_NAME="Your App"

# Postmark (alternative)
# POSTMARK_SERVER_TOKEN=""

# MailPit (local development email capture)
SMTP_HOST="localhost"
SMTP_PORT=1025
SMTP_USER=""
SMTP_PASS=""

# ═══════════════════════════════════════════════════════
# FILE STORAGE
# ═══════════════════════════════════════════════════════

# Cloudflare R2 (recommended — S3-compatible, no egress fees)
R2_ACCOUNT_ID=""
R2_ACCESS_KEY_ID=""
R2_SECRET_ACCESS_KEY=""
R2_BUCKET_NAME=""
R2_PUBLIC_URL="https://files.yourdomain.com"

# AWS S3 (alternative)
# AWS_ACCESS_KEY_ID=""
# AWS_SECRET_ACCESS_KEY=""
# AWS_REGION="us-east-1"
# AWS_S3_BUCKET=""

# ═══════════════════════════════════════════════════════
# AI / LLM
# ═══════════════════════════════════════════════════════

# OpenAI
OPENAI_API_KEY="sk-..."
OPENAI_ORG_ID=""  # Optional

# Anthropic (Claude)
ANTHROPIC_API_KEY="sk-ant-..."

# Ollama (local models — no key needed)
OLLAMA_BASE_URL="http://localhost:11434"

# ═══════════════════════════════════════════════════════
# MONITORING & LOGGING
# ═══════════════════════════════════════════════════════

# Sentry
NEXT_PUBLIC_SENTRY_DSN=""
SENTRY_AUTH_TOKEN=""  # For sourcemaps upload

# ═══════════════════════════════════════════════════════
# OAUTH PROVIDERS (optional)
# ═══════════════════════════════════════════════════════

# GitHub OAuth
GITHUB_CLIENT_ID=""
GITHUB_CLIENT_SECRET=""

# Google OAuth
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""

# ═══════════════════════════════════════════════════════
# FEATURE FLAGS
# ═══════════════════════════════════════════════════════

FEATURE_AI_CHAT=true
FEATURE_PAYMENTS=true
FEATURE_TEAMS=false

# ═══════════════════════════════════════════════════════
# RATE LIMITING
# ═══════════════════════════════════════════════════════

# Requests per minute for authenticated users
RATE_LIMIT_API=100

# Requests per 15 minutes for auth endpoints per IP
RATE_LIMIT_AUTH=5
```

---

## Validation (TypeScript — Zod)

```typescript
// src/lib/env.ts — Validate at startup
import { z } from "zod"

const envSchema = z.object({
  // App
  NODE_ENV: z.enum(["development", "staging", "production"]),
  APP_URL: z.string().url(),

  // Database
  DATABASE_URL: z.string().startsWith("postgresql://"),

  // Auth
  JWT_SECRET: z.string().min(32, "JWT_SECRET must be at least 32 characters"),
  JWT_EXPIRES_IN: z.string().default("15m"),

  // Optional
  REDIS_URL: z.string().optional(),
  STRIPE_SECRET_KEY: z.string().optional(),
  OPENAI_API_KEY: z.string().optional(),
})

export const env = envSchema.parse(process.env)
// This throws at startup if any required env var is missing or invalid
```

---

## Validation (Python — Pydantic Settings)

```python
# src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn, SecretStr

class Settings(BaseSettings):
    # App
    NODE_ENV: str = "development"
    APP_URL: str = "http://localhost:3000"
    DEBUG: bool = False

    # Database
    DATABASE_URL: PostgresDsn
    
    # Cache
    REDIS_URL: RedisDsn | None = None

    # Auth
    JWT_SECRET: SecretStr  # SecretStr prevents accidental logging
    JWT_EXPIRES_IN: str = "15m"

    # AI
    OPENAI_API_KEY: SecretStr | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()
```

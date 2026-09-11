# Docker — Knowledge Base

> **Purpose:** Docker and Docker Compose best practices for development and production.
> **Related:** [../roles/devops.md](../roles/devops.md) · [../snippets/dockerfile.md](../snippets/dockerfile.md)

---

## Overview

Docker is used in this workspace for local development infrastructure and production deployments. Every service must have a health check. Never run containers as root in production.

---

## Best Practices

### Dockerfile — Multi-Stage Builds

```dockerfile
# Stage 1: Install dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production --frozen-lockfile

# Stage 2: Build application
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --frozen-lockfile
COPY . .
RUN npm run build

# Stage 3: Production runtime (minimal image)
FROM node:20-alpine AS runner
WORKDIR /app

# Security: non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy only what's needed
COPY --from=deps --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./

USER nextjs
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/api/health || exit 1

ENV NODE_ENV=production
ENV PORT=3000

CMD ["node", "server.js"]
```

### .dockerignore

```dockerignore
node_modules
.next
.git
.env*
*.log
README.md
docs
tests
coverage
.nyc_output
dist
*.test.ts
*.spec.ts
```

### Python Dockerfile

```dockerfile
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

FROM base AS dependencies
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

FROM base AS runner
WORKDIR /app

# Non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

COPY --from=dependencies /app/.venv /app/.venv
COPY src/ ./src/

USER appuser
ENV PATH="/app/.venv/bin:$PATH"

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/api/health').raise_for_status()"

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.9'

services:
  # ─── Application ─────────────────────────────────────────────
  app:
    build:
      context: .
      target: development    # Use dev stage for hot reload
    ports:
      - "3000:3000"
    volumes:
      - .:/app               # Mount source for hot reload
      - /app/node_modules    # Prevent overwriting installed modules
    environment:
      NODE_ENV: development
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/dev
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  # ─── PostgreSQL ───────────────────────────────────────────────
  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: dev
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/db/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d dev"]
      interval: 5s
      timeout: 5s
      retries: 5

  # ─── Redis ────────────────────────────────────────────────────
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --requirepass "devpassword"
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "devpassword", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  # ─── Tools (dev-only) ─────────────────────────────────────────
  mailpit:
    image: axllent/mailpit
    ports:
      - "1025:1025"    # SMTP
      - "8025:8025"    # Web UI → http://localhost:8025

volumes:
  postgres_data:
  redis_data:
```

---

## Architecture Patterns

### Common Commands

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f app

# Rebuild after Dockerfile changes
docker compose build app
docker compose up -d app

# Shell into container
docker compose exec app sh

# Stop all
docker compose down

# Remove volumes (reset data)
docker compose down -v

# Run one-off command
docker compose run --rm app npm run db:migrate
```

### Image Tagging Strategy

```bash
# Semantic versioning + git SHA for traceability
docker build -t registry/app:v1.2.3 .
docker build -t registry/app:v1.2.3-$(git rev-parse --short HEAD) .
docker tag registry/app:v1.2.3 registry/app:latest

# Never use :latest in production — use explicit version
```

---

## Security

```dockerfile
# Always run as non-root
USER appuser

# Use minimal base images
FROM node:20-alpine  # NOT node:20 (debian)
FROM python:3.11-slim  # NOT python:3.11

# Don't include dev dependencies in production image
RUN npm ci --only=production

# Secrets: never in Dockerfile, use environment variables
# ENV API_KEY=secret123  ← NEVER DO THIS

# Scan images for vulnerabilities
# docker scout cves registry/app:v1.2.3
```

---

## Resources

- [Docker Docs](https://docs.docker.com)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Dive (image analyzer)](https://github.com/wagoodman/dive)
- [Docker Scout (security)](https://docs.docker.com/scout/)

# Database Documentation

> **Purpose:** Database schema, design decisions, migration strategy, and query patterns.
> **Related:** [architecture.md](architecture.md) · [../knowledge/postgres.md](../knowledge/postgres.md) · [../snippets/sql.md](../snippets/sql.md)

---

## Overview

| Attribute | Value |
|-----------|-------|
| Primary Database | PostgreSQL 16 |
| ORM | Prisma (TypeScript) / SQLAlchemy (Python) |
| Migrations | Prisma Migrate / Alembic |
| Extensions | pgvector, uuid-ossp, pg_trgm |
| Hosting | Railway / Supabase / Neon |
| Backups | Daily automated, 30-day retention |
| Connection Pooling | PgBouncer / Prisma Accelerate |

---

## Schema Overview

### Core Tables

```sql
-- Users
users (id, email, name, avatar_url, role, created_at, updated_at)

-- Sessions
sessions (id, user_id, token_hash, expires_at, created_at)

-- Audit Log
audit_log (id, user_id, action, resource_type, resource_id, metadata, created_at)
```

### Feature Tables

```sql
-- Add project-specific tables here
-- projects (id, owner_id, name, description, status, created_at, updated_at)
-- documents (id, project_id, title, content, embedding, created_at)
```

---

## Prisma Schema (TypeScript Projects)

```prisma
// schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  sessions  Session[]

  @@map("users")
}

model Session {
  id        String   @id @default(cuid())
  userId    String   @map("user_id")
  tokenHash String   @map("token_hash")
  expiresAt DateTime @map("expires_at")
  createdAt DateTime @default(now()) @map("created_at")

  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([tokenHash])
  @@map("sessions")
}

enum Role {
  USER
  ADMIN
  SUPERADMIN
}
```

---

## SQLAlchemy Models (Python Projects)

```python
# models.py
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
import enum

class Base(DeclarativeBase):
    pass

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
```

---

## Migration Strategy

### Creating Migrations

```bash
# Prisma
npx prisma migrate dev --name add_user_avatar

# Alembic (Python)
alembic revision --autogenerate -m "add_user_avatar"
```

### Migration Rules

1. **Additive-only in production** — never remove columns in the same deploy that removes code referencing them
2. **Two-phase column removal:** Deploy code ignoring column → Deploy migration removing column
3. **Always add indices** for foreign keys and frequently queried columns
4. **Large tables:** Use `CREATE INDEX CONCURRENTLY` to avoid table locks
5. **Test on production data clone** before deploying any migration that touches large tables

### Rollback-Safe Migrations

```sql
-- SAFE: Adding nullable column
ALTER TABLE users ADD COLUMN avatar_url TEXT;

-- SAFE: Adding column with default
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT true;

-- UNSAFE (data loss): Dropping column — must be two-phase
-- Phase 1: Deploy code that ignores this column
-- Phase 2: DROP COLUMN avatar_url
```

---

## Indexing Strategy

```sql
-- Always index foreign keys
CREATE INDEX idx_sessions_user_id ON sessions(user_id);

-- Composite indexes for common query patterns
CREATE INDEX idx_posts_user_status ON posts(user_id, status) WHERE deleted_at IS NULL;

-- Full-text search
CREATE INDEX idx_documents_content ON documents USING gin(to_tsvector('english', content));

-- Partial index for active records
CREATE INDEX idx_sessions_active ON sessions(token_hash) WHERE expires_at > NOW();

-- Vector similarity search (pgvector)
CREATE INDEX idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
```

---

## Common Query Patterns

```sql
-- Paginated list with total count
SELECT
  *,
  COUNT(*) OVER() AS total_count
FROM users
WHERE deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 20 OFFSET 0;

-- Full-text search
SELECT *, ts_rank(to_tsvector('english', content), query) AS rank
FROM documents, to_tsquery('english', 'search & term') query
WHERE to_tsvector('english', content) @@ query
ORDER BY rank DESC;

-- Vector similarity search (pgvector)
SELECT id, title, 1 - (embedding <=> '[0.1, 0.2, ...]') AS similarity
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 10;

-- Upsert pattern
INSERT INTO user_settings (user_id, key, value)
VALUES ($1, $2, $3)
ON CONFLICT (user_id, key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW();
```

---

## Backup & Recovery

```bash
# Manual backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore
psql $DATABASE_URL < backup_20240115.sql

# Point-in-time recovery (PITR)
# Configure in hosting provider (Neon, Supabase, Railway)
# Retention: 7-30 days depending on plan
```

---

## Performance Monitoring

```sql
-- Slow query analysis
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;

-- Index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

---

## Connection String Formats

```bash
# PostgreSQL DSN
DATABASE_URL="postgresql://user:password@host:5432/dbname?schema=public&sslmode=require"

# With PgBouncer
DATABASE_DIRECT_URL="postgresql://user:password@host:5432/dbname"
DATABASE_URL="postgresql://user:password@pgbouncer:6543/dbname?pgbouncer=true"
```

---

*Last Updated: <!-- YYYY-MM-DD --> | Update when schema changes*

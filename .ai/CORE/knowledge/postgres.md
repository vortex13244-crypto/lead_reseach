# PostgreSQL — Knowledge Base

> **Purpose:** PostgreSQL best practices, query patterns, and performance tuning.
> **Related:** [../docs/database.md](../docs/database.md) · [../snippets/sql.md](../snippets/sql.md) · [../roles/database-engineer.md](../roles/database-engineer.md)

---

## Overview

PostgreSQL is the primary database. Use pgvector for AI/embeddings, pg_trgm for fuzzy text search, and uuid-ossp for UUID generation. Always run in a container locally (see docker.md) or use Neon/Supabase for managed service.

---

## Best Practices

### Schema Design

```sql
-- Always use these column conventions
id          TEXT PRIMARY KEY DEFAULT gen_random_uuid()  -- or cuid via application
created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
deleted_at  TIMESTAMPTZ  -- NULL = active (soft delete)

-- Use check constraints for enums (or native PostgreSQL enums)
status TEXT NOT NULL CHECK (status IN ('active', 'inactive', 'pending'))

-- Foreign keys: always explicit + indexed
user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE
-- Then: CREATE INDEX idx_table_user_id ON table(user_id);

-- Store money as integers (smallest currency unit)
amount_cents INTEGER NOT NULL  -- $9.99 stored as 999
```

### Essential Extensions

```sql
-- Enable in migration
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";    -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pg_trgm";      -- Trigram fuzzy search
CREATE EXTENSION IF NOT EXISTS "vector";        -- pgvector (AI embeddings)
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";  -- Query analysis
```

---

## Indexing

```sql
-- B-tree (default) — equality and range queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);

-- Partial index — only index relevant rows
CREATE INDEX idx_sessions_active ON sessions(token_hash)
WHERE expires_at > NOW();

CREATE INDEX idx_posts_published ON posts(created_at DESC)
WHERE deleted_at IS NULL AND published = true;

-- GIN — full-text search
CREATE INDEX idx_docs_content_fts ON documents
USING gin(to_tsvector('english', content));

-- GIN — JSONB queries
CREATE INDEX idx_metadata ON users USING gin(metadata);

-- HNSW (pgvector) — vector similarity (recommended for accuracy)
CREATE INDEX idx_doc_embeddings ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- IVFFlat (pgvector) — faster to build, slightly less accurate
CREATE INDEX idx_doc_embeddings ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Always use CONCURRENTLY for production tables to avoid locking
CREATE INDEX CONCURRENTLY idx_name ON table(column);
```

---

## Common Queries

### Paginated List

```sql
-- Offset pagination (simple, good for < 10M rows)
SELECT
  *,
  COUNT(*) OVER() AS total_count
FROM users
WHERE deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 20 OFFSET 40;  -- Page 3 (0-indexed: OFFSET = (page - 1) * limit)

-- Cursor pagination (scalable for large tables)
-- First page
SELECT * FROM posts ORDER BY (created_at, id) DESC LIMIT 20;
-- Next page (using cursor from last row)
SELECT * FROM posts
WHERE (created_at, id) < ($last_created_at, $last_id)
ORDER BY (created_at, id) DESC
LIMIT 20;
```

### Full-Text Search

```sql
-- Basic full-text search
SELECT
  id,
  title,
  ts_rank(to_tsvector('english', content), query) AS rank
FROM documents, to_tsquery('english', 'postgresql & index') query
WHERE to_tsvector('english', content) @@ query
ORDER BY rank DESC
LIMIT 20;

-- Fuzzy search with trigrams (find "Postgre" → PostgreSQL)
SELECT name, similarity(name, 'Postgre') AS sim
FROM products
WHERE name % 'Postgre'  -- Trigram similarity threshold (default 0.3)
ORDER BY sim DESC;
```

### Vector Similarity Search (pgvector)

```sql
-- Cosine similarity (most common for embeddings)
SELECT
  id,
  title,
  1 - (embedding <=> $1::vector) AS similarity
FROM documents
WHERE 1 - (embedding <=> $1::vector) > 0.7  -- Threshold
ORDER BY embedding <=> $1::vector
LIMIT 10;

-- L2 distance (for normalized vectors)
SELECT id, embedding <-> $1::vector AS distance
FROM documents
ORDER BY embedding <-> $1::vector
LIMIT 10;
```

### Upsert

```sql
-- PostgreSQL native UPSERT
INSERT INTO user_settings (user_id, key, value, updated_at)
VALUES ($1, $2, $3, NOW())
ON CONFLICT (user_id, key)
DO UPDATE SET
  value = EXCLUDED.value,
  updated_at = NOW()
RETURNING *;
```

### Window Functions

```sql
-- Running totals, rankings, moving averages
SELECT
  user_id,
  created_at,
  amount_cents,
  SUM(amount_cents) OVER (PARTITION BY user_id ORDER BY created_at) AS running_total,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS order_rank,
  LAG(amount_cents, 1) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_amount
FROM orders
WHERE deleted_at IS NULL;
```

---

## Performance

### EXPLAIN ANALYZE

```sql
-- Always check query plans for slow queries
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'user@example.com';

-- Key things to look for:
-- "Seq Scan" on large table → missing index
-- "Sort" on large dataset → add ORDER BY column to index
-- High "rows removed by filter" → index not selective enough
-- Actual vs estimated rows differ greatly → stale statistics (run ANALYZE)
```

### Statistics and Maintenance

```sql
-- Update query planner statistics
ANALYZE users;
ANALYZE VERBOSE users;

-- Check table bloat (dead tuples)
SELECT
  relname,
  n_live_tup,
  n_dead_tup,
  round(n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) * 100, 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY dead_ratio DESC;

-- Manual VACUUM (usually handled by autovacuum)
VACUUM (VERBOSE, ANALYZE) users;
```

### Slow Query Log

```sql
-- Top 10 slowest queries (pg_stat_statements extension required)
SELECT
  left(query, 100) AS query_preview,
  calls,
  round(total_exec_time::numeric / calls, 2) AS avg_ms,
  round(total_exec_time::numeric, 2) AS total_ms,
  rows / calls AS avg_rows
FROM pg_stat_statements
WHERE calls > 10
ORDER BY total_exec_time / calls DESC
LIMIT 10;
```

---

## Configuration (Production)

```ini
# postgresql.conf key settings for production

# Memory
shared_buffers = 256MB          # 25% of RAM
work_mem = 16MB                 # Per sort/hash operation
maintenance_work_mem = 128MB    # For VACUUM, CREATE INDEX

# Connections
max_connections = 100           # Use connection pooler (PgBouncer)
                                # Set lower than you think

# WAL / Replication
wal_level = replica             # Enable for logical replication
max_wal_size = 1GB

# Logging
log_min_duration_statement = 1000  # Log queries > 1s
log_statement = 'ddl'              # Log schema changes
shared_preload_libraries = 'pg_stat_statements'
```

---

## Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [pgvector](https://github.com/pgvector/pgvector)
- [Use The Index, Luke](https://use-the-index-luke.com/)
- [Explain Depesz](https://explain.depesz.com/) — EXPLAIN ANALYZE visualizer
- [PgBouncer](https://www.pgbouncer.org/) — Connection pooler

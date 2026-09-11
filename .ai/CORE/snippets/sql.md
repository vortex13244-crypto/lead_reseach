# Snippet: Safe SQL Patterns

> **Purpose:** Reference patterns for query safety and predictable database access.

## Rules

- Use parameterized queries or a trusted ORM; never concatenate user input into SQL.
- Add an index only for an observed query pattern and verify it with `EXPLAIN`.
- Keep migrations append-only and reversible where practical.
- Limit and order list queries deterministically.

```sql
-- Safe parameterized form; bind `$1` through the database driver.
SELECT id, email, created_at
FROM users
WHERE email = $1;

-- Keyset pagination for a stable, large list.
SELECT id, created_at
FROM events
WHERE created_at < $1
ORDER BY created_at DESC
LIMIT $2;
```

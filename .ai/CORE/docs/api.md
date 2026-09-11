# API Documentation

> **Purpose:** Complete reference for all API endpoints, authentication, data models, and integration patterns.
> **Related:** [architecture.md](architecture.md) · [../roles/backend.md](../roles/backend.md) · [../snippets/api.md](../snippets/api.md)

---

## Overview

| Attribute | Value |
|-----------|-------|
| Base URL (Local) | `http://localhost:8000/api/v1` |
| Base URL (Staging) | `https://staging.yourdomain.com/api/v1` |
| Base URL (Production) | `https://yourdomain.com/api/v1` |
| Protocol | HTTPS (HTTP in local) |
| Format | JSON |
| Authentication | Bearer JWT |
| Rate Limiting | 100 req/min (standard), 1000 req/min (authenticated) |
| API Versioning | URL path (`/v1/`, `/v2/`) |

---

## Authentication

### JWT Authentication

```http
Authorization: Bearer <access_token>
```

### Obtaining a Token

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "expires_in": 900,
  "token_type": "Bearer"
}
```

### Refreshing a Token

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGci..."
}
```

---

## Standard Response Format

### Success

```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

### Error

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

### Standard Error Codes

| Code | HTTP Status | Description |
|------|------------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid auth token |
| `FORBIDDEN` | 403 | Authenticated but lacks permission |
| `NOT_FOUND` | 404 | Resource does not exist |
| `VALIDATION_ERROR` | 422 | Request body failed validation |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Endpoints

### Health

```http
GET /api/health
```

**Response:**
```json
{
  "status": "ok",
  "version": "1.2.3",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "database": "ok",
    "redis": "ok"
  }
}
```

---

### Users

#### Get Current User

```http
GET /api/v1/users/me
Authorization: Bearer <token>
```

#### Update User

```http
PATCH /api/v1/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Name",
  "avatar_url": "https://..."
}
```

#### List Users (Admin)

```http
GET /api/v1/admin/users?page=1&per_page=20&search=john
Authorization: Bearer <admin_token>
```

---

### Resources (Template — Replace with actual resources)

```http
# List
GET /api/v1/resources?page=1&per_page=20&filter[status]=active

# Get one
GET /api/v1/resources/:id

# Create
POST /api/v1/resources
{
  "name": "...",
  "description": "..."
}

# Update
PATCH /api/v1/resources/:id
{
  "name": "..."
}

# Delete
DELETE /api/v1/resources/:id
```

---

## Pagination

All list endpoints support cursor-based or offset-based pagination:

```http
GET /api/v1/resources?page=2&per_page=20
GET /api/v1/resources?cursor=eyJpZCI6MTIzfQ==&limit=20
```

Response includes:
```json
{
  "data": [...],
  "meta": {
    "page": 2,
    "per_page": 20,
    "total": 200,
    "total_pages": 10,
    "has_next": true,
    "has_prev": true
  }
}
```

---

## Rate Limiting

Rate limit headers are included in every response:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1705309800
```

On limit exceeded:
```json
HTTP 429
Retry-After: 45

{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Try again in 45 seconds.",
    "retry_after": 45
  }
}
```

---

## Webhooks

### Configuring Webhooks

```http
POST /api/v1/webhooks
{
  "url": "https://your-server.com/webhook",
  "events": ["user.created", "payment.succeeded"],
  "secret": "your_webhook_secret"
}
```

### Webhook Payload

```json
{
  "id": "evt_abc123",
  "type": "user.created",
  "created_at": "2024-01-15T10:30:00Z",
  "data": { ... }
}
```

### Verifying Webhook Signatures

```typescript
import { createHmac } from 'crypto'

function verifyWebhookSignature(payload: string, signature: string, secret: string): boolean {
  const expected = createHmac('sha256', secret)
    .update(payload)
    .digest('hex')
  return `sha256=${expected}` === signature
}
```

---

## SDK / Client Examples

### TypeScript / JavaScript

```typescript
const client = new ApiClient({
  baseUrl: process.env.API_URL,
  token: userToken,
})

const users = await client.users.list({ page: 1, perPage: 20 })
const user = await client.users.getById('user_123')
```

### Python

```python
import httpx

client = httpx.AsyncClient(
    base_url=settings.API_URL,
    headers={"Authorization": f"Bearer {token}"}
)

response = await client.get("/api/v1/users/me")
user = response.json()["data"]
```

---

## OpenAPI / Swagger

OpenAPI specification available at:
- Local: `http://localhost:8000/docs`
- Staging: `https://staging.yourdomain.com/docs`

Download spec: `GET /api/openapi.json`

---

*Last Updated: <!-- YYYY-MM-DD --> | Update when endpoints change*

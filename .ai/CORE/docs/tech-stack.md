# Tech Stack

> **Scope:** Complete technology inventory — languages, frameworks, databases, infrastructure, and tooling.
> **Audience:** AI agents performing implementation, dependency management, or infrastructure tasks.
> **Related:** [architecture.md](./architecture.md) · [../standards/code-style.md](../standards/code-style.md)

---

## 1. Frontend

| Category          | Technology        | Version   | Purpose                          | Docs / Notes              |
| ----------------- | ----------------- | --------- | -------------------------------- | ------------------------- |
| Language          | <!-- TypeScript -->| <!-- 5.x --> | <!-- Type-safe development --> | <!-- tsconfig notes -->   |
| Framework         | <!-- React -->    | <!-- 18.x -->| <!-- UI rendering -->          | <!-- SPA / SSR -->        |
| State Management  | <!-- Zustand -->  | <!-- 4.x --> | <!-- Client state -->          |                           |
| Styling           | <!-- Tailwind CSS --> | <!-- 3.x --> | <!-- Utility-first CSS --> |                           |
| Build Tool        | <!-- Vite -->     | <!-- 5.x --> | <!-- Bundling, HMR -->         |                           |
| Testing           | <!-- Vitest -->   | <!-- 1.x --> | <!-- Unit & component tests -->|                           |
| E2E Testing       | <!-- Playwright -->| <!-- 1.x -->| <!-- Browser automation -->    |                           |
| Linting           | <!-- ESLint -->   | <!-- 9.x --> | <!-- Code quality -->          |                           |
| Formatting        | <!-- Prettier --> | <!-- 3.x --> | <!-- Consistent formatting --> |                           |

### Frontend Architecture Notes

- <!-- Rendering strategy: CSR / SSR / SSG / ISR -->
- <!-- Routing approach: file-based / code-based -->
- <!-- API communication: REST / GraphQL / tRPC -->

---

## 2. Backend

| Category          | Technology         | Version   | Purpose                          | Docs / Notes              |
| ----------------- | ------------------ | --------- | -------------------------------- | ------------------------- |
| Language          | <!-- Node.js -->   | <!-- 20.x --> | <!-- Runtime -->              |                           |
| Framework         | <!-- Express -->   | <!-- 4.x -->  | <!-- HTTP server -->          |                           |
| API Style         | <!-- REST -->      | <!-- v1 -->   | <!-- Client-server contract -->|                           |
| Validation        | <!-- Zod -->       | <!-- 3.x -->  | <!-- Schema validation -->    |                           |
| ORM / Query       | <!-- Prisma -->    | <!-- 5.x -->  | <!-- Database access -->      |                           |
| Auth              | <!-- JWT -->       | <!-- — -->    | <!-- Token-based auth -->     |                           |
| Testing           | <!-- Jest -->      | <!-- 29.x --> | <!-- Unit & integration -->   |                           |
| Process Manager   | <!-- PM2 -->       | <!-- 5.x -->  | <!-- Production process mgmt -->|                          |

### Backend Architecture Notes

- <!-- Monolith vs. microservices -->
- <!-- Background job processing approach -->
- <!-- Error handling and logging strategy -->

---

## 3. Database

| Category          | Technology          | Version   | Purpose                          | Hosting                  |
| ----------------- | ------------------- | --------- | -------------------------------- | ------------------------ |
| Primary DB        | <!-- PostgreSQL --> | <!-- 16 -->| <!-- Relational data -->         | <!-- RDS / Self-hosted -->|
| Cache             | <!-- Redis -->      | <!-- 7.x -->| <!-- Session, cache, queues --> | <!-- ElastiCache -->     |
| Search            | <!-- Elasticsearch --> | <!-- 8.x --> | <!-- Full-text search -->   | <!-- Managed -->         |
| File Storage      | <!-- S3 -->         | <!-- — --> | <!-- Binary assets -->           | <!-- AWS -->             |

### Database Notes

- <!-- Migration tool: Prisma Migrate / Flyway / Alembic -->
- <!-- Backup strategy and RPO/RTO targets -->
- <!-- Connection pooling: PgBouncer / built-in -->
- <!-- Read replica configuration -->

---

## 4. Infrastructure

| Category          | Technology          | Purpose                           | Notes                    |
| ----------------- | ------------------- | --------------------------------- | ------------------------ |
| Cloud Provider    | <!-- AWS -->        | <!-- Primary hosting -->          |                          |
| Compute           | <!-- ECS Fargate -->| <!-- Container orchestration -->  |                          |
| CDN               | <!-- CloudFront --> | <!-- Static asset delivery -->    |                          |
| DNS               | <!-- Route 53 -->   | <!-- Domain management -->        |                          |
| Load Balancer     | <!-- ALB -->        | <!-- Traffic distribution -->     |                          |
| Secrets           | <!-- AWS Secrets Manager --> | <!-- Credential storage --> |                       |
| IaC               | <!-- Terraform -->  | <!-- Infrastructure as Code -->   |                          |

---

## 5. DevOps

| Category          | Technology          | Purpose                           | Notes                    |
| ----------------- | ------------------- | --------------------------------- | ------------------------ |
| CI/CD             | <!-- GitHub Actions --> | <!-- Build, test, deploy -->   |                          |
| Container Runtime | <!-- Docker -->     | <!-- Containerization -->         |                          |
| Registry          | <!-- ECR -->        | <!-- Container image storage -->  |                          |
| Monitoring        | <!-- Datadog -->    | <!-- APM, metrics, alerts -->     |                          |
| Logging           | <!-- CloudWatch --> | <!-- Centralized logs -->         |                          |
| Error Tracking    | <!-- Sentry -->     | <!-- Runtime error capture -->    |                          |
| Uptime Monitoring | <!-- Pingdom -->    | <!-- Availability checks -->      |                          |

### CI/CD Pipeline

```
Push → Lint → Unit Tests → Build → Integration Tests → Deploy to Staging → Smoke Tests → Deploy to Production
```

---

## 6. AI

| Category              | Technology          | Purpose                           | Notes                    |
| --------------------- | ------------------- | --------------------------------- | ------------------------ |
| LLM Provider          | <!-- OpenAI -->     | <!-- Text generation -->          | <!-- Model version -->   |
| Embedding Model       | <!-- text-embedding-3-small --> | <!-- Vector search --> |                          |
| Vector Database       | <!-- Pinecone -->   | <!-- Similarity search -->        |                          |
| ML Framework          | <!-- PyTorch -->    | <!-- Custom model training -->    |                          |
| Orchestration         | <!-- LangChain -->  | <!-- LLM pipeline management -->  |                          |
| AI Code Assistants    | <!-- Cursor / Copilot --> | <!-- Development velocity --> |                          |

---

## 7. External APIs

| Service             | Purpose                     | Auth Method      | Rate Limits          | Fallback Strategy    |
| ------------------- | --------------------------- | ---------------- | -------------------- | -------------------- |
| <!-- Stripe -->     | <!-- Payment processing --> | <!-- API Key -->  | <!-- 100 req/s -->   | <!-- Queue + retry -->|
| <!-- SendGrid -->   | <!-- Transactional email -->| <!-- API Key -->  | <!-- 600 req/min --> | <!-- SMTP fallback -->|
| <!-- Twilio -->     | <!-- SMS / 2FA -->          | <!-- API Key -->  | <!-- Varies -->      | <!-- Email fallback -->|
| <!-- Google Maps -->| <!-- Geocoding -->          | <!-- API Key -->  | <!-- 50 req/s -->    | <!-- Cache results -->|

### API Integration Guidelines

- Store all API keys in the secrets manager — never in source code or environment files committed to version control.
- Implement circuit breaker patterns for all external API calls.
- Cache responses where appropriate to reduce costs and latency.
- Log all external API calls with request ID, latency, and response status for debugging.
- Define timeout and retry policies per integration.

---

## Version Policy

| Policy               | Rule                                                    |
| -------------------- | ------------------------------------------------------- |
| Language / Runtime   | Track latest LTS. Upgrade within 3 months of release.   |
| Frameworks           | Pin to major version. Evaluate upgrades quarterly.      |
| Libraries            | Use caret ranges (`^`). Review breaking changes on update.|
| Infrastructure Tools | Follow provider deprecation schedules.                  |

---

## Changelog

| Date       | Change Description                                |
| ---------- | ------------------------------------------------- |
| <!-- YYYY-MM-DD --> | <!-- Initial tech stack documented -->      |

# Architecture

> **Scope:** System-level architecture decisions, component boundaries, data flow, and non-functional requirements.
> **Audience:** AI agents performing design, implementation, review, or refactoring tasks.
> **Related:** [tech-stack.md](./tech-stack.md) · [vision.md](./vision.md) · [features.md](./features.md)

---

## 1. Overview

<!-- One-paragraph summary of the system's purpose and architectural style. -->

| Attribute           | Value                              |
| ------------------- | ---------------------------------- |
| Architecture Style  | <!-- e.g., Monolith / Microservices / Modular Monolith / Serverless --> |
| Primary Language    | <!-- e.g., TypeScript, Python, Go --> |
| Deployment Target   | <!-- e.g., AWS, GCP, Self-hosted --> |
| Last Updated        | <!-- YYYY-MM-DD -->                |

---

## 2. Goals

### Functional Goals

- <!-- Goal 1: What the system must accomplish -->
- <!-- Goal 2 -->

### Non-Functional Goals

| Quality Attribute | Target                           | Measurement                     |
| ----------------- | -------------------------------- | ------------------------------- |
| Availability      | <!-- e.g., 99.9% uptime -->      | <!-- Monitoring / SLA -->       |
| Latency           | <!-- e.g., p95 < 200ms -->       | <!-- APM tooling -->            |
| Throughput        | <!-- e.g., 1000 RPS -->          | <!-- Load tests -->             |
| Maintainability   | <!-- e.g., low coupling score -->| <!-- Static analysis -->        |

---

## 3. High-Level Architecture

<!-- Insert or describe the system architecture diagram here. Use a Mermaid diagram or reference an image. -->

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Client     │────▶│   API Layer  │────▶│   Database   │
│  (Web/Mobile)│     │  (Gateway)   │     │              │
└─────────────┘     └──────┬───────┘     └──────────────┘
                           │
                    ┌──────▼───────┐
                    │  Services /  │
                    │  Modules     │
                    └──────────────┘
```

### Layers

| Layer            | Responsibility                                   | Key Technologies |
| ---------------- | ------------------------------------------------ | ---------------- |
| Presentation     | UI rendering, user interaction                   | <!-- ... -->     |
| API / Gateway    | Routing, authentication, rate limiting           | <!-- ... -->     |
| Business Logic   | Domain rules, orchestration, validation          | <!-- ... -->     |
| Data Access      | Persistence, caching, query optimization         | <!-- ... -->     |
| Infrastructure   | Logging, monitoring, messaging, scheduled tasks  | <!-- ... -->     |

---

## 4. Modules

<!-- List each bounded context or module. One subsection per module. -->

### Module: `<!-- module-name -->`

| Attribute      | Value                                      |
| -------------- | ------------------------------------------ |
| Responsibility | <!-- Single-sentence description -->       |
| Owns Data      | <!-- Tables / collections it owns -->      |
| Exposes        | <!-- REST / gRPC / Events / SDK -->        |
| Depends On     | <!-- Other modules -->                     |
| Key Files      | <!-- Entry points, routers, services -->   |

<!-- Repeat for each module -->

---

## 5. Data Flow

### Request Lifecycle

```
Client → Load Balancer → API Gateway → Auth Middleware → Router
  → Controller → Service → Repository → Database
  → Response serialization → Client
```

### Asynchronous Flows

| Trigger              | Producer       | Consumer        | Transport       |
| -------------------- | -------------- | --------------- | --------------- |
| <!-- e.g., Order placed --> | <!-- Service A --> | <!-- Service B --> | <!-- Queue / Event bus --> |

### Data Storage Map

| Data Entity     | Primary Store     | Cache Layer       | Retention Policy  |
| --------------- | ----------------- | ----------------- | ----------------- |
| <!-- Users -->  | <!-- PostgreSQL -->| <!-- Redis -->    | <!-- Indefinite -->|

---

## 6. Dependencies

### Internal Dependencies

<!-- Module dependency graph. Keep it acyclic. -->

```
module-a → module-b → module-c
module-a → module-d
```

### External Dependencies

| Dependency         | Purpose                  | Version Policy       | Risk Level |
| ------------------ | ------------------------ | -------------------- | ---------- |
| <!-- Library A --> | <!-- Auth -->            | <!-- Pin major -->   | <!-- Low -->|
| <!-- Service B --> | <!-- Payment gateway --> | <!-- API v2 -->      | <!-- High -->|

---

## 7. Design Decisions

<!-- Record significant architectural decisions using the ADR (Architecture Decision Record) format. -->

### ADR-001: <!-- Decision Title -->

| Attribute  | Value                                          |
| ---------- | ---------------------------------------------- |
| Status     | <!-- Accepted / Superseded / Deprecated -->    |
| Date       | <!-- YYYY-MM-DD -->                            |
| Context    | <!-- Why this decision was needed -->          |
| Decision   | <!-- What was decided -->                      |
| Rationale  | <!-- Why this option was chosen -->            |
| Trade-offs | <!-- What was given up -->                     |
| Alternatives Considered | <!-- Other options evaluated --> |

<!-- Repeat ADR block for each significant decision -->

---

## 8. Scalability

### Horizontal Scaling Strategy

- <!-- Stateless services behind load balancer -->
- <!-- Database read replicas -->
- <!-- Sharding strategy (if applicable) -->

### Vertical Scaling Limits

- <!-- Known bottlenecks -->
- <!-- Resource-intensive operations -->

### Caching Strategy

| Cache Layer | Technology | TTL Policy | Invalidation Strategy |
| ----------- | ---------- | ---------- | --------------------- |
| <!-- L1 --> | <!-- In-memory --> | <!-- 60s --> | <!-- Event-driven --> |
| <!-- L2 --> | <!-- Redis -->     | <!-- 5m -->  | <!-- TTL expiry -->   |

---

## 9. Security

### Authentication & Authorization

- <!-- Auth mechanism: JWT / OAuth2 / Session -->
- <!-- Authorization model: RBAC / ABAC / ACL -->
- <!-- Token lifecycle and refresh strategy -->

### Data Protection

- <!-- Encryption at rest -->
- <!-- Encryption in transit (TLS) -->
- <!-- PII handling and data masking -->

### Attack Surface Mitigation

| Threat              | Mitigation                        |
| ------------------- | --------------------------------- |
| SQL Injection       | <!-- Parameterized queries -->    |
| XSS                 | <!-- Output encoding -->          |
| CSRF                | <!-- Token validation -->         |
| Rate Abuse          | <!-- Rate limiting -->            |
| Dependency Exploits | <!-- Automated CVE scanning -->   |

---

## 10. Risks

| Risk                              | Likelihood | Impact | Mitigation                           |
| --------------------------------- | ---------- | ------ | ------------------------------------ |
| <!-- Single point of failure -->  | <!-- H --> | <!-- H --> | <!-- Redundancy / failover -->  |
| <!-- Vendor lock-in -->           | <!-- M --> | <!-- M --> | <!-- Abstraction layer -->      |
| <!-- Data loss -->                | <!-- L --> | <!-- H --> | <!-- Backups, replication -->   |

---

## 11. Future Improvements

| Improvement                        | Priority | Blocked By              | Expected Impact          |
| ---------------------------------- | -------- | ----------------------- | ------------------------ |
| <!-- Migrate to event-driven -->   | <!-- P1 --> | <!-- Infra readiness --> | <!-- Lower coupling --> |
| <!-- Add observability stack -->    | <!-- P2 --> | <!-- Budget -->          | <!-- Faster debugging -->|

---

## Changelog

| Date       | Author         | Change Description                   |
| ---------- | -------------- | ------------------------------------ |
| <!-- YYYY-MM-DD --> | <!-- Name / Agent --> | <!-- Initial draft -->  |

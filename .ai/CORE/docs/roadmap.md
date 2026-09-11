# Roadmap

> **Scope:** Project timeline, milestones, priorities, and technical debt tracking.
> **Audience:** AI agents performing planning, prioritization, or scoping tasks.
> **Related:** [vision.md](./vision.md) · [features.md](./features.md) · [architecture.md](./architecture.md)

---

## 1. Current State

### Project Phase

<!-- Select one: Ideation / MVP / Alpha / Beta / Production / Maintenance / Sunset -->

| Attribute              | Value                                     |
| ---------------------- | ----------------------------------------- |
| Phase                  | <!-- e.g., Beta -->                       |
| Last Major Release     | <!-- e.g., v0.8.0 — 2025-01-15 -->       |
| Active Users / Scale   | <!-- e.g., 500 beta users -->             |
| Team Size              | <!-- e.g., 3 engineers + 1 designer -->   |
| Key Constraint         | <!-- e.g., Time / Budget / Headcount -->  |

### What Is Done

- <!-- Core authentication and user management -->
- <!-- REST API v1 with 12 endpoints -->
- <!-- CI/CD pipeline with automated testing -->

### What Is In Progress

| Item                         | Owner          | ETA            | Blocker              |
| ---------------------------- | -------------- | -------------- | -------------------- |
| <!-- Feature X -->           | <!-- Name -->  | <!-- Date -->  | <!-- None / Desc --> |

---

## 2. Next Milestones

### Milestone: <!-- Name --> (Target: <!-- YYYY-MM-DD -->)

**Goal:** <!-- One-sentence objective for this milestone -->

| Deliverable                  | Priority | Status         | Dependencies         |
| ---------------------------- | -------- | -------------- | -------------------- |
| <!-- Deliverable 1 -->       | P0       | <!-- Status --> | <!-- None -->        |
| <!-- Deliverable 2 -->       | P1       | <!-- Status --> | <!-- Deliverable 1 -->|

**Exit Criteria:**
- [ ] <!-- All P0 items shipped -->
- [ ] <!-- Performance benchmarks met -->
- [ ] <!-- No critical bugs open -->

---

### Milestone: <!-- Name --> (Target: <!-- YYYY-MM-DD -->)

**Goal:** <!-- One-sentence objective -->

| Deliverable                  | Priority | Status         | Dependencies         |
| ---------------------------- | -------- | -------------- | -------------------- |
| <!-- Deliverable 1 -->       | P0       | <!-- Status --> | <!-- None -->        |

**Exit Criteria:**
- [ ] <!-- Criteria -->

---

## 3. Long-Term Goals

<!-- 6–18 month vision. These are directional, not commitments. -->

| Goal                                    | Timeframe   | Strategic Value                       |
| --------------------------------------- | ----------- | ------------------------------------- |
| <!-- Multi-region deployment -->        | <!-- Q3 --> | <!-- Latency reduction, compliance -->|
| <!-- Plugin / extension system -->      | <!-- Q4 --> | <!-- Ecosystem growth -->             |
| <!-- ML-powered recommendations -->     | <!-- H2 --> | <!-- User engagement -->              |

---

## 4. Technical Debt

### Debt Registry

| ID       | Description                            | Impact  | Effort | Priority | Introduced |
| -------- | -------------------------------------- | ------- | ------ | -------- | ---------- |
| `TD-001` | <!-- Hardcoded config values -->       | <!-- M --> | <!-- S --> | <!-- P1 --> | <!-- YYYY-MM-DD --> |
| `TD-002` | <!-- Missing input validation on /api/upload --> | <!-- H --> | <!-- M --> | <!-- P0 --> | <!-- YYYY-MM-DD --> |
| `TD-003` | <!-- Monolithic service needs decomposition --> | <!-- H --> | <!-- L --> | <!-- P2 --> | <!-- YYYY-MM-DD --> |

### Impact Scale

| Level | Meaning                                                    |
| ----- | ---------------------------------------------------------- |
| H     | Actively causing bugs, blocking features, or degrading UX  |
| M     | Slowing development velocity or increasing cognitive load  |
| L     | Cosmetic, minor inefficiency, or future risk               |

### Effort Scale

| Level | Meaning                          |
| ----- | -------------------------------- |
| S     | < 1 day                         |
| M     | 1–3 days                        |
| L     | 1–2 weeks                       |
| XL    | > 2 weeks, likely needs a spike |

---

## 5. Priorities

### Priority Framework

| Priority | Label       | Definition                                               |
| -------- | ----------- | -------------------------------------------------------- |
| P0       | Critical    | Must be done immediately. Blocks release or causes outage.|
| P1       | High        | Required for next milestone. Business-critical.          |
| P2       | Medium      | Important but can wait one cycle. Improves quality.      |
| P3       | Low         | Nice-to-have. Do when capacity allows.                   |

### Current Priority Stack

<!-- Ordered list of the most important items right now. Max 10. -->

1. <!-- P0: Fix authentication bypass vulnerability -->
2. <!-- P0: Stabilize database connection pooling -->
3. <!-- P1: Ship user dashboard feature -->
4. <!-- P1: Reduce API latency below 200ms p95 -->
5. <!-- P2: Refactor notification service -->

---

## 6. Release Plan

| Version   | Date          | Type    | Key Changes                          |
| --------- | ------------- | ------- | ------------------------------------ |
| <!-- v1.0.0 --> | <!-- YYYY-MM-DD --> | Major | <!-- Initial production release --> |
| <!-- v1.1.0 --> | <!-- YYYY-MM-DD --> | Minor | <!-- Dashboard + analytics -->    |
| <!-- v1.1.1 --> | <!-- YYYY-MM-DD --> | Patch | <!-- Security fix -->             |

---

## Changelog

| Date       | Change Description                               |
| ---------- | ------------------------------------------------ |
| <!-- YYYY-MM-DD --> | <!-- Initial roadmap created -->           |

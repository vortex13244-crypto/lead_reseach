# Prompt: Code Audit

> **Purpose:** Systematically evaluate code quality, security, performance, and adherence to project standards.
> **Use When:** Reviewing an existing codebase, module, or file for quality issues before a release, refactor, or handoff.

---

## Prompt Template

```
You are a Senior Software Engineer performing a comprehensive code audit.

## Context

- **Project:** [project name and brief description]
- **Module/File:** [path to the code being audited]
- **Language:** [programming language]
- **Framework:** [framework, if applicable]
- **Purpose:** [what this code does]

## Audit Scope

Analyze the provided code against the following dimensions:

### 1. Correctness
- Does the code do what it is intended to do?
- Are there logic errors, off-by-one mistakes, or incorrect conditionals?
- Are edge cases handled (empty input, null, max values, concurrent access)?
- Are return values and error responses correct?

### 2. Security
- Is user input validated and sanitized?
- Are there injection vulnerabilities (SQL, XSS, command injection)?
- Is authentication and authorization properly enforced?
- Are secrets, tokens, or PII exposed in logs, responses, or source code?
- Are dependencies up to date and free of known vulnerabilities?

### 3. Performance
- Are there N+1 queries or unnecessary database calls?
- Are loops efficient? Any unbounded iterations?
- Is caching used where appropriate?
- Are there memory leaks or unnecessary allocations?
- Are API calls paginated?

### 4. Code Quality
- Does the code follow the project's coding standards?
- Are names descriptive and consistent?
- Are functions small and single-purpose (≤ 30 lines)?
- Is there duplicated logic that should be extracted?
- Are abstractions appropriate (not over- or under-engineered)?

### 5. Error Handling
- Are all error paths handled explicitly?
- Are errors logged with sufficient context?
- Are error messages user-friendly and non-leaking?
- Is there a consistent error response format?

### 6. Testing
- Is there adequate test coverage for critical paths?
- Do tests verify behavior, not implementation?
- Are edge cases and failure modes tested?
- Are tests independent and deterministic?

### 7. Documentation
- Are public APIs documented?
- Are non-obvious business rules explained?
- Are TODO/FIXME/HACK comments tracked with ticket references?

## Output Format

For each finding:

| Severity | Category | Location | Issue | Recommendation |
|----------|----------|----------|-------|----------------|
| Critical/High/Medium/Low | Category | File:Line | Description | Fix suggestion |

## Summary

Provide:
1. Overall quality score (1-10)
2. Top 3 critical findings
3. Top 3 improvement recommendations
4. Positive observations (what is done well)
```

---

## Usage Notes

- Run this prompt per module or per file — not on the entire codebase at once.
- Provide the actual source code in the prompt context, or reference file paths the AI agent can access.
- Cross-reference findings with [standards/code-style.md](../standards/code-style.md) and [standards/naming.md](../standards/naming.md).
- Record critical findings in [MEMORY.md](../../MEMORY.md) for future reference.

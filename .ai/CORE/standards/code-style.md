# Code Style Standards

> **Scope:** Language-agnostic coding conventions for consistency, readability, and maintainability.
> **Audience:** AI agents and developers writing or reviewing code.
> **Related:** [naming.md](./naming.md) · [folder-structure.md](./folder-structure.md) · [git.md](./git.md)

---

## 1. Naming

> Detailed naming conventions are in [naming.md](./naming.md). This section covers the principles.

- Names must reveal intent. A reader should understand purpose without checking the implementation.
- Avoid abbreviations unless universally understood (`id`, `url`, `http`, `db`).
- Longer names are acceptable when they improve clarity. `getUserByEmail` is better than `getUsr`.
- Boolean names should read as assertions: `isActive`, `hasPermission`, `canDelete`.
- Avoid generic names: `data`, `info`, `item`, `result`, `temp`, `thing`, `stuff`.

---

## 2. Formatting

### Indentation

- Use the indentation style standard for the project's language (spaces or tabs). Be consistent within the project.
- Configure the formatter (Prettier, Black, gofmt, etc.) in the project root and enforce it in CI.

### Line Length

- Soft limit: 80 characters. Hard limit: 120 characters.
- Break long lines at logical points (after operators, after commas, before dot chains).

### Vertical Spacing

- Separate logical sections within a function with a single blank line.
- Use two blank lines between top-level declarations (classes, functions, constants).
- No trailing blank lines at the end of files. Ensure a single newline at EOF.

### Horizontal Spacing

- One space after commas, colons, and semicolons.
- One space around binary operators (`=`, `+`, `===`, `&&`).
- No space inside parentheses, brackets, or braces: `fn(a, b)`, not `fn( a, b )`.

### File Organization

```
1. Imports / Dependencies (grouped: stdlib → external → internal)
2. Constants and Type Definitions
3. Main exports / Public API
4. Private / Helper functions
5. Module-level side effects (if any — minimize these)
```

---

## 3. Comments

### When to Comment

- **Do** comment on WHY, not WHAT. The code shows what happens. Comments explain why.
- **Do** comment on non-obvious business rules, workarounds, and constraints.
- **Do** mark temporary solutions: `// HACK:`, `// TODO:`, `// FIXME:` with ticket references.
- **Do not** comment obvious code: `i++ // increment i` adds noise.
- **Do not** leave commented-out code in the codebase. Use version control.

### Comment Format

```
// Single-line comments for brief inline notes.

/**
 * Multi-line comments for function/class documentation.
 * Explain purpose, parameters, return values, and exceptions.
 */

// TODO(TICKET-123): Refactor when the new auth module is ready.
// FIXME(TICKET-456): Race condition under high concurrency — needs mutex.
// HACK: Workaround for library bug in v3.2.1. Remove after upgrade.
```

---

## 4. Functions

### Design Rules

- A function should do one thing and do it well. If you need "and" to describe it, split it.
- Maximum function length: ~30 lines of logic (excluding comments and blank lines). If longer, extract subfunctions.
- Maximum parameters: 3. If more are needed, use an options/config object.
- Return early to avoid deep nesting. Guard clauses at the top.
- Avoid side effects in functions that return values. Separate queries (return data) from commands (perform actions).

### Function Structure

```
function doSomething(input: ValidatedInput): Result {
  // 1. Guard clauses / early returns
  if (!input.isValid) return Result.error("Invalid input");

  // 2. Core logic
  const processed = transform(input);

  // 3. Return
  return Result.success(processed);
}
```

---

## 5. Classes

### Design Rules

- A class should represent a single concept with cohesive data and behavior.
- Prefer composition over inheritance. Use inheritance only for "is-a" relationships.
- Keep the public API surface small. Make everything private/internal by default.
- Constructor should only assign dependencies. Do not perform I/O or heavy computation in constructors.
- Static methods should be pure functions. If they need instance state, they should not be static.

### Class Structure

```
class OrderService {
  // 1. Private fields
  // 2. Constructor (dependency injection)
  // 3. Public methods (API surface)
  // 4. Private methods (internal logic)
}
```

---

## 6. Error Handling

### Rules

- Handle errors at the appropriate level. Do not catch exceptions just to re-throw them unchanged.
- Use typed/structured errors, not string messages. Include error codes, context, and suggested actions.
- Never swallow errors silently. Log them at minimum.
- Distinguish between recoverable errors (retry, fallback) and fatal errors (crash with diagnostic info).
- Validate inputs at system boundaries. Do not scatter defensive null checks throughout business logic.

### Error Structure

```
{
  "code": "PAYMENT_DECLINED",
  "message": "The payment method was declined by the issuing bank.",
  "details": { "reason": "insufficient_funds" },
  "timestamp": "2025-01-15T10:30:00Z",
  "requestId": "req_abc123"
}
```

### Anti-Patterns

- `catch (e) {}` — swallowing errors.
- `catch (e) { throw e }` — pointless re-throw.
- `throw new Error("something went wrong")` — vague, unactionable.
- Using exceptions for control flow (e.g., throwing to indicate "not found").

---

## 7. Logging

### Log Levels

| Level   | Use When                                                    |
| ------- | ----------------------------------------------------------- |
| `error` | Operation failed and requires attention. Includes stack trace.|
| `warn`  | Unexpected situation that was handled, but may indicate a problem. |
| `info`  | Significant business events: user registered, payment processed, deploy completed. |
| `debug` | Detailed information for diagnosing issues. Not enabled in production by default. |

### Logging Rules

- Use structured logging (JSON format with consistent fields).
- Always include: `timestamp`, `level`, `message`, `requestId` / `correlationId`.
- Never log sensitive data: passwords, tokens, PII, credit card numbers.
- Log at function boundaries (entry/exit of significant operations), not inside tight loops.
- Include enough context to debug without reproducing: input parameters, result status, elapsed time.

---

## 8. Testing

### Test Naming

- Test names should describe behavior: `should_return_404_when_user_not_found`.
- Use the pattern: `should_[expected behavior]_when_[condition]`.

### Test Structure (Arrange-Act-Assert)

```
test("should calculate total with discount applied", () => {
  // Arrange
  const cart = createCart({ items: [item1, item2], discount: 0.1 });

  // Act
  const total = calculateTotal(cart);

  // Assert
  expect(total).toBe(90);
});
```

### Testing Rules

- Test behavior, not implementation. Tests should not break when internal refactoring occurs.
- Each test should be independent. No shared mutable state between tests.
- Aim for high coverage of business logic. Do not chase 100% coverage — focus on critical paths and edge cases.
- Mock external dependencies (APIs, databases, file system). Do not mock internal implementation details.
- Keep tests fast. If a test takes > 1 second, it likely belongs in the integration test suite.

---

## 9. Documentation

### Code Documentation Rules

- Every public function, class, and module should have a doc comment explaining its purpose.
- Document parameters, return values, thrown exceptions, and usage examples for complex APIs.
- Keep documentation close to the code. External docs go stale; inline docs are more likely to be updated.
- Use the documentation format standard for the project's language (JSDoc, docstrings, GoDoc, XML docs).

### README Standards

Every module or package should have a README with:
1. What it does (one paragraph).
2. How to install/set up.
3. How to use (code example).
4. How to test.
5. Key design decisions or constraints.

---

## 10. Checklist

Before submitting any code:

- [ ] All names are descriptive and follow [naming.md](./naming.md) conventions.
- [ ] Code is formatted with the project's automated formatter.
- [ ] No commented-out code remains.
- [ ] Functions are ≤ 30 lines and have ≤ 3 parameters.
- [ ] Error handling is explicit — no swallowed exceptions.
- [ ] Logging uses structured format with appropriate levels.
- [ ] Tests follow Arrange-Act-Assert and test behavior, not implementation.
- [ ] Public APIs have documentation comments.
- [ ] No hardcoded values — use constants or configuration.
- [ ] No sensitive data in logs, comments, or error messages.

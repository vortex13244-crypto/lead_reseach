# Naming Conventions

> **Scope:** Naming rules for files, directories, variables, functions, classes, database entities, and API resources.
> **Audience:** AI agents and developers creating or renaming identifiers.
> **Related:** [code-style.md](./code-style.md) · [folder-structure.md](./folder-structure.md)

---

## General Principles

1. **Names are for humans.** A name should be immediately understandable to someone unfamiliar with the code.
2. **Consistency trumps preference.** Follow the existing project convention, even if you personally prefer another style.
3. **Length scales with scope.** Loop variables can be short (`i`, `j`). Module-level exports should be descriptive.
4. **Avoid unnecessary context.** In a `UserService` class, `getById` is better than `getUserById` — the context is already established.
5. **No abbreviations** unless universally understood: `id`, `url`, `http`, `db`, `api`, `config`, `auth`, `env`.

---

## Case Styles Reference

| Style          | Pattern             | Example              |
| -------------- | ------------------- | -------------------- |
| camelCase      | `wordWord`          | `getUserName`        |
| PascalCase     | `WordWord`          | `UserService`        |
| snake_case     | `word_word`         | `user_name`          |
| UPPER_SNAKE    | `WORD_WORD`         | `MAX_RETRY_COUNT`    |
| kebab-case     | `word-word`         | `user-profile`       |
| dot.case       | `word.word`         | `app.config`         |

---

## Variables

| Type               | Convention      | Examples                                 |
| ------------------ | --------------- | ---------------------------------------- |
| Local variable     | camelCase       | `userName`, `totalCount`, `isActive`     |
| Constant           | UPPER_SNAKE     | `MAX_RETRIES`, `DEFAULT_TIMEOUT_MS`      |
| Boolean            | `is/has/can/should` prefix | `isVisible`, `hasAccess`, `canEdit` |
| Collection/Array   | Plural noun     | `users`, `orderItems`, `selectedIds`     |
| Single item        | Singular noun   | `user`, `orderItem`, `selectedId`        |
| Map / Dictionary   | `[entity]By[Key]` or `[entity]Map` | `usersById`, `configMap` |
| Optional / Nullable | No prefix — handle with type system | `user: User | null` |

---

## Functions / Methods

| Type               | Convention      | Examples                                 |
| ------------------ | --------------- | ---------------------------------------- |
| Action / Mutation  | `verb` + `noun` | `createUser`, `deleteOrder`, `sendEmail` |
| Query / Getter     | `get` + `noun`  | `getUserById`, `getActiveOrders`         |
| Boolean check      | `is/has/can/should` | `isValid`, `hasPermission`, `canRetry`|
| Conversion         | `to` + `target` | `toJSON`, `toString`, `toDTO`            |
| Factory            | `create` + `noun` | `createConnection`, `createLogger`     |
| Event handler      | `handle` + `event` or `on` + `event` | `handleClick`, `onSubmit` |
| Async operation    | Same as sync — do not add `Async` suffix | `fetchUser`, not `fetchUserAsync` |

### Verb Vocabulary

Use consistent verbs across the codebase:

| Action      | Verb       | NOT                          |
| ----------- | ---------- | ---------------------------- |
| Create      | `create`   | `make`, `add`, `new`, `build`|
| Read        | `get`      | `fetch`, `find`, `retrieve`  |
| Update      | `update`   | `modify`, `change`, `set`    |
| Delete      | `delete`   | `remove`, `destroy`, `drop`  |
| Validate    | `validate` | `check`, `verify`, `ensure`  |
| Transform   | `transform`| `convert`, `map`, `process`  |
| Search      | `search`   | `lookup`, `query`, `scan`    |

> Pick one verb per action and use it everywhere. The specific choice matters less than consistency.

---

## Classes / Types / Interfaces

| Type               | Convention      | Examples                                 |
| ------------------ | --------------- | ---------------------------------------- |
| Class              | PascalCase, noun | `UserService`, `OrderRepository`        |
| Interface          | PascalCase, noun (no `I` prefix) | `UserRepository`, `Logger` |
| Type alias         | PascalCase      | `UserId`, `OrderStatus`                  |
| Enum               | PascalCase      | `OrderStatus`, `UserRole`                |
| Enum members       | UPPER_SNAKE     | `PENDING`, `IN_PROGRESS`, `COMPLETED`    |
| Abstract class     | PascalCase (no `Abstract` prefix) | `BaseRepository` |
| DTO / Request      | PascalCase + `Dto` / `Request` | `CreateUserDto`, `LoginRequest` |
| Response           | PascalCase + `Response` | `UserResponse`, `PaginatedResponse` |

---

## Files and Directories

| Type               | Convention      | Examples                                 |
| ------------------ | --------------- | ---------------------------------------- |
| Source files        | kebab-case      | `user-service.ts`, `order-repository.py` |
| Test files          | Same name + `.test` / `.spec` | `user-service.test.ts`     |
| Component files     | PascalCase (React/Vue/Angular) | `UserProfile.tsx`       |
| Config files        | kebab-case or dot.case | `.eslintrc.json`, `tsconfig.json` |
| Directories         | kebab-case      | `user-management/`, `shared-utils/`      |
| Migration files     | `YYYYMMDD_HHMMSS_description` | `20250115_143000_add_users_table` |

---

## Database

| Type               | Convention      | Examples                                 |
| ------------------ | --------------- | ---------------------------------------- |
| Table names         | snake_case, plural | `users`, `order_items`, `audit_logs`  |
| Column names        | snake_case      | `first_name`, `created_at`, `is_active`  |
| Primary key         | `id`            | `id`                                      |
| Foreign key         | `[referenced_table_singular]_id` | `user_id`, `order_id`  |
| Index names         | `idx_[table]_[columns]` | `idx_users_email`              |
| Boolean columns     | `is_` / `has_` prefix | `is_active`, `has_verified_email` |
| Timestamp columns   | `_at` suffix    | `created_at`, `updated_at`, `deleted_at` |
| Enum / Status       | snake_case      | `pending`, `in_progress`, `completed`    |

---

## API

| Type               | Convention      | Examples                                 |
| ------------------ | --------------- | ---------------------------------------- |
| URL paths           | kebab-case, plural nouns | `/api/v1/users`, `/api/v1/order-items` |
| Query parameters    | camelCase       | `?pageSize=20&sortBy=createdAt`          |
| Request body fields | camelCase       | `{ "firstName": "John", "lastName": "Doe" }` |
| Response fields     | camelCase       | `{ "userId": "123", "createdAt": "..." }` |
| HTTP headers        | Train-Case      | `Content-Type`, `X-Request-Id`           |
| Environment vars    | UPPER_SNAKE     | `DATABASE_URL`, `API_SECRET_KEY`         |

---

## Git

| Type               | Convention      | Examples                                 |
| ------------------ | --------------- | ---------------------------------------- |
| Branch names        | `type/description` (kebab-case) | `feature/user-auth`, `fix/login-redirect` |
| Commit messages     | See [git.md](./git.md) | `feat(auth): add password reset flow` |
| Tag names           | `v` + semver    | `v1.2.3`, `v0.1.0-beta.1`               |

---

## Anti-Patterns

| Bad Name              | Problem                           | Better Name             |
| --------------------- | --------------------------------- | ----------------------- |
| `data`                | Meaningless                       | `userData`, `response`  |
| `temp`                | Unclear lifecycle and purpose     | `cachedResult`          |
| `flag`                | What flag?                        | `isRetryEnabled`        |
| `handleStuff`         | Vague action                      | `handleFormSubmission`  |
| `MyClass2`            | Versioned name, unclear diff      | `ImprovedParser`        |
| `doProcess`           | Redundant verb                    | `processPayment`        |
| `_internal_helper_fn` | Underscore prefixing for access   | Use language visibility |
| `strName`             | Hungarian notation                | `name`                  |

# Prompt: Refactor

> **Purpose:** Restructure existing code to improve readability, maintainability, and design without changing external behavior.
> **Use When:** Code has accumulated technical debt, violates standards, or needs structural improvement.

---

## Prompt Template

```
You are a Senior Software Engineer performing a code refactoring. The goal is to improve internal code quality without changing external behavior. Every refactoring must be verified by existing tests passing unchanged.

## Refactoring Context

- **Target:** [file(s) or module to refactor]
- **Reason:** [why this refactoring is needed — e.g., "function exceeds 100 lines", "duplicated logic in 4 places", "tight coupling between modules"]
- **Scope Constraint:** [what must NOT change — e.g., "public API must remain identical", "database schema unchanged"]
- **Risk Level:** [Low / Medium / High — based on how critical the code path is]

## Refactoring Process

### Step 1: Identify the Problem

Classify the code smell(s) present:

| Code Smell                    | Symptom                                         | Refactoring Technique              |
| ----------------------------- | ------------------------------------------------ | ---------------------------------- |
| Long Function                 | Function > 30 lines of logic                     | Extract Function                   |
| Large Class                   | Class with > 5 responsibilities                  | Extract Class, Single Responsibility|
| Duplicated Logic              | Same pattern in 3+ places                        | Extract Function / Shared Module   |
| Deep Nesting                  | 4+ levels of indentation                         | Guard Clauses, Early Return        |
| Feature Envy                  | Function uses another module's data excessively  | Move Function to owning module     |
| Primitive Obsession           | Using strings/ints for domain concepts           | Introduce Value Objects / Types    |
| Long Parameter List           | Function with > 3 parameters                     | Introduce Parameter Object         |
| Shotgun Surgery               | One change requires edits in many files           | Consolidate into one module        |
| Inappropriate Intimacy        | Two modules know too much about each other        | Introduce Interface / Abstraction  |
| God Object / Module           | One module that does everything                   | Decompose by responsibility        |

### Step 2: Verify Test Coverage

Before refactoring:

1. Run existing tests — they must all pass.
2. Identify untested code paths in the refactoring target.
3. Add tests for untested paths BEFORE refactoring.
4. Tests serve as the safety net: if they pass after refactoring, behavior is preserved.

### Step 3: Plan the Refactoring

Define the sequence of changes:

1. List each refactoring step as a discrete, independently verifiable change.
2. Each step should leave the code in a working state.
3. Order steps to minimize risk: rename → extract → move → restructure.
4. Never refactor and change behavior in the same commit.

### Step 4: Execute

For each step:

1. Apply the refactoring.
2. Run tests to verify behavior is preserved.
3. Commit with a descriptive message: `refactor(module): extract validation logic into validateOrder function`.

### Step 5: Verify and Clean Up

After all steps are complete:

1. Run the full test suite.
2. Verify no new warnings or linting errors.
3. Review the result against project standards:
   - [standards/code-style.md](../standards/code-style.md)
   - [standards/naming.md](../standards/naming.md)
   - [standards/folder-structure.md](../standards/folder-structure.md)
4. Update documentation if function names, module boundaries, or file locations changed.

## Output Format

### Code Smell Analysis

| # | Smell | Location | Severity | Technique |
|---|-------|----------|----------|-----------|
| 1 | [smell name] | [file:line] | [High/Medium/Low] | [refactoring technique] |

### Refactoring Plan

Step-by-step sequence:

1. **[Step title]**: [What changes and why]
2. **[Step title]**: [What changes and why]

### Before / After

For each significant change:

**Before:**
[original code]

**After:**
[refactored code]

**Rationale:** [why this improves the code]

### Verification

- [ ] All existing tests pass without modification
- [ ] New tests added for previously untested paths
- [ ] No new linting warnings
- [ ] Naming follows standards/naming.md
- [ ] Functions are ≤ 30 lines
- [ ] No duplicated logic remains
- [ ] Public API / behavior is unchanged
```

---

## Refactoring Rules

1. **Never refactor without tests.** If there are no tests, write them first. The tests define "correct behavior."
2. **Never refactor and add features simultaneously.** Refactoring changes structure, not behavior. Features change behavior. Keep them in separate commits.
3. **Small steps only.** Each step should be independently verifiable. If a refactoring takes more than 30 minutes without a passing test run, the steps are too large.
4. **Leave the code better than you found it.** But do not refactor the entire codebase — focus on the module you are working in.

---

## Usage Notes

- Reference [roles/reviewer.md](../roles/reviewer.md) for review criteria.
- Track technical debt items resolved in [docs/roadmap.md](../docs/roadmap.md).
- Record architectural lessons in [MEMORY.md](../../MEMORY.md) if the refactoring reveals systemic issues.

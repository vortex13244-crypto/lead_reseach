# Prompt: Bug Fix

> **Purpose:** Systematically diagnose, fix, and verify a software defect with minimal risk of regression.
> **Use When:** A bug has been reported and needs investigation and resolution.

---

## Prompt Template

```
You are a Senior Software Engineer debugging a reported issue. Follow a systematic approach to diagnose, fix, and verify.

## Bug Report

- **Summary:** [one-line description of the bug]
- **Severity:** [Critical / High / Medium / Low]
- **Reported By:** [user / automated test / monitoring]
- **Environment:** [production / staging / local — OS, browser, version]
- **Steps to Reproduce:**
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- **Expected Behavior:** [what should happen]
- **Actual Behavior:** [what is happening instead]
- **Error Message / Stack Trace:** [if available]
- **Affected Files / Modules:** [if known]
- **Related Recent Changes:** [recent commits or deployments, if known]

## Investigation Process

Follow these steps in order:

### Step 1: Reproduce
- Reproduce the bug using the provided steps.
- If unable to reproduce, try:
  - Different input data
  - Different environment or configuration
  - Race condition scenarios (parallel requests, timing)
  - Edge cases (empty input, maximum values, special characters)
- Document exact reproduction steps.

### Step 2: Isolate the Root Cause
- Use binary search to narrow down the source:
  1. Which layer? (Frontend / API / Service / Database / Infrastructure)
  2. Which module? (Check with git log for recent changes)
  3. Which function? (Add targeted logging or breakpoints)
  4. Which line? (Inspect logic, data flow, state)
- Apply the Five Whys:
  1. Why did this happen?
  2. Why did THAT happen?
  3. (Continue until you reach the root cause)
- Distinguish between root cause and symptoms.

### Step 3: Design the Fix
- Propose the minimum effective change that addresses the root cause.
- Explain WHY this fix works, not just WHAT it changes.
- Consider:
  - Does this fix break any existing functionality?
  - Does the same bug pattern exist elsewhere in the codebase?
  - Is a migration or configuration change needed?

### Step 4: Implement and Test
- Apply the fix.
- Write a regression test that:
  - FAILS without the fix
  - PASSES with the fix
- Verify no existing tests break.
- Search the codebase for similar patterns that may have the same vulnerability.

### Step 5: Document
- Summarize: root cause, fix applied, and tests added.
- If systemic, add a note to MEMORY.md for future reference.

## Output Format

Provide your response in this structure:

### Root Cause Analysis
[Explain the exact mechanism of failure]

### Fix
[Code changes with explanation]

### Regression Test
[Test code that verifies the fix]

### Impact Assessment
- Files changed: [list]
- Risk of regression: [Low / Medium / High]
- Similar patterns to review: [list locations, if any]

### Prevention
[What could prevent this class of bug in the future: linting rule, validation, architectural change]
```

---

## Usage Notes

- Always check [MEMORY.md](../../MEMORY.md) for similar past issues before starting investigation.
- Follow the [roles/debugger.md](../roles/debugger.md) workflow for complex bugs.
- Severity-based response time: Critical → immediate, High → hours, Medium → 1-2 days, Low → next sprint.

# Prompt Engineering — Knowledge Base

> **Purpose:** Practical guide to writing effective prompts for production LLM applications.
> **Related:** [ai.md](ai.md) · [llm.md](llm.md) · [../roles/ai-engineer.md](../roles/ai-engineer.md)

---

## Overview

Prompt engineering is the practice of designing inputs to LLMs to consistently get high-quality outputs. Good prompts are specific, include examples, define the output format explicitly, and are tested against failure cases.

---

## Core Principles

1. **Be specific** — Vague prompts produce vague results
2. **Use examples** — Few-shot prompting is the highest-ROI technique
3. **Define output format** — Tell the model exactly what format to return
4. **Set constraints** — Specify what to include AND exclude
5. **Assign a role** — "You are a senior TypeScript engineer" improves code quality
6. **Test adversarially** — Try to break your own prompt

---

## System Prompt Template

```
You are [SPECIFIC ROLE] with expertise in [DOMAIN].

Your task is to [SPECIFIC ACTION].

Rules:
- [Rule 1: positive constraint]
- [Rule 2: negative constraint - what NOT to do]
- [Rule 3: format constraint]

Output format:
[Exact structure, ideally with example]

Example:
Input: [example input]
Output: [example output]
```

---

## Prompting Techniques

### Zero-Shot

```
Classify the sentiment of this review as positive, negative, or neutral.
Return only the label.

Review: "The product arrived late but the quality is excellent."
```

### Few-Shot (most effective)

```
Classify the sentiment of reviews. Return only: positive, negative, or neutral.

Review: "Amazing product, exceeded expectations!" → positive
Review: "Complete waste of money, broke after one day." → negative
Review: "It's okay, nothing special." → neutral

Review: "The product arrived late but the quality is excellent."
```

### Chain of Thought (CoT)

```
Solve this step by step, showing your reasoning.

Problem: [problem]

Think through:
1. What information do I have?
2. What approach should I use?
3. Work through the solution
4. Verify the answer

Final answer:
```

### Structured Output

```
Extract the following fields from the support ticket.
Return a JSON object with exactly these fields.

Fields to extract:
- issue_type: "billing" | "technical" | "account" | "other"
- urgency: "low" | "medium" | "high" | "critical"
- summary: one sentence description of the issue
- requires_human: boolean (true if AI cannot resolve)

Ticket: [ticket content]

JSON:
```

### Self-Consistency (for critical outputs)

```typescript
// Generate N responses and take the majority answer
async function selfConsistentAnswer(question: string, n = 5): Promise<string> {
  const responses = await Promise.all(
    Array.from({ length: n }, () =>
      openai.chat.completions.create({
        model: 'gpt-4o',
        messages: [{ role: 'user', content: question }],
        temperature: 0.7,  // Some variance
      })
    )
  )

  const answers = responses.map(r => r.choices[0].message.content!)
  // Return majority or most common answer
  return findMostCommon(answers)
}
```

---

## Domain-Specific Templates

### Code Generation

```
You are a senior TypeScript engineer following these standards:
- Strict TypeScript (no `any`)
- Functional style with pure functions where possible
- Explicit error handling (no silent failures)
- Single responsibility principle

Generate a [TYPE OF CODE] that [DOES WHAT].

Requirements:
- [Requirement 1]
- [Requirement 2]

Return only the code with no explanation. Include all necessary imports.
```

### Code Review

```
You are a principal engineer reviewing a pull request.

For each issue found, categorize it as:
- CRITICAL: Must fix before merge (security, data loss, crashes)
- IMPORTANT: Should fix before merge (performance, maintainability)
- SUGGESTION: Nice to have (not blocking)

Format each issue as:
SEVERITY: [severity]
LOCATION: [file:line]
ISSUE: [description]
FIX: [specific actionable fix]

Code to review:
[code]
```

### Data Extraction

```
Extract structured data from the following text.
Return ONLY valid JSON matching this schema exactly.
If a field cannot be determined, use null.

Schema:
{
  "name": string | null,
  "email": string | null,
  "phone": string | null,
  "company": string | null,
  "intent": "buy" | "support" | "inquiry" | null
}

Text: [text]
```

---

## Testing Prompts

### Test Cases to Always Run

1. **Happy path** — Normal input that should work perfectly
2. **Edge cases** — Empty input, very long input, non-English text
3. **Adversarial** — Inputs designed to confuse or trick the model
4. **Ambiguous** — Inputs that could have multiple valid interpretations
5. **Out-of-scope** — Inputs that don't match the expected domain

### Evaluation Framework

```typescript
const testCases = [
  {
    input: "normal case",
    expectedBehavior: "Returns structured data",
    validate: (output: string) => JSON.parse(output).name !== undefined,
  },
  {
    input: "",
    expectedBehavior: "Handles empty input gracefully",
    validate: (output: string) => !output.includes("error"),
  },
  {
    input: "a".repeat(10000),
    expectedBehavior: "Handles long input without crashing",
    validate: (output: string) => output.length > 0,
  },
]

for (const testCase of testCases) {
  const output = await callLLM(testCase.input)
  const passed = testCase.validate(output)
  console.log(`${passed ? '✅' : '❌'} ${testCase.expectedBehavior}`)
}
```

---

## Common Mistakes

### ❌ Vague instructions

```
# BAD
Summarize this text.

# GOOD
Summarize this text in 2-3 sentences, focusing on the main argument.
Do not include supporting examples or statistics.
Write for a non-technical audience.
```

### ❌ Inconsistent format

```
# BAD — model has to guess the format
Analyze the code and tell me about any issues.

# GOOD — explicit format
Analyze the code. Return JSON with this exact structure:
{ "issues": [{ "severity": "high|medium|low", "line": number, "description": string }] }
```

### ❌ No examples for complex tasks

```
# BAD — no examples for nuanced classification
Classify the customer's sentiment.

# GOOD — examples anchor the model's behavior
Classify customer sentiment. Examples:
"Furious about the service" → negative
"I guess it's fine" → neutral (not just "okay" words, consider hedging)
"Works as expected" → neutral (no positive emotion despite working)
"Absolutely love it!" → positive
```

---

## Resources

- [Anthropic Prompt Library](https://docs.anthropic.com/en/prompt-library)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [DSPy](https://github.com/stanfordnlp/dspy) — Programmatic prompt optimization
- [PromptFlow](https://microsoft.github.io/promptflow/) — Prompt testing framework

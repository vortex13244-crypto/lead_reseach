# LLM Product Guide

> **Purpose:** Compact design rules for reliable LLM features. See [AI engineering](ai.md) for implementation patterns.

## Use an LLM when

- Input is natural language or unstructured content.
- A probabilistic answer is acceptable with review, guardrails, or a fallback.
- The benefit is greater than the latency and cost.

## Do not use an LLM when

- A deterministic rule, database lookup, or simple form solves the task.
- An incorrect answer could cause harm without meaningful human oversight.

## Required product decisions

| Decision | Record in the product architecture |
| --- | --- |
| Input and allowed data | What is sent to the provider |
| Output contract | JSON schema or clear response format |
| Fallback | What users see on failure or uncertainty |
| Cost and limits | Budget, rate limit, maximum input |
| Safety | Prompt-injection controls, moderation, human escalation |
| Evaluation | Test cases and success criteria |

Never put credentials, private data, or untrusted instructions into system prompts without deliberate controls.

# Project Context Template

Copy these files into a new product as `.ai/`. They are the small, product-specific context an AI should read first.

## Required files

| File | Why it exists | Update frequency |
| --- | --- | --- |
| `AGENTS.md` | Directs an AI to the right context | Rarely |
| `PROJECT.md` | Product goal, scope and stack | At project start / scope change |
| `active-context.md` | What is being worked on now | Every meaningful session |
| `architecture.md` | Boundaries and important design choices | Architecture change |
| `design-brief.md` | Brand and UI direction | Design change |
| `project-state.md` | Environments, conventions and technical health | After delivery/deploy |

Add `decisions.md` and `known-issues.md` once the project has durable decisions or non-trivial limitations.

Do not put API keys or personal data in these files.

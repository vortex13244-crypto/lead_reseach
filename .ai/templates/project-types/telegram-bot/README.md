# Telegram Bot Profile

Use for customer-support bots, assistants, notifications, lead capture, internal automation, and AI-enabled Telegram products.

## Recommended default

- Python + FastAPI for webhook bots, or a maintained Telegram framework with clear routing.
- PostgreSQL only when state, users, tasks, payments, or history must persist.
- Webhook in production; polling is acceptable for early local development.

## Architecture baseline

```text
Telegram update → webhook/polling adapter → command/message handler
→ service layer → repository/integration → response to Telegram
```

Keep Telegram SDK calls inside the adapter/handler layer; business logic belongs in services.

## Security and reliability

- Store `TELEGRAM_BOT_TOKEN` only in `.env`; never log it.
- Verify Telegram webhook secret token in production.
- Check user/chat authorization for privileged commands.
- Make update handling idempotent; Telegram can retry webhook delivery.
- Set timeouts and retries for external APIs and AI calls.
- Rate-limit expensive commands and provide safe fallback messages.

## Context additions

Add these to `.ai/architecture.md`:

| Item | Record |
| --- | --- |
| Commands | Command, audience, expected outcome |
| Update mode | Polling or webhook and why |
| State | What data is stored and retention policy |
| Permissions | Admins, allowed chats, ownership rules |
| Integrations | APIs, timeouts, retry policy |

Add `TELEGRAM_BOT_TOKEN=` and `TELEGRAM_WEBHOOK_SECRET=` to the product's `.env.example`, with empty values.

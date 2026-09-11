# Project Overview

> **Purpose:** Universal project description template. Provides AI agents with essential context about the project at a glance.
> **How to Use:** Fill in all sections when starting a new project. Update as the project evolves.
> **Related:** [INDEX.md](INDEX.md) · [vision](CORE/docs/vision.md) · [architecture](CORE/docs/architecture.md)

---

## Identity

| Attribute          | Value                                      |
| ------------------ | ------------------------------------------ |
| Project Name       | CRM Analyst / Lead Collector Bot           |
| Repository         | vortex13244-crypto/Lead_reseach            |
| Description        | A Telegram bot for collecting and searching lead data (companies, Instagrams, locations) using DuckDB over S3. |
| Type               | Telegram Bot (Python)                      |
| Status             | Active Development                         |
| Created            | 2026-07-31                                 |
| Primary Language   | Python                                     |
| License            | Proprietary                                |

---

## Quick Start

### Prerequisites

- Python 3.10+
- `pip`
- Valid `.env` з ключами AWS S3 та токеном Telegram-бота.

### Setup

```bash
# Встановлення залежностей
pip install -r requirements.txt

# Запуск бота
python bot.py
```

---

## Architecture Summary

| Aspect            | Value                                      |
| ----------------- | ------------------------------------------ |
| Architecture      | Monolith (Telegram Bot)                    |
| Frontend          | Telegram UI                                |
| Backend           | Python (aiogram)                           |
| Database          | DuckDB (in-memory, querying remote Parquet files on S3) |
| Hosting           | Local / VM                                 |

---

## Key Directories

| Directory           | Purpose                                    |
| ------------------- | ------------------------------------------ |
| `handlers/`         | Обробники повідомлень та колбеків Telegram |
| `services/`         | Бізнес-логіка (наприклад, `lead_pipeline.py`) |
| `.ai/`              | AI knowledge base (пам'ять і правила для мене) |

---

## Scaling Hints & Future Architecture (Підказки для масштабування)

- **Черги задач (Task Queues):** Зараз бот виконує запити синхронно і може блокуватись (хоч ми й додали таймаути). Для повноцінного масштабування (наприклад, пошуку сотень тисяч компаній) потрібно додати **Celery + Redis** або `arq`. Бот повинен приймати запит, відправляти його в чергу і надсилати користувачу повідомлення "Ваш звіт генерується...".
- **База даних:** DuckDB, яка читає Parquet з S3 — супер рішення для швидкого старту. Але якщо обсяг даних виросте до Терабайтів і знадобляться складні фільтри + сортування, архітектуру варто змінити на повноцінну OLAP-базу (наприклад, **ClickHouse**) або хоча б партиційований PostgreSQL. 
- **Пагінація та Кешування:** Для Telegram є обмеження на довжину повідомлень. Варто кешувати часті запити (наприклад "всі автосервіси США") в локальному кеші DuckDB або Redis, щоб не смикати S3 щоразу.

---

## Conventions

- **Code Style:** PEP 8.
- **Асинхронність:** Коректне використання `asyncio` та `aiogram`. Важкі запити до DuckDB бажано запускати в окремих пулах потоків (`asyncio.to_thread`), щоб не блокувати Event Loop бота.

---

## Known Issues & Constraints

| Issue / Constraint                    | Impact                 | Workaround / Status            |
| ------------------------------------- | ---------------------- | ------------------------------ |
| S3 Remote Query Slowdown              | High                   | **НЕ ВИКОРИСТОВУВАТИ `ORDER BY`** у DuckDB при запитах до S3, інакше викачується весь файл. Сортування робити локально в Python. |
| Telegram API Timeouts                 | High                   | Використовуються суворі 5-хвилинні таймаути всередині запитів, щоб уникнути крашу бота. |

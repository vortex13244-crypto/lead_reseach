# Python — Knowledge Base

> **Purpose:** Python best practices, patterns, and tooling for production systems.
> **Version:** Python 3.11+
> **Related:** [fastapi.md](fastapi.md) · [postgres.md](postgres.md) · [ai.md](ai.md)

---

## Overview

Python is used in this workspace for backend APIs (FastAPI), AI/ML pipelines, data processing scripts, and automation. Always use Python 3.11+ for better performance and modern type syntax.

---

## Best Practices

### Type Annotations (Always)

```python
# Always annotate function signatures
def calculate_discount(price: float, discount_percent: float) -> float:
    if discount_percent > 100:
        raise ValueError("Discount cannot exceed 100%")
    return price * (1 - discount_percent / 100)

# Use new-style union types (Python 3.10+)
def get_user(user_id: str) -> User | None:
    ...

# Annotate class attributes
class UserService:
    db: AsyncSession
    cache: Redis

    def __init__(self, db: AsyncSession, cache: Redis) -> None:
        self.db = db
        self.cache = cache
```

### Pydantic for Validation

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_settings import BaseSettings

# Request/response models
class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=12)

    @field_validator('name')
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()

# Settings from environment
class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=True)

settings = Settings()
```

### Async/Await

```python
import asyncio
import httpx

# Always async for I/O-bound operations
async def fetch_user_data(user_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        response.raise_for_status()
        return response.json()

# Parallel async operations
async def get_dashboard_data(user_id: str) -> tuple:
    user, posts, stats = await asyncio.gather(
        get_user(user_id),
        get_user_posts(user_id),
        get_user_stats(user_id),
    )
    return user, posts, stats
```

### Error Handling

```python
# Custom exceptions
class AppError(Exception):
    """Base application error"""
    def __init__(self, message: str, code: str = "APP_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, resource: str) -> None:
        super().__init__(f"{resource} not found", "NOT_FOUND")

class ValidationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message, "VALIDATION_ERROR")

# Usage
async def get_user(user_id: str) -> User:
    user = await user_repo.find_by_id(user_id)
    if not user:
        raise NotFoundError("User")
    return user
```

### Logging

```python
import structlog

logger = structlog.get_logger(__name__)

async def create_order(user_id: str, items: list[OrderItem]) -> Order:
    logger.info("Creating order", user_id=user_id, item_count=len(items))
    
    try:
        order = await order_repo.create(user_id, items)
        logger.info("Order created", order_id=order.id, user_id=user_id)
        return order
    except Exception as e:
        logger.error("Failed to create order", user_id=user_id, error=str(e))
        raise
```

---

## Architecture Patterns

### Repository Pattern

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None: ...
    
    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...
    
    @abstractmethod
    async def create(self, data: CreateUserData) -> User: ...

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_by_id(self, user_id: str) -> User | None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()
```

### Context Managers for Resources

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_redis():
    client = await aioredis.create_redis_pool(settings.REDIS_URL)
    try:
        yield client
    finally:
        client.close()
        await client.wait_closed()

# Usage
async with get_redis() as redis:
    await redis.set("key", "value", expire=300)
```

---

## Tooling

```bash
# Package manager: uv (fast) or poetry
uv add fastapi  # Install
uv run python main.py  # Run

# Type checking
mypy src/ --strict

# Linting + formatting
ruff check src/
ruff format src/

# Testing
pytest tests/ -v --cov=src

# Security
pip-audit
```

---

## Common Mistakes

### ❌ Mutable default arguments

```python
# WRONG — shared across all calls
def add_item(items: list = []):
    items.append("new")
    return items

# RIGHT
def add_item(items: list | None = None) -> list:
    if items is None:
        items = []
    items.append("new")
    return items
```

### ❌ Bare except clauses

```python
# WRONG — catches SystemExit, KeyboardInterrupt, etc.
try:
    do_something()
except:
    pass

# RIGHT — be specific
try:
    do_something()
except ValueError as e:
    logger.warning("Validation failed", error=str(e))
except httpx.RequestError as e:
    logger.error("Network request failed", error=str(e))
    raise
```

---

## Resources

- [Python 3.11 Docs](https://docs.python.org/3.11/)
- [Pydantic v2](https://docs.pydantic.dev/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [structlog](https://www.structlog.org/)
- [ruff](https://docs.astral.sh/ruff/)

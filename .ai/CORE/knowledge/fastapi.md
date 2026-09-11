# FastAPI — Knowledge Base

> **Purpose:** FastAPI best practices, patterns, and common pitfalls.
> **Version:** FastAPI 0.110+, Python 3.11+
> **Related:** [python.md](python.md) · [postgres.md](postgres.md) · [../docs/api.md](../docs/api.md)

---

## Overview

FastAPI is the preferred Python web framework for API services in this workspace. It provides automatic OpenAPI documentation, async support, and Pydantic integration out of the box.

---

## Best Practices

### Project Structure

```
src/
├── main.py                  # FastAPI app entry point
├── config.py                # Settings with Pydantic Settings
├── database.py              # DB engine and session setup
├── api/
│   ├── deps.py              # Shared dependencies (auth, db session)
│   └── v1/
│       ├── router.py        # Include all routers
│       ├── users/
│       │   ├── router.py    # User endpoints
│       │   ├── schemas.py   # Pydantic request/response models
│       │   └── service.py   # Business logic
│       └── auth/
│           ├── router.py
│           └── service.py
├── models/
│   └── user.py              # SQLAlchemy models
├── repositories/
│   └── user_repository.py   # Database access layer
└── core/
    ├── security.py          # JWT, password hashing
    ├── exceptions.py        # Custom exception classes
    └── middleware.py        # Request logging, CORS, etc.
```

### App Setup

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from api.v1.router import api_router
from config import settings
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Startup: run migrations, warmup connections
    yield
    # Shutdown: cleanup connections

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else None,  # Disable in production
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Never use ["*"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(api_router, prefix="/api/v1")
```

### Pydantic Schemas

```python
# schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100, strip_whitespace=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=12, max_length=128)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)

class UserResponse(UserBase):
    id: str
    created_at: datetime
    role: UserRole

    model_config = ConfigDict(from_attributes=True)  # Works with SQLAlchemy models

class PaginatedResponse(BaseModel):
    data: list[UserResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
```

### Router Pattern

```python
# api/v1/users/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, get_current_user
from . import schemas, service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    user = await service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
) -> User:
    if await service.user_exists(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    return await service.create_user(db, data)
```

### Dependencies

```python
# api/deps.py
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = verify_token(token)  # Raises if invalid
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user = await get_user_by_id(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user
```

---

## Architecture

### Layered Architecture

```
HTTP Request
    ↓
[Router] — path params, query params, response model
    ↓
[Service] — business logic, orchestration
    ↓
[Repository] — database access only
    ↓
[SQLAlchemy] → PostgreSQL
```

---

## Common Mistakes

### ❌ Business logic in routers

```python
# WRONG
@router.post("/users")
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed = bcrypt.hash(data.password)  # Logic belongs in service
    user = User(email=data.email, password_hash=hashed)
    db.add(user)
    await db.commit()
    return user
```

### ❌ Sync functions in async context

```python
# WRONG — blocks event loop
@router.get("/users")
async def get_users():
    time.sleep(1)  # Blocks ALL requests!
    return []

# RIGHT
@router.get("/users")
async def get_users():
    await asyncio.sleep(1)
    return []
```

---

## Performance Tips

1. Use `async` everywhere — blocking calls will kill throughput
2. Use `asyncpg` driver for PostgreSQL (not `psycopg2`)
3. Enable connection pooling in SQLAlchemy (`pool_size=20`)
4. Use `BackgroundTasks` for non-blocking operations (emails, analytics)
5. Add response compression with `GZipMiddleware`
6. Use `select()` to load only needed columns from DB

---

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [Full-Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template)

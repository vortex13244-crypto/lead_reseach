# Snippet: FastAPI Routes

> **Purpose:** Production-ready FastAPI route patterns.
> **Related:** [../knowledge/fastapi.md](../knowledge/fastapi.md) · [../docs/api.md](../docs/api.md)

---

## Complete CRUD Router

```python
# src/api/v1/users/router.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, get_current_user, require_admin
from models.user import User
from . import schemas
from . import service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=schemas.UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    """Get the authenticated user's profile."""
    return current_user

@router.get(
    "/",
    response_model=schemas.PaginatedUsersResponse,
    dependencies=[Depends(require_admin)],
)
async def list_users(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 20,
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> schemas.PaginatedUsersResponse:
    """List all users. Admin only."""
    users, total = await service.list_users(db, page=page, per_page=per_page, search=search)
    return schemas.PaginatedUsersResponse(
        data=users,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=(total + per_page - 1) // per_page,
    )

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """Get a user by ID. Users can only view their own profile; admins can view any."""
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    user = await service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.patch("/me", response_model=schemas.UserResponse)
async def update_me(
    data: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """Update the authenticated user's profile."""
    return await service.update_user(db, current_user.id, data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a user. Users can delete their own account; admins can delete any."""
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    deleted = await service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
```

---

## Authentication Routes

```python
# src/api/v1/auth/router.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db
from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from . import schemas, service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=schemas.TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> schemas.TokenResponse:
    """Authenticate with email and password."""
    user = await service.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return schemas.TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        token_type="bearer",
        expires_in=900,  # 15 minutes
    )

@router.post("/refresh", response_model=schemas.TokenResponse)
async def refresh_tokens(data: schemas.RefreshRequest) -> schemas.TokenResponse:
    """Exchange refresh token for new access + refresh tokens."""
    user_id = verify_refresh_token(data.refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    return schemas.TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),  # Token rotation
        token_type="bearer",
        expires_in=900,
    )

@router.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(data: schemas.SignupRequest, db: AsyncSession = Depends(get_db)):
    """Create a new user account."""
    if await service.user_exists(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )
    return await service.create_user(db, data)
```

---

## Background Task Pattern

```python
from fastapi import BackgroundTasks

@router.post("/users", response_model=schemas.UserResponse, status_code=201)
async def create_user(
    data: schemas.UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await service.create_user(db, data)

    # Non-blocking: runs after response is sent
    background_tasks.add_task(send_welcome_email, user.email, user.name)
    background_tasks.add_task(track_signup_event, user.id)

    return user
```

---

## Error Handling (Global Handler)

```python
# main.py
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    status_map = {
        "NOT_FOUND": 404,
        "FORBIDDEN": 403,
        "UNAUTHORIZED": 401,
        "VALIDATION_ERROR": 422,
        "CONFLICT": 409,
    }
    return JSONResponse(
        status_code=status_map.get(exc.code, 500),
        content={"error": {"code": exc.code, "message": exc.message}},
    )

@app.exception_handler(PydanticValidationError)
async def validation_error_handler(request: Request, exc: PydanticValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        },
    )
```

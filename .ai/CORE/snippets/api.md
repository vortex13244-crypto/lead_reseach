# Snippet: API Contract

> **Purpose:** A compact starting point for a documented, safe API route. Adapt it to the product; do not copy credentials or example URLs into production.

## Contract before implementation

| Item | Define |
| --- | --- |
| Endpoint and method | `POST /api/v1/resource` |
| Authentication | Public / user / admin |
| Input validation | Zod or Pydantic schema |
| Success response | Status and JSON shape |
| Error responses | Validation, auth, not found, conflict |
| Idempotency | Required for retries? |

## FastAPI route shape

```python
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/items", tags=["items"])

class CreateItemRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)

class ItemResponse(BaseModel):
    id: str
    name: str

@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(payload: CreateItemRequest) -> ItemResponse:
    # Authenticate → validate → service → return a stable response contract.
    raise NotImplementedError
```

Before release, complete [backend checklist](../checklists/backend.md) and [security checklist](../checklists/security.md).

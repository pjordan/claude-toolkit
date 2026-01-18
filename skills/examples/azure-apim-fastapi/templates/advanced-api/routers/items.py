"""Items API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4
import logging

from models.context import APIMContext, UserContext
from models.responses import PaginatedResponse
from services.auth import get_apim_context, get_user_context, require_roles

router = APIRouter(prefix="/api/v1/items", tags=["Items"])
logger = logging.getLogger(__name__)


# Request/Response models
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    tags: list[str] = Field(default_factory=list, description="Item tags")


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[list[str]] = None


class Item(BaseModel):
    id: str
    name: str
    description: Optional[str]
    tags: list[str]
    created_at: str
    updated_at: str
    created_by: Optional[str] = None


# Mock data store (replace with actual database)
_items_store: dict[str, Item] = {}


@router.get("", response_model=PaginatedResponse[Item])
async def list_items(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    ctx: APIMContext = Depends(get_apim_context),
):
    """
    List all items with pagination.

    Supports search filtering by name or description.
    """
    logger.info(
        "Listing items",
        extra={
            "correlation_id": ctx.correlation_id,
            "page": page,
            "page_size": page_size,
            "search": search,
        }
    )

    # Filter items
    items = list(_items_store.values())
    if search:
        search_lower = search.lower()
        items = [
            item for item in items
            if search_lower in item.name.lower()
            or (item.description and search_lower in item.description.lower())
        ]

    # Paginate
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_items = items[start:end]

    return PaginatedResponse.create(paginated_items, total, page, page_size)


@router.post("", response_model=Item, status_code=201)
async def create_item(
    item: ItemCreate,
    ctx: APIMContext = Depends(get_apim_context),
    user: UserContext = Depends(get_user_context),
):
    """
    Create a new item.

    Requires authenticated user context from APIM.
    """
    logger.info(
        f"Creating item: {item.name}",
        extra={
            "correlation_id": ctx.correlation_id,
            "user_id": user.user_id,
        }
    )

    now = datetime.utcnow().isoformat() + "Z"
    new_item = Item(
        id=str(uuid4()),
        name=item.name,
        description=item.description,
        tags=item.tags,
        created_at=now,
        updated_at=now,
        created_by=user.user_id,
    )

    _items_store[new_item.id] = new_item
    return new_item


@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: str,
    ctx: APIMContext = Depends(get_apim_context),
):
    """Get a specific item by ID."""
    logger.info(
        f"Getting item: {item_id}",
        extra={"correlation_id": ctx.correlation_id}
    )

    item = _items_store.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: str,
    update: ItemUpdate,
    ctx: APIMContext = Depends(get_apim_context),
    user: UserContext = Depends(get_user_context),
):
    """Update an existing item."""
    logger.info(
        f"Updating item: {item_id}",
        extra={
            "correlation_id": ctx.correlation_id,
            "user_id": user.user_id,
        }
    )

    item = _items_store.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update fields
    update_data = update.model_dump(exclude_unset=True)
    updated_item = item.model_copy(update={
        **update_data,
        "updated_at": datetime.utcnow().isoformat() + "Z",
    })

    _items_store[item_id] = updated_item
    return updated_item


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: str,
    ctx: APIMContext = Depends(get_apim_context),
    user: UserContext = Depends(require_roles("Admin", "Editor")),
):
    """
    Delete an item.

    Requires Admin or Editor role.
    """
    logger.info(
        f"Deleting item: {item_id}",
        extra={
            "correlation_id": ctx.correlation_id,
            "user_id": user.user_id,
        }
    )

    if item_id not in _items_store:
        raise HTTPException(status_code=404, detail="Item not found")

    del _items_store[item_id]

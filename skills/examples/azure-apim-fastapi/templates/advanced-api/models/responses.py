"""Response wrapper models."""

from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, Any

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    data: T
    meta: Optional[dict[str, Any]] = None


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response."""

    data: list[T]
    pagination: PaginationMeta

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int,
        page_size: int
    ) -> "PaginatedResponse[T]":
        """Create a paginated response from items and pagination info."""
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0

        return cls(
            data=items,
            pagination=PaginationMeta(
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_prev=page > 1,
            )
        )

"""Common schemas for pagination and shared types."""
from typing import TypeVar, Generic, List
from pydantic import BaseModel

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str


class ErrorResponse(BaseModel):
    """Error response."""
    detail: str


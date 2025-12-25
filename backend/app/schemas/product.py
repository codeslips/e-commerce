"""Product schemas."""
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class ProductBase(BaseModel):
    """Base product schema."""
    name: str
    category: str
    price: Decimal = Field(ge=0)
    unit: str
    min_order_quantity: int = Field(ge=1, default=1)
    description: Optional[str] = None
    stock: int = Field(ge=0, default=0)
    is_active: bool = True


class ProductCreate(ProductBase):
    """Product creation schema."""
    pass


class ProductUpdate(BaseModel):
    """Product update schema."""
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = Field(ge=0, default=None)
    unit: Optional[str] = None
    min_order_quantity: Optional[int] = Field(ge=1, default=None)
    description: Optional[str] = None
    stock: Optional[int] = Field(ge=0, default=None)
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    """Product response schema."""
    id: UUID
    name: str
    category: str
    price: Decimal
    unit: str
    min_order_quantity: int
    description: Optional[str] = None
    image_url: Optional[str] = None
    stock: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    """List of categories."""
    categories: List[str]


"""Order schemas."""
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class OrderItemCreate(BaseModel):
    """Order item creation schema."""
    product_id: UUID
    product_name: str
    quantity: int = Field(ge=1)
    unit_price: Decimal = Field(ge=0)


class OrderCreate(BaseModel):
    """Order creation schema."""
    items: List[OrderItemCreate]
    shipping_address: str
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    """Order item response schema."""
    id: UUID
    order_id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Order response schema."""
    id: UUID
    order_no: str
    dealer_id: UUID
    dealer_company: Optional[str] = None
    status: str
    total_amount: Decimal
    shipping_address: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Order status update schema."""
    status: str = Field(..., pattern="^(pending|confirmed|shipped|delivered|cancelled)$")


class OrderStatsResponse(BaseModel):
    """Order statistics response."""
    status_counts: dict
    total_revenue: float
    today_orders: int
    recent_orders: List[dict]


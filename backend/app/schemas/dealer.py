"""Dealer schemas."""
from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class DealerBase(BaseModel):
    """Base dealer schema."""
    company_name: str
    contact_name: str
    phone: str
    address: Optional[str] = None


class DealerCreate(DealerBase):
    """Dealer creation schema (with user account)."""
    username: str
    email: EmailStr
    password: str
    status: str = "pending"


class DealerUpdate(BaseModel):
    """Dealer update schema."""
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class DealerStatusUpdate(BaseModel):
    """Dealer status update schema."""
    status: str  # pending, approved, suspended


class DealerUserResponse(BaseModel):
    """Embedded user response for dealer."""
    id: UUID
    username: str
    email: str
    is_active: bool


class DealerResponse(BaseModel):
    """Dealer response schema."""
    id: UUID
    company_name: str
    contact_name: str
    phone: str
    address: Optional[str] = None
    status: str
    created_at: datetime
    user: DealerUserResponse

    class Config:
        from_attributes = True


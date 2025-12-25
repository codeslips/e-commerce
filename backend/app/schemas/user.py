"""User schemas."""
from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema."""
    password: str
    role: str = "dealer"
    is_active: bool = True


class UserUpdate(BaseModel):
    """User update schema."""
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """User response schema."""
    id: UUID
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


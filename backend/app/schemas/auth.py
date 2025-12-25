"""Authentication schemas."""
from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class LoginRequest(BaseModel):
    """Login request schema."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    """Login response with user info and tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: "UserInfo"


class UserInfo(BaseModel):
    """Basic user information."""
    id: UUID
    username: str
    email: str
    role: str
    is_active: bool
    dealer: Optional["DealerInfo"] = None


class DealerInfo(BaseModel):
    """Basic dealer information for auth response."""
    id: UUID
    company_name: str
    contact_name: str
    phone: str
    address: Optional[str] = None
    status: str


class RefreshRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


class CurrentUserResponse(BaseModel):
    """Current user response with full details."""
    id: UUID
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    dealer: Optional[DealerInfo] = None


# Update forward references
LoginResponse.model_rebuild()
UserInfo.model_rebuild()


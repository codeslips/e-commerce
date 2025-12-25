"""Authentication service with JWT tokens and password hashing."""
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.database import db


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token (7 days expiry)."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None


async def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate user with username and password."""
    user = await db.fetchrow(
        """
        SELECT id, username, email, password_hash, role, is_active
        FROM users WHERE username = $1
        """,
        username
    )
    
    if not user:
        return None
    
    if not verify_password(password, user["password_hash"]):
        return None
    
    if not user["is_active"]:
        return None
    
    return dict(user)


async def get_user_by_id(user_id: UUID) -> Optional[dict]:
    """Get user by ID."""
    user = await db.fetchrow(
        """
        SELECT id, username, email, role, is_active, created_at, updated_at
        FROM users WHERE id = $1
        """,
        user_id
    )
    return dict(user) if user else None


async def get_user_with_dealer(user_id: UUID) -> Optional[dict]:
    """Get user with dealer information if applicable."""
    user = await db.fetchrow(
        """
        SELECT u.id, u.username, u.email, u.role, u.is_active, u.created_at, u.updated_at,
               d.id as dealer_id, d.company_name, d.contact_name, d.phone, d.address, d.status as dealer_status
        FROM users u
        LEFT JOIN dealers d ON d.user_id = u.id
        WHERE u.id = $1
        """,
        user_id
    )
    
    if not user:
        return None
    
    result = dict(user)
    if result.get("dealer_id"):
        result["dealer"] = {
            "id": result.pop("dealer_id"),
            "company_name": result.pop("company_name"),
            "contact_name": result.pop("contact_name"),
            "phone": result.pop("phone"),
            "address": result.pop("address"),
            "status": result.pop("dealer_status"),
        }
    else:
        # Remove dealer fields if not a dealer
        for key in ["dealer_id", "company_name", "contact_name", "phone", "address", "dealer_status"]:
            result.pop(key, None)
    
    return result


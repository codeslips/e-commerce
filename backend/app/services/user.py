"""User service for CRUD operations."""
from typing import Optional, List
from uuid import UUID

from app.database import db
from app.services.auth import hash_password


async def create_user(
    username: str,
    email: str,
    password: str,
    role: str = "dealer",
    is_active: bool = True
) -> dict:
    """Create a new user."""
    password_hash = hash_password(password)
    
    user = await db.fetchrow(
        """
        INSERT INTO users (username, email, password_hash, role, is_active)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, username, email, role, is_active, created_at, updated_at
        """,
        username, email, password_hash, role, is_active
    )
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


async def get_user_by_username(username: str) -> Optional[dict]:
    """Get user by username."""
    user = await db.fetchrow(
        """
        SELECT id, username, email, role, is_active, created_at, updated_at
        FROM users WHERE username = $1
        """,
        username
    )
    return dict(user) if user else None


async def get_user_by_email(email: str) -> Optional[dict]:
    """Get user by email."""
    user = await db.fetchrow(
        """
        SELECT id, username, email, role, is_active, created_at, updated_at
        FROM users WHERE email = $1
        """,
        email
    )
    return dict(user) if user else None


async def update_user(
    user_id: UUID,
    email: Optional[str] = None,
    password: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Optional[dict]:
    """Update user information."""
    updates = []
    params = []
    param_count = 1
    
    if email is not None:
        updates.append(f"email = ${param_count}")
        params.append(email)
        param_count += 1
    
    if password is not None:
        updates.append(f"password_hash = ${param_count}")
        params.append(hash_password(password))
        param_count += 1
    
    if is_active is not None:
        updates.append(f"is_active = ${param_count}")
        params.append(is_active)
        param_count += 1
    
    if not updates:
        return await get_user_by_id(user_id)
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(user_id)
    
    query = f"""
        UPDATE users SET {', '.join(updates)}
        WHERE id = ${param_count}
        RETURNING id, username, email, role, is_active, created_at, updated_at
    """
    
    user = await db.fetchrow(query, *params)
    return dict(user) if user else None


async def list_users(
    page: int = 1,
    page_size: int = 20,
    role: Optional[str] = None
) -> dict:
    """List users with pagination."""
    offset = (page - 1) * page_size
    
    where_clause = ""
    params = [page_size, offset]
    
    if role:
        where_clause = "WHERE role = $3"
        params.append(role)
    
    # Get total count
    count_query = f"SELECT COUNT(*) FROM users {where_clause}"
    if role:
        total = await db.fetchval(count_query, role)
    else:
        total = await db.fetchval("SELECT COUNT(*) FROM users")
    
    # Get users
    query = f"""
        SELECT id, username, email, role, is_active, created_at, updated_at
        FROM users {where_clause}
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2
    """
    
    users = await db.fetch(query, *params)
    
    return {
        "items": [dict(u) for u in users],
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size if total > 0 else 1
    }


async def delete_user(user_id: UUID) -> bool:
    """Delete a user."""
    result = await db.execute(
        "DELETE FROM users WHERE id = $1",
        user_id
    )
    return "DELETE 1" in result


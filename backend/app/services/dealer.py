"""Dealer service for dealer management."""
from typing import Optional
from uuid import UUID

from app.database import db
from app.services.user import create_user


async def create_dealer(
    username: str,
    email: str,
    password: str,
    company_name: str,
    contact_name: str,
    phone: str,
    address: Optional[str] = None,
    status: str = "pending"
) -> dict:
    """Create a new dealer with associated user account."""
    # Create user first
    user = await create_user(username, email, password, role="dealer")
    
    # Create dealer record
    dealer = await db.fetchrow(
        """
        INSERT INTO dealers (user_id, company_name, contact_name, phone, address, status)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id, user_id, company_name, contact_name, phone, address, status, created_at
        """,
        user["id"], company_name, contact_name, phone, address, status
    )
    
    dealer_dict = dict(dealer)
    dealer_dict["user"] = user
    return dealer_dict


async def get_dealer_by_id(dealer_id: UUID) -> Optional[dict]:
    """Get dealer by ID with user information."""
    dealer = await db.fetchrow(
        """
        SELECT d.id, d.user_id, d.company_name, d.contact_name, d.phone, d.address, d.status, d.created_at,
               u.username, u.email, u.is_active
        FROM dealers d
        JOIN users u ON u.id = d.user_id
        WHERE d.id = $1
        """,
        dealer_id
    )
    
    if not dealer:
        return None
    
    result = dict(dealer)
    result["user"] = {
        "id": result.pop("user_id"),
        "username": result.pop("username"),
        "email": result.pop("email"),
        "is_active": result.pop("is_active"),
    }
    
    return result


async def get_dealer_by_user_id(user_id: UUID) -> Optional[dict]:
    """Get dealer by user ID."""
    dealer = await db.fetchrow(
        """
        SELECT d.id, d.user_id, d.company_name, d.contact_name, d.phone, d.address, d.status, d.created_at,
               u.username, u.email, u.is_active
        FROM dealers d
        JOIN users u ON u.id = d.user_id
        WHERE d.user_id = $1
        """,
        user_id
    )
    
    if not dealer:
        return None
    
    result = dict(dealer)
    result["user"] = {
        "id": result.pop("user_id"),
        "username": result.pop("username"),
        "email": result.pop("email"),
        "is_active": result.pop("is_active"),
    }
    
    return result


async def update_dealer(
    dealer_id: UUID,
    company_name: Optional[str] = None,
    contact_name: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None
) -> Optional[dict]:
    """Update dealer information."""
    updates = []
    params = []
    param_count = 1
    
    field_map = {
        "company_name": company_name,
        "contact_name": contact_name,
        "phone": phone,
        "address": address,
    }
    
    for field, value in field_map.items():
        if value is not None:
            updates.append(f"{field} = ${param_count}")
            params.append(value)
            param_count += 1
    
    if not updates:
        return await get_dealer_by_id(dealer_id)
    
    params.append(dealer_id)
    
    query = f"""
        UPDATE dealers SET {', '.join(updates)}
        WHERE id = ${param_count}
        RETURNING id
    """
    
    result = await db.fetchrow(query, *params)
    if not result:
        return None
    
    return await get_dealer_by_id(dealer_id)


async def update_dealer_status(dealer_id: UUID, status: str) -> Optional[dict]:
    """Update dealer status (pending/approved/suspended)."""
    result = await db.fetchrow(
        """
        UPDATE dealers SET status = $1
        WHERE id = $2
        RETURNING id
        """,
        status, dealer_id
    )
    
    if not result:
        return None
    
    return await get_dealer_by_id(dealer_id)


async def list_dealers(
    page: int = 1,
    page_size: int = 20,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> dict:
    """List dealers with pagination and filtering."""
    offset = (page - 1) * page_size
    
    conditions = []
    params = []
    param_count = 1
    
    if status:
        conditions.append(f"d.status = ${param_count}")
        params.append(status)
        param_count += 1
    
    if search:
        conditions.append(f"(d.company_name ILIKE ${param_count} OR d.contact_name ILIKE ${param_count} OR u.email ILIKE ${param_count})")
        params.append(f"%{search}%")
        param_count += 1
    
    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
    
    # Get total count
    count_query = f"""
        SELECT COUNT(*) FROM dealers d
        JOIN users u ON u.id = d.user_id
        {where_clause}
    """
    total = await db.fetchval(count_query, *params)
    
    # Get dealers
    params.extend([page_size, offset])
    query = f"""
        SELECT d.id, d.user_id, d.company_name, d.contact_name, d.phone, d.address, d.status, d.created_at,
               u.username, u.email, u.is_active
        FROM dealers d
        JOIN users u ON u.id = d.user_id
        {where_clause}
        ORDER BY d.created_at DESC
        LIMIT ${param_count} OFFSET ${param_count + 1}
    """
    
    dealers = await db.fetch(query, *params)
    
    items = []
    for d in dealers:
        item = dict(d)
        item["user"] = {
            "id": item.pop("user_id"),
            "username": item.pop("username"),
            "email": item.pop("email"),
            "is_active": item.pop("is_active"),
        }
        items.append(item)
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size if total > 0 else 1
    }


async def delete_dealer(dealer_id: UUID) -> bool:
    """Delete a dealer and associated user."""
    # Get user_id first
    dealer = await db.fetchrow(
        "SELECT user_id FROM dealers WHERE id = $1",
        dealer_id
    )
    
    if not dealer:
        return False
    
    # Delete user (cascades to dealer)
    result = await db.execute(
        "DELETE FROM users WHERE id = $1",
        dealer["user_id"]
    )
    
    return "DELETE 1" in result


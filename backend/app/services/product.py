"""Product service for CRUD operations."""
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

from app.database import db


async def create_product(
    name: str,
    category: str,
    price: Decimal,
    unit: str,
    min_order_quantity: int = 1,
    description: Optional[str] = None,
    image_url: Optional[str] = None,
    stock: int = 0,
    is_active: bool = True
) -> dict:
    """Create a new product."""
    product = await db.fetchrow(
        """
        INSERT INTO products (name, category, price, unit, min_order_quantity, description, image_url, stock, is_active)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        RETURNING id, name, category, price, unit, min_order_quantity, description, image_url, stock, is_active, created_at, updated_at
        """,
        name, category, price, unit, min_order_quantity, description, image_url, stock, is_active
    )
    return dict(product)


async def get_product_by_id(product_id: UUID) -> Optional[dict]:
    """Get product by ID."""
    product = await db.fetchrow(
        """
        SELECT id, name, category, price, unit, min_order_quantity, description, image_url, stock, is_active, created_at, updated_at
        FROM products WHERE id = $1
        """,
        product_id
    )
    return dict(product) if product else None


async def update_product(
    product_id: UUID,
    name: Optional[str] = None,
    category: Optional[str] = None,
    price: Optional[Decimal] = None,
    unit: Optional[str] = None,
    min_order_quantity: Optional[int] = None,
    description: Optional[str] = None,
    image_url: Optional[str] = None,
    stock: Optional[int] = None,
    is_active: Optional[bool] = None
) -> Optional[dict]:
    """Update product information."""
    updates = []
    params = []
    param_count = 1
    
    field_map = {
        "name": name,
        "category": category,
        "price": price,
        "unit": unit,
        "min_order_quantity": min_order_quantity,
        "description": description,
        "image_url": image_url,
        "stock": stock,
        "is_active": is_active,
    }
    
    for field, value in field_map.items():
        if value is not None:
            updates.append(f"{field} = ${param_count}")
            params.append(value)
            param_count += 1
    
    if not updates:
        return await get_product_by_id(product_id)
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(product_id)
    
    query = f"""
        UPDATE products SET {', '.join(updates)}
        WHERE id = ${param_count}
        RETURNING id, name, category, price, unit, min_order_quantity, description, image_url, stock, is_active, created_at, updated_at
    """
    
    product = await db.fetchrow(query, *params)
    return dict(product) if product else None


async def delete_product(product_id: UUID) -> bool:
    """Delete a product."""
    result = await db.execute(
        "DELETE FROM products WHERE id = $1",
        product_id
    )
    return "DELETE 1" in result


async def list_products(
    page: int = 1,
    page_size: int = 20,
    category: Optional[str] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None
) -> dict:
    """List products with pagination and filtering."""
    offset = (page - 1) * page_size
    
    conditions = []
    params = []
    param_count = 1
    
    if category:
        conditions.append(f"category = ${param_count}")
        params.append(category)
        param_count += 1
    
    if search:
        conditions.append(f"(name ILIKE ${param_count} OR description ILIKE ${param_count})")
        params.append(f"%{search}%")
        param_count += 1
    
    if is_active is not None:
        conditions.append(f"is_active = ${param_count}")
        params.append(is_active)
        param_count += 1
    
    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
    
    # Get total count
    count_query = f"SELECT COUNT(*) FROM products {where_clause}"
    total = await db.fetchval(count_query, *params)
    
    # Get products
    params.extend([page_size, offset])
    query = f"""
        SELECT id, name, category, price, unit, min_order_quantity, description, image_url, stock, is_active, created_at, updated_at
        FROM products {where_clause}
        ORDER BY created_at DESC
        LIMIT ${param_count} OFFSET ${param_count + 1}
    """
    
    products = await db.fetch(query, *params)
    
    return {
        "items": [dict(p) for p in products],
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size if total > 0 else 1
    }


async def get_categories() -> List[str]:
    """Get list of unique product categories."""
    rows = await db.fetch(
        "SELECT DISTINCT category FROM products WHERE is_active = true ORDER BY category"
    )
    return [row["category"] for row in rows]


"""Order service for order management."""
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import datetime, timezone

from app.database import db


async def generate_order_no() -> str:
    """Generate unique order number: ORD{YYYYMMDD}{NNN}."""
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    
    # Get today's order count
    count = await db.fetchval(
        """
        SELECT COUNT(*) FROM orders 
        WHERE order_no LIKE $1
        """,
        f"ORD{today}%"
    )
    
    next_num = (count or 0) + 1
    return f"ORD{today}{next_num:03d}"


async def create_order(
    dealer_id: UUID,
    items: List[dict],
    shipping_address: str,
    notes: Optional[str] = None
) -> dict:
    """Create a new order with items."""
    order_no = await generate_order_no()
    
    # Calculate total amount
    total_amount = sum(
        Decimal(str(item["unit_price"])) * item["quantity"] 
        for item in items
    )
    
    # Create order
    order = await db.fetchrow(
        """
        INSERT INTO orders (order_no, dealer_id, status, total_amount, shipping_address, notes)
        VALUES ($1, $2, 'pending', $3, $4, $5)
        RETURNING id, order_no, dealer_id, status, total_amount, shipping_address, notes, created_at, updated_at
        """,
        order_no, dealer_id, total_amount, shipping_address, notes
    )
    
    order_dict = dict(order)
    
    # Create order items
    order_items = []
    for item in items:
        subtotal = Decimal(str(item["unit_price"])) * item["quantity"]
        order_item = await db.fetchrow(
            """
            INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, subtotal)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, order_id, product_id, product_name, quantity, unit_price, subtotal
            """,
            order_dict["id"], item["product_id"], item["product_name"], 
            item["quantity"], Decimal(str(item["unit_price"])), subtotal
        )
        order_items.append(dict(order_item))
    
    order_dict["items"] = order_items
    return order_dict


async def get_order_by_id(order_id: UUID) -> Optional[dict]:
    """Get order by ID with items."""
    order = await db.fetchrow(
        """
        SELECT o.id, o.order_no, o.dealer_id, o.status, o.total_amount, 
               o.shipping_address, o.notes, o.created_at, o.updated_at,
               d.company_name as dealer_company
        FROM orders o
        JOIN dealers d ON d.id = o.dealer_id
        WHERE o.id = $1
        """,
        order_id
    )
    
    if not order:
        return None
    
    order_dict = dict(order)
    
    # Get order items
    items = await db.fetch(
        """
        SELECT id, order_id, product_id, product_name, quantity, unit_price, subtotal
        FROM order_items WHERE order_id = $1
        """,
        order_id
    )
    order_dict["items"] = [dict(item) for item in items]
    
    return order_dict


async def get_order_by_order_no(order_no: str) -> Optional[dict]:
    """Get order by order number with items."""
    order = await db.fetchrow(
        """
        SELECT o.id, o.order_no, o.dealer_id, o.status, o.total_amount, 
               o.shipping_address, o.notes, o.created_at, o.updated_at,
               d.company_name as dealer_company
        FROM orders o
        JOIN dealers d ON d.id = o.dealer_id
        WHERE o.order_no = $1
        """,
        order_no
    )
    
    if not order:
        return None
    
    order_dict = dict(order)
    
    # Get order items
    items = await db.fetch(
        """
        SELECT id, order_id, product_id, product_name, quantity, unit_price, subtotal
        FROM order_items WHERE order_id = $1
        """,
        order_dict["id"]
    )
    order_dict["items"] = [dict(item) for item in items]
    
    return order_dict


async def update_order_status(order_id: UUID, status: str) -> Optional[dict]:
    """Update order status."""
    order = await db.fetchrow(
        """
        UPDATE orders SET status = $1, updated_at = CURRENT_TIMESTAMP
        WHERE id = $2
        RETURNING id, order_no, dealer_id, status, total_amount, shipping_address, notes, created_at, updated_at
        """,
        status, order_id
    )
    
    if not order:
        return None
    
    return await get_order_by_id(order_id)


async def cancel_order(order_id: UUID) -> Optional[dict]:
    """Cancel an order (only if pending)."""
    order = await db.fetchrow(
        """
        UPDATE orders SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP
        WHERE id = $1 AND status = 'pending'
        RETURNING id
        """,
        order_id
    )
    
    if not order:
        return None
    
    return await get_order_by_id(order_id)


async def list_orders(
    page: int = 1,
    page_size: int = 20,
    dealer_id: Optional[UUID] = None,
    status: Optional[str] = None,
    order_no: Optional[str] = None
) -> dict:
    """List orders with pagination and filtering."""
    offset = (page - 1) * page_size
    
    conditions = []
    params = []
    param_count = 1
    
    if dealer_id:
        conditions.append(f"o.dealer_id = ${param_count}")
        params.append(dealer_id)
        param_count += 1
    
    if status:
        conditions.append(f"o.status = ${param_count}")
        params.append(status)
        param_count += 1
    
    if order_no:
        conditions.append(f"o.order_no ILIKE ${param_count}")
        params.append(f"%{order_no}%")
        param_count += 1
    
    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
    
    # Get total count
    count_query = f"SELECT COUNT(*) FROM orders o {where_clause}"
    total = await db.fetchval(count_query, *params)
    
    # Get orders
    params.extend([page_size, offset])
    query = f"""
        SELECT o.id, o.order_no, o.dealer_id, o.status, o.total_amount, 
               o.shipping_address, o.notes, o.created_at, o.updated_at,
               d.company_name as dealer_company
        FROM orders o
        JOIN dealers d ON d.id = o.dealer_id
        {where_clause}
        ORDER BY o.created_at DESC
        LIMIT ${param_count} OFFSET ${param_count + 1}
    """
    
    orders = await db.fetch(query, *params)
    
    return {
        "items": [dict(o) for o in orders],
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size if total > 0 else 1
    }


async def get_order_stats() -> dict:
    """Get order statistics for dashboard."""
    # Total orders by status
    status_counts = await db.fetch(
        """
        SELECT status, COUNT(*) as count
        FROM orders
        GROUP BY status
        """
    )
    
    # Total revenue
    total_revenue = await db.fetchval(
        "SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status != 'cancelled'"
    )
    
    # Today's orders
    today_orders = await db.fetchval(
        """
        SELECT COUNT(*) FROM orders 
        WHERE DATE(created_at) = CURRENT_DATE
        """
    )
    
    # Recent orders
    recent_orders = await db.fetch(
        """
        SELECT o.id, o.order_no, o.status, o.total_amount, o.created_at,
               d.company_name as dealer_company
        FROM orders o
        JOIN dealers d ON d.id = o.dealer_id
        ORDER BY o.created_at DESC
        LIMIT 5
        """
    )
    
    return {
        "status_counts": {row["status"]: row["count"] for row in status_counts},
        "total_revenue": float(total_revenue),
        "today_orders": today_orders,
        "recent_orders": [dict(o) for o in recent_orders]
    }


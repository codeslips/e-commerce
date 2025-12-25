"""Order routes."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate, OrderStatsResponse
from app.schemas.common import PaginatedResponse
from app.services import order as order_service
from app.services import dealer as dealer_service
from app.routers.auth import get_current_user, require_admin, require_approved_dealer

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("", response_model=PaginatedResponse[OrderResponse])
async def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    order_no: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
):
    """List orders (filtered by role - dealers see own orders only)."""
    dealer_id = None
    
    # Dealers can only see their own orders
    if current_user.get("role") != "admin":
        dealer = current_user.get("dealer")
        if not dealer:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Dealer account required",
            )
        dealer_id = dealer["id"]
    
    result = await order_service.list_orders(
        page=page,
        page_size=page_size,
        dealer_id=dealer_id,
        status=status_filter,
        order_no=order_no,
    )
    
    return PaginatedResponse[OrderResponse](
        items=[OrderResponse(**o) for o in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        pages=result["pages"],
    )


@router.get("/stats", response_model=OrderStatsResponse)
async def get_order_stats(
    current_user: dict = Depends(require_admin),
):
    """Get order statistics (admin only)."""
    stats = await order_service.get_order_stats()
    return OrderStatsResponse(**stats)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    current_user: dict = Depends(get_current_user),
):
    """Get order by ID."""
    order = await order_service.get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    
    # Check access
    if current_user.get("role") != "admin":
        dealer = current_user.get("dealer")
        if not dealer or str(dealer["id"]) != str(order["dealer_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
    
    return OrderResponse(**order)


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    current_user: dict = Depends(require_approved_dealer),
):
    """Create a new order (approved dealers only)."""
    dealer = current_user.get("dealer")
    if not dealer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dealer account required",
        )
    
    items = [
        {
            "product_id": item.product_id,
            "product_name": item.product_name,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
        }
        for item in order.items
    ]
    
    result = await order_service.create_order(
        dealer_id=dealer["id"],
        items=items,
        shipping_address=order.shipping_address,
        notes=order.notes,
    )
    
    return OrderResponse(**result)


@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: UUID,
    status_update: OrderStatusUpdate,
    current_user: dict = Depends(require_admin),
):
    """Update order status (admin only)."""
    order = await order_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    
    result = await order_service.update_order_status(order_id, status_update.status)
    return OrderResponse(**result)


@router.delete("/{order_id}", response_model=OrderResponse)
async def cancel_order(
    order_id: UUID,
    current_user: dict = Depends(get_current_user),
):
    """Cancel an order (only pending orders)."""
    order = await order_service.get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    
    # Check access
    if current_user.get("role") != "admin":
        dealer = current_user.get("dealer")
        if not dealer or str(dealer["id"]) != str(order["dealer_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
    
    if order["status"] != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending orders can be cancelled",
        )
    
    result = await order_service.cancel_order(order_id)
    return OrderResponse(**result)


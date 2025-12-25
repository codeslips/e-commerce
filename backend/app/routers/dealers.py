"""Dealer routes."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.schemas.dealer import DealerCreate, DealerUpdate, DealerResponse, DealerStatusUpdate
from app.schemas.common import PaginatedResponse
from app.services import dealer as dealer_service
from app.routers.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/dealers", tags=["Dealers"])


@router.get("", response_model=PaginatedResponse[DealerResponse])
async def list_dealers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = None,
    current_user: dict = Depends(require_admin),
):
    """List dealers (admin only)."""
    result = await dealer_service.list_dealers(
        page=page,
        page_size=page_size,
        status=status_filter,
        search=search,
    )
    
    return PaginatedResponse[DealerResponse](
        items=[DealerResponse(**d) for d in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        pages=result["pages"],
    )


@router.get("/{dealer_id}", response_model=DealerResponse)
async def get_dealer(
    dealer_id: UUID,
    current_user: dict = Depends(get_current_user),
):
    """Get dealer by ID."""
    dealer = await dealer_service.get_dealer_by_id(dealer_id)
    
    if not dealer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dealer not found",
        )
    
    # Non-admin can only view their own dealer profile
    if current_user.get("role") != "admin":
        user_dealer = current_user.get("dealer")
        if not user_dealer or str(user_dealer["id"]) != str(dealer_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
    
    return DealerResponse(**dealer)


@router.post("", response_model=DealerResponse, status_code=status.HTTP_201_CREATED)
async def create_dealer(
    dealer: DealerCreate,
    current_user: dict = Depends(require_admin),
):
    """Create a new dealer (admin only)."""
    try:
        result = await dealer_service.create_dealer(
            username=dealer.username,
            email=dealer.email,
            password=dealer.password,
            company_name=dealer.company_name,
            contact_name=dealer.contact_name,
            phone=dealer.phone,
            address=dealer.address,
            status=dealer.status,
        )
        return DealerResponse(**result)
    except Exception as e:
        if "unique" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists",
            )
        raise


@router.put("/{dealer_id}", response_model=DealerResponse)
async def update_dealer(
    dealer_id: UUID,
    dealer: DealerUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update dealer information."""
    existing = await dealer_service.get_dealer_by_id(dealer_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dealer not found",
        )
    
    # Non-admin can only update their own profile
    if current_user.get("role") != "admin":
        user_dealer = current_user.get("dealer")
        if not user_dealer or str(user_dealer["id"]) != str(dealer_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
    
    result = await dealer_service.update_dealer(
        dealer_id=dealer_id,
        company_name=dealer.company_name,
        contact_name=dealer.contact_name,
        phone=dealer.phone,
        address=dealer.address,
    )
    return DealerResponse(**result)


@router.put("/{dealer_id}/status", response_model=DealerResponse)
async def update_dealer_status(
    dealer_id: UUID,
    status_update: DealerStatusUpdate,
    current_user: dict = Depends(require_admin),
):
    """Update dealer status (admin only)."""
    existing = await dealer_service.get_dealer_by_id(dealer_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dealer not found",
        )
    
    result = await dealer_service.update_dealer_status(dealer_id, status_update.status)
    return DealerResponse(**result)


@router.delete("/{dealer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dealer(
    dealer_id: UUID,
    current_user: dict = Depends(require_admin),
):
    """Delete a dealer (admin only)."""
    success = await dealer_service.delete_dealer(dealer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dealer not found",
        )


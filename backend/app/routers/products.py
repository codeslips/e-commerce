"""Product routes."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query

from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, CategoryListResponse
from app.schemas.common import PaginatedResponse
from app.services import product as product_service
from app.services.storage import storage
from app.routers.auth import get_current_user, require_admin, get_current_user_optional

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """List products with pagination and filtering."""
    # Only show active products to non-admin users
    is_active = None
    if not current_user or current_user.get("role") != "admin":
        is_active = True
    
    result = await product_service.list_products(
        page=page,
        page_size=page_size,
        category=category,
        search=search,
        is_active=is_active,
    )
    
    return PaginatedResponse[ProductResponse](
        items=[ProductResponse(**p) for p in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        pages=result["pages"],
    )


@router.get("/categories", response_model=CategoryListResponse)
async def list_categories():
    """Get list of product categories."""
    categories = await product_service.get_categories()
    return CategoryListResponse(categories=categories)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """Get product by ID."""
    product = await product_service.get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Only show inactive products to admins
    if not product["is_active"]:
        if not current_user or current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
    
    return ProductResponse(**product)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    current_user: dict = Depends(require_admin),
):
    """Create a new product (admin only)."""
    result = await product_service.create_product(
        name=product.name,
        category=product.category,
        price=product.price,
        unit=product.unit,
        min_order_quantity=product.min_order_quantity,
        description=product.description,
        stock=product.stock,
        is_active=product.is_active,
    )
    return ProductResponse(**result)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    product: ProductUpdate,
    current_user: dict = Depends(require_admin),
):
    """Update a product (admin only)."""
    existing = await product_service.get_product_by_id(product_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    result = await product_service.update_product(
        product_id=product_id,
        name=product.name,
        category=product.category,
        price=product.price,
        unit=product.unit,
        min_order_quantity=product.min_order_quantity,
        description=product.description,
        stock=product.stock,
        is_active=product.is_active,
    )
    return ProductResponse(**result)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    current_user: dict = Depends(require_admin),
):
    """Delete a product (admin only)."""
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )


@router.post("/{product_id}/image", response_model=ProductResponse)
async def upload_product_image(
    product_id: UUID,
    file: UploadFile = File(...),
    current_user: dict = Depends(require_admin),
):
    """Upload product image (admin only)."""
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image",
        )
    
    # Save file
    path = await storage.save(file, "products")
    image_url = storage.get_url(path)
    
    # Delete old image if exists
    if product.get("image_url"):
        old_path = product["image_url"].replace("/api/files/", "")
        await storage.delete(old_path)
    
    # Update product
    result = await product_service.update_product(product_id, image_url=image_url)
    return ProductResponse(**result)


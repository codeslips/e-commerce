"""Authentication routes."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.auth import (
    LoginRequest, LoginResponse, TokenResponse, 
    CurrentUserResponse, RefreshRequest, UserInfo, DealerInfo
)
from app.services.auth import (
    authenticate_user, create_access_token, create_refresh_token,
    decode_token, get_user_with_dealer
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> dict:
    """Dependency to get current authenticated user."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    user = await get_user_with_dealer(UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """Dependency to get current user if authenticated."""
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency to require admin role."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def require_approved_dealer(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency to require approved dealer status."""
    if current_user.get("role") == "admin":
        return current_user
    
    dealer = current_user.get("dealer")
    if not dealer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dealer account required",
        )
    
    if dealer.get("status") != "approved":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dealer account not approved",
        )
    
    return current_user


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, response: Response):
    """Authenticate user and return tokens."""
    user = await authenticate_user(request.username, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    # Get full user info with dealer
    full_user = await get_user_with_dealer(user["id"])
    
    # Create tokens
    token_data = {"sub": str(user["id"]), "role": user["role"]}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    # Set refresh token in httpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days
        samesite="lax",
    )
    
    # Build user info
    dealer_info = None
    if full_user.get("dealer"):
        dealer_info = DealerInfo(**full_user["dealer"])
    
    user_info = UserInfo(
        id=full_user["id"],
        username=full_user["username"],
        email=full_user["email"],
        role=full_user["role"],
        is_active=full_user["is_active"],
        dealer=dealer_info,
    )
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_info,
    )


@router.post("/logout")
async def logout(response: Response):
    """Logout and clear refresh token cookie."""
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: Optional[RefreshRequest] = None,
    refresh_token: Optional[str] = Cookie(None),
):
    """Refresh access token."""
    token = request.refresh_token if request else refresh_token
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required",
        )
    
    payload = decode_token(token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id = payload.get("sub")
    role = payload.get("role")
    
    # Create new tokens
    token_data = {"sub": user_id, "role": role}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )


@router.get("/me", response_model=CurrentUserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user information."""
    dealer_info = None
    if current_user.get("dealer"):
        dealer_info = DealerInfo(**current_user["dealer"])
    
    return CurrentUserResponse(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user["email"],
        role=current_user["role"],
        is_active=current_user["is_active"],
        created_at=current_user["created_at"],
        updated_at=current_user["updated_at"],
        dealer=dealer_info,
    )


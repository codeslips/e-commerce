# Schemas package
from app.schemas.common import PaginatedResponse
from app.schemas.auth import LoginRequest, LoginResponse, TokenResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.order import OrderCreate, OrderItemCreate, OrderResponse, OrderItemResponse
from app.schemas.dealer import DealerCreate, DealerUpdate, DealerResponse

__all__ = [
    "PaginatedResponse",
    "LoginRequest", "LoginResponse", "TokenResponse",
    "UserCreate", "UserUpdate", "UserResponse",
    "ProductCreate", "ProductUpdate", "ProductResponse",
    "OrderCreate", "OrderItemCreate", "OrderResponse", "OrderItemResponse",
    "DealerCreate", "DealerUpdate", "DealerResponse",
]


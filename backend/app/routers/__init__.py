# Routers package
from app.routers.auth import router as auth_router
from app.routers.products import router as products_router
from app.routers.orders import router as orders_router
from app.routers.dealers import router as dealers_router
from app.routers.files import router as files_router

__all__ = [
    "auth_router",
    "products_router",
    "orders_router",
    "dealers_router",
    "files_router",
]


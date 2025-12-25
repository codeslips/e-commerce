from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import db
from app.routers import auth_router, products_router, orders_router, dealers_router, files_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()


app = FastAPI(
    title="欣与甜订货平台 API",
    description="Xin Yu Tian Dealer Ordering Platform API",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
origins = [origin.strip() for origin in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(dealers_router)
app.include_router(files_router)


@app.get("/health")
async def health_check():
    """Health check endpoint with database connectivity status."""
    db_status = "disconnected"
    try:
        if db.pool:
            await db.fetchval("SELECT 1")
            db_status = "connected"
    except Exception:
        db_status = "error"
    
    return {
        "status": "healthy",
        "database": db_status,
    }

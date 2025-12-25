"""File serving routes for local storage."""
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.config import settings

router = APIRouter(prefix="/api/files", tags=["Files"])


@router.get("/{path:path}")
async def get_file(path: str):
    """Serve files from local storage."""
    # Only serve from local storage
    if settings.storage_backend != "local":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    
    file_path = Path(settings.storage_path) / path
    
    # Security check - prevent directory traversal
    try:
        file_path = file_path.resolve()
        base_path = Path(settings.storage_path).resolve()
        if not str(file_path).startswith(str(base_path)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    
    return FileResponse(file_path)


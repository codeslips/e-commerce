"""File storage service with local and S3 backends."""
import os
import uuid
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from fastapi import UploadFile

from app.config import settings


class StorageService(ABC):
    """Abstract storage service interface."""
    
    @abstractmethod
    async def save(self, file: UploadFile, path: str) -> str:
        """Save file and return the stored path."""
        pass
    
    @abstractmethod
    def get_url(self, path: str) -> str:
        """Get accessible URL for the file."""
        pass
    
    @abstractmethod
    async def delete(self, path: str) -> bool:
        """Delete file and return success status."""
        pass


class LocalStorage(StorageService):
    """Local filesystem storage implementation."""
    
    def __init__(self, base_path: str = "/data/images"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    async def save(self, file: UploadFile, path: str) -> str:
        """Save file to local filesystem."""
        # Generate unique filename
        ext = Path(file.filename).suffix if file.filename else ""
        unique_name = f"{uuid.uuid4()}{ext}"
        full_path = self.base_path / path / unique_name
        
        # Ensure directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save file
        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Return relative path
        return f"{path}/{unique_name}"
    
    def get_url(self, path: str) -> str:
        """Get URL for accessing the file via API."""
        return f"/api/files/{path}"
    
    async def delete(self, path: str) -> bool:
        """Delete file from local filesystem."""
        try:
            full_path = self.base_path / path
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False


class S3Storage(StorageService):
    """AWS S3 storage implementation (placeholder for future use)."""
    
    def __init__(self):
        import boto3
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_s3_region
        )
        self.bucket = settings.aws_s3_bucket
    
    async def save(self, file: UploadFile, path: str) -> str:
        """Save file to S3."""
        ext = Path(file.filename).suffix if file.filename else ""
        unique_name = f"{uuid.uuid4()}{ext}"
        key = f"{path}/{unique_name}"
        
        self.s3.upload_fileobj(file.file, self.bucket, key)
        return key
    
    def get_url(self, path: str) -> str:
        """Get S3 URL for the file."""
        return f"https://{self.bucket}.s3.{settings.aws_s3_region}.amazonaws.com/{path}"
    
    async def delete(self, path: str) -> bool:
        """Delete file from S3."""
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=path)
            return True
        except Exception:
            return False


def get_storage() -> StorageService:
    """Get storage service based on configuration."""
    if settings.storage_backend == "s3" and settings.aws_s3_bucket:
        return S3Storage()
    return LocalStorage(settings.storage_path)


# Global storage instance
storage = get_storage()


from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://xinyutian:xinyutian@db:5432/xinyutian"
    
    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    jwt_refresh_expire_days: int = 7
    
    # AWS S3
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_s3_bucket: Optional[str] = None
    aws_s3_region: str = "ap-southeast-1"
    
    # Storage
    storage_backend: str = "local"  # local or s3
    storage_path: str = "/data/images"
    
    # App
    app_env: str = "development"
    cors_origins: str = "http://localhost:5173,http://localhost:5500"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()


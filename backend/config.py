from pydantic import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str = "mysql+mysqlconnector://user:password@localhost:3306/wildmedia"
    
    # Security configuration
    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Media configuration
    MEDIA_ROOT: Path = Path("/media")
    SUBTITLE_DIR: Path = Path("/subtitles")
    
    # API configuration
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "WildMediaServer"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
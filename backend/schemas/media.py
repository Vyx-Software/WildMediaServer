from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

class MediaType(str, Enum):
    MOVIE = "movie"
    SHOW = "show"
    MIXED = "mixed"

class MediaLibraryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    path: str = Field(..., regex="^/([a-zA-Z0-9_-]+/)*[a-zA-Z0-9_-]+$")
    media_type: MediaType = MediaType.MIXED
    auto_scan: bool = True

class MediaLibraryResponse(MediaLibraryCreate):
    id: int
    created_at: datetime
    last_scan: Optional[datetime]
    media_count: int

    class Config:
        orm_mode = True

class MediaItemResponse(BaseModel):
    id: int
    name: str
    path: str
    media_type: MediaType
    library_id: int
    metadata: Dict
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MediaScanResult(BaseModel):
    total_files: int
    new_files: int
    updated_files: int
    failed_files: int
    scan_duration: float

class PlaybackRequest(BaseModel):
    media_id: int
    start_time: Optional[float] = 0.0
    subtitle_lang: Optional[str] = "en"
    quality: Optional[str] = "auto"

class PlayerSettings(BaseModel):
    subtitle_font: Optional[str] = "Arial"
    subtitle_size: Optional[int] = 24
    subtitle_color: Optional[str] = "#FFFFFF"
    subtitle_background: Optional[str] = "transparent"
    subtitle_outline: Optional[str] = "#000000"
    subtitle_shadow: Optional[bool] = True
    default_quality: Optional[str] = "1080p"
    autoplay_next: Optional[bool] = True
    skip_intro_duration: Optional[int] = 90
    skip_credits_duration: Optional[int] = 120

    @validator("subtitle_size")
    def validate_subtitle_size(cls, v):
        if not 12 <= v <= 48:
            raise ValueError("Subtitle size must be between 12 and 48")
        return v
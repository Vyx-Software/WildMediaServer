from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class SubtitleFormat(str, Enum):
    SRT = "srt"
    VTT = "vtt"
    ASS = "ass"

class SubtitleConfig(BaseModel):
    font_family: str = "Arial"
    font_size: int = 24
    font_color: str = "#FFFFFF"
    background_color: str = "#00000080"
    outline_color: str = "#000000"
    shadow: bool = True
    vertical_position: int = 90
    horizontal_position: int = 50

    @validator("vertical_position", "horizontal_position")
    def validate_position(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("Position must be between 0 and 100 percent")
        return v

class SubtitleResponse(BaseModel):
    language: str
    format: SubtitleFormat
    path: str
    sync_score: Optional[float]
    download_count: Optional[int]
    source: str

class SubtitleSearchQuery(BaseModel):
    media_title: str
    season: Optional[int] = None
    episode: Optional[int] = None
    year: Optional[int] = None
    language: Optional[str] = "en"
    use_opensubtitles: bool = True

class SubtitleUpload(BaseModel):
    media_id: int
    content: str = Field(..., min_length=10)
    language: str = Field(..., min_length=2, max_length=3)
    format: SubtitleFormat
    convert_to_vtt: bool = True

    @validator("content")
    def validate_subtitle_content(cls, v):
        if len(v.splitlines()) < 5:
            raise ValueError("Invalid subtitle content")
        return v
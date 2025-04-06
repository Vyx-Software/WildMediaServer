from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..session import Base
import enum

class SubtitleFormat(enum.Enum):
    SRT = "srt"
    VTT = "vtt"
    ASS = "ass"
    SSA = "ssa"

class SubtitleSource(enum.Enum):
    LOCAL = "local"
    OPENSUBTITLES = "opensubtitles"
    USER = "user"

class SubtitleSyncStatus(enum.Enum):
    SYNCED = "synced"
    UNSYNCED = "unsynced"
    PENDING = "pending"
    ERROR = "error"

class Subtitle(Base):
    __tablename__ = "subtitles"
    
    id = Column(Integer, primary_key=True, index=True)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False)
    file_path = Column(String(511), unique=True, nullable=False)
    language = Column(String(3), nullable=False)  # ISO 639-2/T
    format = Column(Enum(SubtitleFormat), nullable=False)
    source = Column(Enum(SubtitleSource), nullable=False)
    sync_status = Column(Enum(SubtitleSyncStatus), default=SubtitleSyncStatus.PENDING)
    sync_offset = Column(Float)  # In seconds
    hash = Column(String(128), nullable=False)  # BLAKE2b hash
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    uploader_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    media = relationship("Media", back_populates="subtitles")
    uploader = relationship("User", back_populates="uploaded_subtitles")

class PlayerSettings(Base):
    __tablename__ = "player_settings"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    subtitle_font = Column(String(50), default="Arial")
    subtitle_size = Column(Integer, default=24)
    subtitle_color = Column(String(7), default="#FFFFFF")
    subtitle_background = Column(String(20), default="transparent")
    subtitle_outline = Column(String(7), default="#000000")
    subtitle_shadow = Column(Boolean, default=True)
    default_quality = Column(String(10), default="1080p")
    autoplay_next = Column(Boolean, default=True)
    skip_intro = Column(Boolean, default=True)
    skip_credits = Column(Boolean, default=True)

    # Relationship
    user = relationship("User", back_populates="player_settings")
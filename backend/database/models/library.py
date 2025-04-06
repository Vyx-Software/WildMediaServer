from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..session import Base
from .media import MediaType

class MediaLibrary(Base):
    __tablename__ = "media_libraries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    path = Column(String(511), unique=True, nullable=False)
    media_type = Column(Enum(MediaType), nullable=False)
    auto_scan = Column(Boolean, default=True, nullable=False)
    last_scan = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    media_items = relationship("Media", back_populates="library")
    owner = relationship("User")

    __table_args__ = (
        UniqueConstraint('path', name='_library_path_uc'),
    )
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..session import Base
import enum

class MediaType(enum.Enum):
    MOVIE = "movie"
    SHOW = "show"
    EPISODE = "episode"
    COLLECTION = "collection"

class Media(Base):
    __tablename__ = "media"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    file_path = Column(String(511), unique=True, nullable=False)
    media_type = Column(Enum(MediaType), nullable=False)
    metadata = Column(JSON, nullable=False)
    duration = Column(Integer)  # In seconds
    library_id = Column(Integer, ForeignKey("media_libraries.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    library = relationship("MediaLibrary", back_populates="media_items")
    subtitles = relationship("Subtitle", back_populates="media")
    related_content = relationship(
        "Media",
        secondary="media_relations",
        primaryjoin="Media.id==MediaRelation.media_id",
        secondaryjoin="Media.id==MediaRelation.related_id",
        backref="related_to"
    )

class MediaRelation(Base):
    __tablename__ = "media_relations"
    
    media_id = Column(Integer, ForeignKey("media.id"), primary_key=True)
    related_id = Column(Integer, ForeignKey("media.id"), primary_key=True)
    relation_type = Column(String(50))  # sequel, prequel, collection, etc.
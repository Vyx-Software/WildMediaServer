from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from ..session import Base
import enum

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    profile_icon = Column(String(511))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    created_invites = relationship("InviteCode", back_populates="creator")
    used_invites = relationship("InviteCodeUsage", back_populates="user")
    player_settings = relationship("PlayerSettings", uselist=False, back_populates="user")
    uploaded_subtitles = relationship("Subtitle", back_populates="uploader")

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "with_polymorphic": "*"
    }

class InviteCode(Base):
    __tablename__ = "invite_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    max_uses = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    creator = relationship("User", back_populates="created_invites")
    usages = relationship("InviteCodeUsage", back_populates="invite_code")

    @property
    def used_count(self):
        return len(self.usages)

class InviteCodeUsage(Base):
    __tablename__ = "invite_code_usages"
    
    id = Column(Integer, primary_key=True, index=True)
    used_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invite_code_id = Column(Integer, ForeignKey("invite_codes.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="used_invites")
    invite_code = relationship("InviteCode", back_populates="usages")

    __table_args__ = (
        UniqueConstraint('user_id', 'invite_code_id', name='_user_invite_uc'),
    )
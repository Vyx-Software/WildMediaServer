from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreateAdmin(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = UserRole.USER

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    profile_icon: Optional[str] = Field(
        None, 
        regex="^data:image/(png|jpeg);base64,[a-zA-Z0-9+/]+=*$"
    )

class PasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=100)
    new_password: str = Field(..., min_length=8, max_length=100)

class UserResponse(UserBase):
    id: int
    role: UserRole
    profile_icon: Optional[str]
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True
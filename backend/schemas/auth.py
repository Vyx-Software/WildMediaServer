from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, root_validator
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$")
    password: str = Field(..., min_length=8, max_length=100)
    invite_code: str = Field(..., min_length=8, max_length=32)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "media_lover",
                "password": "strongpassword123",
                "invite_code": "ABCD-1234-EFGH-5678"
            }
        }

class InviteCodeCreate(BaseModel):
    code: str = Field(..., min_length=8, max_length=32)
    expires_at: Optional[datetime] = None
    max_uses: Optional[int] = Field(1, ge=1)

class InviteCodeResponse(BaseModel):
    code: str
    created_at: datetime
    expires_at: Optional[datetime]
    uses_left: int
    is_active: bool

    class Config:
        orm_mode = True
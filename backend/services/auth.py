from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.database.models.user import User, InviteCode
from backend.config import settings
from backend.schemas.auth import TokenData
from backend.utils.exceptions import (
    InvalidCredentialsException,
    InactiveUserException,
    InvalidInviteCodeException
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise InvalidCredentialsException()
        return TokenData(username=username, role=role)
    except JWTError:
        raise InvalidCredentialsException()

def validate_invite_code(db: Session, code: str) -> bool:
    invite_code = db.query(InviteCode).filter(
        InviteCode.code == code,
        InviteCode.expires_at > datetime.utcnow(),
        InviteCode.used == False
    ).first()
    
    if not invite_code:
        return False
    
    invite_code.used = True
    db.commit()
    return True
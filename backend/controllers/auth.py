from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database.models.user import User
from backend.database.session import get_db
from backend.schemas.auth import Token, UserCreate, InviteCodeCreate
from backend.services.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
    validate_invite_code
)
from backend.services.user import create_user, get_current_admin, get_user_by_username
from backend.config import settings

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(
    user_data: UserCreate,
    invite_code: str,
    db: Session = Depends(get_db)
):
    if not validate_invite_code(db, invite_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired invite code"
        )
    
    hashed_password = get_password_hash(user_data.password)
    db_user = create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role="user"
    )
    return {"message": "User created successfully", "user_id": db_user.id}

@router.post("/admin/invite-codes")
async def create_invite_code(
    code_data: InviteCodeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    db_code = create_invite_code(db, code_data)
    return {"code": db_code.code, "expires_at": db_code.expires_at}
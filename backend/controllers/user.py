from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.models.user import User
from backend.database.session import get_db
from backend.schemas.user import (
    UserUpdate,
    PasswordUpdate,
    UserResponse,
    UserCreateAdmin
)
from backend.services.auth import verify_password
from backend.services.user import (
    get_current_user,
    get_current_admin,
    update_user_profile,
    change_user_password,
    create_user_admin,
    get_all_users,
    delete_user
)

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me")
async def update_self(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_user = update_user_profile(db, current_user.id, user_data)
    return {"message": "Profile updated", "user": updated_user}

@router.put("/me/password")
async def change_password(
    password_data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    change_user_password(db, current_user.id, password_data.new_password)
    return {"message": "Password updated successfully"}

@router.post("/admin/users")
async def admin_create_user(
    user_data: UserCreateAdmin,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    user = create_user_admin(db, user_data)
    return {"message": "User created", "user_id": user.id}

@router.get("/admin/users")
async def admin_get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    users = get_all_users(db, skip=skip, limit=limit)
    return users

@router.delete("/admin/users/{user_id}")
async def admin_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    delete_user(db, user_id)
    return {"message": "User deleted"}
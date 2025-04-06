import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from jose import JWTError, jwt
from backend.database.models import (
    User, 
    UserRole,
    InviteCode,
    InviteCodeUsage,
    PlayerSettings
)
from backend.config import settings
from backend.utils.exceptions import (
    InvalidCredentialsException,
    InactiveUserException,
    PermissionDeniedException,
    UserNotFoundException,
    DuplicateUserException,
    InvalidPasswordChangeException,
    InviteCodeException,
    SettingsUpdateException
)

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Get user by username with case-insensitive search"""
        return db.query(User).filter(User.username.ilike(username)).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email with case-insensitive search"""
        return db.query(User).filter(User.email.ilike(email)).first()

    @staticmethod
    def get_current_user(db: Session, token: str) -> User:
        """Get active user from JWT token"""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            username = payload.get("sub")
            if not username:
                raise InvalidCredentialsException()
            
            user = UserService.get_user_by_username(db, username=username)
            if not user or not user.is_active:
                raise InactiveUserException()
                
            return user
            
        except JWTError as e:
            raise InvalidCredentialsException() from e

    @staticmethod
    def get_current_admin(db: Session, token: str) -> User:
        """Get and validate admin user from JWT token"""
        user = UserService.get_current_user(db, token)
        if user.role != UserRole.ADMIN:
            raise PermissionDeniedException()
        return user

    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        """Create new user with password hashing and duplicate checks"""
        try:
            if UserService.get_user_by_username(db, user_data['username']):
                raise DuplicateUserException(context={"field": "username"})
                
            if UserService.get_user_by_email(db, user_data['email']):
                raise DuplicateUserException(context={"field": "email"})
                
            hashed_password = pwd_context.hash(user_data['password'])
            user = User(
                username=user_data['username'].lower(),
                email=user_data['email'].lower(),
                hashed_password=hashed_password,
                role=UserRole.USER
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Initialize default player settings
            UserService.update_user_settings(db, user.id, {})
            
            return user
            
        except IntegrityError as e:
            db.rollback()
            raise DuplicateUserException() from e
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error creating user: {str(e)}")
            raise UserNotFoundException() from e

    @staticmethod
    def create_user_admin(db: Session, user_data: dict) -> User:
        """Admin-specific user creation with role assignment"""
        try:
            existing_user = db.query(User).filter(
                (User.username.ilike(user_data['username'])) |
                (User.email.ilike(user_data['email']))
            ).first()
            
            if existing_user:
                raise DuplicateUserException()
                
            user = User(
                username=user_data['username'].lower(),
                email=user_data['email'].lower(),
                hashed_password=pwd_context.hash(user_data['password']),
                role=user_data.get('role', UserRole.USER),
                is_active=user_data.get('is_active', True)
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
            
        except SQLAlchemyError as e:
            db.rollback()
            raise UserNotFoundException() from e

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """Authenticate user with credentials"""
        user = UserService.get_user_by_username(db, username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            raise InvalidCredentialsException()
            
        if not user.is_active:
            raise InactiveUserException()
            
        return user

    @staticmethod
    def update_user_profile(db: Session, user_id: int, update_data: dict) -> User:
        """Update user profile with data validation"""
        try:
            user = db.query(User).get(user_id)
            if not user:
                raise UserNotFoundException()
                
            if 'email' in update_data:
                existing = UserService.get_user_by_email(db, update_data['email'])
                if existing and existing.id != user_id:
                    raise DuplicateUserException(context={"field": "email"})
                user.email = update_data['email'].lower()
                
            if 'username' in update_data:
                existing = UserService.get_user_by_username(db, update_data['username'])
                if existing and existing.id != user_id:
                    raise DuplicateUserException(context={"field": "username"})
                user.username = update_data['username'].lower()
                
            if 'profile_icon' in update_data:
                user.profile_icon = update_data['profile_icon']
                
            db.commit()
            db.refresh(user)
            return user
            
        except SQLAlchemyError as e:
            db.rollback()
            raise UserNotFoundException() from e

    @staticmethod
    def change_user_password(db: Session, user_id: int, old_password: str, new_password: str) -> None:
        """Change user password with old password validation"""
        user = db.query(User).get(user_id)
        if not user:
            raise UserNotFoundException()
            
        if not pwd_context.verify(old_password, user.hashed_password):
            raise InvalidPasswordChangeException()
            
        try:
            user.hashed_password = pwd_context.hash(new_password)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise SettingsUpdateException() from e

    @staticmethod
    def create_invite_code(db: Session, admin_id: int, code_data: dict) -> InviteCode:
        """Create new invite code with admin validation"""
        admin = db.query(User).get(admin_id)
        if not admin or admin.role != UserRole.ADMIN:
            raise PermissionDeniedException()
            
        try:
            expires_at = datetime.utcnow() + timedelta(days=code_data.get('expiry_days', 7))
            
            invite_code = InviteCode(
                code=code_data['code'],
                expires_at=expires_at,
                max_uses=code_data.get('max_uses', 1),
                creator_id=admin_id
            )
            
            db.add(invite_code)
            db.commit()
            db.refresh(invite_code)
            return invite_code
            
        except IntegrityError as e:
            db.rollback()
            raise InviteCodeException("Invite code already exists") from e
        except SQLAlchemyError as e:
            db.rollback()
            raise InviteCodeException("Failed to create invite code") from e

    @staticmethod
    def validate_invite_code(db: Session, code: str) -> bool:
        """Validate and consume invite code"""
        try:
            invite = db.query(InviteCode).filter(
                InviteCode.code == code,
                InviteCode.expires_at > datetime.utcnow(),
                InviteCode.is_active == True
            ).first()
            
            if not invite or len(invite.usages) >= invite.max_uses:
                return False
                
            usage = InviteCodeUsage(
                invite_code_id=invite.id,
                user_id=None  # Set after user creation
            )
            
            db.add(usage)
            db.commit()
            return True
            
        except SQLAlchemyError as e:
            db.rollback()
            raise InviteCodeException("Invite code validation failed") from e

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """Get paginated list of users"""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        """Delete user account"""
        try:
            user = db.query(User).get(user_id)
            if not user:
                raise UserNotFoundException()
                
            db.delete(user)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise UserNotFoundException() from e

    @staticmethod
    def update_user_settings(db: Session, user_id: int, settings: dict) -> PlayerSettings:
        """Update or create player settings for user"""
        try:
            db_settings = db.query(PlayerSettings).filter(
                PlayerSettings.user_id == user_id
            ).first()
            
            if not db_settings:
                db_settings = PlayerSettings(user_id=user_id)
                db.add(db_settings)
                
            for key, value in settings.items():
                if hasattr(db_settings, key):
                    setattr(db_settings, key, value)
                    
            db.commit()
            db.refresh(db_settings)
            return db_settings
            
        except SQLAlchemyError as e:
            db.rollback()
            raise SettingsUpdateException() from e

    @staticmethod
    def get_user_settings(db: Session, user_id: int) -> PlayerSettings:
        """Get user's player settings"""
        settings = db.query(PlayerSettings).filter(
            PlayerSettings.user_id == user_id
        ).first()
        
        if not settings:
            raise SettingsUpdateException("Settings not found")
            
        return settings
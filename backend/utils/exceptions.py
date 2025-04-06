from fastapi import HTTPException, status
from typing import Optional, Dict, Any

class APIException(HTTPException):
    """Base exception class for API errors"""
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": message,
                "context": context or {}
            }
        )
        self.error_code = error_code
        self.context = context

# Authentication & Authorization Exceptions
class InvalidCredentialsException(APIException):
    """Invalid username/password combination"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="invalid_credentials",
            message="Invalid username or password",
            context=context
        )

class InactiveUserException(APIException):
    """User account is disabled"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="inactive_user",
            message="User account is inactive",
            context=context
        )

class PermissionDeniedException(APIException):
    """Insufficient permissions for operation"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="permission_denied",
            message="You don't have permission to perform this action",
            context=context
        )

# User Management Exceptions
class UserNotFoundException(APIException):
    """Requested user not found"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="user_not_found",
            message="User not found",
            context=context
        )

class DuplicateUserException(APIException):
    """Username/email already exists"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code="duplicate_user",
            message="User with this username or email already exists",
            context=context
        )

class InvalidPasswordChangeException(APIException):
    """Invalid password change attempt"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="invalid_password_change",
            message="Current password is incorrect",
            context=context
        )

# Media & Library Exceptions
class MediaNotFoundException(APIException):
    """Requested media not found"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="media_not_found",
            message="Media file not found",
            context=context
        )

class InvalidMediaTypeException(APIException):
    """Invalid media type specified"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="invalid_media_type",
            message="Invalid media type specified",
            context=context
        )

class DirectoryScanException(APIException):
    """Directory scanning failed"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="directory_scan_failed",
            message="Failed to scan media directory",
            context=context
        )

# Subtitle Exceptions
class SubtitleDownloadException(APIException):
    """Subtitle download failed"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="subtitle_download_failed",
            message="Failed to download subtitles",
            context=context
        )

class SubtitleConversionException(APIException):
    """Subtitle format conversion failed"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="subtitle_conversion_failed",
            message="Subtitle format conversion failed",
            context=context
        )

class SubtitleSyncException(APIException):
    """Subtitle synchronization failed"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code="subtitle_sync_failed",
            message="Subtitles are not synchronized with media",
            context=context
        )

class InvalidSubtitleException(APIException):
    """Invalid subtitle file format/content"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error_code="invalid_subtitle",
            message="Invalid subtitle file format or content",
            context=context
        )

class SubtitleParseException(APIException):
    """Subtitle parsing failed"""
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="subtitle_parse_failed",
            message="Failed to parse subtitle file",
            context=context
        )

# Common Error Codes
COMMON_ERROR_CODES = {
    # Authentication
    "invalid_credentials": "Invalid username or password",
    "inactive_user": "User account is disabled",
    "permission_denied": "Insufficient permissions",
    
    # User Management
    "user_not_found": "User not found",
    "duplicate_user": "User already exists",
    
    # Media
    "media_not_found": "Media file not found",
    "invalid_media_type": "Unsupported media type",
    
    # Subtitle
    "subtitle_download_failed": "Subtitle download failed",
    "subtitle_conversion_failed": "Format conversion failed",
    "subtitle_sync_failed": "Subtitle synchronization failed",
    "invalid_subtitle": "Invalid subtitle file"
}
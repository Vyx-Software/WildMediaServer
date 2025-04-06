from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.models import User, MediaLibrary
from backend.database.session import get_db
from backend.schemas.media import (
    MediaLibraryCreate,
    MediaLibraryResponse,
    MediaItemResponse,
    MediaScanResult
)
from backend.services.media import (
    create_media_library,
    scan_media_directory,
    get_all_libraries,
    get_library_by_id,
    get_library_media
)
from backend.services.user import get_current_admin, get_current_user
from backend.utils.exceptions import (
    MediaNotFoundException,
    DirectoryScanException,
    InvalidMediaTypeException
)

router = APIRouter()

@router.post("/libraries", response_model=MediaLibraryResponse)
async def create_library(
    library_data: MediaLibraryCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Create a new media library with admin privileges"""
    try:
        library = create_media_library(db, {
            "name": library_data.name,
            "path": library_data.path,
            "media_type": library_data.media_type,
            "owner_id": admin.id
        })
        return library
    except DirectoryScanException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid library path: {e.context.get('path')}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to create media library"
        )

@router.post("/libraries/{library_id}/scan", response_model=MediaScanResult)
async def scan_library(
    library_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Scan a media library for new content"""
    try:
        library = get_library_by_id(db, library_id)
        result = scan_media_directory(db, library.id)
        return {
            "total_files": result["total_files"],
            "new_files": result["new_files"],
            "updated_files": result["updated_files"],
            "failed_files": result["failed_files"]
        }
    except MediaNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DirectoryScanException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Library scan failed"
        )

@router.get("/libraries", response_model=list[MediaLibraryResponse])
async def list_libraries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """List all available media libraries"""
    try:
        return get_all_libraries(db, skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve libraries"
        )

@router.get("/libraries/{library_id}/media", response_model=list[MediaItemResponse])
async def get_library_media(
    library_id: int,
    genre: str = None,
    media_type: str = None,
    sort: str = "title",
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Get media items from a specific library"""
    try:
        return get_library_media(
            db,
            library_id,
            genre=genre,
            media_type=media_type,
            sort=sort
        )
    except MediaNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidMediaTypeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve media items"
        )
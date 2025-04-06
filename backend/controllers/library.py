from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.models.user import User
from backend.database.session import get_db
from backend.schemas.media import LibraryConfig, DirectoryScanResult
from backend.services.media import (
    scan_directory,
    update_library_config,
    get_directory_metadata
)
from backend.services.user import get_current_admin

router = APIRouter()

@router.post("/admin/libraries/scan", response_model=DirectoryScanResult)
async def admin_scan_directory(
    path: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    try:
        scan_result = scan_directory(path)
        return {
            "path": path,
            "total_files": scan_result.total_files,
            "media_files": scan_result.media_files,
            "subtitles_found": scan_result.subtitles_found
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/admin/libraries/config")
async def update_config(
    config: LibraryConfig,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    updated_config = update_library_config(db, config)
    return {"message": "Library config updated", "config": updated_config}

@router.get("/admin/libraries/metadata")
async def get_directory_metadata(
    path: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    metadata = get_directory_metadata(path)
    return metadata
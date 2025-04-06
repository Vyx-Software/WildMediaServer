from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from backend.database.models import User, Media
from backend.database.session import get_db
from backend.schemas.media import (
    PlaybackRequest,
    SubtitleConfig,
    PlayerSettings
)
from backend.services.media import (
    get_media_item,
    get_media_stream,
    get_subtitle_file,
    get_related_media
)
from backend.services.user import (
    get_current_user,
    update_user_settings,
    get_user_settings
)
from backend.utils.exceptions import (
    MediaNotFoundException,
    SubtitleNotFoundException,
    SettingsUpdateException
)

router = APIRouter()

@router.get("/stream/{media_id}")
async def stream_media(
    media_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Stream media content with byte-range support"""
    try:
        media = get_media_item(db, media_id)
        if not media:
            raise MediaNotFoundException()
        
        range_header = request.headers.get("range")
        stream_gen = get_media_stream(media.file_path, range_header)
        
        return StreamingResponse(
            content=stream_gen["content"],
            status_code=stream_gen["status_code"],
            media_type=stream_gen["media_type"],
            headers=stream_gen["headers"]
        )
    except MediaNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to stream media content"
        )

@router.get("/subtitles/{media_id}")
async def get_subtitles(
    media_id: int,
    language: str = "en",
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Get subtitle file for specified media"""
    try:
        subtitle_path = get_subtitle_file(db, media_id, language)
        return FileResponse(
            subtitle_path,
            media_type="text/vtt",
            headers={
                "Content-Disposition": f"inline; filename={subtitle_path.name}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except SubtitleNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve subtitles"
        )

@router.post("/settings")
async def update_player_settings(
    settings: PlayerSettings,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Update user-specific player settings"""
    try:
        updated = update_user_settings(db, user.id, settings.dict())
        return {
            "message": "Player settings updated",
            "settings": {
                "subtitle_font": updated.subtitle_font,
                "subtitle_size": updated.subtitle_size,
                "subtitle_color": updated.subtitle_color,
                "default_quality": updated.default_quality
            }
        }
    except SettingsUpdateException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to update settings"
        )

@router.get("/related/{media_id}")
async def get_related_content(
    media_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Get related media content"""
    try:
        related = get_related_media(db, media_id)
        return {"related": [{
            "id": media.id,
            "title": media.name,
            "type": media.media_type.value,
            "thumbnail": media.metadata.get("thumbnail")
        } for media in related]}
    except MediaNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to find related content"
        )
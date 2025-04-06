import os
from sqlalchemy.orm import Session
from pathlib import Path
from backend.database.models.media import Media, MediaLibrary
from backend.utils.file_scanner import (
    scan_directory,
    get_directory_metadata
)
from backend.utils.exceptions import (
    InvalidPathException,
    LibraryNotFoundException
)

def validate_library_path(path: str) -> None:
    path_obj = Path(path)
    if not path_obj.exists():
        raise InvalidPathException(f"Path does not exist: {path}")
    if not path_obj.is_dir():
        raise InvalidPathException(f"Path is not a directory: {path}")
    if not os.access(path, os.R_OK):
        raise InvalidPathException(f"Read access denied: {path}")

def update_library_config(db: Session, library_id: int, config: dict) -> MediaLibrary:
    library = db.query(MediaLibrary).get(library_id)
    if not library:
        raise LibraryNotFoundException()
    
    if 'path' in config:
        validate_library_path(config['path'])
        library.path = config['path']
    
    if 'auto_scan' in config:
        library.auto_scan = config['auto_scan']
    
    if 'media_type' in config:
        library.media_type = config['media_type']
    
    db.commit()
    db.refresh(library)
    return library

def get_library_stats(db: Session, library_id: int) -> dict:
    library = db.query(MediaLibrary).get(library_id)
    if not library:
        raise LibraryNotFoundException()
    
    stats = {
        'total_media': db.query(Media).filter(
            Media.library_id == library_id).count(),
        'movies': db.query(Media).filter(
            Media.library_id == library_id,
            Media.media_type == 'movie').count(),
        'shows': db.query(Media).filter(
            Media.library_id == library_id,
            Media.media_type == 'show').count(),
        'last_scan': library.last_scan,
        'storage_used': sum(
            m.metadata.get('size', 0) 
            for m in library.media_items
        )
    }
    
    return stats
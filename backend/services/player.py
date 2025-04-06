import os
import subprocess
from pathlib import Path
from typing import Generator
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.database.models.media import Media
from backend.config import settings
from backend.utils.exceptions import (
    MediaNotFoundException,
    SubtitleNotFoundException
)

def get_media_stream(file_path: str, range_header: str) -> Generator:
    file_size = os.path.getsize(file_path)
    start, end = 0, file_size - 1
    
    if range_header:
        range_ = range_header.split("=")[1]
        start, end = map(int, range_.split("-"))
    
    chunk_size = 1024 * 1024  # 1MB chunks
    with open(file_path, "rb") as video_file:
        video_file.seek(start)
        remaining = end - start + 1
        while remaining > 0:
            bytes_to_read = min(chunk_size, remaining)
            data = video_file.read(bytes_to_read)
            if not data:
                break
            remaining -= len(data)
            yield data

def convert_subtitle_to_vtt(srt_path: Path) -> Path:
    vtt_path = srt_path.with_suffix(".vtt")
    try:
        subprocess.run(
            ["ffmpeg", "-i", str(srt_path), str(vtt_path)],
            check=True,
            capture_output=True
        )
        return vtt_path
    except subprocess.CalledProcessError as e:
        raise SubtitleNotFoundException(
            f"Subtitle conversion failed: {e.stderr.decode()}")

def get_subtitle_file(media_id: int, language: str) -> Path:
    media = Media.query.get(media_id)
    if not media:
        raise MediaNotFoundException()
    
    media_path = Path(media.file_path)
    subtitle_dir = settings.SUBTITLE_DIR / str(media_id)
    
    # Check for existing converted VTT files
    vtt_file = subtitle_dir / f"{language}.vtt"
    if vtt_file.exists():
        return vtt_file
    
    # Check for SRT files and convert
    srt_file = subtitle_dir / f"{language}.srt"
    if srt_file.exists():
        return convert_subtitle_to_vtt(srt_file)
    
    # Fallback to opensubtitles integration
    return fetch_opensubtitles(media, language)

def fetch_opensubtitles(media: Media, language: str) -> Path:
    # Implementation for OpenSubtitles API integration
    raise SubtitleNotFoundException("Subtitles not available")
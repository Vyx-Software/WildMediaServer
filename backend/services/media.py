import os
import re
import logging
from pathlib import Path
import subprocess
from guessit import guessit  # Added local metadata parser
from sqlalchemy.orm import Session
from backend.config import settings
from backend.utils.exceptions import MediaProcessingError

logger = logging.getLogger(__name__)

class MediaService:
    @staticmethod
    def extract_metadata(file_path: Path) -> dict:
        """Extract metadata using filename analysis and local file properties"""
        try:
            # Parse filename with guessit
            guess = guessit(str(file_path))
            
            # Get basic file info
            stat = file_path.stat()
            
            # Build metadata
            metadata = {
                'title': guess.get('title', file_path.stem),
                'year': guess.get('year'),
                'duration': MediaService._get_local_duration(file_path),
                'resolution': guess.get('screen_size'),
                'type': guess.get('type', 'movie'),
                'season': guess.get('season'),
                'episode': guess.get('episode'),
                'file_size': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime
            }
            
            # Add video codec if detected
            if guess.get('video_codec'):
                metadata['video_codec'] = guess.get('video_codec')
                
            # Add audio codec if detected
            if guess.get('audio_codec'):
                metadata['audio_codec'] = guess.get('audio_codec')
                
            return metadata
            
        except Exception as e:
            logger.error(f"Local metadata extraction failed: {str(e)}")
            return {}

    @staticmethod
    def _get_local_duration(path: Path) -> float:
        """Get duration using ffprobe"""
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 
                 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return float(result.stdout.decode().strip())
        except Exception as e:
            logger.warning(f"Duration detection failed: {str(e)}")
            return 0.0
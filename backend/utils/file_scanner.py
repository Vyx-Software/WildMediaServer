import os
import logging
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
from backend.config import settings

logger = logging.getLogger(__name__)

class FileScanner:
    MEDIA_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov', 'flv'}
    SUB_EXTENSIONS = {'srt', 'vtt', 'ass'}

    @classmethod
    def scan_directory(cls, path: Path) -> Tuple[List[Dict], List[Dict]]:
        """Scan directory and return media/subtitle files with metadata"""
        media_files = []
        subtitle_files = []
        
        try:
            for entry in path.rglob('*'):
                if entry.is_file():
                    ext = entry.suffix[1:].lower()
                    metadata = cls._get_file_metadata(entry)
                    
                    if ext in cls.MEDIA_EXTENSIONS:
                        media_files.append(metadata)
                    elif ext in cls.SUB_EXTENSIONS:
                        subtitle_files.append(metadata)
                        
        except Exception as e:
            logger.error(f"Directory scan failed: {str(e)}")
            
        return media_files, subtitle_files

    @classmethod
    def find_new_files(cls, path: Path, last_scan: float) -> List[Dict]:
        """Find files modified since last scan"""
        new_files = []
        try:
            for entry in path.rglob('*'):
                if entry.is_file() and entry.stat().st_mtime > last_scan:
                    new_files.append(cls._get_file_metadata(entry))
        except Exception as e:
            logger.error(f"New file detection failed: {str(e)}")
        return new_files

    @staticmethod
    def _get_file_metadata(path: Path) -> Dict:
        stat = path.stat()
        return {
            "path": str(path),
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "created": stat.st_ctime,
            "hash": FileScanner.calculate_hash(path),
            "extension": path.suffix[1:].lower()
        }

    @staticmethod
    def calculate_hash(path: Path) -> str:
        """Calculate BLAKE2b file hash with chunked reading"""
        blake = hashlib.blake2b()
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                blake.update(chunk)
        return blake.hexdigest()
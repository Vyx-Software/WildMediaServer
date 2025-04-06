import os
import hashlib
from pathlib import Path
from typing import List, Dict
from backend.config import settings

MEDIA_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov', 'flv'}

def scan_directory(path: str) -> List[Dict]:
    media_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.split('.')[-1].lower() in MEDIA_EXTENSIONS:
                file_path = Path(root) / file
                media_files.append({
                    'path': str(file_path),
                    'size': file_path.stat().st_size,
                    'modified': file_path.stat().st_mtime,
                    'hash': calculate_file_hash(file_path)
                })
    return media_files

def calculate_file_hash(file_path: Path, chunk_size: int = 8192) -> str:
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_directory_metadata(path: str) -> Dict:
    path_obj = Path(path)
    if not path_obj.is_dir():
        return {}
    
    return {
        'total_size': sum(f.stat().st_size for f in path_obj.glob('**/*') if f.is_file()),
        'file_count': sum(1 for _ in path_obj.glob('**/*') if _.is_file()),
        'media_files': scan_directory(path)
    }
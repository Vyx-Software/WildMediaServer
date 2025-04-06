import re
import unicodedata
from pathlib import Path

class NameBeautifier:
    @staticmethod
    def beautify(filename: str) -> str:
        """
        Clean media filenames by removing unwanted patterns and normalizing
        """
        # Remove file extension
        name = Path(filename).stem
        
        # Remove common scene tags and metadata
        patterns = [
            r'\[.*?\]', r'\(.*?\)', r'\b(?:WEB|BD|DVD|RIP|HD|HQ|UHD|HDR|SDR)\b',
            r'\b(?:x264|x265|HEVC|AVC|AAC|AC3|DTS)\b',
            r'\b(?:5\.1|7\.1|2\.0|CH|Dual)\b',
            r'\b(?:REPACK|PROPER|READNFO|NFO)\b',
            r'[-_.]{2,}', r'^[-_.]+', r'[-_.]+$'
        ]
        
        for pattern in patterns:
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)
            
        # Remove resolution patterns
        name = re.sub(r'\b\d{3,4}p\b', '', name)
        
        # Normalize special characters
        name = unicodedata.normalize('NFKD', name)
        name = name.encode('ascii', 'ignore').decode()
        
        # Clean remaining special characters
        name = re.sub(r'[^\w\s-]', '', name)
        
        # Handle year notations
        name = re.sub(r'(?<!\d)(\d{4})(?!\d)', r'(\1)', name)
        
        # Final cleanup
        name = re.sub(r'\s+', ' ', name).strip()
        return name

    @staticmethod
    def generate_filesafe_name(name: str) -> str:
        """Generate filesystem-safe version of the name"""
        safe_name = re.sub(r'[^\w\s-]', '', name).strip().lower()
        safe_name = re.sub(r'[-\s]+', '-', safe_name)
        return safe_name[:200]
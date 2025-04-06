import re
import logging
import subprocess
import chardet
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from pysrt import SubRipFile, SubRipItem, SubRipTime, open as open_srt
from webvtt import WebVTT, Caption, MalformedFileError
from ffmpeg import probe
from ffmpeg import Error as FFmpegError

logger = logging.getLogger(__name__)

class SubtitleParserError(Exception):
    """Base exception for subtitle parsing errors"""

class InvalidSubtitleError(SubtitleParserError):
    """Raised when subtitle file is invalid or malformed"""

class SubtitleShiftError(SubtitleParserError):
    """Raised when subtitle shifting fails"""

class SubtitleSyncError(SubtitleParserError):
    """Raised when subtitle synchronization validation fails"""

class SubtitleParser:
    @staticmethod
    def parse(path: Path, encoding: str = None) -> List[Dict]:
        """
        Parse subtitle file into structured format with advanced validation
        Returns list of subtitle entries with start/end times in milliseconds
        """
        try:
            # Detect encoding if not specified
            if not encoding:
                with open(path, 'rb') as f:
                    raw_data = f.read(1024)
                    encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'

            if path.suffix.lower() == '.srt':
                return SubtitleParser._parse_srt(path, encoding)
            elif path.suffix.lower() == '.vtt':
                return SubtitleParser._parse_vtt(path, encoding)
            else:
                raise InvalidSubtitleError(f"Unsupported format: {path.suffix}")
                
        except (UnicodeDecodeError, MalformedFileError) as e:
            logger.error(f"Subtitle decoding failed: {str(e)}")
            raise InvalidSubtitleError("Encoding detection failed") from e
        except Exception as e:
            logger.error(f"Subtitle parsing failed: {str(e)}")
            raise InvalidSubtitleError("Invalid subtitle file") from e

    @staticmethod
    def _parse_srt(path: Path, encoding: str) -> List[Dict]:
        """Parse SRT file with advanced validation"""
        subs = open_srt(path, encoding=encoding)
        parsed = []
        
        for sub in subs:
            if not SubtitleParser._validate_srt_timing(sub):
                logger.warning(f"Invalid timing in subtitle line {sub.index}")
                continue
                
            parsed.append({
                "index": sub.index,
                "start": sub.start.ordinal,
                "end": sub.end.ordinal,
                "text": SubtitleParser._clean_text(sub.text),
                "position": sub.position,
                "coordinates": sub.position
            })
            
        return parsed

    @staticmethod
    def _parse_vtt(path: Path, encoding: str) -> List[Dict]:
        """Parse WebVTT file with cue validation"""
        try:
            vtt = WebVTT().read(path, encoding=encoding)
            parsed = []
            
            for i, caption in enumerate(vtt.captions, start=1):
                start_ms = SubtitleParser._vtt_time_to_ms(caption.start)
                end_ms = SubtitleParser._vtt_time_to_ms(caption.end)
                
                if start_ms >= end_ms:
                    logger.warning(f"Invalid timing in caption {i}")
                    continue
                    
                parsed.append({
                    "index": i,
                    "start": start_ms,
                    "end": end_ms,
                    "text": SubtitleParser._clean_text(caption.text),
                    "styles": caption.identifier,
                    "position": caption.position
                })
                
            return parsed
        except MalformedFileError as e:
            raise InvalidSubtitleError("Malformed WebVTT file") from e

    @staticmethod
    def shift_subtitles(path: Path, offset_seconds: float, output_path: Path = None) -> Path:
        """
        Shift subtitle timings by specified offset in seconds
        Returns path to new shifted subtitle file
        """
        try:
            subs = SubtitleParser.parse(path)
            offset_ms = int(offset_seconds * 1000)
            
            if path.suffix.lower() == '.srt':
                return SubtitleParser._shift_srt(path, offset_ms, output_path)
            elif path.suffix.lower() == '.vtt':
                return SubtitleParser._shift_vtt(path, offset_ms, output_path)
            else:
                raise InvalidSubtitleError("Unsupported format for shifting")
                
        except Exception as e:
            logger.error(f"Subtitle shifting failed: {str(e)}")
            raise SubtitleShiftError("Failed to shift subtitles") from e

    @staticmethod
    def _shift_srt(original_path: Path, offset_ms: int, output_path: Path) -> Path:
        subs = open_srt(original_path)
        for sub in subs:
            sub.start += offset_ms
            sub.end += offset_ms
            
        output_path = output_path or original_path.with_stem(f"{original_path.stem}_shifted")
        subs.save(output_path, encoding='utf-8')
        return output_path

    @staticmethod
    def _shift_vtt(original_path: Path, offset_ms: int, output_path: Path) -> Path:
        vtt = WebVTT().read(original_path)
        for caption in vtt.captions:
            caption.start = SubtitleParser._ms_to_vtt_time(
                SubtitleParser._vtt_time_to_ms(caption.start) + offset_ms
            )
            caption.end = SubtitleParser._ms_to_vtt_time(
                SubtitleParser._vtt_time_to_ms(caption.end) + offset_ms
            )
            
        output_path = output_path or original_path.with_stem(f"{original_path.stem}_shifted")
        vtt.save(output_path)
        return output_path

    @staticmethod
    def validate_sync(media_path: Path, subtitle_path: Path, tolerance: float = 0.05) -> bool:
        """
        Validate subtitle synchronization using media duration
        tolerance: allowed relative difference (5% default)
        """
        try:
            media_info = probe(media_path)
            media_duration = float(media_info['format']['duration']) * 1000  # to ms
            
            sub_duration = SubtitleParser.calculate_subtitle_duration(subtitle_path)
            relative_diff = abs(media_duration - sub_duration) / media_duration
            
            if relative_diff > tolerance:
                logger.warning(f"Subtitle sync mismatch: {relative_diff:.2%}")
                return False
                
            return True
            
        except FFmpegError as e:
            logger.error(f"FFprobe error: {str(e)}")
            raise SubtitleSyncError("Media duration detection failed") from e
        except Exception as e:
            logger.error(f"Sync validation failed: {str(e)}")
            raise SubtitleSyncError("Sync validation error") from e

    @staticmethod
    def calculate_subtitle_duration(path: Path) -> float:
        """Calculate total subtitle duration in milliseconds"""
        subs = SubtitleParser.parse(path)
        if not subs:
            return 0.0
        return subs[-1]['end'] - subs[0]['start']

    @staticmethod
    def convert_format(
        input_path: Path,
        output_format: str,
        output_path: Path = None,
        encoding: str = 'utf-8'
    ) -> Path:
        """
        Convert between subtitle formats (SRT <-> VTT)
        Returns path to converted file
        """
        if output_format.lower() not in ('srt', 'vtt'):
            raise InvalidSubtitleError("Unsupported output format")

        try:
            subs = SubtitleParser.parse(input_path)
            output_path = output_path or input_path.with_suffix(f".{output_format}")
            
            if output_format.lower() == 'srt':
                SubtitleParser._write_srt(subs, output_path, encoding)
            else:
                SubtitleParser._write_vtt(subs, output_path, encoding)
                
            return output_path
            
        except Exception as e:
            logger.error(f"Format conversion failed: {str(e)}")
            raise SubtitleParserError("Conversion failed") from e

    @staticmethod
    def _write_srt(subs: List[Dict], output_path: Path, encoding: str):
        srt_file = SubRipFile()
        for i, sub in enumerate(subs, start=1):
            srt_file.append(SubRipItem(
                index=i,
                start=SubRipTime(milliseconds=sub['start']),
                end=SubRipTime(milliseconds=sub['end']),
                text=sub['text']
            ))
        srt_file.save(output_path, encoding=encoding)

    @staticmethod
    def _write_vtt(subs: List[Dict], output_path: Path, encoding: str):
        vtt = WebVTT()
        for sub in subs:
            caption = Caption(
                SubtitleParser._ms_to_vtt_time(sub['start']),
                SubtitleParser._ms_to_vtt_time(sub['end']),
                sub['text']
            )
            vtt.captions.append(caption)
        vtt.save(output_path)

    @staticmethod
    def _validate_srt_timing(sub: SubRipItem) -> bool:
        """Validate SRT entry timing consistency"""
        return sub.start.ordinal < sub.end.ordinal

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean subtitle text from formatting and artifacts"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove duplicated newlines
        text = re.sub(r'\n{2,}', '\n', text)
        # Trim whitespace
        return text.strip()

    @staticmethod
    def _vtt_time_to_ms(time_str: str) -> int:
        """Convert VTT timestamp to milliseconds"""
        if '.' in time_str:
            time_format = "%H:%M:%S.%f"
        else:
            time_format = "%H:%M:%S"
            
        dt = datetime.strptime(time_str, time_format)
        delta = timedelta(
            hours=dt.hour,
            minutes=dt.minute,
            seconds=dt.second,
            microseconds=dt.microsecond
        )
        return int(delta.total_seconds() * 1000)

    @staticmethod
    def _ms_to_vtt_time(milliseconds: int) -> str:
        """Convert milliseconds to VTT timestamp format"""
        seconds, ms = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}.{ms:03}"
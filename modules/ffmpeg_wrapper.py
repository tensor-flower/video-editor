"""FFmpeg wrapper for video operations."""
import subprocess
import os
from typing import Optional


def check_ffmpeg_installed() -> bool:
    """
    Check if FFmpeg is installed and accessible.

    Returns:
        True if ffmpeg and ffprobe are available
    """
    try:
        subprocess.run(
            ['ffmpeg', '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        subprocess.run(
            ['ffprobe', '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def probe_duration(video_path: str) -> float:
    """
    Get video duration using ffprobe.

    Args:
        video_path: Path to video file

    Returns:
        Duration in seconds (float)

    Raises:
        RuntimeError: If ffprobe fails
    """
    try:
        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )

        duration_str = result.stdout.strip()
        return float(duration_str)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to probe video: {e.stderr}")
    except ValueError:
        raise RuntimeError(f"Invalid duration value: {result.stdout}")


def split_video(
    input_path: str,
    output_path: str,
    start: float,
    duration: float,
    show_progress: bool = True,
    reencode: bool = False
) -> None:
    """
    Extract a video clip.

    Args:
        input_path: Source video file
        output_path: Output clip path
        start: Start time in seconds
        duration: Duration of clip in seconds
        show_progress: Whether to show ffmpeg progress output
        reencode: Re-encode for perfect sync (slower, but eliminates A/V desync)

    Raises:
        RuntimeError: If ffmpeg fails
    """
    if reencode:
        # Re-encode mode: Perfect A/V sync but slower
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output file
            '-ss', str(start),  # Start time
            '-i', input_path,  # Input file
            '-t', str(duration),  # Duration
            '-c:v', 'libx264',  # Re-encode video with H.264
            '-preset', 'fast',  # Fast encoding preset
            '-crf', '18',  # High quality (lower = better)
            '-c:a', 'aac',  # Re-encode audio
            '-b:a', '192k',  # Audio bitrate
            '-af', 'aresample=async=1',  # Audio sync
            '-vsync', 'cfr',  # Constant frame rate
            output_path
        ]
    else:
        # Stream copy mode: Fast but may have slight keyframe offset
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output file
            '-ss', str(start),  # Start time (fast seek to keyframe)
            '-i', input_path,  # Input file
            '-t', str(duration),  # Duration
            '-c', 'copy',  # Stream copy (no re-encoding)
            '-avoid_negative_ts', 'make_zero',  # Reset timestamps to 0
            '-map', '0:v:0',  # Map first video stream
            '-map', '0:a:0',  # Map first audio stream
            output_path
        ]

    if not show_progress:
        cmd.extend(['-v', 'error'])

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE if not show_progress else None,
            stderr=subprocess.PIPE if not show_progress else None,
            check=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        raise RuntimeError(f"Failed to split video: {error_msg}")


def merge_videos(
    clip_paths: list,
    output_path: str,
    temp_dir: str,
    show_progress: bool = True,
    reencode: bool = False
) -> None:
    """
    Merge multiple video clips using concat demuxer.

    Args:
        clip_paths: List of video clip paths (in order)
        output_path: Final merged output path
        temp_dir: Temporary directory for filelist
        show_progress: Whether to show ffmpeg progress output
        reencode: Re-encode during merge for perfect sync

    Raises:
        RuntimeError: If ffmpeg fails
    """
    # Create filelist.txt for concat demuxer
    filelist_path = os.path.join(temp_dir, 'filelist.txt')

    with open(filelist_path, 'w') as f:
        for clip_path in clip_paths:
            # Use absolute paths and escape single quotes
            abs_path = os.path.abspath(clip_path)
            f.write(f"file '{abs_path}'\n")

    if reencode:
        # Re-encode during merge for perfect sync
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output file
            '-f', 'concat',  # Concat demuxer
            '-safe', '0',  # Allow absolute paths
            '-i', filelist_path,  # Input filelist
            '-c:v', 'libx264',  # Re-encode video
            '-preset', 'fast',  # Fast encoding
            '-crf', '18',  # High quality
            '-c:a', 'aac',  # Re-encode audio
            '-b:a', '192k',  # Audio bitrate
            '-af', 'aresample=async=1',  # Audio sync
            '-vsync', 'cfr',  # Constant frame rate
            output_path
        ]
    else:
        # Stream copy (fast but may have slight offset)
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output file
            '-f', 'concat',  # Concat demuxer
            '-safe', '0',  # Allow absolute paths
            '-i', filelist_path,  # Input filelist
            '-c', 'copy',  # Stream copy (no re-encoding)
            '-avoid_negative_ts', 'make_zero',  # Ensure proper timestamp handling
            '-fflags', '+genpts',  # Generate presentation timestamps
            '-map', '0:v:0',  # Map first video stream
            '-map', '0:a:0',  # Map first audio stream
            output_path
        ]

    if not show_progress:
        cmd.extend(['-v', 'error'])

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE if not show_progress else None,
            stderr=subprocess.PIPE if not show_progress else None,
            check=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        raise RuntimeError(f"Failed to merge videos: {error_msg}")

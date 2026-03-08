#!/usr/bin/env python3
"""
Interactive Video Editor - Main Application

Allows users to select multiple timestamp ranges from a video file
and merge them into a single output video, ordered by start timestamp.
"""
import os
import sys
from typing import List, Tuple

from modules import ffmpeg_wrapper
from modules import timestamp_parser
from modules import cli_handler
from modules import file_manager


# Configuration
INPUT_VIDEO = 'input.MP4'
OUTPUT_VIDEO = 'output_final.mp4'

# Performance vs Quality trade-off:
# - REENCODE_MODE = False: Fast (stream copy), may have 20-50ms A/V offset from keyframe seeking
# - REENCODE_MODE = True: Slower (re-encodes), perfect A/V sync, slight quality loss
REENCODE_MODE = False  # Set to True if you experience audio desync


def validate_environment() -> None:
    """
    Validate that all requirements are met.

    Raises:
        RuntimeError: If requirements aren't met
    """
    # Check FFmpeg installation
    if not ffmpeg_wrapper.check_ffmpeg_installed():
        raise RuntimeError(
            "FFmpeg is not installed or not in PATH.\n"
            "Install it with: brew install ffmpeg (macOS) or "
            "apt-get install ffmpeg (Linux)"
        )

    # Validate input file
    file_manager.validate_input_file(INPUT_VIDEO)

    # Ensure output is writable
    file_manager.ensure_output_writable(OUTPUT_VIDEO)


def collect_ranges(duration: float) -> List[Tuple[float, float]]:
    """
    Interactively collect timestamp ranges from user.

    Args:
        duration: Video duration in seconds

    Returns:
        List of (start, end) tuples in seconds
    """
    ranges = []

    while True:
        # Prompt for range
        user_input = cli_handler.prompt_range(len(ranges))

        # Handle EOF or done
        if user_input is None or user_input.lower() == 'done':
            break

        # Skip empty input
        if not user_input:
            continue

        try:
            # Parse range
            start, end = timestamp_parser.parse_range(user_input)

            # Validate range
            timestamp_parser.validate_range(start, end, duration)

            # Add to list
            ranges.append((start, end))
            cli_handler.confirm_range(start, end)

        except ValueError as e:
            cli_handler.print_error(str(e))
            continue

    return ranges


def extract_clips(
    input_path: str,
    ranges: List[Tuple[float, float]],
    temp_manager: file_manager.TempFileManager,
    reencode: bool = False
) -> List[Tuple[str, float]]:
    """
    Extract video clips for each range.

    Args:
        input_path: Input video path
        ranges: List of (start, end) tuples
        temp_manager: Temporary file manager
        reencode: Re-encode clips for perfect sync

    Returns:
        List of (clip_path, start_time) tuples
    """
    clips = []

    for idx, (start, end) in enumerate(ranges):
        clip_path = temp_manager.get_clip_path(idx)
        duration = end - start

        mode_str = "Re-encoding" if reencode else "Extracting"
        cli_handler.print_progress(
            f"{mode_str} clip {idx + 1}/{len(ranges)}: "
            f"{timestamp_parser.format_seconds(start)} - "
            f"{timestamp_parser.format_seconds(end)}"
        )

        ffmpeg_wrapper.split_video(
            input_path,
            clip_path,
            start,
            duration,
            show_progress=False,
            reencode=reencode
        )

        clips.append((clip_path, start))

    return clips


def merge_clips(
    clips: List[Tuple[str, float]],
    output_path: str,
    temp_manager: file_manager.TempFileManager,
    reencode: bool = False
) -> None:
    """
    Merge clips into final output, sorted by start time.

    Args:
        clips: List of (clip_path, start_time) tuples
        output_path: Final output video path
        temp_manager: Temporary file manager
        reencode: Re-encode during merge for perfect sync
    """
    # Sort clips by start time
    sorted_clips = sorted(clips, key=lambda x: x[1])
    clip_paths = [clip[0] for clip in sorted_clips]

    mode_str = "Re-encoding and merging" if reencode else "Merging"
    cli_handler.print_progress(
        f"{mode_str} {len(clip_paths)} clips into {output_path}..."
    )

    ffmpeg_wrapper.merge_videos(
        clip_paths,
        output_path,
        temp_manager.temp_dir,
        show_progress=False,
        reencode=reencode
    )


def main() -> int:
    """
    Main application entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Validate environment
        cli_handler.print_progress("Checking requirements...")
        validate_environment()

        # Probe video duration
        cli_handler.print_progress(f"Analyzing {INPUT_VIDEO}...")
        duration = ffmpeg_wrapper.probe_duration(INPUT_VIDEO)

        # Print header
        cli_handler.print_header(INPUT_VIDEO, duration)

        # Collect ranges
        ranges = collect_ranges(duration)

        # Check if any ranges were collected
        if not ranges:
            cli_handler.print_error("No ranges provided. Exiting.")
            return 1

        # Print summary
        cli_handler.print_summary(ranges)

        # Display mode information
        if REENCODE_MODE:
            cli_handler.print_progress(
                "Using RE-ENCODE mode for perfect A/V sync (slower)"
            )
        else:
            cli_handler.print_progress(
                "Using STREAM COPY mode for fast processing "
                "(may have slight keyframe offset)"
            )

        # Process video with temp file management
        with file_manager.TempFileManager() as temp_manager:
            # Extract clips
            cli_handler.print_progress("Processing clips...")
            clips = extract_clips(INPUT_VIDEO, ranges, temp_manager, REENCODE_MODE)

            # Merge clips
            merge_clips(clips, OUTPUT_VIDEO, temp_manager, REENCODE_MODE)

        # Success
        cli_handler.print_success(
            f"Video created successfully: {OUTPUT_VIDEO}"
        )

        return 0

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 1

    except Exception as e:
        cli_handler.print_error(str(e))
        return 1


if __name__ == '__main__':
    sys.exit(main())

"""Timestamp parsing and validation module."""
import re
from typing import Tuple


def parse_timestamp(ts: str) -> float:
    """
    Parse timestamp string to seconds (float).

    Supports formats:
    - HH:MM:SS (e.g., "1:02:03")
    - MM:SS (e.g., "2:03")
    - Seconds (e.g., "123" or "123.5")

    Args:
        ts: Timestamp string

    Returns:
        Float representing seconds

    Raises:
        ValueError: If format is invalid
    """
    ts = ts.strip()

    # Try HH:MM:SS format
    if match := re.match(r'^(\d+):(\d+):(\d+)$', ts):
        h, m, s = map(int, match.groups())
        return h * 3600 + m * 60 + s

    # Try MM:SS format
    elif match := re.match(r'^(\d+):(\d+)$', ts):
        m, s = map(int, match.groups())
        return m * 60 + s

    # Try seconds format
    elif match := re.match(r'^(\d+\.?\d*)$', ts):
        return float(match.group(1))

    raise ValueError(f"Invalid timestamp format: '{ts}'")


def parse_range(input_str: str) -> Tuple[float, float]:
    """
    Parse range string to tuple of (start_seconds, end_seconds).

    Supports separators: ' to ', ' - ', '..', '-'
    Example: "2:03 to 5:24" -> (123.0, 324.0)

    Args:
        input_str: Range string (e.g., "2:03 to 5:24")

    Returns:
        Tuple of (start_seconds, end_seconds)

    Raises:
        ValueError: If format is invalid or end <= start
    """
    input_str = input_str.strip()

    # Try different separators
    for sep in [' to ', ' - ', '..', '-']:
        if sep in input_str:
            parts = input_str.split(sep, 1)
            if len(parts) == 2:
                try:
                    start = parse_timestamp(parts[0])
                    end = parse_timestamp(parts[1])

                    if start >= end:
                        raise ValueError("End time must be after start time")

                    return start, end
                except ValueError as e:
                    if "End time must be after start time" in str(e):
                        raise
                    continue

    raise ValueError("Use format: '2:03 to 5:24' or '2:03-5:24'")


def validate_range(start: float, end: float, duration: float) -> None:
    """
    Validate that a time range is within video duration.

    Args:
        start: Start time in seconds
        end: End time in seconds
        duration: Video duration in seconds

    Raises:
        ValueError: If range is invalid
    """
    if start < 0:
        raise ValueError(f"Start time cannot be negative: {start}")

    if end > duration:
        raise ValueError(
            f"End time {format_seconds(end)} exceeds video duration "
            f"{format_seconds(duration)}"
        )

    if start >= end:
        raise ValueError("End time must be after start time")


def format_seconds(seconds: float) -> str:
    """
    Format seconds as HH:MM:SS string.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted string (HH:MM:SS)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

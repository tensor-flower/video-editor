"""CLI interaction and user prompt handling."""
from typing import Optional
from .timestamp_parser import format_seconds


def print_header(video_path: str, duration: float) -> None:
    """
    Print application header with video information.

    Args:
        video_path: Path to input video
        duration: Video duration in seconds
    """
    print("\n" + "=" * 60)
    print("Interactive Video Editor")
    print("=" * 60)
    print(f"\nInput: {video_path}")
    print(f"Duration: {format_seconds(duration)}")
    print("\nEnter timestamp ranges to extract (e.g., '2:03 to 5:24')")
    print("Supported formats:")
    print("  - HH:MM:SS to HH:MM:SS  (e.g., '1:02:03 to 1:30:00')")
    print("  - MM:SS to MM:SS        (e.g., '2:03 to 5:24')")
    print("  - Seconds to Seconds    (e.g., '123 to 324')")
    print("\nType 'done' when finished adding ranges.\n")


def prompt_range(range_count: int) -> Optional[str]:
    """
    Prompt user for a timestamp range.

    Args:
        range_count: Current number of ranges collected

    Returns:
        User input string, or None if EOF
    """
    try:
        user_input = input(f"Range #{range_count + 1} (or 'done'): ").strip()
        return user_input
    except EOFError:
        return None


def confirm_range(start: float, end: float) -> None:
    """
    Print confirmation of added range.

    Args:
        start: Start time in seconds
        end: End time in seconds
    """
    print(f"  ✓ Added: {format_seconds(start)} - {format_seconds(end)}")


def print_error(message: str) -> None:
    """
    Print error message.

    Args:
        message: Error message
    """
    print(f"  ✗ Error: {message}")


def print_summary(ranges: list) -> None:
    """
    Print summary of collected ranges.

    Args:
        ranges: List of (start, end) tuples
    """
    print(f"\n{'-' * 60}")
    print(f"Collected {len(ranges)} range(s):")
    for idx, (start, end) in enumerate(ranges, 1):
        duration = end - start
        print(
            f"  {idx}. {format_seconds(start)} - {format_seconds(end)} "
            f"(duration: {format_seconds(duration)})"
        )
    print(f"{'-' * 60}\n")


def print_progress(message: str) -> None:
    """
    Print progress message.

    Args:
        message: Progress message
    """
    print(f"[*] {message}")


def print_success(message: str) -> None:
    """
    Print success message.

    Args:
        message: Success message
    """
    print(f"\n{'=' * 60}")
    print(f"✓ {message}")
    print(f"{'=' * 60}\n")

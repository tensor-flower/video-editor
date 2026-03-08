"""File and temporary directory management."""
import os
import shutil
import tempfile
from typing import Optional


class TempFileManager:
    """Manages temporary files and cleanup."""

    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize temp file manager.

        Args:
            base_dir: Base directory for temp files (default: system temp)
        """
        self.temp_dir = None
        self.base_dir = base_dir

    def create_temp_dir(self) -> str:
        """
        Create temporary directory for video clips.

        Returns:
            Path to temporary directory
        """
        if self.base_dir:
            self.temp_dir = tempfile.mkdtemp(
                prefix='video_edit_',
                dir=self.base_dir
            )
        else:
            self.temp_dir = tempfile.mkdtemp(prefix='video_edit_')

        return self.temp_dir

    def get_clip_path(self, index: int) -> str:
        """
        Generate path for a clip file.

        Args:
            index: Clip index

        Returns:
            Full path to clip file
        """
        if not self.temp_dir:
            raise RuntimeError("Temp directory not created")

        filename = f"clip_{index:03d}.mp4"
        return os.path.join(self.temp_dir, filename)

    def cleanup(self) -> None:
        """Remove temporary directory and all its contents."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                print(f"Warning: Failed to cleanup temp directory: {e}")

    def __enter__(self):
        """Context manager entry."""
        self.create_temp_dir()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup temp files."""
        self.cleanup()
        return False


def validate_input_file(file_path: str) -> None:
    """
    Validate that input file exists and is readable.

    Args:
        file_path: Path to input file

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file isn't readable
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Cannot read input file: {file_path}")


def ensure_output_writable(file_path: str) -> None:
    """
    Ensure output file path is writable.

    Args:
        file_path: Path to output file

    Raises:
        PermissionError: If directory isn't writable
    """
    output_dir = os.path.dirname(file_path) or '.'

    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory doesn't exist: {output_dir}")

    if not os.access(output_dir, os.W_OK):
        raise PermissionError(f"Cannot write to directory: {output_dir}")

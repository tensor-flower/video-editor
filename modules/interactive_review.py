"""Interactive review screen for range selection."""
import curses
from typing import List, Tuple
from .timestamp_parser import format_seconds


def review_ranges(ranges: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Interactive review screen for selected ranges.

    Users can navigate with arrow keys and toggle ranges on/off.

    Args:
        ranges: List of (start, end) tuples

    Returns:
        List of selected (start, end) tuples

    Controls:
        - Up/Down Arrow: Navigate
        - Space/Enter: Toggle selection
        - A: Select all
        - N: Deselect all
        - D: Delete current range
        - C: Continue with selected ranges
        - Q: Quit without changes
    """
    # Initialize with all ranges selected
    selected = [True] * len(ranges)

    def draw_screen(stdscr, current_index):
        """Draw the review screen."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Header
        title = "Review and Select Ranges"
        stdscr.addstr(0, 0, "=" * min(width - 1, 70), curses.A_BOLD)
        stdscr.addstr(1, 0, title, curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr(2, 0, "=" * min(width - 1, 70), curses.A_BOLD)
        stdscr.addstr(3, 0, "")

        # Instructions
        stdscr.addstr(4, 0, "Controls:", curses.A_BOLD)
        stdscr.addstr(5, 0, "  ↑/↓  Navigate   Space/Enter  Toggle   D  Delete")
        stdscr.addstr(6, 0, "  A    Select All   N  Deselect All   C  Continue   Q  Quit")
        stdscr.addstr(7, 0, "")

        # Ranges list
        stdscr.addstr(8, 0, "Ranges:", curses.A_BOLD)
        stdscr.addstr(9, 0, "-" * min(width - 1, 70))

        for idx, ((start, end), is_selected) in enumerate(zip(ranges, selected)):
            if idx >= height - 12:  # Leave room for footer
                break

            duration = end - start
            line_num = 10 + idx

            # Selection indicator
            checkbox = "[✓]" if is_selected else "[ ]"

            # Format range info
            range_info = (
                f"{checkbox} {idx + 1}. "
                f"{format_seconds(start)} - {format_seconds(end)} "
                f"(duration: {format_seconds(duration)})"
            )

            # Highlight current line
            if idx == current_index:
                stdscr.addstr(line_num, 0, "> ", curses.A_BOLD)
                stdscr.addstr(line_num, 2, range_info, curses.A_REVERSE)
            else:
                stdscr.addstr(line_num, 0, "  ")
                stdscr.addstr(line_num, 2, range_info)

        # Footer
        footer_line = height - 3
        selected_count = sum(selected)
        total_duration = sum(end - start for (start, end), sel
                           in zip(ranges, selected) if sel)

        stdscr.addstr(footer_line, 0, "-" * min(width - 1, 70))
        stdscr.addstr(footer_line + 1, 0,
                     f"Selected: {selected_count}/{len(ranges)} ranges | "
                     f"Total duration: {format_seconds(total_duration)}",
                     curses.A_BOLD)

        stdscr.refresh()

    def interactive_select(stdscr):
        """Main interactive loop."""
        curses.curs_set(0)  # Hide cursor
        current_index = 0

        while True:
            draw_screen(stdscr, current_index)

            try:
                key = stdscr.getch()
            except KeyboardInterrupt:
                return None  # User cancelled

            # Navigation
            if key == curses.KEY_UP:
                current_index = max(0, current_index - 1)
            elif key == curses.KEY_DOWN:
                current_index = min(len(ranges) - 1, current_index + 1)

            # Toggle selection
            elif key in (ord(' '), ord('\n'), curses.KEY_ENTER, 10, 13):
                selected[current_index] = not selected[current_index]

            # Select all
            elif key in (ord('a'), ord('A')):
                selected[:] = [True] * len(ranges)

            # Deselect all
            elif key in (ord('n'), ord('N')):
                selected[:] = [False] * len(ranges)

            # Delete current range
            elif key in (ord('d'), ord('D')):
                if len(ranges) > 1:
                    ranges.pop(current_index)
                    selected.pop(current_index)
                    current_index = min(current_index, len(ranges) - 1)
                else:
                    # Can't delete the last range, just deselect it
                    selected[current_index] = False

            # Continue with selection
            elif key in (ord('c'), ord('C')):
                if any(selected):
                    return [r for r, s in zip(ranges, selected) if s]
                else:
                    # Show message and continue loop
                    stdscr.addstr(0, 0,
                                "ERROR: Select at least one range! Press any key...",
                                curses.A_BOLD | curses.A_REVERSE)
                    stdscr.refresh()
                    stdscr.getch()

            # Quit without changes
            elif key in (ord('q'), ord('Q'), 27):  # 27 = ESC
                return None

    # Run curses application
    try:
        result = curses.wrapper(interactive_select)
        return result if result is not None else ranges
    except Exception as e:
        # Fallback if curses fails (e.g., not in terminal)
        print(f"\nWarning: Interactive mode not available: {e}")
        print("Proceeding with all ranges...")
        return ranges

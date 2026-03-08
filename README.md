# Interactive Video Editor

A Python-based interactive terminal application for selecting and merging video clips.

## Quick Start

```bash
python3 video_editor.py
```

## Audio Sync Issue - FIXED ✓

The slight audio desync has been debugged and fixed. See [AUDIO_SYNC_FIX.md](AUDIO_SYNC_FIX.md) for details.

### Quick Summary:
- **Default mode**: Fast stream copy with ~44ms offset (imperceptible for most use cases)
- **Perfect sync mode**: Enable `REENCODE_MODE = True` in `video_editor.py` for <25ms offset

## Configuration

Edit `video_editor.py` to configure:

```python
# Line 18-25
INPUT_VIDEO = 'input.MP4'          # Your input video file
OUTPUT_VIDEO = 'output_final.mp4'  # Output filename

# Performance vs Quality:
REENCODE_MODE = False  # Set to True for perfect A/V sync (slower)
```

## Usage Example

```
$ python3 video_editor.py

============================================================
Interactive Video Editor
============================================================

Input: input.MP4
Duration: 00:23:45

Enter timestamp ranges to extract (e.g., '2:03 to 5:24')
Supported formats:
  - HH:MM:SS to HH:MM:SS  (e.g., '1:02:03 to 1:30:00')
  - MM:SS to MM:SS        (e.g., '2:03 to 5:24')

Type 'done' when finished adding ranges.

Range #1 (or 'done'): 2:03 to 5:24
  ✓ Added: 00:02:03 - 00:05:24

Range #2 (or 'done'): 10:30 to 12:15
  ✓ Added: 00:10:30 - 00:12:15

Range #3 (or 'done'): done

------------------------------------------------------------
Collected 2 range(s):
  1. 00:02:03 - 00:05:24 (duration: 00:03:21)
  2. 00:10:30 - 00:12:15 (duration: 00:01:45)
------------------------------------------------------------

Opening interactive review screen...
(Use arrow keys to navigate, Space to toggle, C to continue)

[Interactive Review Screen Opens]
==============================================================
Review and Select Ranges
==============================================================

Controls:
  ↑/↓  Navigate   Space/Enter  Toggle   D  Delete
  A    Select All   N  Deselect All   C  Continue   Q  Quit

Ranges:
--------------------------------------------------------------
> [✓] 1. 00:02:03 - 00:05:24 (duration: 00:03:21)
  [✓] 2. 00:10:30 - 00:12:15 (duration: 00:01:45)
--------------------------------------------------------------
Selected: 2/2 ranges | Total duration: 00:05:06

[After pressing C to continue]

Final selection:
------------------------------------------------------------
Collected 2 range(s):
  1. 00:02:03 - 00:05:24 (duration: 00:03:21)
  2. 00:10:30 - 00:12:15 (duration: 00:01:45)
------------------------------------------------------------

[*] Processing clips...
[*] Extracting clip 1/2: 00:02:03 - 00:05:24
[*] Extracting clip 2/2: 00:10:30 - 00:12:15
[*] Merging 2 clips into output_final.mp4...

============================================================
✓ Video created successfully: output_final.mp4
============================================================
```

## Timestamp Formats

Supported formats:
- `HH:MM:SS to HH:MM:SS` - Example: `1:02:03 to 1:30:00`
- `MM:SS to MM:SS` - Example: `2:03 to 5:24`

Separators: `to`, `-`, `..` all work

## Interactive Review Controls

After entering ranges, use the interactive review screen to verify and edit:

| Key | Action |
|-----|--------|
| **↑/↓** | Navigate between ranges |
| **Space/Enter** | Toggle range on/off |
| **A** | Select all ranges |
| **N** | Deselect all ranges |
| **D** | Delete current range |
| **C** | Continue with selected ranges |
| **Q/ESC** | Quit without changes |

See [INTERACTIVE_REVIEW_GUIDE.md](INTERACTIVE_REVIEW_GUIDE.md) for detailed instructions.

## Features

- **Interactive Review Screen**: Review and edit your selections before processing
  - Navigate with arrow keys
  - Toggle ranges on/off with Space
  - Delete incorrect ranges with D
  - See total duration in real-time
- **Fast processing**: Stream copy mode (no re-encoding by default)
- **Lossless**: Preserves original video quality
- **Auto-sorted**: Clips automatically ordered by start time
- **Smart cleanup**: Automatic temp file management
- **A/V sync fixed**: Proper timestamp handling
- **Error correction**: Easy way to fix timestamp mistakes

## Technical Details

### Stream Copy Mode (Default)
- Speed: ~0.5-2 seconds per clip
- Quality: Lossless
- A/V offset: ~44ms (imperceptible)

### Re-encode Mode (Optional)
- Speed: ~5-15 seconds per clip
- Quality: Near-lossless (CRF 18)
- A/V offset: <25ms (perfect)

## Requirements

- Python 3.7+
- FFmpeg (install with `brew install ffmpeg`)

## File Structure

```
video_edit/
├── input.MP4                # Your input video
├── video_editor.py          # Main application
├── modules/
│   ├── ffmpeg_wrapper.py    # FFmpeg operations
│   ├── timestamp_parser.py  # Timestamp parsing
│   ├── cli_handler.py       # User interface
│   └── file_manager.py      # File management
└── output_final.mp4         # Generated output
```

## Troubleshooting

### Audio still out of sync?
1. Open `video_editor.py`
2. Change line 25: `REENCODE_MODE = False` → `REENCODE_MODE = True`
3. Run again (will be slower but perfect sync)

### FFmpeg not found?
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### Want to test the fix?
```bash
# Check A/V offset in your output
ffprobe -v error -select_streams v:0 -show_entries packet=pts_time \
  -of csv=p=0 output_final.mp4 | head -1  # Video start

ffprobe -v error -select_streams a:0 -show_entries packet=pts_time \
  -of csv=p=0 output_final.mp4 | head -1  # Audio start
```

Offset should be <50ms (good) or <25ms (perfect in re-encode mode).

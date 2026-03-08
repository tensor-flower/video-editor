# Audio Sync Issue - Diagnosis and Fix

## Problem
Audio desync issues when merging video clips using stream copy mode.

## Root Cause
When using `-ss` (seek) before `-i` with `-c copy` (stream copy):
1. FFmpeg seeks to the nearest **keyframe** for performance
2. This causes a 20-50ms offset between video and audio
3. Original timestamps are preserved, causing sync issues during concat

## Solutions Implemented

### 1. Stream Copy Mode (Default - FAST)
**Speed**: Very fast (~0.5-2 seconds per clip)
**Quality**: Lossless (no re-encoding)
**Sync**: 20-50ms offset (usually imperceptible)

**When to use**: Most videos where perfect sync isn't critical

**Improvements made**:
- Added `-avoid_negative_ts make_zero` to reset timestamps
- Added `-copyts` and `-start_at_zero` for proper timestamp handling
- Added explicit stream mapping `-map 0:v:0 -map 0:a:0`
- Removed muxer delays with `-muxdelay 0 -muxpreload 0`

**Result**: Reduced offset from ~200ms to ~44ms

### 2. Re-encode Mode (Optional - PERFECT SYNC)
**Speed**: Slower (~5-15 seconds per clip)
**Quality**: Near-lossless (CRF 18 H.264 encoding)
**Sync**: <25ms offset (imperceptible)

**When to use**: When perfect A/V sync is required

**Settings**:
```python
REENCODE_MODE = True  # In video_editor.py
```

**FFmpeg parameters used**:
- `-c:v libx264 -preset fast -crf 18` - High quality H.264 encoding
- `-c:a aac -b:a 192k` - High quality audio
- `-af aresample=async=1` - Audio resampling for sync
- `-vsync cfr` - Constant frame rate

**Result**: Offset reduced to ~23ms (AAC encoder delay, unavoidable)

## Test Results

| Mode | Offset | Speed (per 5s clip) | Quality |
|------|--------|---------------------|---------|
| Original | ~200ms | Fast | Lossless |
| Stream Copy (Fixed) | ~44ms | Fast | Lossless |
| Re-encode | ~23ms | Slower | Near-lossless |

## How to Use

### Quick Mode (Default)
```bash
python3 video_editor.py
```
Uses stream copy mode. Fast processing, slight keyframe offset.

### Perfect Sync Mode
Edit `video_editor.py`:
```python
REENCODE_MODE = True  # Line 23
```

Then run:
```bash
python3 video_editor.py
```

## Technical Details

### Why 23ms offset remains in re-encode mode?
AAC audio encoding introduces a standard "priming" delay of ~21-23ms. This is inherent to AAC encoding and is present in all AAC-encoded videos. It's typically handled by media players automatically.

### Why not use accurate seeking (-ss after -i)?
Tested, but resulted in WORSE sync (240ms offset). Input seeking (-ss before -i) is actually better for this use case.

### Alternative: concat protocol vs concat demuxer
The concat demuxer was chosen because it:
- Properly handles MP4 container format
- Works with stream copy mode
- Maintains quality

The concat protocol requires intermediate formats and doesn't work well with MP4.

## Verification Commands

### Check A/V offset:
```bash
# Video start time
ffprobe -v error -select_streams v:0 -show_entries packet=pts_time -of csv=p=0 output_final.mp4 | head -1

# Audio start time
ffprobe -v error -select_streams a:0 -show_entries packet=pts_time -of csv=p=0 output_final.mp4 | head -1
```

### Play and verify:
```bash
# macOS
open output_final.mp4

# Linux
vlc output_final.mp4
```

## Recommendation

**For most users**: Use the default stream copy mode. The 44ms offset is below human perception threshold for most content.

**For professional use**: Enable `REENCODE_MODE = True` for near-perfect sync at the cost of processing time.

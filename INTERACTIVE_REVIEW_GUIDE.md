# Interactive Review Screen - User Guide

## Overview
After entering your timestamp ranges, you'll see an interactive review screen where you can:
- Review all entered ranges
- Toggle ranges on/off
- Delete incorrect ranges
- See total selected duration

## Screen Layout

```
==============================================================
Review and Select Ranges
==============================================================

Controls:
  ↑/↓  Navigate   Space/Enter  Toggle   D  Delete
  A    Select All   N  Deselect All   C  Continue   Q  Quit

Ranges:
--------------------------------------------------------------
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [✓] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)
  [ ] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)
  [✓] 4. 00:13:20 - 00:14:10 (duration: 00:00:50)
--------------------------------------------------------------
Selected: 3/4 ranges | Total duration: 00:07:58
```

## Keyboard Controls

| Key | Action |
|-----|--------|
| **↑** (Up Arrow) | Move to previous range |
| **↓** (Down Arrow) | Move to next range |
| **Space** or **Enter** | Toggle current range on/off |
| **A** | Select all ranges |
| **N** | Deselect all ranges (None) |
| **D** | Delete current range permanently |
| **C** | Continue with selected ranges |
| **Q** or **ESC** | Quit without changes |

## Visual Indicators

- **`[✓]`** - Range is selected (will be included)
- **`[ ]`** - Range is deselected (will be excluded)
- **`>`** - Current cursor position
- **Highlighted line** - Current range being edited

## Workflow Example

### Scenario: You entered a wrong timestamp

**Step 1: Review ranges**
```
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [✓] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)  ← Wrong!
  [✓] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)
```

**Step 2: Navigate to wrong range**
- Press **↓** to move cursor to range #2

**Step 3: Options**

**Option A - Toggle off (keep in list but don't use)**:
- Press **Space** to deselect
```
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [ ] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)  ← Deselected
  [✓] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)
```

**Option B - Delete permanently**:
- Press **D** to remove from list
```
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [✓] 2. 00:10:00 - 00:12:00 (duration: 00:02:00)  ← Deleted #2
```

**Step 4: Continue**
- Press **C** to proceed with selected ranges

## Tips

1. **Made a mistake entering ranges?**
   - Don't worry! Deselect or delete them in the review screen

2. **Want to process only some clips?**
   - Use **Space** to toggle specific ranges off

3. **Changed your mind about everything?**
   - Press **N** to deselect all, then press **C** to exit
   - Or press **Q** to quit without changes

4. **Quick selection changes:**
   - **A** - Select all (start over fresh)
   - **N** - Deselect all (start from scratch)

5. **Must select at least one range:**
   - If you press **C** with no ranges selected, you'll get an error
   - Select at least one range before continuing

## Common Use Cases

### Use Case 1: Remove one bad range
```
Press ↓/↑ to navigate to the bad range
Press Space to deselect it
Press C to continue
```

### Use Case 2: Keep only specific ranges
```
Press N to deselect all
Press ↓/↑ to navigate to each range you want
Press Space on each one to select it
Press C to continue
```

### Use Case 3: Delete permanently
```
Press ↓/↑ to navigate to the range
Press D to delete it
Press C to continue
```

### Use Case 4: Start over
```
Press Q to quit without changes
Re-run the program
```

## Troubleshooting

**Screen looks garbled?**
- Your terminal might not support curses properly
- The app will fall back to using all ranges automatically
- Try resizing your terminal window

**Can't see the cursor?**
- This is intentional! Look for the `>` symbol and highlighted line

**Pressed wrong key?**
- No problem! Press the opposite action:
  - Selected by mistake? Press Space again
  - Deleted by mistake? Press Q to quit and start over

## After Review

Once you press **C**:
1. The app shows your final selection
2. Processing begins immediately
3. Only selected ranges are extracted and merged

The ranges will be automatically sorted by start time, so don't worry about the order!

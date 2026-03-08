# Interactive Review Screen - Visual Demo

## What You'll See

After entering your timestamp ranges and typing "done", the screen will transition to:

```
==============================================================
Review and Select Ranges
==============================================================

Controls:
  ↑/↓  Navigate   Space/Enter  Toggle   D  Delete
  A    Select All   N  Deselect All   C  Continue   Q  Quit

Ranges:
--------------------------------------------------------------
> [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
  [✓] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)
  [✓] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)
--------------------------------------------------------------
Selected: 3/3 ranges | Total duration: 00:09:08
```

## Example Scenarios

### Scenario 1: Remove One Wrong Range

**Initial state:**
```
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [✓] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)  ← WRONG TIME!
  [✓] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)

Selected: 3/3 ranges | Total duration: 00:09:08
```

**Press Space to deselect:**
```
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [ ] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)  ← Deselected
  [✓] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)

Selected: 2/3 ranges | Total duration: 00:08:51
```

**Press C to continue** with ranges 1 and 3 only.

---

### Scenario 2: Keep Only One Range

**Initial state:**
```
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [✓] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)
  [✓] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)
  [✓] 4. 00:13:00 - 00:15:00 (duration: 00:02:00)
```

**Press N (deselect all):**
```
  [ ] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [ ] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)
  [ ] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)
  [ ] 4. 00:13:00 - 00:15:00 (duration: 00:02:00)

Selected: 0/4 ranges | Total duration: 00:00:00
```

**Press ↓ to navigate to range #3:**
```
  [ ] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
  [ ] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)
> [ ] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)  ← Current
  [ ] 4. 00:13:00 - 00:15:00 (duration: 00:02:00)
```

**Press Space to select only this one:**
```
  [ ] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
  [ ] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)
> [✓] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)  ← Selected!
  [ ] 4. 00:13:00 - 00:15:00 (duration: 00:02:00)

Selected: 1/4 ranges | Total duration: 00:02:00
```

**Press C to continue** with only range #3.

---

### Scenario 3: Delete Permanently

**Initial state:**
```
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [✓] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)  ← Wrong entry
  [✓] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)
```

**Press D to delete range #2:**
```
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [✓] 2. 00:10:00 - 00:12:00 (duration: 00:02:00)  ← Old #3, now #2

Selected: 2/2 ranges | Total duration: 00:08:51
```

Range #2 is permanently removed from the list.

---

### Scenario 4: Quick Select All

**After deselecting some ranges:**
```
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [ ] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)
  [ ] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)

Selected: 1/3 ranges
```

**Press A to select all again:**
```
  [✓] 1. 00:00:59 - 00:07:50 (duration: 00:06:51)
> [✓] 2. 00:08:09 - 00:08:26 (duration: 00:00:17)
  [✓] 3. 00:10:00 - 00:12:00 (duration: 00:02:00)

Selected: 3/3 ranges | Total duration: 00:09:08
```

---

## Real-Time Feedback

The status line updates immediately as you make changes:

```
Selected: 3/4 ranges | Total duration: 00:09:08
         ↑               ↑
    How many selected   Total time of selected clips
```

This helps you see exactly what will be processed before committing!

---

## Tips for Power Users

1. **Quick deselect all then pick**: Press **N**, then use **↑/↓** and **Space** to select only what you want

2. **Delete bad entries**: Use **D** to permanently remove mistakes

3. **Changed your mind?**: Press **Q** to exit without changes and start over

4. **Visual confirmation**: The highlighted line shows exactly where you are

5. **No mistakes in processing**: Only checked [✓] ranges will be extracted!

---

## Try It!

Run this to test the interactive review screen:
```bash
python3 test_review_ui.py
```

This will load sample ranges so you can practice navigating before using it on your real video!

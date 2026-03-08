#!/usr/bin/env python3
"""Test script for interactive review UI."""
import sys
sys.path.insert(0, '/Users/guowanqi/video_edit')

from modules.interactive_review import review_ranges

# Test data - sample ranges
test_ranges = [
    (59.0, 470.0),   # 00:00:59 - 00:07:50
    (489.0, 506.0),  # 00:08:09 - 00:08:26
    (600.0, 720.0),  # 00:10:00 - 00:12:00
    (800.0, 850.0),  # 00:13:20 - 00:14:10
]

print("Testing interactive review screen...")
print("Sample ranges loaded. Opening review UI...")
print()

result = review_ranges(test_ranges)

if result is None:
    print("\nUser cancelled the review.")
elif result:
    print(f"\nUser selected {len(result)} range(s):")
    for start, end in result:
        print(f"  - {start}s to {end}s")
else:
    print("\nNo ranges selected.")

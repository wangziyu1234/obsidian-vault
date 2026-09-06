#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Obsidian math rendering: convert problematic inline math to display math.
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

MD_DIR = r'C:\Users\23720\OneDrive\数学二'

# Patterns that break Obsidian inline math
BREAK_PATTERNS = [
    r'\\displaystyle',
    r'\\dfrac',
    r'\\left\.',
    r'\\left\\{',
    r'\\begin\{cases\}',
    r'\\begin\{pmatrix\}',
    r'\\begin{bmatrix\}',
    r'\\int_{.*?}^{.*?}',  # integrals with limits
]

def fix_line(line):
    """Convert problematic inline math to display math."""
    # Find all inline math $...$
    parts = re.split(r'(?<!\$)\$(?!\$)', line)
    if len(parts) < 3:
        return line

    # Process every other part (the math parts)
    new_parts = [parts[0]]
    for i in range(1, len(parts), 2):
        math = parts[i]
        needs_display = False
        for pat in BREAK_PATTERNS:
            if re.search(pat, math):
                needs_display = True
                break

        if needs_display:
            # Convert to display math: wrap in $$
            new_parts.append('$$' + math + '$$')
        else:
            new_parts.append('$' + math + '$')

    if len(parts) % 2 == 0:
        new_parts.append(parts[-1])

    return ''.join(new_parts)

count = 0
for year in range(1987, 2026):
    fpath = os.path.join(MD_DIR, f'{year}年考研数学二试题.md')
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()

    changed = False
    new_lines = []
    for line in lines:
        if '$' in line and '\\\\' not in line:
            new_line = fix_line(line.rstrip('\n'))
            if new_line != line.rstrip('\n'):
                changed = True
            new_lines.append(new_line + '\n')
        else:
            new_lines.append(line)

    if changed:
        with open(fpath, 'w', encoding='utf-8') as fh:
            fh.writelines(new_lines)
        count += 1
        print(f'  Fixed: {year}')

print(f'\nTotal: {count} files fixed')

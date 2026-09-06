#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan all OCR output for junk patterns to build a comprehensive filter."""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = r'C:\Users\23720\OneDrive\数学二\_ocr_output'

# Collect all unique lines across all OCR files
all_lines = set()
for fname in sorted(os.listdir(OUTPUT_DIR)):
    if not fname.endswith('.txt'):
        continue
    fpath = os.path.join(OUTPUT_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                all_lines.add(line)

# Find junk patterns
junk_keywords = [
    '扫码', '关注', '线上打印', '顺丰包邮', '免费网课', '无水印', '超高质量', '价格最低',
    '公众号', '免费分享', '研池大叔', '微信公众号', 'B站', '向老师讲数学',
    '淘宝', '光速考研', '精品资料', '历年考研数学真题解析及复习思路',
    '更多考研', '网店', '店铺',
]

print("=== LINES WITH JUNK KEYWORDS ===")
for line in sorted(all_lines):
    for kw in junk_keywords:
        if kw in line:
            print(f"  {line[:100]}")
            break

# Find lines that are just numbers (page numbers)
print("\n=== NUMERIC-ONLY LINES ===")
num_only = [l for l in all_lines if re.match(r'^\d{1,4}$', l)]
for l in sorted(num_only):
    print(f"  {l}")

# Find lines with "第X页" (page markers)
print("\n=== PAGE MARKERS ===")
for line in sorted(all_lines):
    if '第' in line and '页' in line:
        print(f"  {line[:80]}")

# Find lines with "姓名" or "分数"
print("\n=== SCORE/NAME LINES ===")
for line in sorted(all_lines):
    if '姓名' in line or '分数' in line:
        print(f"  {line[:80]}")

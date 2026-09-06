#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean all generated markdown files: remove watermarks, junk, fix OCR artifacts.
Also prepares PDF page images for re-OCR with professional tools.
"""
import os, re, sys, fitz
sys.stdout.reconfigure(encoding='utf-8')

MD_DIR = r'C:\Users\23720\OneDrive\数学二'
IMG_DIR = r'C:\Users\23720\OneDrive\数学二\_pages_for_ocr'
os.makedirs(IMG_DIR, exist_ok=True)

# ── Junk patterns to remove (order matters: longer first) ──
JUNK_LINES = [
    # Advertisements
    '扫码关注', '线上打印', '顺丰包邮', '免费网课+无水印PDF', '超高质量', '价格最低',
    '免费网课', '无水印PDF',
    # Watermark authors
    '公众号：研池大叔免费分享考研课程&书籍',
    '公众号：研池大叔免费分享考研课&',
    '公众号：研池大叔免费分享考研课程',
    '公众号：研池大叔免费分享课程&',
    '公众号：研池大叔 免费分享考研课程＆书籍',
    '公众号：研池大叔',
    '微信公众号：向老师讲数学',
    'B站：向老师讲数学',
    '历年考研数学真题解析及复习思路（数学二）',
    '历年考研数学真题解析及复习思路(数学二)',
    # Book source
    '更多考研精品资料',
    '关注淘宝店铺：光速考研工作室',
    # Header/footer
    '姓名', '分数',
]

JUNK_RE = re.compile(
    r'^(' +
    '|'.join(re.escape(j) for j in sorted(JUNK_LINES, key=len, reverse=True)) +
    r')\s*$'
)

# Page number patterns
PAGE_NUM_RE = re.compile(r'^\d{1,4}$')
PAGE_MARKER_RE = re.compile(r'^第\s*\d+\s*页.*共\s*\d+\s*页')

# Header patterns (year + exam name, not real content)
HEADER_RE = re.compile(r'^(19|20)\d{2}\s*年.*考试.*$')
HEADER2_RE = re.compile(r'^年全国.*考试.*$')
HEADER3_RE = re.compile(r'^(数学|数\s*学)\s*[（(][一二三][)）]')
HEADER4_RE = re.compile(r'^（科目代码[：:]?\s*\d+\s*）')
HEADER5_RE = re.compile(r'^科目代码[：:]?\s*\d+')
EXAM_CODE_RE = re.compile(r'^(19|20)\d{2}\s*年.*数学.*[（(][一二三][)）]')
SUBJECT_RE = re.compile(r'^数\s*学\s*[（(]\s*[一二三]\s*[)）]')

# Previous year/book title watermark (appears mid-text)
BOOK_TITLE_RE = re.compile(r'^.*历年考研数学真题解析.*$')

def is_junk(line):
    """Return True if line is junk that should be removed."""
    if not line.strip():
        return False  # Keep empty lines for structure
    if JUNK_RE.match(line.strip()):
        return True
    if PAGE_NUM_RE.match(line.strip()):
        return True
    if PAGE_MARKER_RE.match(line.strip()):
        return True
    if BOOK_TITLE_RE.match(line.strip()):
        return True
    return False

def clean_text(lines):
    """Clean a list of text lines, remove junk, fix headers."""
    cleaned = []
    skip_next_header = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip junk
        if is_junk(stripped):
            continue

        # Skip exam metadata lines at the top
        if HEADER_RE.match(stripped):
            continue
        if HEADER2_RE.match(stripped):
            continue
        if HEADER3_RE.match(stripped):
            continue
        if HEADER4_RE.match(stripped):
            continue
        if HEADER5_RE.match(stripped):
            continue
        if SUBJECT_RE.match(stripped):
            continue

        # Fix "19874" → "1987年", "2010" alone on a line → skip
        m = re.match(r'^((?:19|20)\d{3})4$', stripped)
        if m:
            continue  # Skip OCR garble like "19874"

        # "(试卷Ⅲ)" → skip exam paper code
        if re.match(r'^[（(]试卷.*[)）]$', stripped):
            continue

        cleaned.append(stripped)

    return cleaned

def export_pdf_pages():
    """Export all PDF pages as images for re-OCR."""
    pdfs = [
        (r'C:\Users\23720\OneDrive\数学二\【合集】1987-2023年考研数学二纯真题版.pdf', 'collection'),
        (r'C:\Users\23720\OneDrive\数学二\2024年考研数学二试题.pdf', '2024'),
        (r'C:\Users\23720\OneDrive\数学二\2025年考研数学二试题.pdf', '2025'),
    ]

    for pdf_path, label in pdfs:
        if not os.path.exists(pdf_path):
            print(f'  SKIP: {pdf_path} not found')
            continue
        doc = fitz.open(pdf_path)
        out_dir = os.path.join(IMG_DIR, label)
        os.makedirs(out_dir, exist_ok=True)
        n = len(doc)
        for i in range(n):
            page = doc[i]
            pix = page.get_pixmap(dpi=300)
            img_path = os.path.join(out_dir, f'p{i+1:03d}.png')
            pix.save(img_path)
        doc.close()
        print(f'  {label}: {n} pages exported')

def clean_existing_mds():
    """Clean all existing markdown files."""
    import glob
    md_files = sorted(glob.glob(os.path.join(MD_DIR, '*年考研数学二试题.md')))
    print(f'Cleaning {len(md_files)} markdown files...')

    for fpath in md_files:
        basename = os.path.basename(fpath)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')

        # Remove H1 title line (we'll re-add it)
        if lines and lines[0].startswith('# '):
            lines = lines[1:]

        cleaned = clean_text(lines)

        # Rebuild
        year_match = re.match(r'(\d{4})年', basename)
        year = year_match.group(1) if year_match else '????'
        md = f'# {year}年考研数学二试题\n\n'
        md += '\n'.join(cleaned)
        md = md.rstrip() + '\n'

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(md)

        # Count non-empty lines
        real_lines = len([l for l in cleaned if l.strip()])
        print(f'  {basename}: {real_lines} content lines')

if __name__ == '__main__':
    print('=== Cleaning existing markdown files ===')
    clean_existing_mds()

    print('\n=== Exporting PDF pages as images ===')
    export_pdf_pages()

    print('\nDone!')

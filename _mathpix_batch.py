#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathpix batch OCR for math exam PDF pages.
Converts PDF page images to clean LaTeX/markdown.

Usage:
  1. Get a Mathpix API key from https://mathpix.com/api
  2. Set environment variable:  set MATHPIX_API_KEY=your_key_here
  3. Run:  python _mathpix_batch.py

Output: One .md file per year in _mathpix_output/
"""
import os, sys, json, time, base64, glob, re
sys.stdout.reconfigure(encoding='utf-8')

# ── Config ──
API_KEY = os.environ.get('MATHPIX_API_KEY', '')
API_URL = 'https://api.mathpix.com/v3/latex'
IMG_DIR = r'C:\Users\23720\OneDrive\数学二\_pages_for_ocr'
OUT_DIR = r'C:\Users\23720\OneDrive\数学二\_mathpix_output'
os.makedirs(OUT_DIR, exist_ok=True)

# Page mapping (collection PDF pages → year)
COLLECTION_PAGES = {
    1987: (2, 3), 1988: (4, 5), 1989: (6, 7), 1990: (8, 9),
    1991: (10, 11), 1992: (12, 13), 1993: (14, 15), 1994: (16, 17),
    1995: (18, 19), 1996: (20, 21), 1997: (22, 23), 1998: (24, 26),
    1999: (27, 29), 2000: (30, 31), 2001: (32, 35), 2002: (36, 38),
    2003: (39, 41), 2004: (42, 44), 2005: (45, 47), 2006: (48, 50),
    2007: (51, 52), 2008: (53, 55), 2009: (56, 58), 2010: (59, 62),
    2011: (63, 66), 2012: (67, 70), 2013: (71, 74), 2014: (75, 78),
    2015: (79, 82), 2016: (83, 86), 2017: (87, 90), 2018: (91, 94),
    2019: (95, 98), 2020: (99, 102), 2021: (103, 106),
    2022: (107, 109), 2023: (110, 112),
}

def ocr_image_mathpix(img_path, api_key):
    """Send an image to Mathpix API and return LaTeX + text."""
    import urllib.request

    with open(img_path, 'rb') as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')

    # Determine format
    ext = os.path.splitext(img_path)[1].lower()
    fmt = {'png': 'png', '.jpg': 'jpg', '.jpeg': 'jpg'}.get(ext, 'png')

    payload = json.dumps({
        'src': f'data:image/{fmt};base64,{img_data}',
        'formats': ['latex', 'text'],
        'data_options': {
            'include_drawing': False,
        }
    }).encode('utf-8')

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            'app_id': 'mathpix_harvest',
            'app_key': api_key,
            'Content-Type': 'application/json',
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            latex = result.get('latex', '')
            text = result.get('text', '')
            return latex, text
    except Exception as e:
        print(f'    ERROR: {e}')
        return '', ''

def process_collection(api_key):
    """Process all years from the collection PDF."""
    for year, (start, end) in sorted(COLLECTION_PAGES.items()):
        print(f'\n=== {year} (pages {start}-{end}) ===')
        all_latex = []
        all_text = []

        for page_num in range(start, end + 1):
            img_path = os.path.join(IMG_DIR, 'collection', f'p{page_num:03d}.png')
            if not os.path.exists(img_path):
                print(f'  Page {page_num}: NOT FOUND')
                continue

            print(f'  Page {page_num}...', end=' ', flush=True)
            latex, text = ocr_image_mathpix(img_path, api_key)
            if latex:
                all_latex.append(latex)
                print(f'OK ({len(latex)} chars)')
            else:
                print('EMPTY')
            if text:
                all_text.append(text)

            time.sleep(0.5)  # Rate limit

        # Save results
        out_path = os.path.join(OUT_DIR, f'{year}.tex')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(f'% {year}年考研数学二试题 (Mathpix OCR)\n\n')
            f.write('\n\n'.join(all_latex))

        out_md = os.path.join(OUT_DIR, f'{year}_text.md')
        with open(out_md, 'w', encoding='utf-8') as f:
            f.write(f'# {year}年考研数学二试题\n\n')
            f.write('\n\n'.join(all_text))

        print(f'  Saved: {out_path} ({os.path.getsize(out_path)} bytes)')

def process_separate_pdfs(api_key):
    """Process 2024 and 2025 PDFs."""
    for year in [2024, 2025]:
        print(f'\n=== {year} ===')
        all_latex = []
        all_text = []

        for page_num in range(1, 5):
            img_path = os.path.join(IMG_DIR, str(year), f'p{page_num:03d}.png')
            if not os.path.exists(img_path):
                continue

            print(f'  Page {page_num}...', end=' ', flush=True)
            latex, text = ocr_image_mathpix(img_path, api_key)
            if latex:
                all_latex.append(latex)
                print(f'OK ({len(latex)} chars)')
            else:
                print('EMPTY')
            if text:
                all_text.append(text)

            time.sleep(0.5)

        out_path = os.path.join(OUT_DIR, f'{year}.tex')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(f'% {year}年考研数学二试题 (Mathpix OCR)\n\n')
            f.write('\n\n'.join(all_latex))

        out_md = os.path.join(OUT_DIR, f'{year}_text.md')
        with open(out_md, 'w', encoding='utf-8') as f:
            f.write(f'# {year}年考研数学二试题\n\n')
            f.write('\n\n'.join(all_text))

        print(f'  Saved: {out_path}')

if __name__ == '__main__':
    if not API_KEY:
        print('='*60)
        print('ERROR: MATHPIX_API_KEY not set!')
        print()
        print('Steps to get an API key:')
        print('  1. Go to https://mathpix.com/api')
        print('  2. Sign up (free tier: 500 requests/month)')
        print('  3. Get your API key from the dashboard')
        print('  4. Run:')
        print('     set MATHPIX_API_KEY=your_key_here')
        print('     python _mathpix_batch.py')
        print('='*60)
        sys.exit(1)

    print(f'API Key: {API_KEY[:8]}...')
    print(f'Images: {IMG_DIR}')
    print(f'Output: {OUT_DIR}')
    print()

    process_collection(API_KEY)
    process_separate_pdfs(API_KEY)

    print('\n' + '='*60)
    print('DONE! Check output in:', OUT_DIR)

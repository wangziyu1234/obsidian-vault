#!/usr/bin/env python3
import re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

MD_DIR = r'C:\Users\23720\OneDrive\数学二'

def parse_questions_debug(text, year):
    lines = text.split('\n')
    questions = []
    current_section = ''
    current_q = ''
    current_qnum = ''
    in_answer = False

    answer_markers = ['答案速查', '参考答案', '答案与解析']
    q_pat_cn = re.compile(r'^[（(](\d+)[）)]')
    q_pat_plain = re.compile(r'^(\d+)[.．]')
    sec_pat = re.compile(r'^[一二三四五六七八九十]+[、．.]')
    score_pat = re.compile(r'本题满分')

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            if current_q:
                current_q += '\n'
            continue

        # Check for answer section
        if any(m in stripped for m in answer_markers):
            in_answer = True
            if current_q and current_qnum:
                questions.append((current_section, current_qnum, current_q.strip()))
                current_q = ''
                current_qnum = ''
            continue

        if in_answer:
            continue

        # Check for section header
        if sec_pat.match(stripped):
            if current_q and current_qnum:
                questions.append((current_section, current_qnum, current_q.strip()))
                current_q = ''
                current_qnum = ''
            current_section = stripped.rstrip('：:')
            continue

        # Score marker on its own line → treat as section separator, not question start
        if score_pat.match(stripped) and not q_pat_cn.match(stripped) and not q_pat_plain.match(stripped):
            # This is a standalone score marker like "二、（本题满分6分)" - already handled by sec_pat
            # Or "(本题满分10分)" - treat as section info
            continue

        # Check for question number
        m = q_pat_cn.match(stripped)
        if m:
            if current_q and current_qnum:
                questions.append((current_section, current_qnum, current_q.strip()))
            current_qnum = m.group(1)
            current_q = stripped + '\n'
            continue

        m = q_pat_plain.match(stripped)
        if m and not sec_pat.match(stripped):
            if current_q and current_qnum:
                questions.append((current_section, current_qnum, current_q.strip()))
            current_qnum = m.group(1)
            current_q = stripped + '\n'
            continue

        # Continuation
        current_q += stripped + '\n'

    if current_q and current_qnum:
        questions.append((current_section, current_qnum, current_q.strip()))

    return questions

# Test on actual files
import glob
md_files = sorted(glob.glob(os.path.join(MD_DIR, '*年考研数学二试题.md')))
for fpath in md_files[:5]:
    basename = os.path.basename(fpath)
    year_match = re.match(r'(\d{4})年', basename)
    if not year_match:
        continue
    year = int(year_match.group(1))
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    questions = parse_questions_debug(text, year)
    print(f'{year}: {len(questions)} questions')
    for sec, qnum, qtxt in questions[:3]:
        print(f"  [{sec[:30]}] Q{qnum}: {qtxt[:50]}...")
    if len(questions) > 3:
        print(f"  ... and {len(questions)-3} more")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a one-question-per-page practice PDF for Xiaomi Tablet 7S Pro.
Page: 240mm × 160mm (3:2 ratio), pure white, no grid/lines, minimalist.
"""
import os, re, sys, glob, subprocess
sys.stdout.reconfigure(encoding='utf-8')

MD_DIR = r'C:\Users\23720\OneDrive\数学二'
OUT_DIR = r'C:\Users\23720\OneDrive\数学二\刷题版'
os.makedirs(OUT_DIR, exist_ok=True)

# ── LaTeX preamble ──
PREAMBLE = r"""% !TEX program = xelatex
\documentclass[11pt]{article}

% ── Page geometry: 240mm × 160mm (3:2 for Xiaomi Tablet 7S Pro) ──
\usepackage[paperwidth=240mm,paperheight=160mm,left=15mm,right=15mm,top=12mm,bottom=12mm]{geometry}

% ── Fonts ──
\usepackage{fontspec}
\usepackage[UTF8]{ctex}
\setCJKmainfont{Noto Serif SC}
\setCJKsansfont{Noto Sans SC}
\setmainfont{Times New Roman}

% ── Math ──
\usepackage{amsmath,amssymb,amsthm}

% ── Colors ──
\usepackage{xcolor}
\definecolor{titleblue}{HTML}{1a5276}
\definecolor{lightgray}{HTML}{999999}

% ── No headers/footers ──
\pagestyle{empty}

% ── Tight spacing ──
\setlength{\parskip}{0pt}
\setlength{\parindent}{0pt}

\begin{document}
"""

POSTAMBLE = r"""
\end{document}
"""

def sanitize_latex(text):
    """Escape LaTeX special characters."""
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('\\{', '\\lbrace{}')
    text = text.replace('\\}', '\\rbrace{}')
    for ch in ['&', '%', '#', '_']:
        text = text.replace(ch, '\\' + ch)
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('^', '\\textasciicircum{}')
    return text

def parse_questions(text):
    """Extract individual questions from markdown."""
    lines = text.split('\n')
    questions = []
    current_section = ''
    current_q = ''
    current_qnum = ''
    in_answer = False

    answer_markers = ['参考答案', '答案速查', '答案与解析']
    q_pat_cn = re.compile(r'^[（(](\d+)[）)]')
    q_pat_plain = re.compile(r'^(\d+)[.．]')
    sec_pat = re.compile(r'^[一二三四五六七八九十]+[、．.]')

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_q:
                current_q += '\n'
            continue

        if any(m in stripped for m in answer_markers):
            in_answer = True
            if current_q and current_qnum:
                questions.append((current_section, current_qnum, current_q.strip()))
                current_q = ''
                current_qnum = ''
            continue
        if in_answer:
            continue

        if sec_pat.match(stripped):
            if current_q and current_qnum:
                questions.append((current_section, current_qnum, current_q.strip()))
                current_q = ''
                current_qnum = ''
            current_section = stripped.rstrip('：:')
            continue

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

        current_q += stripped + '\n'

    if current_q and current_qnum:
        questions.append((current_section, current_qnum, current_q.strip()))
    return questions

def get_sec_label(sec):
    """Extract short section label."""
    if not sec:
        return ''
    if '填空' in sec:
        return '填空题'
    if '选择' in sec:
        return '选择题'
    if '解答' in sec:
        return '解答题'
    if '计算' in sec:
        return '计算题'
    if '证明' in sec:
        return '证明题'
    return ''

def build_latex(all_questions):
    """Build LaTeX document with one question per page."""
    latex = PREAMBLE

    for year, sec, qnum, qtxt in all_questions:
        sec_label = get_sec_label(sec)
        # Build header
        header_parts = [f'{year}年']
        if sec_label:
            header_parts.append(sec_label)
        header_parts.append(f'第{qnum}题')
        title = ' · '.join(header_parts)

        # Clean question text for LaTeX
        body_lines = qtxt.split('\n')
        body_parts = []
        for line in body_lines:
            line = line.strip()
            if not line:
                continue
            body_parts.append(sanitize_latex(line))

        body = ' \\\\\n'.join(body_parts) if body_parts else ''

        # Each question on its own page
        latex += f'\\par\\vspace*{{0pt}}\n'
        latex += f'{{\\large\\color{{titleblue}}\\textbf{{{title}}}}}\n'
        latex += f'\\vspace{{6pt}}\n'
        latex += f'\\hrule height 0.3pt depth 0pt\n'
        latex += f'\\vspace{{8pt}}\n'
        latex += body + '\n'
        latex += f'\\newpage\n\n'

    latex += POSTAMBLE
    return latex

def compile_pdf(tex_path):
    """Compile LaTeX to PDF."""
    dirn = os.path.dirname(tex_path)
    basename = os.path.basename(tex_path)
    for _ in range(2):
        subprocess.run(
            ['xelatex', '-interaction=nonstopmode', basename],
            cwd=dirn, capture_output=True, timeout=120
        )
    pdf_path = os.path.join(dirn, os.path.splitext(basename)[0] + '.pdf')
    if os.path.exists(pdf_path):
        return True, os.path.getsize(pdf_path)
    return False, 0

def main():
    md_files = sorted(glob.glob(os.path.join(MD_DIR, '*年考研数学二试题.md')))
    print(f'Found {len(md_files)} markdown files')

    all_questions = []
    for fpath in md_files:
        basename = os.path.basename(fpath)
        year_match = re.match(r'(\d{4})年', basename)
        if not year_match:
            continue
        year = int(year_match.group(1))

        with open(fpath, 'r', encoding='utf-8') as f:
            text = f.read()

        # Skip files that are clearly bad OCR (too short or starts with junk)
        lines = [l for l in text.split('\n') if l.strip()]
        if len(lines) < 5:
            print(f'  {year}: SKIPPED (too short)')
            continue

        questions = parse_questions(text)
        for sec, qnum, qtxt in questions:
            all_questions.append((year, sec, qnum, qtxt))
        print(f'  {year}: {len(questions)} questions')

    total = len(all_questions)
    print(f'\nTotal: {total} questions')

    # Build LaTeX
    tex = build_latex(all_questions)
    tex_path = os.path.join(OUT_DIR, '数学二刷题版_平板.tex')
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(tex)
    print(f'Written: {tex_path}')

    # Compile
    print('\nCompiling PDF...')
    ok, size = compile_pdf(tex_path)
    if ok:
        print(f'PDF generated: {size//1024} KB')
    else:
        print('PDF compilation failed')

if __name__ == '__main__':
    main()

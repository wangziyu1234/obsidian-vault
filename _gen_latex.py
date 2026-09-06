#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse markdown exam files and generate a one-question-per-page LaTeX刷题版PDF.
"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

MD_DIR = r'C:\Users\23720\OneDrive\数学二'
OUT_DIR = r'C:\Users\23720\OneDrive\数学二\刷题版'
os.makedirs(OUT_DIR, exist_ok=True)

# ── LaTeX preamble ──
LATEX_PREAMBLE = r"""% !TEX program = xelatex
\documentclass[a4paper,11pt]{article}
\usepackage{fontspec}
\usepackage[UTF8, heading=true]{ctex}
\usepackage[margin=2cm, top=2.5cm, bottom=2cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{fancyhdr}
\usepackage{tikz}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{tabularx}

% ── colors ──
\definecolor{yearblue}{HTML}{1a5276}
\definecolor{sectgreen}{HTML}{1e8449}
\definecolor{taggray}{HTML}{666666}
\definecolor{qbg}{HTML}{f8f9fa}
\definecolor{abg}{HTML}{eaf2e3}

% ── header / footer ──
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{taggray}考研数学二 · 刷题版}
\fancyhead[R]{\small\color{taggray}\leftmark}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% ── question box ──
\newtcolorbox{qbox}[2][]{%
  enhanced,
  colback=qbg, colframe=yearblue, coltitle=white,
  fonttitle=\bfseries\large,
  title={#2},
  attach boxed title to top left={yshift=-2mm,xshift=4mm},
  boxed title style={colback=yearblue, sharp corners},
  sharp corners=south,
  breakable,
  left=6pt, right=6pt, top=4pt, bottom=4pt,
  #1
}

% ── section label ──
\newcommand{\seclabel}[1]{%
  \par\vspace{2pt}%
  {\color{sectgreen}\bfseries\small #1}\par\vspace{4pt}%
}

% ── answer box (hidden by default, toggle with showanswers) ──
\newtcolorbox{abox}[1][]{%
  enhanced,
  colback=abg, colframe=sectgreen,
  fonttitle=\bfseries\small,
  title={参考答案},
  sharp corners,
  breakable,
  left=6pt, right=6pt, top=2pt, bottom=2pt,
  #1
}

% ── fix OCR garble: make \text{...} safe ──
\newcommand{\fix}[1]{\text{#1}}

\begin{document}

"""

LATEX_POSTAMBLE = r"""
\end{document}
"""

def read_md(filepath):
    """Read a markdown file and return its text."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def sanitize_latex(text):
    """Escape special LaTeX characters in raw OCR text, keep it readable."""
    # Order matters: backslash first
    text = text.replace('\\', '\\textbackslash{}')
    # Protect already-escaped chars
    text = text.replace('\\{', '\\lbrace{}')
    text = text.replace('\\}', '\\rbrace{}')
    # Escape LaTeX specials
    for ch in ['&', '%', '#', '_']:
        text = text.replace(ch, '\\' + ch)
    # Dollar signs: wrap lone $ in text (they're OCR artifacts, not LaTeX)
    # Don't touch $$ blocks
    # Tilde
    text = text.replace('~', '\\textasciitilde{}')
    # Caret
    text = text.replace('^', '\\textasciicircum{}')
    return text

def parse_questions(text, year):
    """
    Split exam text into individual questions.
    Returns list of (section_name, q_number, q_text).
    """
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

        # Section header takes priority
        if sec_pat.match(stripped):
            if current_q and current_qnum:
                questions.append((current_section, current_qnum, current_q.strip()))
                current_q = ''
                current_qnum = ''
            current_section = stripped.rstrip('：:')
            continue

        # Question number: full-width (1) or half-width (1)
        m = q_pat_cn.match(stripped)
        if m:
            if current_q and current_qnum:
                questions.append((current_section, current_qnum, current_q.strip()))
            current_qnum = m.group(1)
            current_q = stripped + '\n'
            continue

        # Question number: 1. 2. etc.
        m = q_pat_plain.match(stripped)
        if m and not sec_pat.match(stripped):
            if current_q and current_qnum:
                questions.append((current_section, current_qnum, current_q.strip()))
            current_qnum = m.group(1)
            current_q = stripped + '\n'
            continue

        # Continuation line
        current_q += stripped + '\n'

    if current_q and current_qnum:
        questions.append((current_section, current_qnum, current_q.strip()))

    return questions

def text_to_latex_body(raw_text):
    """Convert raw OCR text to LaTeX body content."""
    lines = raw_text.split('\n')
    parts = []
    for line in lines:
        line = line.strip()
        if not line:
            parts.append('')
            continue
        s = sanitize_latex(line)
        # Wrap in \fix{} for safety (prevents most OCR garble from breaking LaTeX)
        parts.append(s)
    return ' \\\\\n'.join(parts) if parts else ''

def generate_latex_all():
    """Generate one big LaTeX file with all questions, one per page."""
    md_files = sorted(glob.glob(os.path.join(MD_DIR, '*年考研数学二试题.md')))
    print(f'Found {len(md_files)} markdown files')

    all_questions = []  # (year, section, qnum, text)

    for fpath in md_files:
        basename = os.path.basename(fpath)
        year_match = re.match(r'(\d{4})年', basename)
        if not year_match:
            continue
        year = int(year_match.group(1))
        text = read_md(fpath)
        questions = parse_questions(text, year)
        for sec, qnum, qtxt in questions:
            all_questions.append((year, sec, qnum, qtxt))
        print(f'  {year}: {len(questions)} questions parsed')

    print(f'Total questions: {len(all_questions)}')

    # ── Build LaTeX ──
    latex = LATEX_PREAMBLE

    prev_year = None
    for year, sec, qnum, qtxt in all_questions:
        # New year → new page + year header
        if year != prev_year:
            if prev_year is not None:
                latex += '\\newpage\n'
            latex += f'\\phantomsection\\addcontentsline{{toc}}{{section}}{{{year}年}}\n'
            prev_year = year

        # Build title (avoid parentheses/commas that break tcolorbox keys)
        sec_short = ''
        if sec:
            # Extract just the section type: 填空题, 选择题, 解答题 etc.
            if '填空' in sec:
                sec_short = '填空题'
            elif '选择' in sec:
                sec_short = '选择题'
            elif '解答' in sec:
                sec_short = '解答题'
            else:
                # Use first 4 chars
                sec_short = sec[:8].rstrip('：:')

        title = f'{year}年'
        if sec_short:
            title += f' {sec_short}'
        title += f' 第{qnum}题'

        # Build question body
        body = text_to_latex_body(qtxt)

        latex += f'\\begin{{qbox}}[{title}]\n'
        latex += body + '\n'
        latex += '\\end{qbox}\n'
        latex += '\\vfill\n\n'

    latex += LATEX_POSTAMBLE

    # Write tex file
    tex_path = os.path.join(OUT_DIR, '数学二刷题版.tex')
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(latex)
    print(f'Written: {tex_path}')
    return tex_path

if __name__ == '__main__':
    tex_path = generate_latex_all()
    print(f'\nLaTeX file ready: {tex_path}')
    print('Compile with: xelatex -interaction=nonstopmode "数学二刷题版.tex"')

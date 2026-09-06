#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate one-question-per-page LaTeX刷题版 — split by year to avoid memory overflow.
"""
import os, re, sys, glob, subprocess
sys.stdout.reconfigure(encoding='utf-8')

MD_DIR = r'C:\Users\23720\OneDrive\数学二'
OUT_DIR = r'C:\Users\23720\OneDrive\数学二\刷题版'
os.makedirs(OUT_DIR, exist_ok=True)

# ── LaTeX preamble (with proper CJK + Unicode fonts) ──
LATEX_PREAMBLE = r"""% !TEX program = xelatex
\documentclass[a4paper,11pt]{article}
\usepackage{fontspec}
\usepackage[UTF8, heading=true]{ctex}
\setCJKmainfont{Noto Serif SC}
\setCJKsansfont{Noto Sans SC}
\setmainfont{Times New Roman}
\usepackage[margin=2cm, top=2.5cm, bottom=2cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{fancyhdr}
\usepackage{hyperref}

% ── colors ──
\definecolor{yearblue}{HTML}{1a5276}
\definecolor{sectgreen}{HTML}{1e8449}
\definecolor{taggray}{HTML}{666666}
\definecolor{qbg}{HTML}{f8f9fa}

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

\begin{document}
"""

LATEX_POSTAMBLE = r"""
\end{document}
"""

def read_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def sanitize_latex(text):
    """Escape LaTeX specials, keep CJK/Unicode safe."""
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('\\{', '\\lbrace{}')
    text = text.replace('\\}', '\\rbrace{}')
    for ch in ['&', '%', '#', '_']:
        text = text.replace(ch, '\\' + ch)
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('^', '\\textasciicircum{}')
    return text

def parse_questions(text):
    """Split exam text into individual questions."""
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

def get_sec_short(sec):
    if not sec:
        return ''
    if '填空' in sec:
        return '填空题'
    if '选择' in sec:
        return '选择题'
    if '解答' in sec:
        return '解答题'
    return sec[:6]

def text_to_latex_body(raw_text):
    lines = raw_text.split('\n')
    parts = []
    for line in lines:
        line = line.strip()
        if not line:
            parts.append('')
            continue
        parts.append(sanitize_latex(line))
    return ' \\\\\n'.join(parts) if parts else ''

def generate_year_file(year, questions):
    """Generate a LaTeX file for one year's questions."""
    fname = f'{year}.tex'
    fpath = os.path.join(OUT_DIR, fname)

    latex = LATEX_PREAMBLE
    latex += f'\\title{{\\textbf{{{year}年 考研数学二试题}}}}\n'
    latex += f'\\author{{刷题版}}\n'
    latex += '\\date{}\n'
    latex += '\\maketitle\n'
    latex += '\\thispagestyle{fancy}\n\n'

    for sec, qnum, qtxt in questions:
        sec_short = get_sec_short(sec)
        title = f'{year}年'
        if sec_short:
            title += f' {sec_short}'
        title += f' 第{qnum}题'

        body = text_to_latex_body(qtxt)
        latex += f'\\begin{{qbox}}[{title}]\n'
        latex += body + '\n'
        latex += '\\end{qbox}\n'
        latex += '\\newpage\n\n'

    latex += LATEX_POSTAMBLE

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(latex)
    return fpath

def compile_tex(tex_path):
    """Compile a .tex file to PDF with xelatex."""
    dirn = os.path.dirname(tex_path)
    basename = os.path.basename(tex_path)
    name_no_ext = os.path.splitext(basename)[0]
    # Run twice for cross-references
    for i in range(2):
        result = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', basename],
            cwd=dirn, capture_output=True, text=True, timeout=120
        )
    # Check if PDF was created
    pdf_path = os.path.join(dirn, name_no_ext + '.pdf')
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) // 1024
        return True, size_kb
    return False, 0

def main():
    md_files = sorted(glob.glob(os.path.join(MD_DIR, '*年考研数学二试题.md')))
    print(f'Found {len(md_files)} markdown files')

    all_years = {}
    for fpath in md_files:
        basename = os.path.basename(fpath)
        year_match = re.match(r'(\d{4})年', basename)
        if not year_match:
            continue
        year = int(year_match.group(1))
        text = read_md(fpath)
        questions = parse_questions(text)
        all_years[year] = questions
        print(f'  {year}: {len(questions)} questions')

    total_q = sum(len(q) for q in all_years.values())
    print(f'\nTotal: {total_q} questions across {len(all_years)} years')

    # Generate and compile each year
    print('\n--- Generating & compiling ---')
    success = 0
    failed = []
    for year in sorted(all_years.keys()):
        questions = all_years[year]
        tex_path = generate_year_file(year, questions)
        ok, size_kb = compile_tex(tex_path)
        if ok:
            success += 1
            print(f'  {year}: OK ({size_kb} KB)')
        else:
            failed.append(year)
            print(f'  {year}: FAILED')

    print(f'\nDone: {success}/{len(all_years)} years compiled successfully')
    if failed:
        print(f'Failed: {failed}')

    # Merge all PDFs
    if success > 0:
        print('\n--- Merging PDFs ---')
        pdf_files = []
        for year in sorted(all_years.keys()):
            pdf_path = os.path.join(OUT_DIR, f'{year}.pdf')
            if os.path.exists(pdf_path):
                pdf_files.append(pdf_path)

        if pdf_files:
            # Use pdftk or qpdf to merge
            merged_path = os.path.join(OUT_DIR, '数学二刷题版_全部.pdf')
            # Try qpdf first
            cmd = ['qpdf', '--empty', '--pages'] + pdf_files + ['--', merged_path]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if os.path.exists(merged_path):
                    size_mb = os.path.getsize(merged_path) / (1024*1024)
                    print(f'Merged PDF: {merged_path} ({size_mb:.1f} MB)')
                else:
                    print('qpdf merge failed, trying pdftk...')
                    raise FileNotFoundError
            except (FileNotFoundError, subprocess.TimeoutExpired):
                # Try pypdf
                try:
                    from pypdf import PdfWriter, PdfReader
                    writer = PdfWriter()
                    for pdf_path in pdf_files:
                        reader = PdfReader(pdf_path)
                        for page in reader.pages:
                            writer.add_page(page)
                    with open(merged_path, 'wb') as f:
                        writer.write(f)
                    size_mb = os.path.getsize(merged_path) / (1024*1024)
                    print(f'Merged PDF: {merged_path} ({size_mb:.1f} MB)')
                except Exception as e:
                    print(f'Merge failed: {e}')

if __name__ == '__main__':
    main()

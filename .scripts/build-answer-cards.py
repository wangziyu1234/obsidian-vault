#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build-answer-cards.py — 考研数学二「答案与解析」md → 题卡 LaTeX → PDF（常驻工具）

把某一年的

    数学\\考研数学二\\YYYY年考研数学二答案与解析.md

转换成归档风格的 LaTeX（与 _题卡LaTeX源 里既有的 YYYY年考研数学二答案与解析.tex
逐行一致），用 xelatex 编两遍，再把 PDF 复制进 习题册\\。

用法
----
    python .scripts\\build-answer-cards.py 2003              # 写 tex + 编译两遍 + 复制 PDF
    python .scripts\\build-answer-cards.py 2003 --tex-only   # 只写 tex，不编译、不碰 PDF
    python .scripts\\build-answer-cards.py 2003 --check      # 写进 scratch 并与归档 tex 逐行对比
    python .scripts\\build-answer-cards.py --all             # 所有年份，只写 tex（默认不产 PDF）
    python .scripts\\build-answer-cards.py --all --tex-only  # 同上（显式）
    python .scripts\\build-answer-cards.py --all --pdf       # 所有年份，写 tex + 编译 + 复制 PDF
    python .scripts\\build-answer-cards.py --all --check     # 所有年份的对比

    --scratch DIR   草稿目录（默认 %TEMP%\\answer-cards），--check 与编译都在这里进行
    --if-changed    生成的 tex 与归档 tex 相同（且目标 PDF 已在位）就整年跳过：不写 tex、
                    不编译、不复制。`--all --pdf --if-changed` 可以做到「只重编改动的那几年」。

退出码：0 成功；非 0 表示失败（编译出错 / 缺文件 / --check 有差异）。
仅用标准库。
"""

import argparse
import difflib
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------- 路径与常量

ROOT = Path(__file__).resolve().parent.parent
SUBJECT_DIR = ROOT / "数学" / "考研数学二"
TEX_DIR = SUBJECT_DIR / "_题卡LaTeX源"
PDF_DIR = SUBJECT_DIR / "习题册"

MD_NAME = "{year}年考研数学二答案与解析.md"
TEX_NAME = "{year}年考研数学二答案与解析.tex"
PDF_NAME = "{year}年考研数学二答案与解析.pdf"

DEFAULT_XELATEX = r"C:\texlive\2026\bin\windows\xelatex.exe"
DEFAULT_SCRATCH = Path(os.environ.get("TEMP") or os.environ.get("TMP") or "/tmp") / "answer-cards"

# tex 前 15 行（第 1 行是空行）+ 标题行，抄自归档 tex，逐字节固定。
PREAMBLE_LINES = [
    "",
    r"\documentclass[UTF8,11pt,fontset=windows]{ctexart}",
    r"\usepackage[paperwidth=240mm,paperheight=200mm,margin=14mm,top=12mm,bottom=12mm]{geometry}",
    r"\usepackage{amsmath,amssymb,mathtools,bm}",
    r"\usepackage{xcolor,needspace}",
    r"\pagestyle{empty}",
    r"\setlength{\parindent}{0pt}",
    r"\setlength{\parskip}{6pt}",
    r"\linespread{1.08}",
    r"\setlength{\emergencystretch}{3em}",
    r"\allowdisplaybreaks[2]",
    r'\xeCJKDeclareCharClass{CJK}{"2460 -> "24FF}',
    r'\xeCJKDeclareCharClass{CJK}{"2160 -> "2188}',
    r"\ctexset{section={format=\Large\bfseries,beforeskip=12pt,afterskip=7pt}}",
    r"\begin{document}",
]
TITLE_TEMPLATE = r"{\LARGE\bfseries %s\par}\vspace{6pt}"

# 正文里的裸 Unicode 数学符号：归档转换器只对这两个做了替换（ρ/θ/− 等一律原样保留），
# 这里照抄，不自行扩大映射表。
UNICODE_MAP = {
    "\u03c0": r"$\pi$",        # π
    "\u27f9": r"$\Rightarrow$",  # ⟹
}

RE_ITEM = re.compile(r"^\*\*\d+\.\s*[（(]")
RE_SUBHEADING = re.compile(r"^#{3,6}\s+(.+)$")
RE_NUMBERED_TITLE = re.compile(r"^\d+\.\s*[（(]")
RE_CALLOUT = re.compile(r"^>\s*\[!([A-Za-z]+)\]\s*(.*)$")
RE_WIKI = re.compile(r"\[\[([^\[\]|]+)(?:\|([^\[\]]+))?\]\]")
RE_MATH_INLINE = re.compile(r"\$\$[^$\n]*\$\$|\$[^$\n]*\$")
RE_BOLD = re.compile(r"\*\*(.+?)\*\*")
RE_ESCAPE = re.compile(r"(?<!\\)([%&#_])")
RE_PLACEHOLDER = re.compile(r"\x00(\d+)\x00")

# ---------------------------------------------------------------- 行内转换


def inline(text):
    """把一行 md 转成 LaTeX 行内形式。

    与既有的试题卡生成器 gen.py 共用同一套约定：
    先切出数学段（`$…$` 与 `$$…$$`）并保护，只在非数学段转义 `%&#_`，最后统一 `**…**` → `\\textbf{…}`。
    """
    store = []

    def keep(match):
        store.append(match.group(0))
        return "\x00%d\x00" % (len(store) - 1)

    text = RE_MATH_INLINE.sub(keep, text)
    # `[[目标]]` → 目标；`[[目标|别名]]` → 别名
    text = RE_WIKI.sub(lambda m: m.group(2) if m.group(2) is not None else m.group(1), text)
    text = RE_ESCAPE.sub(r"\\\1", text)
    text = RE_BOLD.sub(r"\\textbf{\1}", text)
    for src, dst in UNICODE_MAP.items():
        text = text.replace(src, dst)
    return RE_PLACEHOLDER.sub(lambda m: store[int(m.group(1))], text)


def is_heading_line(line):
    """行首出现加粗段（`**…**` 开头）的行是「小标题」，前面发 \\Needspace{6\\baselineskip}。

    条目行（`**N.（…）**`）在调用之前已被 RE_ITEM 分流，不会重复发 5/6 两种版本。
    归档里 `**路①（题给的物理律）**：体积…` 这类「行首加粗 + 冒号正文」同样算小标题，
    所以判据就是朴素的行首加粗，不再对加粗段收尾字符另设条件。
    """
    return line.startswith("**")


# ---------------------------------------------------------------- 核心转换


def convert(md_text):
    """md 全文 → 归档风格的 tex 全文（CRLF，无 BOM，末尾一个换行）。"""
    # md 的行尾混用 LF 与 CRLF，先统一
    lines = md_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()

    out = []
    math = None            # None / '$$' / '$'：多行数学块状态
    first_section = True   # 第一个 `##` 前不加 \clearpage
    prev_section = False   # 紧跟 \section* 的那一行不加 \clearpage
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # --- 多行数学块：原样透传 ---
        if math is not None:
            out.append(line)
            if stripped == math:
                math = None
            prev_section = False
            i += 1
            continue
        if stripped in ("$$", "$"):
            math = stripped
            out.append(line)
            prev_section = False
            i += 1
            continue

        # --- H1 → 前 15 行固定前言 + 标题行 ---
        if i == 0 and line.startswith("# "):
            out.extend(PREAMBLE_LINES)
            out.append(TITLE_TEMPLATE % line[2:].strip())
            i += 1
            continue

        # --- H3-H6：题号标题沿用每题分页，其余作为小标题 ---
        subheading = RE_SUBHEADING.match(line)
        if subheading:
            title = subheading.group(1).replace("✏️", "").replace("✏", "").strip()
            if RE_NUMBERED_TITLE.match(title):
                line = "**%s**" % title
            else:
                out.append(r"\Needspace{6\baselineskip}")
                out.append(r"{\bfseries %s\par}" % inline(title))
                prev_section = False
                i += 1
                continue

        # --- `>` 块：连续 `>` 行合为一块 ---
        if line.startswith(">"):
            callout = RE_CALLOUT.match(line)
            first_body = line[1:]
            if first_body.startswith(" "):
                first_body = first_body[1:]
            body = []
            if callout is None and first_body.strip():
                body.append(inline(first_body))
            i += 1
            disp = False
            while i < n and lines[i].startswith(">"):
                cont = lines[i][1:]
                if cont.startswith(" "):
                    cont = cont[1:]
                if disp:
                    # 将整个公式保存在同一段，避免输出段间空行时拆开 aligned。
                    # 数学内容原样透传，防止 `_` `%` `&` 被误转义。
                    if cont.strip():
                        body[-1] += "\r\n" + cont
                    if cont.strip() == "$$":
                        disp = False
                elif cont.strip() == "$$":
                    body.append(cont)
                    disp = True
                elif cont.strip():
                    paragraph = inline(cont)
                    if is_heading_line(cont):
                        paragraph = r"\Needspace{9\baselineskip}" + paragraph
                    body.append(paragraph)
                i += 1
            if callout is not None:
                # callout：`\Needspace{4\baselineskip}` + 加粗小标题 + 正文段落
                out.append(r"\Needspace{4\baselineskip}")
                out.append(r"{\bfseries %s\par}" % inline(callout.group(2).strip()))
                for k, para in enumerate(body):
                    if k:
                        out.append("")
                    out.append(para)
            elif body:
                # 普通引用块：整块套一个灰色 group，段与段之间空行
                body[0] = r"\begingroup\color{gray}" + body[0]
                body[-1] = body[-1] + r"\par\endgroup"
                for k, para in enumerate(body):
                    if k:
                        out.append("")
                    out.append(para)
            else:
                out.append("")
            prev_section = False
            continue

        # --- `## 标题` → \clearpage + \section*（首个且为「答案速查」时不加 \clearpage）---
        if line.startswith("## "):
            title = line[3:].strip()
            if not (first_section and title == "答案速查"):
                out.append(r"\clearpage")
                out.append("")
            first_section = False
            out.append(r"\section*{%s}" % inline(title))
            prev_section = True
            i += 1
            continue

        # --- 题目条目 `**N.（…）…**` → \clearpage + \Needspace{5\baselineskip} ---
        if RE_ITEM.match(line):
            if not prev_section:
                out.append(r"\clearpage")
                out.append("")
            out.append(r"\Needspace{5\baselineskip}" + inline(line))
            prev_section = False
            i += 1
            continue

        # --- 小标题式加粗行 → \Needspace{6\baselineskip}；段落式加粗则照常输出 ---
        if line.startswith("**"):
            if is_heading_line(line):
                out.append(r"\Needspace{6\baselineskip}" + inline(line))
            else:
                out.append(inline(line))
            prev_section = False
            i += 1
            continue

        # --- 普通行 / 空行（连续空行并成一行）---
        if not stripped and out and out[-1] == "":
            i += 1
            continue
        out.append(inline(line))
        if stripped:
            prev_section = False
        i += 1

    out.append(r"\end{document}")
    return "\r\n".join(out) + "\r\n"


# ---------------------------------------------------------------- 文件读写


def read_text(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return fh.read()


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def md_path(year):
    return SUBJECT_DIR / MD_NAME.format(year=year)


def tex_path(year):
    return TEX_DIR / TEX_NAME.format(year=year)


def pdf_path(year):
    return PDF_DIR / PDF_NAME.format(year=year)


def find_years():
    years = []
    for p in SUBJECT_DIR.glob("*年考研数学二答案与解析.md"):
        m = re.match(r"(\d{4})年考研数学二答案与解析\.md$", p.name)
        if m:
            years.append(int(m.group(1)))
    return sorted(years)


def xelatex_binary():
    found = shutil.which("xelatex")
    if found:
        return found
    if Path(DEFAULT_XELATEX).is_file():
        return DEFAULT_XELATEX
    return None


# ---------------------------------------------------------------- 编译


def compile_pdf(year, tex_text, scratch):
    """在 scratch 里编译两遍，返回 (pdf 路径, 页数, 错误列表, 备注)。"""
    binary = xelatex_binary()
    if not binary:
        return None, None, ["找不到 xelatex（既不在 PATH，也不在 %s）" % DEFAULT_XELATEX], ""
    build = scratch / ("build-%d" % year)
    build.mkdir(parents=True, exist_ok=True)
    for stale in build.iterdir():
        if stale.is_file():
            stale.unlink()
    tex_file = build / ("%d.tex" % year)
    write_text(tex_file, tex_text)

    env = os.environ.copy()
    texlive_dir = str(Path(binary).parent)
    env["PATH"] = texlive_dir + os.pathsep + env.get("PATH", "")
    cmd = [binary, "-no-shell-escape", "-halt-on-error", "-interaction=nonstopmode", tex_file.name]
    note = ""
    for _ in range(2):
        res = subprocess.run(cmd, cwd=str(build), env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = (build / ("%d.log" % year))
        log_text = log.read_text(encoding="utf-8", errors="replace") if log.exists() else \
            (res.stdout or b"").decode("utf-8", "replace")
        if res.returncode != 0:
            note = "xelatex 退出码 %d" % res.returncode
            break

    errors = [l for l in log_text.splitlines() if l.startswith("! ")]
    pages = None
    m = re.search(r"Output written on .*?\((\d+) pages?", log_text)
    if m:
        pages = int(m.group(1))
    produced = build / ("%d.pdf" % year)
    if not produced.exists():
        errors.append("未生成 PDF")
        return None, pages, errors, note
    return produced, pages, errors, note


# ---------------------------------------------------------------- 各模式


def do_check(year, scratch, show, limit=None):
    src = md_path(year)
    arch = tex_path(year)
    if not src.exists():
        return "err", "%d 缺少 md：%s" % (year, src)
    if not arch.exists():
        return "err", "%d 缺少归档 tex：%s" % (year, arch)
    generated = convert(read_text(src))
    scratch_file = scratch / ("%d.tex" % year)
    write_text(scratch_file, generated)

    expected = read_text(arch)
    if generated == expected:
        return "same", "%d  0 差异行（生成 tex：%s）" % (year, scratch_file)

    a = expected.split("\r\n")
    b = generated.split("\r\n")
    diff = [l for l in difflib.unified_diff(a, b, fromfile="archive", tofile="generated", lineterm="", n=1)
            if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    msg = ["%d  %d 差异行（生成 tex：%s）" % (year, len(diff), scratch_file)]
    if show:
        hunks = [l for l in difflib.unified_diff(a, b, fromfile="archive", tofile="generated", lineterm="", n=1)]
        if limit:
            hunks = hunks[:limit]
        msg.extend("      " + l[:240] for l in hunks)
    return "diff", "\n".join(msg)


def do_build(year, scratch, tex_only, want_pdf, if_changed=False):
    src = md_path(year)
    if not src.exists():
        return "err", "%d 缺少 md：%s" % (year, src)
    generated = convert(read_text(src))
    target = tex_path(year)
    dest = pdf_path(year)
    if if_changed and target.exists() and read_text(target) == generated \
            and (tex_only or not want_pdf or dest.exists()):
        # 生成的 tex 与归档 tex 一致，且 PDF 已在位：整年跳过（不写 tex、不编译、不复制）
        return "skip", "%d  无变化，跳过（tex 与归档一致%s）" % (
            year, "，PDF 已在位" if (want_pdf and not tex_only) else "")
    write_text(target, generated)
    lines = ["tex=%s" % target]
    if tex_only or not want_pdf:
        lines.append("      tex-only：未编译，未改动 %s" % PDF_DIR.name)
        return "ok", "\n".join(lines)
    produced, pages, errors, note = compile_pdf(year, generated, scratch)
    real_errors = [e for e in errors if e != "未生成 PDF"]
    if produced is None or real_errors:
        out = ["tex=%s" % target]
        out.append("      编译失败：pages=%s errors=%d %s" % (pages, len(real_errors), note))
        out.extend("        " + e[:220] for e in (real_errors or errors)[:10])
        return "err", "\n".join(out)
    dest = pdf_path(year)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(produced, dest)
    lines.append("      pages=%s  xelatex errors=0  pdf=%s" % (pages, dest))
    if note:
        lines.append("      备注：%s" % note)
    return "ok", "\n".join(lines)


# ---------------------------------------------------------------- main


def main(argv=None):
    # 先切 UTF-8 输出，否则中文（包括 --help / 报错）在 GBK 控制台上会乱码
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="考研数学二答案卡：md → LaTeX → PDF")
    parser.add_argument("years", nargs="*", type=int, help="年份，如 2003；或改用 --all")
    parser.add_argument("--all", action="store_true", help="处理所有能找到的年份")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--tex-only", action="store_true", help="只写 tex，不编译、不碰 PDF")
    group.add_argument("--pdf", action="store_true", help="写 tex 并编译、复制 PDF")
    group.add_argument("--check", action="store_true", help="写进 scratch 并与归档 tex 逐行对比")
    parser.add_argument("--scratch", type=Path, default=DEFAULT_SCRATCH,
                        help="草稿目录（默认 %s）" % DEFAULT_SCRATCH)
    parser.add_argument("--if-changed", action="store_true",
                        help="生成的 tex 与归档 tex 相同（且目标 PDF 已在位）就跳过：不写 tex、不编译、不复制")
    parser.add_argument("-v", "--verbose", action="store_true", help="--check 时打印差异片段")
    args = parser.parse_args(argv)

    if args.all:
        years = find_years()
    elif args.years:
        years = sorted(set(args.years))
    else:
        parser.error("请给出年份，或使用 --all")
    if not years:
        print("没有找到任何年份的 md", file=sys.stderr)
        return 1

    args.scratch.mkdir(parents=True, exist_ok=True)
    started = time.time()
    statuses = []
    for year in years:
        if args.check:
            status, message = do_check(year, args.scratch, args.verbose, limit=None if args.verbose else 12)
        else:
            # 年份模式默认产 PDF；--all 模式默认只写 tex，须显式 --pdf
            want_pdf = bool(args.pdf) or (not args.all)
            status, message = do_build(year, args.scratch, args.tex_only, want_pdf, args.if_changed)
        statuses.append(status)
        print(message)
        if status == "err":
            print("      → %d 失败" % year, file=sys.stderr)

    elapsed = time.time() - started
    n_diff = sum(1 for s in statuses if s == "diff")
    n_err = sum(1 for s in statuses if s == "err")
    n_skip = sum(1 for s in statuses if s == "skip")
    print("—— %d 年，用时 %.1fs，失败 %d，差异 %d%s"
          % (len(years), elapsed, n_err, n_diff,
             "，跳过 %d" % n_skip if n_skip else ""))
    if n_err:
        return 1
    if args.check and n_diff:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

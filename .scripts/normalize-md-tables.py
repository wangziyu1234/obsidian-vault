#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 Markdown 表格压回「紧凑源码」风格（本库约定）。

背景：Obsidian 源码模式下**编辑过的表格会被自动按列宽补空格对齐**
（核心编辑器行为，无开关、与插件无关）。对齐后表格行可达 200+ 字符，
既违反「横向珍惜」的排版约定，又会在 git 里产生大量纯空白 diff。
本脚本把表格还原成 `| a | b |` + `| :-- | :-- |` 的紧凑形式，
与本库其它页面（777 各章答案速查表、目录页）保持一致。

用法：
    python .scripts/normalize-md-tables.py <文件或目录> [<文件或目录> ...]
    python .scripts/normalize-md-tables.py --check <文件或目录>     # 只报告不改写

约定：
- 单元格内容 strip 后用 ` | ` 连接，行首尾补 `| `；
- **分隔行只去掉多余空格，保留原有对齐语义**（`:--` 左、`:-:` 居中、`:--:` 右），
  不要把 `:---` 统一成 `:--`；
- 末尾空单元格写成 `| |`（不插入多余空格），避免无意义 diff；
- 按未转义的 `|` 切分，表格内 wikilink/图片的 `\\|` 转义不受影响；
- 输出一律 CRLF（本库行尾约定）。
"""
import os
import re
import sys

SPLIT = re.compile(r'(?<!\\)\|')


def cells(line):
    """按未转义的 | 切分，去掉首尾两个空项，逐格 strip。"""
    parts = SPLIT.split(line)
    return [c.strip() for c in parts[1:-1]]


PAD = re.compile(r'\|\s{2,}\S|\S\s{2,}\|')


def is_sep_row(cs):
    return bool(cs) and all(re.fullmatch(r':?-+:?', c) for c in cs if c)


def render(row):
    """把一行压回紧凑形式；已经紧凑的行原样返回（避免无意义 diff）。"""
    cs = cells(row)
    if is_sep_row(cs):                       # 分隔行：压到最短，保留对齐语义
        def norm(c):
            if c.count('-') <= 2:      # 已经是最短形式（`:--` / `:-:` / `--:`），原样保留
                return c
            return (':' if c.startswith(':') else '') + '--' + (':' if c.endswith(':') else '')
        out = '| ' + ' | '.join(norm(c) for c in cs) + ' |'
        return out if out != row else row
    if not PAD.search(row):                  # 数据行：只在确有对齐空格时才重写
        return row
    return '| ' + ' | '.join(cs) + ' |'


def normalize(text):
    """返回 (新文本, 改动的表格块数)。"""
    lines = text.replace('\r\n', '\n').split('\n')
    out, i, blocks, changed = [], 0, 0, 0

    def is_row(l):
        return l.startswith('|') and l.rstrip().endswith('|')

    while i < len(lines):
        if is_row(lines[i]):
            j = i
            blk = []
            while j < len(lines) and is_row(lines[j]):
                blk.append(lines[j])
                j += 1
            new = [render(row) for row in blk]
            if new != blk:
                changed += 1
            out.extend(new)
            blocks += 1
            i = j
        else:
            out.append(lines[i])
            i += 1

    return '\r\n'.join(out), blocks, changed


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs
                           if d not in ('.git', '.obsidian', '.workbuddy', '.venv')]
                for f in files:
                    if f.endswith('.md'):
                        yield os.path.join(root, f)
        elif p.endswith('.md'):
            yield p


def main(argv):
    check_only = '--check' in argv
    paths = [a for a in argv if not a.startswith('--')]
    if not paths:
        print(__doc__)
        return 1

    files = list(iter_files(paths))
    total_changed = 0
    for p in files:
        raw = open(p, 'rb').read().decode('utf-8')
        new, blocks, changed = normalize(raw)
        status = 'OK'
        if changed:
            status = '需规范化' if check_only else '已规范化'
            total_changed += 1
            if not check_only:
                open(p, 'wb').write(new.encode('utf-8'))
        if blocks or changed:
            print(f'{status:6s} {p}  表格块 {blocks}  改动 {changed}')

    if check_only:
        print(f'\n共 {total_changed} 个文件的表格与紧凑风格不一致。')
    else:
        print(f'\n共规范化 {total_changed} 个文件。')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

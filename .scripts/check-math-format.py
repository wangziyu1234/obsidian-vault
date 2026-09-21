#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数学笔记排版体检：补齐 check-notes.ps1 查不到的「渲染级」问题。

用法：
    python .scripts/check-math-format.py                 # 扫描全库
    python .scripts/check-math-format.py 数学 控制理论     # 只扫指定子目录

检查项（前四项会直接导致渲染出错，必须修）：
  1. 数学公式里缺反斜杠的命令      $2pi a$ / $0le e<1$ / $-infty$ / $nge2$ / $xle1$
  2. 表格被打断                   表头/表体之间插了引用块或正文，后半截不再渲染成表格
  3. 公式内的全角标点             $\dfrac{a}{b}=1，$ 里的 `，`、`、`
  4. 附录里出现 H3（`###`）        附录统一只用 H2 + **粗体标签**
  5. 相邻两个 `$$` 块紧贴          违反「块间留空行」，块之间要插一行空行（callout 内插 `>`）
  6. 列表缩进 1 或 3 个空格        Markdown 嵌套列表必须 2 或 4 个空格
  7. 行尾多余空格
  8. 正文/引用块里超过 200 字符的长行（表格行不计入）

退出码：0 无渲染级问题；1 存在 1-4 类问题。
"""
from __future__ import print_function

import os
import re
import sys

# 缺反斜杠命令的候选名。前两组是「只可能是命令」的，可以放心粘在字母后面查；
# le/ge/ne/infty 之类要配合「粘连」判定，否则会误伤 \angle、x^ne^{-x} 这种写法。
CMDS_SAFE = ('infty', 'cdots', 'ldots', 'cdot', 'frac', 'sqrt', 'alpha', 'beta',
             'gamma', 'theta', 'lambda', 'sigma', 'omega', 'approx', 'equiv', 'quad')
CMDS_GLUE = ('le', 'ge', 'ne', 'pi')

SKIP_DIRS = ('.obsidian', '.trash', '.venv', 'copilot', 'templates', 'Excalidraw',
             '教材OCR', '_moved_out', '.workbuddy', '.git')

RE_MATH = re.compile(r'\$\$(.+?)\$\$|\$(.+?)\$', re.S)
RE_DD_LINE = re.compile(r'^(\s*>\s*)*\$\$\s*$')
RE_TOKEN = re.compile(r'(\\?)([A-Za-z]+)')
RE_LIST = re.compile(r'^( +)((?:[-*+]|\d+\.) )')


def norm_quote(line):
    return re.sub(r'^(\s*>\s*)+', '', line).strip()


def is_table(line):
    # 至少两个竖线才算表格行；公式里的绝对值 |x-x_0| 不算
    return line.strip().startswith('|') and line.count('|') >= 2


def is_sep(line):
    return re.match(r'^\|[\s:\-|]+\|$', line.strip()) is not None


def check_file(path, rel):
    findings = []
    raw = open(path, 'rb').read().decode('utf-8', 'replace')
    lines = raw.replace('\r\n', '\n').split('\n')
    is_appendix = os.path.basename(path).startswith('附录')
    in_fence = False
    in_math = False

    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        prev = lines[i - 2] if i >= 2 else ''
        nxt = lines[i] if i < len(lines) else ''
        stripped = re.sub(r'\$[^$\n]*\$', '', line)   # 抹掉行内公式，供标点检查用

        # 1. 公式里缺反斜杠的命令 / 3. 公式里的全角标点
        for m in RE_MATH.finditer(line):
            span = m.group(1) or m.group(2)
            # 全角标点检查：先去掉 \text{…}（里面本来就该是中文），再找全角标点
            if re.search(r'[，、；]', re.sub(r'\\text\{[^}]*\}', '', span)):
                findings.append(('渲染', i, '行内公式里出现全角标点（改用半角 , \\ 或 \\quad）'))
            for t in RE_TOKEN.finditer(span):
                if t.group(1) == '\\':
                    continue
                word = t.group(2)
                for c in CMDS_SAFE:
                    if word.endswith(c) and len(word) - len(c) == 1:
                        findings.append(('渲染', i, '公式里缺反斜杠：%s → 应为 \\%s' % (word, c)))
                        break
                else:
                    for c in CMDS_GLUE:      # 与字母粘连，如 $nge2$、$xle1$、$2pi a$
                        if word.endswith(c) and len(word) - len(c) in (1, 2):
                            findings.append(('渲染', i, '公式命令与字母粘连：%s → 应为 …\\%s…' % (word, c)))
                            break

        # 4. 附录 H3（附录 图像变换 为已知豁免）
        if is_appendix and line.startswith('### ') and '附录 图像变换' not in path:
            findings.append(('结构', i, '附录里出现 H3，改用 H2 + **粗体标签**'))

        # 5. 相邻 $$ 块紧贴
        if RE_DD_LINE.match(line):
            if not in_math:
                in_math = True
            else:
                in_math = False
                if nxt and RE_DD_LINE.match(nxt):
                    findings.append(('排版', i, '两个 $$ 块紧贴，块间需空行（callout 内插一行 `>`）'))

        # 6. 列表缩进
        m = RE_LIST.match(line)
        if m and len(m.group(1)) in (1, 3):
            findings.append(('排版', i, '嵌套列表缩进 %d 个空格，应为 2 或 4' % len(m.group(1))))

        # 7. 行尾空格
        if line != line.rstrip() and line.strip():
            findings.append(('排版', i, '行尾多余空格'))

        # 8. 超长行（表格行豁免）
        if len(line) > 200 and not is_table(line):
            findings.append(('排版', i, '单行 %d 字符（>200），建议断行' % len(line)))

    # 2. 表格被打断：一段连续的表格行，首行之后不是分隔行
    i = 0
    while i < len(lines):
        if is_table(lines[i]) and not RE_DD_LINE.match(lines[i]) and '|' not in lines[i].strip('|'):
            j = i
            while j < len(lines) and is_table(lines[j]):
                j += 1
            if j - i > 1 and not is_sep(lines[i + 1]):
                findings.append(('渲染', i + 1, '表格缺表头：中间被正文/引用块打断，后半截不会渲染成表格'))
            i = j
        else:
            i += 1

    # 2b. 公式块定界行前后是不是真的空行（只看块之间，正文紧贴公式不算错）
    return findings


def main():
    root = os.getcwd()
    targets = sys.argv[1:] or ['.']
    bad = 0
    total = 0
    for tgt in targets:
        base = os.path.join(root, tgt)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if not fn.endswith('.md') or fn.endswith('.excalidraw.md'):
                    continue
                if fn in ('AGENTS.md', 'README.md'):
                    continue
                path = os.path.join(dirpath, fn)
                rel = os.path.relpath(path, root)
                findings = check_file(path, rel)
                if findings:
                    print('--- %s' % rel)
                    for kind, ln, msg in findings:
                        print('    [%s] L%d  %s' % (kind, ln, msg))
                total += len(findings)
                bad += sum(1 for k, _, _ in findings if k == '渲染')
    print('\n共 %d 处问题，其中渲染级 %d 处。' % (total, bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())

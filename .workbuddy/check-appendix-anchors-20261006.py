from pathlib import Path
import re
import json

root = Path('D:/obsidian')
base = root / '控制理论/自动控制原理'
files = sorted(base.glob('附录*.md')) + [base / n for n in (
    '自动控制原理.md', '07-1 采样与z变换.md', '07 第7章 线性离散系统的分析与校正.md',
    '05-3-1 幅相曲线的画法与最小相位.md', '05-3 奈氏图（幅相特性与奈氏判据）.md',
    '05 第5章 线性系统的频域分析法.md')]
all_paths = list((root/'控制理论').rglob('*.md')) + list((root/'数学').rglob('*.md')) + [root/'README.md']
by_name = {p.stem: p for p in all_paths}
issues = []
anchors = 0
for file in files:
    text = file.read_text(encoding='utf-8-sig')
    for m in re.finditer(r'\[\[([^\]\n]+)\]\]', text):
        target = m.group(1).replace('\\|', '|').split('|', 1)[0]
        if '#' not in target:
            continue
        name, anchor = target.split('#', 1)
        dest = file if not name else by_name.get(name.removesuffix('.md')) or by_name.get(name.split('/')[-1].removesuffix('.md'))
        if dest is None:
            issues.append((file.name, 'missing file', target))
            continue
        body = dest.read_text(encoding='utf-8-sig')
        headings = re.findall(r'^#{1,6}\s+(.+?)\s*$', body, re.M)
        valid = bool(re.search(r'(?m)(?:^|\s)\^' + re.escape(anchor[1:]) + r'\s*$', body)) if anchor.startswith('^') else anchor in headings
        anchors += 1
        if not valid:
            issues.append((file.name, 'missing anchor', target))
    for m in re.finditer(r'\*\*([^\n]+?)\*\*', text):
        if re.search(r'\$[^$]*\^\*[^$]*\$', m.group(1)):
            issues.append((file.name, 'star formula in bold', m.group(0)))
print(json.dumps({'files':len(files), 'anchors':anchors, 'issues':issues}, ensure_ascii=False, indent=2))
raise SystemExit(bool(issues))

from pathlib import Path
import re
import json
import collections
import os

root = Path('D:/obsidian')
base = root / '控制理论/777习题集'
files = sorted([*base.glob('现控200题基础*.md'), *base.glob('现控200题强化*.md')])
expected = {('基础', 1): 27, ('基础', 2): 12, ('基础', 3): 27,
            ('基础', 4): 19, ('基础', 5): 34,
            ('强化', 1): 31, ('强化', 2): 29, ('强化', 3): 33}
topic_numbers = {'一': 1, '二': 2, '三': 3}
allfiles = [p for folder in ['控制理论', '数学', '英语', '附件']
            for p in (root / folder).rglob('*') if p.is_file()]
allfiles += list(root.glob('*.md'))
names = collections.defaultdict(list)
for p in allfiles:
    names[p.name].append(p)
    names[p.stem].append(p)
errors = []
stats = []
cache = {}


def err(p, msg):
    errors.append(str(p.relative_to(root)) + ': ' + msg)


def read(p):
    if p not in cache:
        cache[p] = p.read_text(encoding='utf-8-sig')
    return cache[p]


def group(p):
    if '现控200题基础' in p.name:
        return '基础', int(re.search(r'第(\d+)章', p.name)[1])
    return '强化', topic_numbers[re.search(r'专题([一二三])', p.name)[1]]


def resolve(target):
    target = target.replace('\\', '/')
    for p in [root / target, root / (target + '.md')]:
        if p.is_file():
            return p
    for p in names.get(Path(target).name, []):
        if '/' not in target or p.as_posix().endswith('/' + target) or p.as_posix().endswith('/' + target + '.md'):
            return p


def heads(t):
    return re.findall(r'^#{1,6} (.+?)\s*$', t, re.M)


def wiki(t):
    for m in re.finditer(r'(!?)\[\[([^\]]+)\]\]', t):
        target = m[2].replace('\\|', '|').split('|')[0]
        fn, sep, anchor = target.partition('#')
        yield m, target, fn, sep, anchor


if len(files) != 16:
    errors.append('Expected 16 files, got ' + str(len(files)))

for p in files:
    t = read(p)
    key = group(p)
    chapter = key[1]
    sol = '答案与解析' in p.name
    ns = re.findall(r'^#### ✏️ (\d+-\d+)　' + ('解析' if sol else '题目') + '$', t, re.M)
    want = [f'{chapter}-{n}' for n in range(1, expected[key] + 1)]
    if ns != want:
        err(p, 'exercise headings not sequential/complete ' + str(ns))
    peers = [x for x in files if group(x) == key and ('（题目）' in x.name if sol else '（答案与解析）' in x.name)]
    if len(peers) != 1:
        err(p, 'paired file count ' + str(len(peers)))
        continue
    peer = peers[0]
    for n in want:
        if f'[[{peer.stem}#✏️ {n}　' + ('题目' if sol else '解析') + '|' not in t:
            err(p, 'missing paired link ' + n)
    if t.count('[[#🔎 题号直达|返回题号导航]]') != len(want):
        err(p, 'return navigation count')
    if not sol:
        start = t.find('## 🔎 题号直达')
        end = t.find('\n## ', start + 1)
        if start < 0 or end < 0:
            err(p, 'question navigation missing')
        else:
            found = re.findall(r'\[\[#✏️ (\d+-\d+)　题目\\\|', t[start:end])
            if sorted(found) != sorted(want):
                err(p, 'question navigation incomplete')
    if len(re.findall(r'^# ', t, re.M)) != 1:
        err(p, 'H1 count')
    if t.find('> [!abstract]') < t.find('\n# ') or '> [!abstract]' not in t:
        err(p, 'abstract order')
    if not re.match(r'\A---\r?\ncreate:.*?\r?\nmodify:.*?\r?\ntags:', t, re.S):
        err(p, 'frontmatter field order')
    if re.search(r'TODO|FIXME|待补|\?\?|\[\[\]\]', t):
        err(p, 'placeholder')
    if sol:
        for tag, start_marker, end_marker in [('nav', '## 🔎 题号直达', '## 答案速查'), ('table', '## 答案速查', '\n## 【')]:
            start = t.find(start_marker)
            end = t.find(end_marker, start + len(start_marker))
            if start < 0 or end < 0:
                err(p, tag + ' section missing')
                continue
            frag = t[start:end]
            found = re.findall(r'\[\[#✏️ (\d+-\d+)　解析\\\|', frag)
            if sorted(found) != sorted(want):
                err(p, tag + ' coverage ' + str(found))
    imagecount = linkcount = 0
    for m, target, fn, sep, anchor in wiki(t):
        dest = resolve(fn) if fn else p
        if not dest:
            err(p, 'missing ' + target)
            continue
        if m[1]:
            imagecount += 1
        else:
            linkcount += 1
        if sep and not anchor.startswith('^'):
            if heads(read(dest)).count(anchor) != 1:
                err(p, 'anchor not unique/missing ' + target)
    clean = re.sub(r'^(?:\s*>\s?)+', '', t, flags=re.M)
    blocks = re.findall(r'\$\$([\s\S]*?)\$\$', clean)
    if clean.count('$$') % 2:
        err(p, 'display delimiters')
    for b in blocks:
        stack = []
        for m in re.finditer(r'\\(begin|end)\{([^}]+)\}', b):
            if m[1] == 'begin':
                stack.append(m[2])
            elif not stack or stack.pop() != m[2]:
                err(p, 'environment nesting')
        if stack:
            err(p, 'open environment')
        if len(re.findall(r'\\left(?![a-zA-Z])', b)) != len(re.findall(r'\\right(?![a-zA-Z])', b)):
            err(p, 'left/right pair')
        if '[[' in b:
            err(p, 'wikilink in math')
    for line in t.splitlines():
        if line.lstrip('> ').startswith('|'):
            if any(re.search(r'(?<!\\)\|', w) for w in re.findall(r'\[\[(.*?)\]\]', line)):
                err(p, 'table wiki pipe unescaped')
    stats.append(dict(file=p.name, exercises=len(ns), links=linkcount,
                      images=imagecount, math_blocks=len(blocks)))

for key in expected:
    q = next(p for p in files if group(p) == key and '（题目）' in p.name)
    a = next(p for p in files if group(p) == key and '（答案与解析）' in p.name)
    def imgs(p):
        return {resolve(fn) for m, target, fn, sep, anchor in wiki(read(p)) if m[1]}
    missing = imgs(q) - imgs(a)
    if missing:
        err(a, 'question images absent ' + str(missing))
    for n in range(1, expected[key] + 1):
        number = f'{key[1]}-{n}'
        def exercise_text(p, kind):
            text = read(p)
            start = re.search(r'^#### ✏️ ' + re.escape(number) + '　' + kind + '$', text, re.M)
            if not start:
                return ''
            tail = text[start.end():]
            end = re.search(r'^#{2,4} ', tail, re.M)
            return tail[:end.start()] if end else tail
        def image_destinations(text):
            return {resolve(fn) for m, target, fn, sep, anchor in wiki(text) if m[1]}
        absent = image_destinations(exercise_text(q, '题目')) - image_destinations(exercise_text(a, '解析'))
        if absent:
            err(a, 'question images absent in matching exercise ' + number + ': ' + str(absent))

# Scan note sources outside the 16 deliverables, including templates and root pages.
# Generated files, OCR source material, configuration, and archived notes are excluded.
excluded = {'.git', '.obsidian', '.venv', '.trash', '.workbuddy', '.scripts',
            'node_modules', '教材OCR', '_moved_out', '__pycache__'}
external_files = external_refs = external_anchors = 0
selected = set(files)
for folder, dirs, filenames in os.walk(root):
    dirs[:] = [d for d in dirs if d not in excluded and not d.startswith('.')]
    for name in filenames:
        p = Path(folder) / name
        if p.suffix != '.md' or p in selected or name == 'AGENTS.md':
            continue
        external_files += 1
        for m, target, fn, sep, anchor in wiki(read(p)):
            if not fn:
                continue
            dest = resolve(fn)
            if dest not in selected:
                continue
            external_refs += 1
            if sep:
                external_anchors += 1
                if anchor.startswith('^'):
                    if not re.search(r'(?:^|\s)' + re.escape(anchor) + r'\s*$', read(dest), re.M):
                        err(p, 'external block reference missing ' + target)
                elif heads(read(dest)).count(anchor) != 1:
                    err(p, 'external anchor not unique/missing ' + target)

result = dict(files=stats, unique_exercises=sum(expected.values()),
              external_scan=dict(files=external_files, references=external_refs,
                                 anchors=external_anchors), errors=errors)
out = root / '.workbuddy/mc-all-final-validation.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))

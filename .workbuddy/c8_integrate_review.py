from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
target = next((root / '控制理论' / '777习题集').glob('基础300题 第8章*答案与解析*.md'))
a, b = map(int, sys.argv[1:3])
draft = root / '.workbuddy' / f'c8-review-{a}-{b}.md'
raw = target.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
s = raw.decode('utf-8-sig').replace('\r\n', '\n')
start = re.search(rf'^\*\*8-{a}　解析\*\*', s, re.M).start()
if b == 43:
    end = len(s)
else:
    end = re.search(rf'^\*\*8-{b+1}　解析\*\*', s, re.M).start()
    # Retain the next knowledge-point heading outside this range.
    section = list(re.finditer(r'^## .*$', s[start:end], re.M))
    if section:
        last = start + section[-1].start()
        if not re.search(r'^\*\*8-\d+　解析\*\*', s[last:end], re.M):
            end = last
body = draft.read_text(encoding='utf-8-sig').replace('\r\n', '\n').strip()
assert body.startswith(f'**8-{a}　解析**'), 'Draft must start with exercise heading'
result = s[:start] + body + '\n\n' + s[end:]
result = result.replace('modify: 2026-09-26', 'modify: 2026-10-05', 1)
bom = b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
target.write_bytes(bom + result.replace('\n', newline).encode('utf-8'))
print(f'integrated {a}-{b}')

from pathlib import Path
import re

base = Path('D:/obsidian/控制理论/777习题集')
for chapter, expected in [(1, 27), (2, 12), (5, 34)]:
    path = next(base.glob(f'现控200题基础 第{chapter}章*（题目）.md'))
    raw = path.read_bytes()
    bom = b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    text = raw[len(bom):].decode('utf-8')
    if text.count('[[#🔎 题号直达|返回题号导航]]') == expected:
        print(path, 'already complete')
        continue
    original_crlf = text.count('\r\n')
    original_lf = text.count('\n')
    text, count = re.subn(
        r'^(\[\[现控200题基础 [^\r\n]+\|(?:查看解析|直达解析)\]\])(?=\r?$)',
        r'\1 · [[#🔎 题号直达|返回题号导航]]', text, flags=re.M)
    assert count == expected, (path, count, expected)
    text, count = re.subn(r'^modify: [^\r\n]+', 'modify: 2026-10-07', text, count=1, flags=re.M)
    assert count == 1
    assert text.count('\r\n') == original_crlf and text.count('\n') == original_lf
    path.write_bytes(bom + text.encode('utf-8'))
    print(path, expected, 'backlinks added; BOM and line endings preserved')

path = next(base.glob('现控200题强化 专题三*（题目）.md'))
raw = path.read_bytes()
newline = b'\r\n' if b'\r\n' in raw else b'\n'
path.write_bytes(raw.rstrip(b'\r\n') + newline)
print(path, 'trailing blank lines removed')

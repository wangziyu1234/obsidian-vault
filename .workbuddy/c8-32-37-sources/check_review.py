from pathlib import Path
import re
p=Path('D:/obsidian/.workbuddy/c8-review-32-37.md')
t=p.read_text('utf8')
assert t.startswith('**8-32\u3000解析**')
assert re.findall(r'^\*\*(8-\d+)\u3000解析',t,re.M)==[f'8-{n}' for n in range(32,38)]
assert t.count('$$')%2==0
assert t.replace('$$','').count('$')%2==0
assert re.findall(r'\\begin\{([^}]+)\}',t)==re.findall(r'\\end\{([^}]+)\}',t)
assert len(re.findall(r'\\left(?![a-zA-Z])',t))==len(re.findall(r'\\right(?![a-zA-Z])',t))
assert 'TODO' not in t and 'FIXME' not in t and '？' not in t
assert len(re.findall(r'^## ',t,re.M))==1
for m in re.finditer(r'\$\$(.*?)\$\$',t,re.S):
    if len(m[1].strip())>170:print('CHECK LONG MATH',len(m[1].strip()))
print('PASS: six titles; knowledge heading; dollar, environment, delimiter pairs; no placeholders.')

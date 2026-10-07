from pathlib import Path
import re
root=Path('D:/obsidian')
for p in (root/'控制理论/777习题集').glob('现控200题强化 专题二*.md'):
 t=p.read_text(encoding='utf-8');p.write_bytes((t.rstrip()+'\n').replace('\n','\r\n').encode('utf-8'))
 ids=re.findall(r'^#### ✏️ 2-(\d+)',t,re.M)
 assert list(map(int,ids))==list(range(1,30))
 print('q' if '题目）' in p.name else 'a','29 anchors verified')
 for m in re.finditer(r'\$\$([\s\S]*?)\$\$',t):
  if len(m[1])>170 and r'\begin{aligned}' not in m[1]:
   print('LONG',t[:m.start()].count('\n')+1,len(m[1]),ascii(m[1]))

from pathlib import Path
import re
base=Path('D:/obsidian/控制理论/777习题集')
for p in base.glob('现控200题基础 第2章*.md'):
    raw=p.read_bytes(); t=raw.decode('utf-8-sig').replace('\r\n','\n')
    if '（题目）' in p.name and '## 🔎 题号直达' not in t:
        nav=['## 🔎 题号直达','','| 题号范围 | 直达题目 |','| :-- | :-- |']
        for st in range(1,13,5):
            en=min(st+4,12)
            nav.append(f'| 2-{st}～2-{en} | '+' · '.join(f'[[#✏️ 2-{i}　题目\\|2-{i}]]' for i in range(st,en+1))+' |')
        t=t.replace('## 【题型1】','\n'.join(nav)+'\n\n## 【题型1】',1)
    if '（答案与解析）' in p.name:
        t=t.replace('>\n> ![[附件/现控2-9-采样系统方框图.png|520]]','\n![[附件/现控2-9-采样系统方框图.png|520]]')
    t='\n'.join(line.rstrip() for line in t.split('\n'))
    p.write_bytes(t.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))

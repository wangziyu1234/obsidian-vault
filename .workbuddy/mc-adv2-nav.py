from pathlib import Path
import re

root = Path('D:/obsidian')
base = '现控200题强化 专题二 线性系统的能控能观性及稳定性分析'
qp = root/'控制理论/777习题集'/f'{base}（题目）.md'
ap = root/'控制理论/777习题集'/f'{base}（答案与解析）.md'
q = qp.read_text(encoding='utf-8-sig')
a = ap.read_text(encoding='utf-8-sig')
assert '#### ✏️ 2-1' not in q
for suffix, t in [('q',q),('a',a)]:
    (root/'.workbuddy'/f'mc-adv2-original-{suffix}.md').write_text(t,encoding='utf-8')

def split(t,pat):
    ms = list(re.finditer(pat,t,re.M))
    out = {}
    for i,m in enumerate(ms):
        end = ms[i+1].start() if i+1<len(ms) else len(t)
        s=t[m.end():end]; tail=''
        h=re.search(r'\n## ',s)
        if h:s,tail=s[:h.start()],s[h.start():]
        out[int(m[1])]=[m[0],s,tail]
    return t[:ms[0].start()],out

qh,qs=split(q,r'^\*\*2-(\d+)（[^\n]+?\*\*')
ah,ans=split(a,r'^\*\*2-(\d+)　答案\*\*')
assert len(qs)==len(ans)==29

def nav(kind):
    rows=['## 🔎 题号直达','','| 题号范围 | 直达'+kind+' |','| :-- | :-- |']
    for start in range(1,30,5):
        end=min(start+4,29)
        links=' · '.join(f'[[#✏️ 2-{n}　{kind}\\|2-{n}]]' for n in range(start,end+1))
        rows.append(f'| 2-{start}～2-{end} | {links} |')
    return '\n'.join(rows)+'\n\n'

def quote(t):
    return '\n'.join('> '+line if line else '>' for line in t.strip().splitlines())

# Keep established section labels and existing mathematics unchanged in this pass.
qh=qh.replace('modify: 2026-10-01','modify: 2026-10-07')
ah=ah.replace('modify: 2026-10-01','modify: 2026-10-07')
qh=qh.replace('## 【题型1】',nav('题目')+'## 【题型1】')
ah=ah.replace('## 答案速查',nav('解析')+'## 答案速查')
ah=re.sub(r'(?<=\| )2-(\d+)(?= \|)',lambda m:f'[[#✏️ 2-{m[1]}　解析\\|2-{m[1]}]]',ah)

qout=qh
aout=ah
for n in range(1,30):
    src=qs[n][0].split('（',1)[1].removesuffix('**')
    src='（'+src
    qb=src+' '+qs[n][1].lstrip()
    qout+=(f'#### ✏️ 2-{n}　题目\n\n'
           f'[[{base}（答案与解析）#✏️ 2-{n}　解析|查看解析]] · [[#🔎 题号直达|返回题号导航]]\n\n'
           +qb.strip()+'\n\n'+qs[n][2])
    # Preserve images outside the collapsed text for immediate reference.
    imgs=re.findall(r'^!\[\[.*?\]\]$',qb,re.M)
    qt=re.sub(r'^!\[\[.*?\]\]\n?', '',qb, flags=re.M)
    aout+=(f'#### ✏️ 2-{n}　解析\n\n'
           f'[[{base}（题目）#✏️ 2-{n}　题目|原题]] · [[#🔎 题号直达|返回题号导航]]\n\n'
           '> [!note]- 本题题设\n'+quote(qt)+'\n\n'
           +('\n\n'.join(imgs)+'\n\n' if imgs else '')
           +ans[n][1].strip()+'\n\n'+ans[n][2])
qp.write_bytes(qout.replace('\n','\r\n').encode('utf-8'))
ap.write_bytes(aout.replace('\n','\r\n').encode('utf-8'))
print('Created 29 paired question / answer anchors with local navigation and copied statements.')

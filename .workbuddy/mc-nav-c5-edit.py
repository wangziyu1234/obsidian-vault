from pathlib import Path
import re
import pymupdf

root=Path('D:/obsidian')
base=root/'控制理论/777习题集'
q=next(base.glob('现控200题基础 第5章*题目*.md'))
a=next(base.glob('现控200题基础 第5章*答案*.md'))
qt=q.read_text(encoding='utf-8'); at=a.read_text(encoding='utf-8')
qt=qt.replace('现控5-8-阶跃响应.png|637','现控5-8-阶跃响应.png|430')
matches=list(re.finditer(r'^\*\*(5-\d+)(.*?)\*\*(.*)$',qt,re.M))
questions={}
for i,m in enumerate(matches):
    end=matches[i+1].start() if i+1<len(matches) else len(qt)
    part=qt[m.start():end].split('\n## ')[0].strip()
    questions[m[1]]=part
nav=['## 🔎 题号直达','','| 题号范围 | 直达解析 |','| :-- | :-- |']
for lo in range(1,35,5):
    hi=min(lo+4,34)
    nav.append(f'| 5-{lo}～5-{hi} | '+' · '.join(f'[[#✏️ 5-{n}　解析\\|5-{n}]]' for n in range(lo,hi+1))+' |')
at=at.replace('## 答案速查','\n'.join(nav)+'\n\n## 答案速查',1)
start=at.index('| 题号 | 答案 |'); end=at.index('\n## ',start)
rows={}
for line in at[start:end].splitlines()[2:]:
    cells=line.strip('|').split('|')
    if len(cells)==4:
        for ix in (0,2): rows[int(cells[ix].strip().split('-')[1])]=cells[ix+1].strip()
table=['| 题号 | 结论与关键结果 |','| :-- | :-- |']
for n in range(1,35): table.append(f'| [[#✏️ 5-{n}　解析\\|5-{n}]] | {rows[n]} |')
at=at[:start]+'\n'.join(table)+'\n'+at[end:]
def sol(m):
    num=m[1]
    body=questions[num]
    # Keep the original diagrams visible and include text in a collapsible note.
    pics=re.findall(r'^!\[\[.*?\]\]$',body,re.M)
    body=re.sub(r'^!\[\[.*?\]\]\n?', '',body,flags=re.M).strip()
    call='> [!note]- 本题题设\n'+'\n'.join('> '+x if x else '>' for x in body.splitlines())
    return f'#### ✏️ {num}　解析\n\n'+f'[[{q.stem}#✏️ {num}　题目|查看题目]] · [[#🔎 题号直达|返回题号导航]]\n\n'+call+'\n\n'+('\n\n'.join(pics)+'\n\n' if pics else '')+m[0]
at=re.sub(r'^\*\*(5-\d+).*$',sol,at,flags=re.M)
qt=re.sub(r'^(\*\*(5-\d+).*?)$',lambda m:f'#### ✏️ {m[2]}　题目\n\n[[{a.stem}#✏️ {m[2]}　解析|直达解析]]\n\n'+m[1],qt,flags=re.M)
at=at.replace('（完全能控且完全能观）','（记 $B=b$、$C=c$，维数分别为 $n\\times1$、$1\\times n$）')
at=at.replace('C[sI-(A-BK)]^{-1}b','C[sI-(A-BK)]^{-1}B')
at=at.replace('只决定估计误差 $\\bar x$ 的收敛速度。','决定估计误差 $\\bar x$ 的动态；只有 $A-GC$ 为 Hurwitz 矩阵时，误差才渐近收敛。上述分块变换与零初态传递函数恒等式本身不要求完全能控或完全能观。')
at=at.replace('设计状态观测器（全维或降维）','设计全维状态观测器')
at=at.replace('② 输出反馈：','**补充辨析：输出反馈与输出注入。** 原题第（2）问的状态反馈设计已完成，下面比较两种其他结构。\n\n② 输出反馈：',1)
at=at.replace('四阶系统里能控性矩阵只有一列注入','四阶系统只有一个输入通道')
at=at.replace('A+bK','A+BK')
for p,s in ((q,qt),(a,at)):
    raw=p.read_bytes(); nl='\r\n' if b'\r\n' in raw else '\n'
    p.write_bytes(s.replace('\n',nl).encode('utf-8'))

# Original scans: preserve all arrows, linework and a margin; no binarization/autotrim.
lib=Path('E:/BaiduNetdiskDownload/777现控200题➕答案')
qd=pymupdf.open(next(lib.glob('*题目册*.pdf')))
ad=pymupdf.open(next(lib.glob('*答案册*.pdf')))
items=[
 (qd,61,'现控5-8-阶跃响应',(0.60,0.215,0.87,0.360)),
 (qd,64,'现控5-15-方框图',(0.39,0.652,0.95,0.815)),
 (qd,70,'现控5-26-方框图',(0.46,0.108,0.67,0.164)),
 (qd,70,'现控5-27-同步卫星示意图',(0.60,0.640,0.94,0.795)),
 (qd,74,'现控5-34-观测器状态反馈结构图',(0.36,0.113,0.84,0.355)),
 (ad,100,'现控5-31-状态反馈模拟结构图',(0.31,0.738,0.83,0.955)),
]
for doc,num,name,box in items:
    page=doc[num-1]; w,h=page.rect.width,page.rect.height
    clip=pymupdf.Rect(box[0]*w,box[1]*h,box[2]*w,box[3]*h)
    page.get_pixmap(clip=clip,dpi=240).save(root/'附件'/f'{name}.png')
print('34 question anchors, 34 solution anchors, 34 shortcuts; 6 original scans recropped')

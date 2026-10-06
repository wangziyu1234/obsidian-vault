from pathlib import Path
import re
import json

root=Path('D:/obsidian')
manifest=json.loads((root/'.workbuddy/appendix-move-manifest-20261006.json').read_text(encoding='utf-8-sig'))
def read(p):
    raw=p.read_bytes()
    return raw,raw.decode('utf-8-sig').replace('\r\n','\n')
def save(p,raw,text,dated=True):
    if dated: text=re.sub(r'^modify: .*$', 'modify: 2026-10-06',text,count=1,flags=re.M)
    p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
def change(p, pairs):
    raw,text=read(p)
    for old,new in pairs:
        assert text.count(old)==1,(str(p),old)
        text=text.replace(old,new)
    save(p,raw,text)

for item in manifest:
    p=Path(item['target'])
    raw,text=read(p)
    m=re.search(r'^> 返回(?:目录)?：.*$',text,re.M)
    assert m,(p,'return line')
    old=m.group()
    if '[[附录目录]]' in old:
        continue
    if old.startswith('> 返回：'):
        new='> 返回：[[附录目录]] | 原文：'+old[len('> 返回：'):]
    else:
        new='> 返回：[[附录目录]] | '+old[2:]
    text=text[:m.start()]+new+text[m.end():]
    save(p,raw,text)

for course,oldnav,newcaption in [
    ('自动控制原理','[[#📖 附录与工具|公式与工具]]','*篇数包含课程目录内笔记与公共附录中的自控附录，按本地文件实时更新；不含825真题。*'),
    ('现代控制理论','[[#📖 速查附录|公式与判据]]','*篇数包含课程目录内笔记与公共附录中的现控附录，按本地文件实时更新；主体范围为绪论与第1–5章。*')]:
    p=root/'控制理论'/course/(course+'.md')
    raw,text=read(p)
    if newcaption in text:
        continue
    text=text.replace(oldnav,'[[控制理论/附录/附录目录|附录目录]]')
    query=f'> FROM "控制理论/{course}"'
    assert text.count(query)==1
    text=text.replace(query,query+' OR "控制理论/附录"\n'+f'> WHERE startswith(file.path, "控制理论/{course}/") OR contains(tags, "{course}")')
    oldcaption='*篇数与附录数按本地文件实时更新，包含章节、专题、工具与本页；不含 825 真题。*' if course=='自动控制原理' else '*笔记与附录数按本地文件实时更新；主体范围为绪论与第 1–5 章。*'
    assert oldcaption in text
    text=text.replace(oldcaption,newcaption)
    save(p,raw,text)

change(root/'README.md',[
    ('| 第1–9章及补充，132篇 |','| 第1–9章及补充，122篇；附录另列 |'),
    ('| 绪论、第1–5章及补充，68篇 |','| 绪论、第1–5章及补充，66篇；附录另列 |'),
    ('| **777 习题集** | [[控制理论/777习题集目录', '| **控制附录** | [[控制理论/附录/附录目录\\|自控 · 现控 · 常用公式]] | 14篇附录＋1篇目录 |\n| **777 习题集** | [[控制理论/777习题集目录'),
    ('*下方目录数量为 2026-10-05 的本地快照；页首卡片自动统计当前收录。*','*控制理论目录数量更新至2026-10-06，其余数量保留2026-10-05快照；页首卡片自动统计当前收录。*'),
    ('> ├── 控制理论/           250篇（不含825本地材料）\n> │   ├── 自动控制原理/   132篇\n> │   ├── 现代控制理论/   68篇',
     '> ├── 控制理论/           253篇（不含825本地材料）\n> │   ├── 附录/           15篇（14篇附录＋1篇目录）\n> │   ├── 自动控制原理/   122篇\n> │   ├── 现代控制理论/   66篇'),
    ('> | `控制理论/自动控制原理/` | 章节、专题、附录、工具页与入口 |',
     '> | `控制理论/附录/` | 自控、现控课程附录与统一目录，常用总表在前 |\n> | `控制理论/自动控制原理/` | 章节、专题、工具页与入口 |')])

change(root/'AGENTS.md',[
    ('- 附录：不带数字前缀，直接 `附录 XXX.md`',
     '- 附录：不带数字前缀，直接 `附录 XXX.md`；自控、现控的课程附录集中在 `控制理论/附录/`，与两门课程目录同级，入口为 [[控制理论/附录/附录目录]]')])

# Local-only exam material and device workspace references stay out of Git.
p=root/'控制理论/青岛大学825真题/选择题练习/00 选择题练习总览.md'
if p.exists():
    change(p,[('[[控制理论/自动控制原理/附录 常用e指数值速查|常用e指数值速查]]','[[附录 常用e指数值速查|常用e指数值速查]]')])
p=root/'.obsidian/workspace.json'
if p.exists():
    raw,text=read(p)
    for item in manifest:
        old=Path(item['source']).relative_to(root).as_posix()
        new=Path(item['target']).relative_to(root).as_posix()
        text=text.replace(old,new)
    save(p,raw,text,dated=False)

p=root/'控制理论/附录/附录目录.md'
text=p.read_text(encoding='utf-8-sig')
p.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
print('Updated appendix returns, course queries, navigation, directory map, and local path references.')

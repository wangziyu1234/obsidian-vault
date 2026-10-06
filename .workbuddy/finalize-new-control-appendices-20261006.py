from pathlib import Path
import re
import json

base=Path('D:/obsidian/控制理论/自动控制原理')
names=['附录 自控常用公式总表.md','附录 非线性系统速查.md','自动控制原理.md','08 第8章 非线性控制系统分析.md','附录 教材对照与复习索引.md']
p=base/names[0]
text=p.read_text(encoding='utf-8-sig')
p.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
issues=[]
count=0
for name in names:
    f=base/name
    body=f.read_text(encoding='utf-8-sig')
    for match in re.finditer(r'\[\[([^\]\n]+)\]\]',body):
        target=match.group(1).replace('\\|','|').split('|',1)[0]
        if '#' not in target: continue
        target_name,anchor=target.split('#',1)
        dest=f if not target_name else base/(target_name+'.md')
        if '/' in target_name:
            dest=base.parents[1]/(target_name+'.md')
        if not dest.exists():
            issues.append((name,target,'missing target'))
            continue
        headings=re.findall(r'^#{1,6}\s+(.+?)\s*$',dest.read_text(encoding='utf-8-sig'),re.M)
        count+=1
        if anchor not in headings: issues.append((name,target,'missing anchor'))
    if name.startswith('附录 ') and name!='附录 教材对照与复习索引.md':
        assert len(re.findall(r'^# ',body,re.M))==1
        assert not re.search(r'^### ',body,re.M)
        assert not re.search(r'(TODO|FIXME|\[\[\]\])',body)
        assert b'\r\n' in f.read_bytes()
print(json.dumps({'checked':len(names),'anchors':count,'issues':issues},ensure_ascii=False))
raise SystemExit(bool(issues))

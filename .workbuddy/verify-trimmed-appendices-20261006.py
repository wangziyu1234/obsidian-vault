from pathlib import Path
import subprocess
import re
import json
from collections import Counter

root=Path('D:/obsidian')
base=root/'控制理论/附录'
def git(*args): return subprocess.check_output(['git',*args],cwd=root)
changed=[root/p for p in git('diff','--name-only','-z','--','控制理论/附录').decode().split('\0') if p]
# Restore the original local CRLF convention after mixed editing tools.
for p in changed:
    raw=p.read_bytes()
    text=raw.decode('utf-8-sig').replace('\r\n','\n')
    p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\n','\r\n').encode('utf-8'))

all_md=[]
for d in ('控制理论','数学','英语'):
    all_md.extend((root/d).rglob('*.md'))
all_md.extend([root/'README.md',root/'AGENTS.md'])
by_name={p.stem:p for p in all_md}
appendix_names={p.stem for p in base.glob('*.md')}
cache={}
def read(p):
    if p not in cache: cache[p]=p.read_text(encoding='utf-8-sig')
    return cache[p]
issues=[]; anchors=0
for p in all_md:
    body=read(p)
    for m in re.finditer(r'\[\[([^\]\n]+)\]\]',body):
        target=m.group(1).replace('\\|','|').split('|',1)[0]
        if '#' not in target: continue
        name,anchor=target.split('#',1)
        if p.parent!=base and Path(name).name not in appendix_names: continue
        if name.endswith('.pdf'): continue
        dest=p if not name else (root/(name+'.md') if '/' in name else by_name.get(name))
        if not dest or not dest.exists(): issues.append((p.name,target,'target')); continue
        targetbody=read(dest)
        valid=bool(re.search(r'(?:^|\s)\^'+re.escape(anchor[1:])+r'\s*$',targetbody,re.M)) if anchor.startswith('^') else anchor in re.findall(r'^#{1,6}\s+(.+?)\s*$',targetbody,re.M)
        anchors+=1
        if not valid: issues.append((p.name,target,'anchor'))

stats=[]
for p in changed:
    old=git('show','HEAD:'+p.relative_to(root).as_posix()).decode('utf-8-sig').replace('\r\n','\n')
    new=read(p)
    if p.name!='附录目录.md':
        assert not re.search(r'\[!(?:derivation|example)\]',new),p.name
    if p.name=='附录 幅相曲线速查.md':
        imagepat=r'!\[\[([^\]|]+\.png)'
        assert set(re.findall(imagepat,old))==set(re.findall(imagepat,new))
    if p.name=='附录 常用e指数值速查.md':
        rows=lambda x: Counter(line for line in x.splitlines() if line.startswith('| $'))
        assert rows(old)==rows(new)
    stats.append({'file':p.name,'old_lines':len(old.splitlines()),'new_lines':len(new.splitlines()),'old_chars':len(old),'new_chars':len(new)})
assert git('show','HEAD:控制理论/附录/附录 自控常用公式总表.md').decode('utf-8-sig').replace('\r\n','\n')==read(base/'附录 自控常用公式总表.md')
print(json.dumps({'anchors_checked':anchors,'issues':issues,'stats':stats},ensure_ascii=False))
raise SystemExit(bool(issues))

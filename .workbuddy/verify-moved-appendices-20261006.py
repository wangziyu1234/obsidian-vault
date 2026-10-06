from pathlib import Path
import subprocess
import json
import re

root=Path('D:/obsidian')
manifest=json.loads((root/'.workbuddy/appendix-move-manifest-20261006.json').read_text(encoding='utf-8-sig'))
dest=root/'控制理论/附录'
assert len(list(dest.glob('*.md')))==15
index=(dest/'附录目录.md').read_text(encoding='utf-8-sig')
for row in manifest:
    old=Path(row['source'])
    new=Path(row['target'])
    assert not old.exists() and new.exists()
    before=subprocess.check_output(['git','show','HEAD:'+old.relative_to(root).as_posix()],cwd=root).decode('utf-8-sig').replace('\r\n','\n')
    after=new.read_text(encoding='utf-8-sig')
    assert before[before.index('\n# '):]==after[after.index('\n# '):],(new.name,'body changed')
    assert f'[[{new.stem}]]' in index,new.name
    assert '[[附录目录]]' in after.split('\n# ')[0]
counts={name:len(list((root/'控制理论'/name).rglob('*.md'))) for name in ('自动控制原理','现代控制理论','附录','777习题集')}
assert counts=={'自动控制原理':122,'现代控制理论':66,'附录':15,'777习题集':49},counts
query_counts={course:sum(course in re.search(r'^tags: (.*)$',p.read_text(encoding='utf-8-sig'),re.M).group(1) for p in dest.glob('*.md')) for course in ('自动控制原理','现代控制理论')}
assert query_counts=={'自动控制原理':12,'现代控制理论':2},query_counts
# Short links must resolve once across both tracked notes and local exam material.
all_md=list((root/'控制理论').rglob('*.md'))+list((root/'数学').rglob('*.md'))+list((root/'英语').rglob('*.md'))+[root/'README.md']
for row in manifest:
    stem=Path(row['target']).stem
    assert sum(p.stem==stem for p in all_md)==1,stem
print(json.dumps({'moved':len(manifest),'unchanged_bodies':len(manifest),'directory_counts':counts,'course_appendix_counts':query_counts,'index':'14/14 linked'},ensure_ascii=False))

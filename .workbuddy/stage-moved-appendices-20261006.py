from pathlib import Path
import json
import subprocess

root=Path('D:/obsidian')
def git(*args):
    return subprocess.check_output(['git',*args],cwd=root)
assert not git('diff','--cached','--name-only').strip(), 'Other staged changes exist'
manifest=json.loads((root/'.workbuddy/appendix-move-manifest-20261006.json').read_text(encoding='utf-8-sig'))
paths=[]
for row in manifest:
    paths.extend(Path(row[k]).relative_to(root).as_posix() for k in ('source','target'))
paths += ['控制理论/附录/附录目录.md','控制理论/自动控制原理/自动控制原理.md','控制理论/现代控制理论/现代控制理论.md','README.md','AGENTS.md']
git('add','--',*paths)
git('diff','--cached','--check')
print('Staged appendix moves and navigation only; local workspace and exam notes excluded.')

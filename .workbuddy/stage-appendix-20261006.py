from pathlib import Path
import subprocess

root = Path('D:/obsidian')
def git(*args, data=None):
    return subprocess.check_output(['git', *args], cwd=root, input=data)

assert not git('diff', '--cached', '--name-only').strip(), 'Index contains other staged changes; inspect before proceeding.'
base = root / '控制理论/自动控制原理'
owned = [p.relative_to(root).as_posix() for p in sorted(base.glob('附录*.md'))]
owned += ['控制理论/自动控制原理/' + n for n in (
    '自动控制原理.md', '07-1 采样与z变换.md', '07 第7章 线性离散系统的分析与校正.md',
    '05 第5章 线性系统的频域分析法.md')]
owned += ['.scripts/figures/zero-combination-nyquist.py', '附件/频域-幅相-零点组合-Ⅰ型复零点对.png']
git('add', '--', *owned)

# Stage only our link edits in the two notes that were dirty before this task.
partial = {
    '控制理论/自动控制原理/05-3-1 幅相曲线的画法与最小相位.md': [
        ('14 张典型曲线、零点组合九种、双惯性特征点的速算另立一篇 [[05-3-8 双惯性系统特征点速算]]',
         '典型曲线与零点组合见 [[附录 幅相曲线速查]]，双惯性特征点见 [[05-3-8 双惯性系统特征点速算]]'),
        ('见 [[附录 幅相曲线速查]] §5.3.2.8。',
         '见 [[附录 幅相曲线速查#🛡️ (5) 边界与补充辨析|零极点半平面组合与边界辨析]]。')],
    '控制理论/自动控制原理/05-3 奈氏图（幅相特性与奈氏判据）.md': [
        ('14 张典型曲线', '典型幅相曲线')]
}
for rel, pairs in partial.items():
    original = git('show', ':' + rel)
    desired = original
    working = (root / rel).read_text(encoding='utf-8-sig')
    for old, new in pairs:
        assert desired.count(old.encode()) == 1, (rel, old)
        assert new in working, (rel, new)
        desired = desired.replace(old.encode(), new.encode())
    oid = git('hash-object', '-w', '--stdin', data=desired).decode().strip()
    mode = git('ls-files', '-s', '--', rel).decode().split()[0]
    git('update-index', '--cacheinfo', f'{mode},{oid},{rel}')
staged = git('diff', '--cached', '--name-only', '-z').decode().strip('\0').split('\0')
assert set(staged) == set(owned) | set(partial), staged
git('diff', '--cached', '--check')
print(f'Staged only task changes in {len(staged)} files, including selective link changes in two previously modified notes.')

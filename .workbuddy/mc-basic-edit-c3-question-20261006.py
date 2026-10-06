from pathlib import Path

p = Path('控制理论/777习题集/现控200题基础 第3章 能控性和能观性（题目）.md')
data = p.read_bytes()
replacements = [
    ('modify: 2026-09-27', 'modify: 2026-10-06'),
    ('线性定常系统的传递函数备为：', '线性定常系统的传递函数为：'),
    ('已知一个双人双出的线性定常连续系统', '已知一个双入双出的线性定常连续系统'),
]
for old, new in replacements:
    src, dst = old.encode('utf-8'), new.encode('utf-8')
    assert data.count(src) == 1, old
    data = data.replace(src, dst)
p.write_bytes(data)
print('question edits applied, original line endings retained')

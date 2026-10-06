from pathlib import Path
import re

base = Path('D:/obsidian/控制理论/自动控制原理')
changes = {
    '05-3-1 幅相曲线的画法与最小相位.md': [
        ('14 张典型曲线、零点组合九种、双惯性特征点的速算另立一篇 [[05-3-8 双惯性系统特征点速算]]',
         '典型曲线与零点组合见 [[附录 幅相曲线速查]]，双惯性特征点见 [[05-3-8 双惯性系统特征点速算]]'),
        ('[[附录 幅相曲线速查#🧩 (2) 零点组合与终点方向|零点组合与终点方向]]',
         '[[附录 幅相曲线速查#🛡️ (5) 边界与补充辨析|零极点半平面组合与边界辨析]]')],
    '05-3 奈氏图（幅相特性与奈氏判据）.md': [('14 张典型曲线', '典型幅相曲线')],
    '05 第5章 线性系统的频域分析法.md': [('14 张典型曲线 · 零点组合', '典型曲线 · 零点组合')]
}
for name, pairs in changes.items():
    p = base / name
    raw = p.read_bytes()
    text = raw.decode('utf-8-sig').replace('\r\n', '\n')
    for old, new in pairs:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    text = re.sub(r'^modify: .*$', 'modify: 2026-10-06', text, count=1, flags=re.M)
    p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + text.replace('\n', '\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
print('Updated graph-index labels and the moved boundary reference.')

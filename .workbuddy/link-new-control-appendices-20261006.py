from pathlib import Path
import re

base=Path('D:/obsidian/控制理论/自动控制原理')
def change(name, old, new):
    p=base/name
    raw=p.read_bytes()
    text=raw.decode('utf-8-sig').replace('\r\n','\n')
    assert text.count(old)==1,(name,old)
    text=text.replace(old,new)
    text=re.sub(r'^modify: .*$', 'modify: 2026-10-06',text,count=1,flags=re.M)
    p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))

change('自动控制原理.md',
       '> [!note|study-course] 常用公式与图表\n',
       '> [!note|study-course] 常用公式与图表\n> - [[附录 自控常用公式总表]] — 跨章常用公式，无解释版\n')
change('自动控制原理.md',
       '> - [[附录 根轨迹特殊点速查]] — 按目标选方程，查分离点、临界阻尼与虚轴交点\n',
       '> - [[附录 根轨迹特殊点速查]] — 按目标选方程，查分离点、临界阻尼与虚轴交点\n> - [[附录 非线性系统速查]] — 描述函数、自振判别、相平面与奇点\n')
change('08 第8章 非线性控制系统分析.md',
       '|:--|:--|:--|\n',
       '|:--|:--|:--|\n| [[附录 非线性系统速查]] | 本章速查 | 常用描述函数、幅值域、自振候选、相平面与奇点 |\n')
change('附录 教材对照与复习索引.md',
       '## (9) 第8章 非线性系统\n',
       '## (9) 第8章 非线性系统\n\n**本章速查**：[[附录 非线性系统速查]]。\n')
print('Linked both appendices from the home page and chapter references.')

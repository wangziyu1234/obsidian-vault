from pathlib import Path
import re

root = Path('D:/obsidian')
base = root / '控制理论/自动控制原理'

def read(name):
    p = base / name
    raw = p.read_bytes()
    return p, raw, raw.decode('utf-8-sig').replace('\r\n', '\n')

def save(p, raw, text):
    text = re.sub(r'^modify: .*$', 'modify: 2026-10-06', text, count=1, flags=re.M)
    nl = '\r\n' if b'\r\n' in raw else '\n'
    p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + text.replace('\n', nl).encode('utf-8'))

def sections(text):
    parts = re.split(r'(?=^## )', text, flags=re.M)
    return parts[0], {x.split('\n', 1)[0][3:]: x.rstrip() for x in parts[1:]}

p, raw, text = read('附录 时域分析速查.md')
head, sec = sections(text)
head = head.replace('所有推导与例题见 [[03 第3章 线性系统的时域分析法]]（03-1~03-6）。', '先查二阶指标与稳态误差；一阶公式、劳斯表随后，非欠阻尼补充放在末尾。推导与例题见 [[03 第3章 线性系统的时域分析法]]。')
head += '''**常用**：[[#二阶系统|二阶指标]] · [[#稳态误差|稳态误差]] · [[#一阶系统|一阶响应]] · [[#劳斯判据|劳斯判稳]]

**补充**：[[#极点等值线与非欠阻尼补充|极点等值线与非欠阻尼]]

'''
second = sec['二阶系统（欠阻尼 $0<\\zeta<1$）']
second, supplement = second.split('> [!tip] s平面等值线', 1)
second = second.replace('## 二阶系统（欠阻尼 $0<\\zeta<1$）', '## 二阶系统\n\n**适用**：无零点、直流增益为 1 的标准二阶系统，零初始条件、单位阶跃输入；本节动态指标取 $0<\\zeta<1$。')
second = second.replace('| **0.707** | **≈4.3%** | **最佳阻尼比**（45°线） |', '| $\\frac{\\sqrt2}{2}$ | ≈4.3% | 常用折中值（45°线），并非对所有目标最优 |')
second = second.replace('| 1.0 | 0% | 临界阻尼，最快无振荡 |', '| 1 | 0% | 临界阻尼；固定 $\\omega_n$ 时，标准无零点模型在 $\\zeta\\ge1$ 中响应最快 |')
second = second.replace('**ζ 与性能对应**', '**阻尼比与性能对照**（最后一行为非欠阻尼对照，不套上面的时间指标）')
second = second.replace('> [!note] 非欠阻尼不要套上表', '> [!note] 非欠阻尼不要套上表')
second = second.rstrip() + '\n\n> [!note] 接近临界阻尼或带零点时\n> 调节时间近似与超调公式要重新核对模型；临界/过阻尼见 [[#极点等值线与非欠阻尼补充|页末补充]]，零点影响见 [[03-3-2 零点影响与二阶性能改善]]。'
first = sec['一阶系统'].replace('## 一阶系统', '## 一阶系统\n\n**适用**：$T>0$、零初始条件、单位阶跃输入。')
first = first.replace('| 时间常数 $T$ | $T$ 越小 → 响应越快 | $t_s(5\\%)\\approx3T$，$t_s(2\\%)\\approx4T$ |', '| 调节时间 $t_s$(5%) | $T\\ln20$ | 常用估算 $\\approx3T$ |\n| 调节时间 $t_s$(2%) | $T\\ln50$ | 常用估算 $\\approx4T$ |')
first = first.replace('| 延迟时间 $t_d$ | $0.69T$（50%） | |', '| 延迟时间 $t_d$ | $T\\ln2$ | 首次到达终值的50% |')
first += '\n\n时间常数 $T$ 越小，响应越快；手算答案优先保留上表的对数形式。'
error = sec['稳态误差'].replace('以下速查按闭环稳定、误差信号满足终值定理条件使用；先判稳，再求误差。', '以下取比较点偏差 $e=r-b$，其他独立输入为零；先查闭环稳定性。表中有限值还须满足终值定理条件，$\\infty$ 表示误差不收敛到有限常数。非单位反馈时，偏差不等于跟踪误差 $r-c$。')
error = error.replace('$K_p=\\lim G(s)H(s)$', '$K_p=\\lim_{s\\to0}G(s)H(s)$').replace('$K_v=\\lim sG(s)H(s)$', '$K_v=\\lim_{s\\to0}sG(s)H(s)$').replace('$K_a=\\lim s^2G(s)H(s)$', '$K_a=\\lim_{s\\to0}s^2G(s)H(s)$')
error = error.replace('**静态误差系数表**', '**静态误差系数表**（$K$ 为尾一开环增益）')
extra = r'''## 极点等值线与非欠阻尼补充

> [!tip] s平面等值线
> - 竖直线 $\zeta\omega_n=\text{常数}$：欠阻尼近似等调节时间，越左衰减越快。
> - 水平线 $\omega_d=\text{常数}$：等峰值时间，离实轴越远，峰值时间越短。
> - 原点射线：等阻尼比、等超调量。
> - 原点圆弧：等自然频率；阻尼比不同，时间指标仍可能不同。

**临界阻尼**：无零点标准二阶取 $\zeta=1$，相对误差带为 $\delta$，调节时间由完整响应确定：

$$
(1+\omega_n t_s)\mathrm e^{-\omega_n t_s}=\delta
$$

5%与2%分别取 $\delta=0.05$、$0.02$。手算可保留此精确关系；若题目要求估算，教材式3-26给出5%口径 $t_s\approx4.75/\omega_n$，不能套欠阻尼公式。

**过阻尼**：用慢模态或完整响应计算。完整推导见 [[03-3-2 零点影响与二阶性能改善]]。
'''
text = head + '\n\n'.join([second, error, first, sec['劳斯判据'], extra.rstrip()]) + '\n'
save(p, raw, text)

p, raw, text = read('附录 开环增益与闭环增益.md')
head, sec = sections(text)
head += '''**常用**：[[#核心结论速查|先看结论]] · [[#定义与换算|三种增益换算]] · [[#开环增益的作用|稳态与动态影响]] · [[#闭环增益的作用|闭环幅值与响应]]

**补充**：[[#解题陷阱与校正应用|校正应用]] · [[#参数灵敏度补充|参数灵敏度]]

'''
sensitivity = sec['闭环增益的作用'].split('**抗参数漂移**', 1)[1]
sec['闭环增益的作用'] = sec['闭环增益的作用'].split('**抗参数漂移**', 1)[0].rstrip()
sec['参数灵敏度补充'] = '## 参数灵敏度补充\n\n**抗参数漂移**' + sensitivity
sec['解题陷阱与校正应用'] = sec['解题陷阱与校正应用'].replace('附加相位约 $-39.29°$', '附加相位为 $45°-\\arctan10<0$')
sec['关联导航'] = sec['关联导航'].replace('[[05-4-1 奈氏判据]] — 幅值裕度与条件稳定系统', '[[05-4-3 稳定裕度]] — 幅值裕度与条件稳定系统')
text = head + '\n\n'.join(sec[k] for k in ['核心结论速查', '定义与换算', '开环增益的作用', '闭环增益的作用', '解题陷阱与校正应用', '参数灵敏度补充', '关联导航']) + '\n'
save(p, raw, text)

p, raw, text = read('附录 教材对照与复习索引.md')
text = text.replace('type: cheatsheet', 'type: index')
head, sec = sections(text)
head += '''**按章回查**：[[#(4) 第3章 时域分析|时域]] · [[#(5) 第4章 根轨迹|根轨迹]] · [[#(6) 第5章 频域分析|频域]] · [[#(7) 第6章 校正方法|校正]] · [[#(8) 第7章 离散系统|离散]]

**其他位置**：[[#(2) 第1章 一般概念|一般概念]] · [[#(3) 第2章 数学模型|建模]] · [[#(9) 第8章 非线性系统|非线性]] · [[#(10) 第9章 状态空间|状态空间]] · [[#(11) 工具附录与延伸范围|工具与范围]]

'''
text = head + '\n\n'.join(sec.values()) + '\n'
text = text.replace('[[05-4-1 奈氏判据\\|相角裕度与增益裕度]]', '[[05-4-3 稳定裕度\\|相角裕度与增益裕度]]')
save(p, raw, text)

p, raw, text = read('自动控制原理.md')
start = text.index('> [!note|study-course]- 速查表、计算工具与题源')
end = text.index('\n## 全书主线', start)
nav = '''> [!note|study-course] 常用公式与图表
> - [[附录 时域分析速查]] — 二阶指标、稳态误差、一阶响应与劳斯表
> - [[附录 频域分析速查]] — 伯德图、奈氏判稳与稳定裕度
> - [[附录 拉氏变换表与z变换表|拉氏变换与z变换对表]] — 正反变换的三栏对照，长式纵向查
> - [[附录 z变换与离散化速查]] — 采样换算、ZOH、差分方程与离散判稳
> - [[附录 幅相曲线速查]] — 典型曲线、零点组合与终点方向
> - [[附录 根轨迹特殊点速查]] — 按目标选方程，查分离点、临界阻尼与虚轴交点

> [!note|study-course]- 概念辨析与数学补充
> - [[附录 开环增益与闭环增益]] — 开环/闭环增益、换算与作用
> - [[附录 常用数学补充]] — 相角、分贝、复数运算与响应形态

> [!note|study-course]- 教材回查、题源与备用工具
> - [[附录 教材对照与复习索引]] — 教材节号、书内页码与覆盖边界
> - [[控制理论/青岛大学825真题/附录 825真题考法清单与复习优先级|825真题考法清单与复习优先级]] — 考法、题源与取舍清单（数据止于2025）
> - [[777习题集目录]] — 基础300题、强化300题、现控200题
> - [[附录 常用e指数值速查]] — 精确式与小数对照，供数值核对备用
> - [[11 MATLAB 基础速查]] — 建模、连接与分章分析命令
> - [[12 资料索引（OneDrive）]] — 教材、按章PPT与Word资料位置

'''
text = text[:start] + nav + text[end:]
save(p, raw, text)

# This source note already has unrelated edits. Only this link change is ours.
p, raw, text = read('05-3-1 幅相曲线的画法与最小相位.md')
old = '见 [[附录 幅相曲线速查]] §5.3.2.8。'
new = '见 [[附录 幅相曲线速查#🧩 (2) 零点组合与终点方向|零点组合与终点方向]]。'
assert text.count(old) == 1
text = text.replace(old, new)
save(p, raw, text)
print('Updated four owned notes and one source link.')

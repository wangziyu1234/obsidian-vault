from pathlib import Path
import re
import subprocess
root=Path('控制理论/自动控制原理')
def read(name): return subprocess.check_output(['git','show','HEAD:'+(root/name).as_posix()],encoding='utf-8').replace('\r\n','\n')
def save(name,t):
 p=root/name; raw=p.read_bytes(); nl='\r\n' if b'\r\n' in raw else '\n'; t=re.sub(r'(?m)^modify: [^\n]+','modify: 2026-10-06',t,count=1); p.write_bytes(t.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
def intro(t,body):
 a=t.index('> [!abstract]'); b=t.index('\n## ',a); return t[:a]+'> [!abstract] 本讲定位\n> '+body+'\n'+t[b:]
def cutcall(t,heading):
 a=t.index(heading); b=t.find('\n\n',a); b=b if b>=0 else len(t); return t[:a]+t[b:]

n='05-5-3 频域解题套路.md';t=read(n)
t=intro(t,'拿到传函或频率曲线后，按对象、画图、判稳、裕度的顺序作答。保留两道分段计算示范；实验辨识见 [[05-5-2 频率特性的实验确定与MATLAB]]。')
a=t.index('> [!note] 图形平移怎么看');b=t.index('\n## ',a)
t=t[:a]+r'''> [!note] 图形平移：先写出频率缩放关系
> 幅频、相频整体向右移到原频率的 $\lambda$ 倍（$\lambda>1$），对应
>
> $$
> G_{\mathrm{新}}(s)=G_{\mathrm{旧}}(s/\lambda)
> $$
>
> 时间常数除以 $\lambda$，截止频率乘以 $\lambda$；单位负反馈下闭环也作同样缩放，因此阶跃超调不变、同一误差带的调节时间除以 $\lambda$。
> 型别不变，但尾1标准式中 $\nu$ 型的增益变为 $\lambda^\nu K$。例如Ⅰ型的速度误差系数乘以 $\lambda$，斜坡误差相应减小；不能概括为“所有稳态误差不变”。这要求整个传函作同一缩放，仅看幅频平移不足以排除额外全通或延迟。
''' +t[b:]
t=t.replace('振荡环节在 $\omega_n$ 附近按 $\zeta$ 补谐振峰修正。','振荡环节在 $\omega_n$ 处按 $-20\lg(2\zeta)$ 修正；该点不一定是谐振峰。')
t=t.replace('常由 $\\operatorname{Im}G(\\mathrm{j}\\omega)=0$ 解','可由 $\\operatorname{Im}G(\\mathrm{j}\\omega)=0$ 且实部为负筛选')
t=t.replace('再由峰值反解 $\\zeta$','再由该环节的归一化幅值反解 $\\zeta$')
for h in ['> [!tip] 思路']:
 while h in t:t=cutcall(t,h)
t=t.replace('> MATLAB 表示：`num=[10]; den=conv([1 0],conv([0.5 1],[0.1 1])); sys = tf(num, den)`\n>\n','')
t=t.replace('> 精确解幅值方程则给 $\\omega_c\\approx9.2684$、$\\gamma\\approx56.05°$——不要把渐近线读数当成精确频响。','> 若需实际裕度，解精确幅值方程后再代入相频；数值复核约为 $\\omega_c=9.27$、$\\gamma=56.1°$。上面的 $55°$ 只是渐近估计。')
t=t.replace('> **② 低频段一点。** 型别 $\\nu=1$，斜率 $-20$ dB/dec；$\\omega=1$ 处','> **② 低频延长线一点。** 型别 $\\nu=1$，斜率 $-20$ dB/dec；其延长线在 $\\omega=1$ 处')
t=t.replace('最后要代**精确相频**复核——上面算例二的 $55°$ 与 $56.05°$ 就是这么差出来的。','须先校核实际截止频率，再代完整相频；仅换用精确相频不会消除截止频率的误差。')
save(n,t)

n='05-5-2 频率特性的实验确定与MATLAB.md';t=read(n)
t=intro(t,'由正弦实验辨识频率特性，并区分 MATLAB 中的环路与闭环对象。例5.18演示“斜率 → 环节 → 归一化峰值 → 参数”。')
t=t.replace('（教材 §5-2.6，常考方法题）','（教材 §5-2.6）')
t=t.replace('——斜率**为正**时 $\\nu<0$，系统含微分环节（教材例5-7 的低频渐近线斜率为 $+20$ dB/dec，故 $\\nu=-1$、$K=1$）','；正斜率对应原点零点，记作 $\\nu<0$')
a=t.index('> [!warning] 闭式根为什么');b=t.index('#### ✏️ 例5.18',a)
t=t[:a]+r'''> [!derivation]- 为什么只取小根
> 令 $u=\zeta^2$，由归一化峰值公式得
>
> $$
> u^2-u+\frac1{4M_r^2}=0
> $$
>
> 两个代数根中，仅小根满足有正频率谐振峰的条件 $\zeta<1/\sqrt2$。完整演算见 [[05-2-e 伯德图反求例题]] 例5.24。

''' +t[b:]
t=cutcall(t,'> [!tip] 思路')
t=t.replace('> 教材取 $\\zeta\\approx0.204$。','> 按图读精度取 $\\zeta\\approx0.204$。')
t=t.replace('\\approx2.512','\\approx2.51').replace('\\approx0.2033','\\approx0.203')
a=t.index('### 常见错法');b=t.index('> [!tip] 下一步',a)
t=t[:a]+'''**峰值口径**：总峰减其他环节基线仅在这些环节变化缓慢时近似可用；严格辨识应逐频率相除。幅频不足以区分同幅的全通、延迟或非最小相位模型，必须结合实测相位。

'''+t[b:]
save(n,t)

n='05-5-1 三频段与闭环频域指标.md';t=read(n)
t=intro(t,'先用开环三频段理解精度、动态与抗噪，再读闭环带宽、谐振峰和时域估算。适用条件随公式说明；精确二阶关系见 [[05-5-b-2 二阶相角裕度与时域指标例题]]。')
a=t.index('- **低频段**');b=t.index('### 5.5.1',a)
t=t[:a]+'''提高环路增益会移动截止频率，裕度需重算；只整形低频段则不必同幅抬高中高频段。

'''+t[b:]
t=t.replace('低频段渐近线只要**读两个数**：斜率定型别 $\\nu$，$\\omega=1$ 处高度定开环增益 $K$。','低频斜率定型别 $\\nu$，低频渐近线的延长线在 $\\omega=1$ 处的高度定尾1标准增益 $K$。以下误差公式要求闭环稳定、单位负反馈、误差为输入端偏差且无额外前馈。')
a=t.index('- 统一表述：');b=t.index('### 5.5.2',a)
t=t[:a]+'''型别决定对哪类输入无静差，增益决定有限误差系数。完整输入定义与误差表见 [[03-5 稳态误差]]。

'''+t[b:]
t=t.replace('> [!derivation] 等 $M$ 圆的可计算形式','> [!derivation]- 等幅圆的推导')
a=t.index('> [!note] 教材归纳的另两条');b=t.index('- **高阶系统时域指标',a)
t=t[:a]+t[b:]
t=t.replace('> [!note] 经验式偏保守','> [!note]- 经验式与实际响应的比较')
t=t.replace('  验证：由 $M_r=\\frac{1}{2\\zeta\\sqrt{1-\\zeta^2}}$ 算得 $\\zeta=0.4\\to M_r\\approx1.36$、$\\zeta=0.7\\to M_r\\approx1.00$ ✓\n','')
a=t.index('## ⚠️ 边界与易错');b=t.index('> 相关：',a)
t=t[:a]+'''## ⚠️ 边界与易错

- **公式先看模型**：二阶精确式针对单位直流增益、无零点标准模型；高阶经验式针对可用主导共轭极点近似的系统，只用于初选。
- **指标须用同一口径**：带宽相对自身直流幅值定义；比较调节时间须统一2%或5%误差带。
- **跨模型不能机械排序**：谐振峰、带宽与超调、快慢的对应只适用于形状相近的系统。实际性能仍由完整闭环与信号通道核对。

'''+t[b:]
save(n,t)

for n,body in [
 ('05-5 闭环频域指标·解题套路与综合题型.md','稳定判定后，学习闭环指标、实验辨识和反求设计。先读性能，再按需要查工具与例题；本页保留阅读入口。'),
 ('05-5-b 综合题型与例题.md','按“读图 → 参数 → 传函 → 验收”练习综合题。先做二阶指标互算，再做响应反求与教材设计案例。')]:
 t=intro(read(n),body);save(n,t)
print('Updated five metrics/process/index notes.')

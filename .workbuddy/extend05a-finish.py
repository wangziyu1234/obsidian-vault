from pathlib import Path
import re,json,subprocess
r=Path('D:/obsidian');folder=r/'控制理论/自动控制原理'
def load(pre):
 p=next(folder.glob(pre+' *.md'));return p,p.read_text(encoding='utf-8-sig')
def save(p,s):
 b=p.read_bytes();nl='\r\n' if b.count(b'\r\n')>b.count(b'\n')/2 else '\n'
 s=re.sub(r'(?m)^modify: .*','modify: 2026-10-06',s)
 p.write_bytes((b'\xef\xbb\xbf' if b.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\n',nl).encode())
def sec(s,a,b,new):return s[:s.index(a)]+new+'\n\n'+s[s.index(b,s.index(a)):]
p,s=load('05-2-1')
s=s.replace('转折点数 $=$ 惯性 $+$ 一阶复合微分 $+$ 振荡 $+$ 二阶复合微分；','各非原点环节均已计入；同频转折合并，斜率变化取代数和；').replace('相频终值 $\\to-90°(n-m)$。','正增益最小相位有理系统的相频终值 $\\to-90°(n-m)$；其他情况逐环节求和。')
s=sec(s,'> [!note] 修正量什么时候','**几何法',r'''> [!note] 何时改用精确频响？
> 折点接近或阻尼较小时，多个环节的修正会叠加。是否可忽略应按题目精度判断；要求实际截止频率或裕度时，回代完整幅值与相角。
>
> 振荡环节在自身折点的修正为 $-20\lg(2\zeta)$；其他频率用完整幅值式。完整核算见 [[05-2-d 伯德图绘图例题]] 例5.25。''')
s=sec(s,'**画完顺手能读的三个量**','### 5.3.2',r'''基准点 $(1,20\lg K)$ 属于低频延长线。完整反求方法见 [[05-2-b 由伯德图反求（方法与口径）]]。

![[频域-Bode绘制示例.png|430]]

> [!note]- 课程原图对照
> 下图仅用于对照课件的折线布局；相频应由具体传函逐环节计算。
>
> ![[自控-频域-Bode折线与相频.png|430]]''')
s=s.replace('\\omega_x=\\sqrt{10}\\approx3.162','\\omega_x=\\sqrt{10}')
s=sec(s,'## ⚠️ 边界与易错','> 相关：','## ⚠️ 边界与易错\n\n- 截止频率若由渐近线求得，注明“渐近值”；实际值解 $|G(\\mathrm j\\omega_c)|=1$。\n- 同一处 $-40$ dB/dec 变化可能来自振荡环节，也可能来自两个同频惯性环节；仅凭斜率不能唯一确定。\n- 基准点属于低频延长线，不能直接当作折线或实际频响在该频率的读数。')
save(p,s)
p,s=load('05-2-b')
s=s.replace('**低频定 $K$ 与 $\\nu$，转折定时间常数，斜率定环节类型。** 三句话之外都是细节。','**适用条件**：只凭幅频唯一反求，须限定为正增益最小相位模型并有频率标定。先看低频，再看转折；谐振峰法只适用于有正频率峰的振荡因子。')
s=s.replace('$\\omega_0=K^{1/\\nu}$（Ⅰ 型即 $K$，Ⅱ 型即 $\\sqrt K$）','$\\omega_0=K^{1/\\nu}$（$\\nu>0$；Ⅰ 型为 $K$，Ⅱ 型为 $\\sqrt K$）')
s=s.replace('四步走完要回代三遍：**数值**（分段折线的高度）、**相频**（惯性折点 $±45°$、振荡环节 $\\omega_n$ 处 $-90°$）、**奈氏图的落点**（见 [[05-3-a 伯德图与奈氏图的点对应]]），三处都对上才算定案。','求出模型后，回代题给幅值与相角；若题目还给奈氏图，再核对同频点。')
s=sec(s,'三种型别的低频延长线都过','### 5.11.3',r'''Ⅱ型中，若第一折点 $\omega_1$ 使斜率从 $-40$ 变为 $-20$ dB/dec，且该段与零分贝线交于 $\omega_c$，则

$$
K=\omega_1\omega_c=\omega_0^2
$$

这是渐近线关系；推导与三种读法见 [[05-2-e 伯德图反求例题]] 例5.26。

> [!note]- 课程原图对照
> 红虚线是低频延长线。具体增益关系仍须按各段斜率列式，不能把Ⅰ型与Ⅱ型公式混用。
>
> ![[自控-频域-反求延长线与K.png|430]]''')
s=s.replace('$\\zeta$ 由 $\\omega_2$ 处谐振峰按 $\\Delta L=-20\\lg2\\zeta$ 反解','$\\zeta$ 可由自然频率处的振荡因子幅值确定；须先扣除其他环节贡献')
s=s.replace('=10\\sqrt{10}=31.6','=10\\sqrt{10}')
s=sec(s,'**读数口径**','> 相关：','**读数口径**\n\n渐近线用于识别结构与估算，精确截止频率须解完整幅值方程。误差取决于具体模型与所在频段，不能把某道例题的误差比例当成通则。')
save(p,s)
p,s=load('05-2-e')
s=re.sub(r'> \[!tip\] 思路\n(?:>[^\n]*\n)*\n','',s)
s=s.replace(r'K=10^{1.5}\approx31.6',r'K=10^{3/2}=10\sqrt{10}').replace(r'\frac{31.6}{0.5s+1}=\frac{31.6}{\dfrac{s}{2}+1}',r'\frac{10\sqrt{10}}{0.5s+1}')
s=s.replace(r'\omega_c=2\times10^{1.5}\approx63.2\ \mathrm{rad/s}',r'\omega_{c,\mathrm{a}}=20\sqrt{10}\ \mathrm{rad/s}')
s=sec(s,'> **⑤ 相频回代。**','> ![[频域-反求-一阶Bode',r'''> **⑤ 精确回代。** $\varphi(2)=-45°$、高频相角趋于 $-90°$，与题设一致。实际截止频率由
>
> $$
> \frac{1000}{1+\omega_c^2/4}=1
> $$
>
> 得
>
> $$
> \omega_c=2\sqrt{999}\ \mathrm{rad/s}
> $$
>''')
s=sec(s,'> **② 峰高归一化。**','> ![[频域-反求-二阶Bode',r'''> **② 由峰高求阻尼。** 先扣去低频增益的 $20$ dB，得到归一化峰值
>
> $$
> M_r=10^{(28-20)/20}=10^{2/5}
> $$
>
> 由 $M_r^{-1}=2\zeta\sqrt{1-\zeta^2}$，令 $u=\zeta^2$：
>
> $$
> u^2-u+\frac{10^{-4/5}}4=0
> $$
>
> 图中有正频率谐振峰，须满足 $u<1/2$，因此舍去大根：
>
> $$
> \zeta=\sqrt{\frac{1-\sqrt{1-10^{-4/5}}}{2}}
> $$
>
> **③ 定自然频率。** 相频在 $30$ rad/s 处过 $-90°$，故取 $\omega_n=30$。峰位应为
>
> $$
> \omega_r=30\sqrt{1-2\zeta^2}
> $$
>
> 题给峰高、峰位是图上近似读数，只需在读图精度内相符；不能把二者同时当作精确约束。
>
> **④ 写传函。** 保留上面求出的 $\zeta$：
>
> $$
> G(s)=\frac{9000}{s^2+60\zeta s+900}
> $$
>
> 读图取 $\zeta\approx0.203$ 时，分母一次项系数约为 $12.18$，配图按此近似模型绘制。
>
> **⑤ 区分两种截止频率。** 高频渐近线给出
>
> $$
> \omega_{c,\mathrm a}=30\sqrt{10}
> $$
>
> 实际频响令 $x=(\omega_c/30)^2$，由幅值为1得
>
> $$
> (1-x)^2+4\zeta^2x=100
> $$
>
> 取正根：
>
> $$
> \omega_c=30\sqrt{1-2\zeta^2+\sqrt{(1-2\zeta^2)^2+99}}
> $$
>
> 渐近值约 $94.9$ rad/s、实际值约 $99.1$ rad/s；图中零分贝交点对应后者。
>''')
s=s.replace(r'\xi',r'\zeta')
s=s.replace('*解法 II（在 $\\omega_c$ 处直接令 $\\lvert G\\rvert=1$）*','*解法 II（在渐近零分贝交点令渐近幅值为1）*')
s=s.replace(r'\lvert G(\mathrm j\omega_c)\rvert=\frac{\omega_c}{\omega_1}',r'A_{\mathrm a}(\omega_c)=\frac{\omega_c}{\omega_1}')
s=sec(s,'> **③ 三条路的关系与','> ![[频域-反求-Ⅱ型Bode', '> **③ 参数是否定全？** 三种读法都给出 $K=\\omega_1\\omega_c$。仅有渐近线不能定 $\\zeta$；还需振荡因子在自然频率处的幅值或其他精确频响数据。\n>')
s=sec(s,'## ⚠️ 例题之外','> 相关：','## ⚠️ 例题之外还要盯的两点\n\n- 仅凭幅频反求须有最小相位等先验条件，见 [[05-2-b 由伯德图反求（方法与口径）]]。\n- 渐近交点与实际交点分开标明，最终按题目要求选择；图上近似数据不宜写成多位精确小数。')
save(p,s)
# Concise index: preserve navigation, shorten duplicated prose.
p,s=load('05-2')
s=sec(s,'> **本部分任务**','## 🗂️','> 先由传函画伯德图，再由曲线反求传函。按下表顺读；判稳与裕度见 [[05-4 频域稳定判据与稳定裕度]]。')
s=sec(s,'> [!tip] 本部分的最小学习闭环','## ⚠️','> [!tip] 完成标准\n> 能独立画渐近线、按完整频响修正关键点，并回代验证反求出的传函。')
s=sec(s,'> [!warning] ①','下一站：','- 折点附近的渐近读数需修正，实际截止频率解完整幅值方程。\n- 相角连续展开，二阶环节注意象限；判稳计数见 [[05-4-2 对数频率稳定判据]]。\n- 谐振峰高先扣除其他环节贡献，区分峰频与自然频率。')
save(p,s)
# final report
names=json.loads((r/'.workbuddy/extend05a-images.json').read_text(encoding='utf-8'))
rows=[]
for p in sorted(folder.glob('05-[12]*.md')):
 old=subprocess.check_output(['git','show','HEAD:'+p.relative_to(r).as_posix()]).decode('utf-8-sig');new=p.read_text(encoding='utf-8-sig')
 rows.append((p.name,len(old),len(new),old.replace('\r\n','\n')!=new.replace('\r\n','\n')))
report='# 05-1 / 05-2 正文整理与图片检查\n\n逐篇通读14篇；保留例题与主要标题锚点。未改文件名，未提交。\n\n|文件|原字符|现字符|处理|\n|---|---:|---:|---|\n'
for n,a,b,c in rows:report+=f'|{n}|{a}|{b}|'+('精简重复定位/速记，保留推导与关键条件' if c else '已阅读，现有结构简洁，保留')+'|\n'
report+=f'\n合计：{sum(a for _,a,_,_ in rows)} → {sum(b for _,_,b,_ in rows)} 字符；压缩 {1-sum(b for _,_,b,_ in rows)/sum(a for _,a,_,_ in rows):.1%}。\n'
report+='\n数学与口径修正：概念幅值比改振幅比；重复矢量式改指向含K的专题；例5.9独立单$改成$$；例5.23 K=10√10、实际ωc=2√999；例5.24用精确根式求ζ，区分图上近似数据/渐近94.9/实际99.1；例5.25保留修正量可手算加和式；同频转折合并、最小相位高频相角条件、自然频率修正与谐振峰分开。\n\n## 图片逐张检查\n\n34张均看联系表，裁切/压字/箭头疑图另看原图。未修改共享绘图源码。\n'
for n in names:
 issue='图面可读，保留'
 if '典型环节' in n and 'Bode' in n:issue='建议统一上下两幅，明确参数；有转折的图误用ωc，延迟图相角截断（bode-typical-links.py）'
 if n in ['频域-典型环节-惯性Nyquist.png','频域-典型环节-振荡Nyquist.png']:issue='原图确认方向箭头未沿局部曲线切向，修数据方向箭头（ch5-typical-links-nyquist.py）'
 if n=='频域-图示法-尼科尔斯图.png':issue='原图确认右侧ω=0标签裁切；曲线低频/高频端宜补极限（ch5-three-plots.py）'
 if n=='频域-惯性环节-描点.png':issue='原图确认左侧文字叠压，改特征点编号/表格（ch5-vector-method.py）'
 if n.startswith('自控-频域'):issue='课程图相频/增益关系不能作为通则；已折叠参考并去掉错误图注'
 if n=='频域-反求-一阶Bode.png':issue='图面可读，但传函标题31.6为近似；应同步精确10√10（freq-inverse-bode-first-order.py）'
 report+=f'- {n}：{issue}。\n'
(r/'.workbuddy/extend-05a-report.md').write_text(report,encoding='utf-8')

from pathlib import Path
import re,json
root=Path('D:/obsidian'); folder=root/'控制理论/自动控制原理'
files=sorted(folder.glob('05-[12]*.md'))
original={p.name:p.read_bytes() for p in files}
def load(prefix):
 p=next(p for p in files if p.name.startswith(prefix+' '));return p,p.read_text(encoding='utf-8-sig')
def save(p,s):
 s=re.sub(r'(?m)^modify: .*','modify: 2026-10-06',s)
 b=original[p.name]; nl='\r\n' if b.count(b'\r\n')>b.count(b'\n')/2 else '\n'
 p.write_bytes((b'\xef\xbb\xbf' if b.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n',nl).encode())
def section(s,start,end,new):
 a=s.index(start);b=s.index(end,a);return s[:a]+new+'\n\n'+s[b:]
# Remove repeated memorization boxes and navigation prose; preserve all derivations.
for p in files:
 s=p.read_text(encoding='utf-8-sig')
 s=re.sub(r'> \[!tip\] 🎯 考点速记\n(?:>[^\n]*\n)*\n','',s)
 s=re.sub(r'> \[!tip\] 延伸\n(?:>[^\n]*\n)*\n','',s)
 if s!=p.read_text(encoding='utf-8-sig'):save(p,s)
p,s=load('05-1-1')
s=section(s,'> **讲什么**','## 📐', '> 学会频率特性的三种定义，并用对应通道求正弦稳态。矢量与图示另见 [[05-1-1-a 矢量法与频率特性图示]]。\n>\n> **教材**：§5-1（书内197—202页 / PDF205—210页）。')
s=section(s,'**物理意义。**','**频域法求正弦稳态响应', '')
s=s.replace('——这正是定义一：$\\lvert\\Phi\\rvert=\\dfrac{\\lvert c_s(t)\\rvert}{A}$、$\\angle\\Phi=\\angle c_s(t)-\\angle r(t)$。','。')
s=s.replace('由实验可直接测得的两个量定义','设输入、输出正弦的振幅分别为 $R_m$、$C_m$，初相分别为 $\\theta_r$、$\\theta_c$：')
s=s.replace(r'\frac{\lvert c_s(t)\rvert}{\lvert r(t)\rvert}',r'\frac{C_m}{R_m}').replace(r'\angle c_s(t)-\angle r(t)',r'\theta_c-\theta_r')
s=section(s,'> [!derivation] 定义三','### 5.1.3',r'''> [!derivation]- 定义三与传递函数的关系
> 零初始条件下 $c=g*r$。当相应傅氏变换存在时，卷积定理给出
>
> $$
> C(\mathrm j\omega)=G(\mathrm j\omega)R(\mathrm j\omega)
> $$
>
> 在 $R(\mathrm j\omega)\ne0$ 的频率处即可取比值。稳定系统冲激响应的傅氏变换，等于传递函数在虚轴上的取值。''')
s=s.replace('> [!derivation] 定义一','> [!derivation]- 定义一')
s=section(s,'$G(\\mathrm j\\omega)$ 可以写成','### 5.1.4', '从零极点指向 $\\mathrm j\\omega$，幅值取长度之比并乘 $|K|$，相角取零点角之和减极点角之和，再加 $\\arg K$。完整公式与例5.1见 [[05-1-1-a 矢量法与频率特性图示#5.1.3 矢量法|矢量法]]。')
s=section(s,'三张图看的是','> 相关：','奈氏图用实部、虚部作坐标；伯德图按频率分别画幅值与相角；尼科尔斯图以相角、对数幅值作坐标。三图对照与对数分度见 [[05-1-1-a 矢量法与频率特性图示#5.1.5 三种图示法|三种图示法]]。')
save(p,s)
p,s=load('05-1-1-b')
s=re.sub(r'> \[!tip\] 思路\n(?:>[^\n]*\n)*\n','',s)
s=section(s,'> **⑤ 与频域法对照。**','> **三点校验**', '> **⑤ 与频域法对照。** 稳态项正是输入幅值乘 $|G(\\mathrm j\\omega)|$、初相加 $\\arg G(\\mathrm j\\omega)$；频域法直接给出这一项。\n>')
s=section(s,'- **教材原式含电容初值**','- **不要漏掉暂态**', '- **非零初值**：若 $u_c(0^-)=U_0$，在上式另加 $U_0e^{-t/T}$，即教材式(5-4)中的初值项。')
save(p,s)
p,s=load('05-1-1-b-1')
s=re.sub(r'> \$\$\n> (?:c_{ss}\(t\)\\approx|e_{ss}\(t\)\\approx|\\dot C_m\\approx|\\dot E_m\\approx)[^\n]*\n> \$\$\n>\n','',s)
s=s.replace(r'\approx-63.435°',r'\approx-63.4°').replace(r'\approx26.565°',r'\approx26.6°')
s=s.replace(r'\arg\dot E_m\approx\arctan\frac{164.210}{108.420}\approx56.565°',r'\arg\dot E_m=30°+\arctan\frac12')
s=s.replace('30°-(-33.435°)','30°-(30°-\\arctan2)')
s=section(s,'> [!derivation] 补充：','> [!derivation]- 非单位',r'''> [!note]- 换初相与象限
> 只把输入初相改为 $230°$，偏差振幅不变，相角为 $230°+\arctan(1/2)$，在第三象限；减去 $360°$ 得等价主值。
>
> 复数实部为负不等于振幅为负。模始终非负；只有最终正弦前的负号才可并入 $180°$ 相移。''')
save(p,s)
p,s=load('05-1-2-c')
s=re.sub(r'> \[!tip\] 思路\n(?:>[^\n]*\n)*\n','',s)
s=section(s,'> 振荡环节的相角由','> 所以题给', '> 对正增益、正阻尼的振荡环节，分母实部为零时相角才是 $-90°$，即 $\\omega_n^2-\\omega^2=0$。\n>')
s=section(s,'> 三条自检：','> [!warning]',r'''> 回代 $s=\mathrm j10$：
>
> $$
> G(\mathrm j10)=\frac{150}{\mathrm j50}=-3\mathrm j
> $$
>
> 幅值为 $3$、相角为 $-90°$，且 $G(0)=1.5$，与题设全部一致。

''')
s=section(s,'> [!note] 与例5.24','> 相关：','> [!note] 另一种反求条件\n> 由谐振峰反求参数见 [[05-2-e 伯德图反求例题]] 例5.24。若相角不是 $-90°$，必须联立一般幅值与相角方程，不能直接令 $\\omega=\\omega_n$。')
save(p,s)
p,s=load('05-1-2-b')
s=section(s,'- 幅值恒为 $1$','![[频域-典型环节-延迟Bode', '- 延迟不改幅值，因而不移动原有截止频率；在该处损失相角 $\\omega_c\\tau$ rad（度数为 $180°\\omega_c\\tau/\\pi$）。\n- 相角随频率持续滞后，没有固定终值。采样与保持器的区别见 [[05-1-2 典型环节频率特性]]。')
save(p,s)
p,s=load('05-2-d')
s=s.replace('> $\n','> $$\n')
s=re.sub(r'> \[!tip\] 思路\n(?:>[^\n]*\n)*\n','',s)
s=section(s,'> [!note] 本例 $0.5$','## ⚠️',r'''> [!derivation]- 例5.25：在频率0.5处核算修正量
> 微分、惯性、振荡三项的修正相加：
>
> $$
> \begin{aligned}
> \Delta L&=10\lg2-10\lg(1+0.4^2)\\
> &\quad-10\lg\big[(1-0.5^2)^2+0.5^2\big]
> \end{aligned}
> $$
>
> 对应表中的约 $+3.3$ dB。振荡环节仅在自身转折频率 $\omega_n=1$ 处修正量为零，不能据此省略其他频率的修正。''')
s=re.sub(r'> \*实线 = 精确对数幅频[^\n]*', '> *实线为精确幅频，虚线为渐近线；按上面的斜率序列核对。*',s)
s=re.sub(r'> \*实线 = 精确幅频/相频[^\n]*', '> *实线为精确频响，虚线为渐近线，点划线为低频延长线。*',s)
save(p,s)
p,s=load('05-2-c')
s=s.replace('|780]]','|520]]').replace('\\approx3.16','').replace('\\approx316','').replace('10^{-0.5}\\approx0.316',r'1/\sqrt{10}')
s=section(s,'> [!tip] 三图共用','> 相关：','> [!warning] 两个读图边界\n> (b) 低频延长线的零分贝交点用于定 $K$，不是折点；(c) 渐近线本身不能确定阻尼比，精确峰高还需额外读数。')
save(p,s)
# Introductory boilerplate: compact each abstract while retaining source and related links.
abstracts={
'05-1-2':'识别各环节的转折频率、斜率与相角。先查两张总表，再读一阶环节；二阶与延迟见 [[05-1-2-b 振荡·二阶微分与延迟环节]]。默认 $K,T,\\omega_n>0$、$0<\\zeta<1$、$\\tau\\ge0$。',
'05-2-1':'按“标准化 → 排折点 → 定低频线 → 加斜率 → 修正 → 自检”画伯德图，再逐环节相加得到相频。完整绘图题见 [[05-2-d 伯德图绘图例题]]。',
'05-2-b':'由低频段定型别与增益，由折点定环节参数，再回代核验。例题见 [[05-2-e 伯德图反求例题]]、[[05-2-c 反求传函·教材习题5-12]]。',
'05-2-d':'两道完整绘图题：例5.9练非最小相位环节，例5.25练标准化与修正。方法见 [[05-2-1 开环伯德图（画法·相频·修正）]]。',
'05-2-e':'三道反求题：例5.23一阶、例5.24二阶振荡、例5.26Ⅱ型。方法见 [[05-2-b 由伯德图反求（方法与口径）]]；渐近读数与精确频响应分开核算。',
'05-2-c':'教材习题5-12（书内250页，图5-62）：练习0型、Ⅱ型和微分型三种读图。方法见 [[05-2-b 由伯德图反求（方法与口径）]]。'}
for pre,abstract in abstracts.items():
 p,s=load(pre); a=s.index('> [!abstract]'); b=s.index('\n## ',a)
 old=s[a:b];source=re.search(r'> \*\*对应教材\*\*：[^\n]*',old)
 s=s[:a]+'> [!abstract] 本讲定位\n> '+abstract+ ('\n>\n'+source.group(0) if source else '')+'\n'+s[b:];save(p,s)
stats=[]
for p in files:
 before=original[p.name].decode('utf-8-sig');after=p.read_text(encoding='utf-8-sig')
 stats.append((p.name,len(before),len(after)))
(root/'.workbuddy/extend05a-stats.json').write_text(json.dumps(stats,ensure_ascii=False),encoding='utf-8')

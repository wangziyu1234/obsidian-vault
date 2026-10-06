from pathlib import Path
import re
root=Path('D:/obsidian/控制理论/自动控制原理')
stats=[]
def edit(prefix,fn):
 p=next(root.glob(prefix+' *.md')); raw=p.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); s=raw.decode('utf-8-sig'); nl='\r\n' if '\r\n' in s else '\n'; s=s.replace('\r\n','\n'); old=s
 s=fn(s)
 if s!=old:
  s=re.sub(r'(?m)^modify: .*','modify: 2026-10-06',s); p.write_bytes((b'\xef\xbb\xbf' if bom else b'')+s.replace('\n',nl).encode('utf-8'))
 stats.append((p.name,len(old.splitlines()),len(s.splitlines())))
def remove_callout(s,title):
 return re.sub(r'(?m)^> \[!\w+\][^\n]*'+re.escape(title)+r'[^\n]*\n(?:>[^\n]*\n)*\n?','',s)
def trim(s):
 s=remove_callout(s,'🎯 考点速记')
 return s.replace('\\dfrac','\\frac')
def three(s):
 s=trim(s)
 a=s.index('## ⚠️ 奈氏图这边'); b=s.index('下一站：',a)
 s=s[:a]+'''## ⚠️ 奈氏图这边最容易错的三点

- 先用起止点、实虚部符号和交轴点画图，再判稳；仅连起止点可能漏掉回转。
- 正频率半支计数时，自上而下穿过 $(-\\infty,-1)$ 记正穿越，自下而上记负穿越。
- 虚轴极点要补弧；虚轴零点处曲线连续过原点，相角可以跳变，不补无穷大弧。详见 [[05-4-1 奈氏判据]]。

'''+s[b:]
 s=s.replace('（含例5.4 的四种型别对照表）','（四种型别对照见 [[05-3-4 例题·Ⅰ型双惯性\\|例5.4]]）')
 return s
edit('05-3',three)
def drawing(s):
 s=trim(s)
 s=remove_callout(s,'最易混淆的两个判断')
 s=remove_callout(s,'镜像、倒数、负比例，分开记')
 s=s.replace('**这一篇讲什么**：**第二部分·奈氏图的知识点篇**——幅相曲线的通式与三条绘图规则（起点、终点、交点）、画图五步，以及最小相位与非最小相位的判定与镜像关系。','按“低频 → 高频 → 交轴点 → 分段连线”画正频率支，再区分镜像、倒数与最小相位。')
 s=s.replace('正确的连续相角','各非零频段内的连续相角')
 return s
edit('05-3-1',drawing)
def case4(s):
 s=trim(s);s=remove_callout(s,'思路');s=remove_callout(s,'三个关键数据')
 s=s.replace('两道写字面上的「画图成图」例题：','两道幅相曲线例题：').replace('**ν 越大越贴原点**，只有"从哪个象限进来、沿什么方向收尾"这两件事不变。','每增加一重积分，相角减少 $90^\\circ$，幅值再除以 $\\omega$；起止象限按上表读取。')
 return s.replace('\\frac{1}{\\sqrt2}\\approx0.7071','\\frac{1}{\\sqrt2}')
edit('05-3-4',case4)
def case5(s):
 s=trim(s).replace('原截图的第三象限分支需要补条件','“零点最近”不等于超前足够')
 s=s.replace('### ④ 用一组明确参数复现截图中的两种走向','### ④ 代入参数画图')
 s=s.replace('这是为绘图选取的参数，**不是截图已给出的数值**。','以下仅作绘图示例。')
 s=remove_callout(s,'为什么终点仍相同')
 return s
edit('05-3-5',case5)
def case6(s):
 s=trim(s);s=remove_callout(s,'交点很靠近原点也不能省掉')
 s=re.sub(r'\\approx(?:0\.40161|-0\.0267094|2\.48998|0\.412336\\mathrm j)','',s)
 return s
edit('05-3-6',case6)
def case7(s):
 s=trim(s);s=remove_callout(s,'保留原题的Ⅱ型结构');s=remove_callout(s,'这类题的解题顺序')
 s=s.replace('\\frac{1}{2\\sqrt2}\\approx0.35355','\\frac{1}{2\\sqrt2}')
 s=s.replace('### ⑦ 用特征多项式复核，但不替代 Nyquist 过程','### ⑦ 劳斯复核')
 return s
edit('05-3-7',case7)
def double(s):
 s=trim(s).replace('\\omega_g','\\omega_x')
 s=remove_callout(s,'记号口径');s=remove_callout(s,'解题顺序')
 s=s.replace('### 四、$\\omega_x$：穿越频率、幅值裕度与临界增益','### 四、$\\omega_x$：穿越频率、幅值裕度与临界增益')
 s=s.replace('### 二、通式：两个落轴方程、六个交点','### 二、通式：两个落轴方程、六个交点\n\n记 $\\tau_c=\\frac{T_1T_2}{T_1+T_2}$，它是Ⅰ型有限穿越点存在的门限。')
 s=s.replace('还需 $\\tau>T_1+T_2$ |',' $\\tau>T_1+T_2$ 且 $0<K<K_c$ 稳定 |')
 s=s.replace('**低频渐近线** $K','**Ⅰ型低频竖直渐近线** $K')
 old=r'\omega_x=\sqrt{\frac{4-3}{4\times1\times2}}=\frac{1}{2\sqrt2}=0.354,\qquad G(\mathrm j\omega_x)=-\frac{32}{3},\qquad K_c=\frac{3}{32}'
 new=r'\omega_x=\sqrt{\frac{4-3}{4\times1\times2}}=\frac{1}{2\sqrt2}'+'\n$$\n\n$$\n'+r'G(\mathrm j\omega_x)=-\frac{32}{3}'+'\n$$\n\n$$\n'+r'K_c=\frac{3}{32}'
 return s.replace(old,new)
edit('05-3-8',double)
def single(s):
 s=trim(s).replace('\\omega_g','\\omega_x');s=remove_callout(s,'一眼看完三行');s=remove_callout(s,'解题顺序')
 s=s.replace('原点，$\\varphi_\\infty=-180^\\circ$','原点：$\\tau=0$ 时 $-180^\\circ$，$\\tau>0$ 时 $-90^\\circ$').replace('原点，$\\varphi_\\infty=-270^\\circ$','原点：$\\tau=0$ 时 $-270^\\circ$，$\\tau>0$ 时 $-180^\\circ$')
 a=s.index('> [!warning] $\\tau=T$');b=s.index('**判稳结论**',a)
 s=s[:a]+'''> [!warning] 单独处理零极点相消
> $\\tau=T$ 时化为 $G(s)=K/s^\\nu$：0型闭环无动态极点，Ⅰ型闭环根为 $-K$；Ⅱ型有 $s=\\pm\\mathrm j\\sqrt K$，不渐近稳定。此时曲线整段落轴，不能当作孤立穿越点。

'''+s[b:]
 s=s.replace('**判稳结论**（$P=0$，曲线不绕 $(-1,\\mathrm j0)$）：','**判稳结论**（单位负反馈，以下 $h=\\infty$ 仅针对 $\\tau\\ne T$）：')
 s=s.replace(r'$\frac{K\tau}{T\omega^{\nu+1}}$ | $\omega_c\approx\left(\frac{K\tau}{T}\right)^{\frac1{\nu+1}}$',r'$\frac{K\tau}{T\omega^\nu}$ | $\omega_c\approx\left(\frac{K\tau}{T}\right)^{\frac1\nu}$（$\nu>0$）')
 s=s.replace('$\\tau<T$（惯性折点在前）时中间段','上表要求 $\\tau>0$。$\\tau=0$ 时没有零点折点：高频幅值为 $\\frac{K}{T\\omega^{\\nu+1}}$，故 $\\omega_c\\approx(K/T)^{1/(\\nu+1)}$。若某段幅值为常数，不能用幂次公式求唯一交点。\n\n$0<\\tau<T$（惯性折点在前）时中间段')
 s=s.replace('无整洁闭式，数值解','取正根；必要时作渐近估算')
 s=s.replace('用第三行估算','用无零点高频式估算')
 s=s.replace('**曲线不绕','**曲线不绕')
 a=s.index('> [!warning] 同型题的两个坑');b=s.index('### 五、',a)
 s=s[:a]+'''> [!warning] 先判稳，再解释裕度
> Ⅱ型仅在 $\\tau>T$ 时渐近稳定；$\\tau=T$ 是临界，$\\tau<T$ 不稳定。没有有限穿越点而记 $h=\\infty$，不能据此判稳。

'''+s[b:]
 s=s.replace('（分子分母同号才有解）','（分母非零，且结果为正）')
 s=s.replace('**分段线性（777 口径）**','0型若 $K=1$ 且 $\\tau=T$，所有频率的幅值都为1，没有唯一截止频率。\n\n**分段线性（777 口径）**')
 return s
edit('05-3-9',single)
def principles(s):
 s=trim(s);s=remove_callout(s,'$P=0$ 不等于「开环渐近稳定」');s=remove_callout(s,'画的方向 ≠ 数的方向');s=remove_callout(s,'下一步')
 a=s.index('> [!note] 虚轴上的**零点**');b=s.index('**穿越怎么记。**',a)
 s=s[:a]+'''> [!note] 虚轴零点不补无穷大弧
> $G(\\mathrm j\\omega_0)=0$，曲线连续经过原点；该点相角无定义，简单零点两侧的相角极限可相差 $180^\\circ$。不能把“曲线连续”说成“相角连续”。见 [[05-4-c 例题·虚轴零点与奈氏判据|习题5-16]]。

'''+s[b:]
 a=s.index('### 常见错法');b=s.index('### 判稳不等于',a);s=s[:a]+s[b:]
 s=s.replace('判据只对这类系统成立','本页以实系数负反馈写法计数；正反馈先改写特征方程')
 s=s.replace('计数要沿弧顺时针走回','计数按实际映射方向沿弧顺时针走回')
 return s
edit('05-4-1',principles)
def logarithmic(s):
 s=trim(s);s=remove_callout(s,'「相角减小」与「奈氏图上自下而上」是同一件事');s=remove_callout(s,'下一步')
 s=s.replace('两种判据完全等价：伯德图上相频穿越 $-180°$，正对应奈氏图穿过 $(-1,\\mathrm j0)$ 左侧负实轴，$N$ 相同、结论一致。伯德图的优点是幅值、相位分画两张图，数值分级直观、便于手绘。','以上对应仅在 $L(\\omega)>0$ 段成立；$L=0$ 且相角为奇数倍 $180^\\circ$ 时，须单独检查临界根。')
 s=s.replace('不可能包围 $(-1,\\mathrm j0)$','不可能穿过 $(-\\infty,-1)$')
 return s
edit('05-4-2',logarithmic)
def examples(s):
 s=trim(s);s=remove_callout(s,'思路')
 s=re.sub(r'> MATLAB 表示：[^\n]+\n>\n','',s)
 s=s.replace('\\frac{2\\pi}{3\\sqrt3}\\approx1.2092','\\frac{2\\pi}{3\\sqrt3}')
 s=s.replace('相角账面跳变','相角两侧极限相差180度')
 a=s.index('> 其中 $K=4$ 时的截止频率'); b=s.index('> **④ 判稳。**',a);s=s[:a]+s[b:]
 s=s.replace('延迟环节只加相角滞后、不改幅值，所以它**只恶化稳定性**。','本例幅值单调下降，增大延迟会使首次负实轴交点向外移，因而缩小稳定余量。')
 return s
edit('05-4-b',examples)
def logexamples(s):
 s=trim(s);s=remove_callout(s,'思路')
 s=s.replace('ωg = 3.16','ωx = √10')
 s=s.replace('\\omega_x=\\sqrt{10}\\approx3.162','\\omega_x=\\sqrt{10}')
 s=s.replace('\\frac{K}{11.0}','\\frac{K}{11}')
 return s
edit('05-4-d',logexamples)
Path('D:/obsidian/.workbuddy/extend-05b-stats.txt').write_text('\n'.join(map(str,stats)),encoding='utf-8')

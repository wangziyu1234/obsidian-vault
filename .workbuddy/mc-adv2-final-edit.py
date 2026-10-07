from pathlib import Path
import re
import sympy as s
root=Path('D:/obsidian'); folder=root/'控制理论/777习题集'
ap=next(folder.glob('现控200题强化 专题二*答案与解析*.md'));qp=next(folder.glob('现控200题强化 专题二*题目*.md'))
a=ap.read_text(encoding='utf-8-sig');q=qp.read_text(encoding='utf-8-sig')
def rep(old,new):
 global a
 assert old in a,old[:100]
 a=a.replace(old,new)
def section(n,fn):
 global a
 start=a.index(f'#### ✏️ 2-{n}　解析'); end=a.find('#### ✏️ ',start+5)
 if end<0:end=a.index('## 录入说明',start)
 a=a[:start]+fn(a[start:end])+a[end:]
def between(t,start,end,new):
 i=t.index(start);j=t.index(end,i);return t[:i]+new+t[j:]
rep(r'x(1)=[0.434\ \ 0.334]^T',r'y(1)=\frac{\mathrm e}{2}+\frac{3\mathrm e^{-3}}2-1')
rep(r',\qquad x(1)=\begin{bmatrix}0.434\\0.334\end{bmatrix}','')
rep('输出值 $y(1)=x_1(1)=0.434$。',r'''代入 $t=1$，状态和输出均保留精确形式：

$$
x(1)=\begin{bmatrix}\frac{\mathrm e}{2}+\frac{3\mathrm e^{-3}}2-1\\[4pt]\frac{\mathrm e}{2}-\frac{\mathrm e^{-3}}2-1\end{bmatrix}
$$

$$
y(1)=x_1(1)=\frac{\mathrm e}{2}+\frac{3\mathrm e^{-3}}2-1
$$''')
section(5,lambda t:between(t,'对 $M=', '**不论如何',r'''由题设矩阵可直接看出 $(A-\lambda E)^2=0$。右乘 $b$ 得

$$
A^2b-2\lambda Ab+\lambda^2b=0
$$

所以 $M=[b\ \ Ab\ \ A^2b]$ 的三列恒线性相关：

$$
r(M)\le2<3
$$

'''))
rep('李二法判稳不满秩正定时结论是"不稳定"而非"不确定"时，可用特征值直接佐证；','本题由正特征根确认不稳定，不能把“某个候选 $P$ 不正定”当作一般的不稳定判据；')
rep(r'S=[b\ \ Ab\ \ A^2b]=\begin{bmatrix}0&0&1\\0&1&0\\1&0&0\end{bmatrix}',r'S=[b\ \ Ab\ \ A^2b]=\begin{bmatrix}0&0&1\\0&1&1\\1&1&1\end{bmatrix}')
rep(r'$P_3=(0,0,1)^T$',r'$P_3=(1,0,1)^T$')
section(10,lambda t:between(t,'即二维能控子系统','（2）',r'''令 $\bar x=Px$，其中 $\bar x_3=x_2+x_3$ 是变换后的第三分量，不是原坐标 $x_3$。二维能控子系统为

$$
\dot{\bar x}_c=\begin{bmatrix}1&0\\1&2\end{bmatrix}\bar x_c+\begin{bmatrix}2\\-2\end{bmatrix}\bar x_3+\begin{bmatrix}1&0\\0&1\end{bmatrix}u
$$

一维不能控子系统为

$$
\dot{\bar x}_3=3\bar x_3
$$

'''))
section(11,lambda t:between(t,'$$','> [!note] 本题总结',r'''令

$$
\lambda_1=\frac{-3+\sqrt5}{2}
$$

$$
\lambda_2=\frac{-3-\sqrt5}{2}
$$

部分分式展开为

$$
G(s)=\frac{1}{\sqrt5}\frac1{s-\lambda_1}-\frac{1}{\sqrt5}\frac1{s-\lambda_2}
$$

取 $X_i(s)=U(s)/(s-\lambda_i)$，得到精确对角型实现：

$$
\dot x=\begin{bmatrix}\lambda_1&0\\0&\lambda_2\end{bmatrix}x+\begin{bmatrix}1\\1\end{bmatrix}u
$$

$$
y=\begin{bmatrix}\frac1{\sqrt5}&-\frac1{\sqrt5}\end{bmatrix}x
$$

核验能控、能观矩阵的行列式：

$$
\det[b\ \ Ab]=\lambda_2-\lambda_1=-\sqrt5\ne0
$$

$$
\det\begin{bmatrix}c\\cA\end{bmatrix}=\frac1{\sqrt5}\ne0
$$

所以该实现既能控又能观。

'''))
rep(r'$\dot x=\begin{bmatrix}-0.38&0\\0&-2.62\end{bmatrix}x+\begin{bmatrix}1\\1\end{bmatrix}u$，$y=[0.45\ \ -0.45]x$（约当/对角型实现）',r'$A=\mathrm{diag}(\frac{-3+\sqrt5}{2},\frac{-3-\sqrt5}{2})$，$b=[1\ \ 1]^T$，$c=\frac1{\sqrt5}[1\ \ -1]$')
section(12,lambda t:t.replace('（4）李雅普诺夫方程',r'''这里的状态应记为 $z=Tx$。作为原系统的可逆状态变换，必须仍满足 $a\ne1,\frac12$：

$$
T=\begin{bmatrix}3c+cA\\c\end{bmatrix}=\begin{bmatrix}3-2a&1\\1&a\end{bmatrix}
$$

$$
\det T=-(2a-1)(a-1)\ne0
$$

直接相乘可验证 $TA=\bar AT$、$Tb=\bar b$、$c=\bar cT$。退化参数 $a=1$ 或 $\frac12$ 时，上述矩阵仍给出同传递函数的一种实现，但不再是原系统的相似变换。

（4）李雅普诺夫方程''').replace(r'\dot x=\begin{bmatrix}0&-2\\1&-3\end{bmatrix}x+\begin{bmatrix}1\\a\end{bmatrix}u,\qquad y=[0\ \ 1]x',r'\dot z=\begin{bmatrix}0&-2\\1&-3\end{bmatrix}z+\begin{bmatrix}1\\a\end{bmatrix}u,\qquad y=[0\ \ 1]z'))
A=s.Matrix([[1,-1],[1,-2]]);T=s.Matrix([[1,-1],[0,1]]);b=s.Matrix([1,1]);c=s.Matrix([[1,0]])
assert T*A*T.inv()==s.Matrix([[0,1],[1,-1]]) and T*b==s.Matrix([0,1]) and c*T.inv()==s.Matrix([[1,1]])
section(13,lambda t:t.replace('（3）按勘误口径',r'''对应的状态变换可取

$$
z=Tx=\begin{bmatrix}1&-1\\0&1\end{bmatrix}x
$$

即 $z_1=x_1-x_2$、$z_2=x_2$。此时 $TAT^{-1}=\bar A$、$Tb=\bar b$、$cT^{-1}=\bar c$，核对了标准型与原状态的关系。下问反馈增益仍针对原坐标 $x$ 求取。

（3）按勘误口径'''))
rep(r'P=\begin{bmatrix}1&0&0\\-1&1&0\\0&-1&1\end{bmatrix}',r'P=\begin{bmatrix}1&0&0\\-1&1&0\\1&-1&1\end{bmatrix}')
section(14,lambda t:t.replace('不可观测。',r'''还须检查后续行没有增加秩：

$$
cA^2=-c-2cA=[-2\ \ 3\ \ -4]
$$

所以完整能观矩阵 $[c;cA;cA^2]$ 的秩仍为 $2$，系统不可观测。''',1))
old=r'\begin{bmatrix}2.78&7.94\\7.94&95.07\end{bmatrix}'
new=r'\begin{bmatrix}\frac{25}{9}&\frac{500}{63}\\[2pt]\frac{500}{63}&\frac{113800}{1197}\end{bmatrix}'
rep(old,new)
section(17,lambda t:between(t,'> [!warning]','> [!note] 本题总结',r'''逐项比较可得

$$
-\frac9{25}p_{11}=-1
$$

$$
\frac45p_{11}-\frac7{25}p_{12}=0
$$

$$
p_{11}+\frac95p_{12}-\frac{19}{100}p_{22}=-1
$$

顺序主子式为

$$
\Delta_1=\frac{25}{9}>0
$$

$$
\Delta_2=\det P=\frac{1685000}{8379}>0
$$

> [!warning] 复算更正
> 原书 $P_{22}$ 印 $95.4$，正确精确值为 $\frac{113800}{1197}$；旧笔记的分数与小数也不正确，现统一用精确分数。

$P$ 正定，系统在平衡状态 $x_e=0$ 处大范围渐近稳定。

'''))
section(19,lambda t:between(t,'（考点：','> [!note] 本题总结',r'''（考点：非线性系统的李一法及平衡点前提）

先代入原题检查平衡点：

$$
f(0,0)=\begin{bmatrix}0\\-1+2\end{bmatrix}=\begin{bmatrix}0\\1\end{bmatrix}\ne0
$$

> [!warning] 原题前提矛盾
> 按扫描原文的常数项 $+2$，原点不是平衡点，不能讨论它作为平衡点的稳定性。原答案未检查此前提就线性化，因而不适用于原题。

若明确附加假设：把第二式常数项 $+2$ 改为 $+1$，则原点才是平衡点。在这一假设下：

$$
J(0)=\begin{bmatrix}1&-3\\2&3\end{bmatrix}
$$

$$
\det(\lambda E-J(0))=\lambda^2-4\lambda+9
$$

$$
\lambda_{1,2}=2\pm\sqrt5\,\mathrm j
$$

有正实部特征值，因此修改后的系统在原点不稳定。该结论必须连同“常数项改为 $+1$”的假设一起使用。

'''))
rep(r'$A=\cfrac{\partial f}{\partial x}\Big|_{0}=\begin{bmatrix}1&-3\\2&3\end{bmatrix}$，$\lambda=2\pm\sqrt5\,\mathrm j$ 有正实部，不稳定',r'原题 $f(0)=[0\ \ 1]^T\ne0$，原点不是平衡点；若常数项改为 $+1$，则原点不稳定')
warning='> [!warning] 原题前提核对\n> 按原文常数项 $+2$，代入原点得 $f(0)=[0\\ \\ 1]^T\\ne0$，因此原点不是平衡点；题设保留原样，解析中区分原题与附加修正假设。\n\n'
i=q.index('#### ✏️ 2-20');q=q[:i]+warning+q[i:]
rep(r'\Delta_2=\frac14\times\frac{7}{12}-\frac{1}{144}=\frac14>0',r'\Delta_2=\frac14\times\frac{7}{12}-\frac{1}{144}=\frac5{36}>0')
rep('![[附件/现控强化2-20-ans-状态变量图.png|430]]',r'''由闭环 $A-bK$ 写出各积分器的输入：

$$
\dot x_1=v-2x_2
$$

$$
\dot x_2=x_1-2x_2
$$

$$
y=x_1+x_2
$$

![[现控强化2-20-正确状态变量图.png|430]]

> [!note]- 原书状态变量图（保留供勘误对照）
> ![[附件/现控强化2-20-ans-状态变量图.png|430]]''')
section(20,lambda t:t.replace('> [!warning] ⚠️ 复算提示（两处）','> [!warning] 复算提示').replace('（下图照录）','（下方折叠保留）').replace('图中反馈系数疑有排印错误，引用时注意。','正文已按正确闭环重新绘图。\n>\n> ③ 原书最终 $P$ 矩阵右下角误印 $\\frac1{12}$，同页方程解为 $\\frac14$；应采用后者。'))
rep(r'\begin{bmatrix}1.25&0.25\\0.25&0.25\end{bmatrix}',r'\begin{bmatrix}\frac54&\frac14\\[2pt]\frac14&\frac14\end{bmatrix}')
rep('系统为线性系统，则只有 $x_e=0$ 一个平衡状态。','零输入时平衡点满足 $Ax_e=0$。因 $\\det A=2\\ne0$，只有 $x_e=0$ 一个平衡状态。')
rep('即 $\\dot V(x)$ 仅在平衡点 $(0,0)$ 处为零。','所以集合 $\\{x:\\dot V(x)=0\\}$ 中的最大不变集只有原点。由 LaSalle 不变集原理，')
rep('故系统在平衡点处**大范围渐近稳定**。','故系统在平衡点处**大范围渐近稳定**。')
rep('$\\dot V=-4x_2^2$ 严格说是半负定，"仅在原点为零"要借 $\\dot x_2=-x_1^3$ 把 $x_2=0$ 线上的运动赶出该线（即拉萨尔不变集思路的初等版本）。','$\\dot V=-4x_2^2$ 为负半定，在整条 $x_2=0$ 线上为零；渐近稳定性来自零导数集合的最大不变集只有原点。')
section(25,lambda t:between(t,'（1）','$$\nP=',r'''（1）离散系统平衡状态满足 $(E-G)x_e=0$，而

$$
\det(E-G)=1-\frac14=\frac34\ne0
$$

所以唯一平衡状态为 $x_e=0$。

（2）取 $Q=E$，令对称矩阵

$$
P=\begin{bmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{bmatrix}
$$

由 $G^TPG-P=-E$，得到

$$
\frac14p_{22}-p_{11}=-1
$$

$$
-\frac34p_{12}=0
$$

$$
\frac14p_{11}-p_{22}=-1
$$

解得 $p_{11}=p_{22}=\frac43$、$p_{12}=0$：

'''))
for name in ['a','q']:
 t=globals()[name];t=t.replace(r'\ddot y-\dot y=\dot u-u',r'\dddot y-\dot y=\dot u-u');globals()[name]=t
section(28,lambda t:between(t,'> [!warning] ⚠️ 题面与阶数','（1）',r'''原题为三阶微分方程 $\dddot y-\dot y=\dot u-u$，已逐点核对扫描页。以下在零初始条件下求传递函数。

'''))
rep('①当且仅当传递函数无零极点对消时系统为 BIBO 稳定——有对消时要看**约简后**的极点；','①连续有理真有理系统 BIBO 稳定当且仅当约简后所有极点均在左半平面；')
rep('三阶口径 $G(s)','三阶原题 $G(s)')
# Replace stale history with current, reviewable conclusions.
a=a[:a.index('## 录入说明')]+r'''## 录入说明

> [!note] 覆盖与核验
> 本页涵盖 2-1—2-29 全部 29 题，与题目页逐题互链；每题保留题设、解答、总结及必要勘误。2026-10-07 复核原题、答案扫描页与官方勘误，并补齐精确数值、状态变换前提和稳定性论证。
>
> 官方勘误中 2-8 的导数下标、2-13 的参考输入、2-14 的能观矩阵、2-20 的状态响应已落实。2-28 的传递函数更正采纳，但“BIBO 稳定”的结论未采纳：约简后仍有零极点。

> [!warning] 复习时重点回查
> 2-19 原题原点不是平衡点；2-28 原题确为三阶，不存在旧笔记所称的阶数冲突。
>
> 2-14 修正能控变换逆矩阵并补能观矩阵秩依据；2-17 用精确分数解离散李雅普诺夫方程；2-20 修正 $P$ 的行列式、标出原书矩阵与图的排印问题，并补正确状态变量图。
>
> 2-9 修正能控矩阵，2-10 区分变换后坐标并修正特征向量，2-12 补状态变换可逆条件，2-22 用最大不变集论证，2-25 用 $E-G$ 判断平衡点。公式和结论以各题的推导及回代核验为准。
'''
rep('> 全批矩阵结论均经 sympy/numpy 独立复算（`_verify_xq2.py`，80 项全过；见各题尾注与文末录入说明）。','> 原页与复算结论不一致时，正文分别保留原题、指出矛盾并列明修正假设，详见各题提示。')
for p,t in [(ap,a),(qp,q)]:p.write_bytes(t.replace('\n','\r\n').encode('utf-8'))
print('Applied approved topic 2 mathematical corrections.')

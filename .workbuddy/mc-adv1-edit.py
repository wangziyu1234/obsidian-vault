from pathlib import Path
import re
root=Path('D:/obsidian')
base='现控200题强化 专题一 状态空间描述'
qp=root/'控制理论/777习题集'/f'{base}（题目）.md'
ap=root/'控制理论/777习题集'/f'{base}（答案与解析）.md'
q=qp.read_text(encoding='utf-8-sig'); a=ap.read_text(encoding='utf-8-sig')
for name,t in [('q',q),('a',a)]: (root/'.workbuddy'/f'mc-adv1-original-{name}.md').write_text(t,encoding='utf-8')
def parts(t,pat):
    ms=list(re.finditer(pat,t,re.M)); out={}
    for i,m in enumerate(ms):
        end=ms[i+1].start() if i+1<len(ms) else len(t)
        s=t[m.end():end]; tail=''
        h=re.search(r'\n## ',s)
        if h: s,tail=s[:h.start()],s[h.start():]
        out[int(m.group(1))]=[m.group(0),s,tail]
    return t[:ms[0].start()],out
qh,qs=parts(q,r'^\*\*1-(\d+)（[^\n]+?\*\*')
ah,ans=parts(a,r'^\*\*1-(\d+)　答案\*\*')
def rep(n,old,new):
    assert old in ans[n][1],(n,old[:70])
    ans[n][1]=ans[n][1].replace(old,new)
def body(n,t): ans[n][1]='\n\n'+t.strip()+'\n\n'
rep(1,'由电路图可知','取电感电流 $x_2$ 的正方向为从 $R_1$ 经 $L$ 向右，输入向量 $u=[u_1,u_2]^T$。节点电压为 $y=u_1-x_1$。由 KVL、KCL 分别有')
rep(1,'y=R_2x_2','y=R_1x_2')
rep(1,r'\\[4pt]\frac{1}{L}&-\frac{R_1}{L}',r'\\[4pt]-\frac{1}{L}&-\frac{R_1}{L}')
rep(1,r'\\[4pt]\frac{1}{L}&\frac{1}{L}',r'\\[4pt]\frac{1}{L}&-\frac{1}{L}')
rep(1,'整理成矩阵形式得',r'''代入 $y=u_1-x_1$，先解出两个状态的一阶导数：

$$
\dot x_1=-\frac{x_1}{R_2C}+\frac{x_2}{C}+\frac{u_1}{R_2C}
$$

$$
\dot x_2=-\frac{x_1}{L}-\frac{R_1x_2}{L}+\frac{u_1-u_2}{L}
$$

整理成矩阵形式得''')
ans[2][1]=re.sub(r'\n>\n> 另注：原书把阻尼.*?此差异仅作提示。','',ans[2][1])
rep(2,'令 $f(t)$ 为输入量','位移以静平衡位置为零点、向下为正，因此重力已由静态平衡抵消；图中 $B_2$ 连接固定端与 $M_2$。令 $f(t)$ 为输入量')
rep(3,r'(x_1+x_2)R_1=-R_2',r'(x_1+x_2)R_3=-R_2')
rep(4,'以弹簧的伸长度 $y_1,y_2$','以两质量块相对平衡位置的位移 $y_1,y_2$（$k_1$ 的伸长量为 $y_1-y_2$）')
rep(4,'$C=c$ 的记号要按一阶导理解','图中 $c_1,c_2$ 均为速度')
rep(4,r'\dot y_1=C_1=x_3,\qquad \dot y_2=C_2=x_4',r'\dot y_1=c_1=x_3,\qquad \dot y_2=c_2=x_4')
rep(5,'（3）输出可观测、状态不可观测时，可构造**全维状态观测器**重构状态：设 $\\dot{\\hat x}=(A-GC)\\hat x+Bu+Gy$，选增益 $G$ 使 $A-GC$ 的极点（观测器极点）配置在期望位置（一般取系统极点的 2~5 倍），再用重构状态 $\\hat x$ 代替真实状态实现状态反馈。',r'''（3）原题“只有输出可观测、状态不可观测”指输出可测量、状态不能直接测量，并非系统不满足能观性。

本题输出为 $x_1$，能观矩阵为

$$
Q_o=\begin{bmatrix}1&0&0&0\\0&1&0&0\\-12&-0.02&12&0\\0.24&-11.9996&-0.24&12\end{bmatrix}
$$

其行列式为 $144\ne0$，故能够任意配置观测器极点。构造

$$
\dot{\hat x}=A\hat x+Bu+G(y-C\hat x)
$$

选择 $G$ 使 $A-GC$ 为 Hurwitz 矩阵，再用

$$
u=v-K\hat x
$$

实现状态反馈。由于本题完全能控，$K$ 可配置控制闭环 $A-BK$ 的极点；观测器极点通常选得比控制闭环主导极点快 2~5 倍，并兼顾测量噪声。''')
rep(6,'$s$ 为微分环节（$sx=\\dot x$）、$\\frac1s$ 为积分环节（$\\frac1s x=x$）','零初值下 $sX(s)$ 对应微分，$X(s)/s$ 对应积分')
body(7,r'''（考点：结构图建模、交叉反馈与极点）

令第一个求和点的输出为 $w=u_1-c_1$，并取 $u=[u_1,u_2]^T$、$c=[c_1,c_2]^T$。从原图逐条读出

$$
(s+1)X_1=W,\qquad C_1=X_1+X_2
$$

$$
(s+2)X_2=U_2-C_2,\qquad C_2=W+X_3
$$

$$
(s+2)X_3=X_2
$$

最后一条支路是正增益 $1/(s+2)$，不能额外添加负号。代入 $w=u_1-x_1-x_2$ 后，得

$$
\dot x_1=-2x_1-x_2+u_1
$$

$$
\dot x_2=x_1-x_2-x_3-u_1+u_2
$$

$$
\dot x_3=x_2-2x_3
$$

$$
\dot x=\begin{bmatrix}-2&-1&0\\1&-1&-1\\0&1&-2\end{bmatrix}x+\begin{bmatrix}1&0\\-1&1\\0&0\end{bmatrix}u
$$

$$
c=\begin{bmatrix}1&1&0\\-1&-1&1\end{bmatrix}x+\begin{bmatrix}0&0\\1&0\end{bmatrix}u
$$

由特征多项式

$$
\det(\lambda E-A)=(\lambda+2)(\lambda^2+3\lambda+4)
$$

得到系统极点

$$
\lambda_1=-2
$$

$$
\lambda_{2,3}=\frac{-3\pm\mathrm j\sqrt7}{2}
$$

> [!warning] 原答案负号有误
> 原答案册将第三条写为 $(s+2)X_3=-X_2$，与原题正增益支路不符，因而给出了另一组极点。本题按原题图列式并重新计算。
''')
ans[8][1]=re.sub(r'（3）分母.*?(?=\n> \[!warning\])',r'''（3）记分母为 $p(s)=s^3+2s^2+4s-1$。有 $p(0)=-1<0$、$p(1)=6>0$，由连续性知区间 $(0,1)$ 内至少有一个正实根；该根不能与分子唯一的零点 $s=-1$ 相消。因此系统**不是 BIBO 稳定**，无需计算小数根。

''',ans[8][1],flags=re.S)
rep(14,'取\n\n$$\nP=', '作坐标变换 $\\bar x=Px$，取\n\n$$\nP=')
rep(15,'（1）由题可知','（1）本问按题目所隐含的三阶实现理解：传递函数本身不能唯一决定非最小实现的能控、能观性。由题可知')
rep(17,'（4）由上题解可知 $S=[b\\ \\ Ab]$，$\\mathrm{rank}\\,S=2$；$V=\\begin{bmatrix}C\\\\CA\\end{bmatrix}$，$\\mathrm{rank}\\,V=2$，所以系统可控可观。',r'''（4）直接在本题计算能控、能观矩阵：

$$
S=[B\ AB]=\begin{bmatrix}0&-2\\2&0\end{bmatrix}
$$

$$
V=\begin{bmatrix}C\\CA\end{bmatrix}=\begin{bmatrix}0&1\\6&0\end{bmatrix}
$$

两者行列式分别为 $4$、$-6$，均非零，所以系统完全能控、完全能观。''')
rep(18,r'\mathrm{rank}\,Q_c=\mathrm{rank}[B\ \ AB]=\begin{bmatrix}1&-5\\1&1\end{bmatrix}=2',r'Q_c=[B\ AB]=\begin{bmatrix}1&-5\\1&1\end{bmatrix}')
rep(18,'故该系统完全能控。','由于 $\\det Q_c=6\\ne0$，故 $r(Q_c)=2$，该系统完全能控。')
rep(19,'BIBO 判据（传函无零极点对消时看传函极点）','BIBO 判据（看约分后的传函极点）')
rep(20,'（1）\n\n$$',r'''（1）对于零初态、单位阶跃输入，$t=0^+$ 时有

$$
B=\dot x(0^+)-Ax(0)=\dot x(0^+)=\begin{bmatrix}1\\-1\end{bmatrix}
$$

也可代入任意 $t>0$ 检查 $\dot x-Ax=B$。以下状态转移矩阵用于回验给定响应。

$$''')
rep(22,r'\Phi(-3t)=\begin{bmatrix}e^{-3t}&-6te^{-3t}\\0&e^{-3t}\end{bmatrix}',r'\Phi(-3t)=\begin{bmatrix}e^{-3t}&-6te^{-3t}\\0&e^{-3t}\end{bmatrix}^{-1}')
rep(22,r'\Phi(3t)=\begin{bmatrix}e^{3t}&-6te^{3t}\\0&e^{3t}\end{bmatrix}',r'\Phi(3t)=\Phi(-3t)^{-1}=\begin{bmatrix}e^{-3t}&-6te^{-3t}\\0&e^{-3t}\end{bmatrix}')
rep(22,'（2）设该系统',r'''由 $A=\dot\Phi(0)$ 得

$$
A=\begin{bmatrix}-1&-2\\0&-1\end{bmatrix}
$$

$$
Q_o=\begin{bmatrix}c\\cA\end{bmatrix}=\begin{bmatrix}\rho&0\\-\rho&-2\rho\end{bmatrix}
$$

因此 $\det Q_o=-2\rho^2$，**完全能观的充要条件为 $\rho\ne0$**。

（2）设该系统''')
rep(23,'1.98','1.9892'); rep(23,'0.9861','0.990888');rep(23,'h_0-5=0.99','h_0-5=0.990888');rep(23,'h_0=5.99','h_0=5.990888');rep(23,'h_1=2.98','h_1=2.9892')
rep(23,'（3）系统全维状态观测器结构图如下',r'''于是观测器为

$$
\dot{\hat x}=A\hat x+Bu+h(y-C\hat x)
$$

$$
h=\begin{bmatrix}5.990888\\2.9892\\-1.99\end{bmatrix}
$$

以上小数是题给有限小数进行精确运算后的结果，未进行舍入。原书的 $5.99,2.98$ 仅为近似增益，不能与指定极点写成精确等号。

（3）系统全维状态观测器结构图如下''')
rep(24,r'|sI-A-BK|',r'|sI-A+BK|')
rep(25,'> [!note] 说明\n> 原书 (2) 问只列了闭环状态空间表达式、未展开传递函数与不可控/不可观模态的分析，本页照录；两者的传递函数与模态归属可由上式闭环矩阵直接求出。','')
rep(25,'> 观测器（下半）与原系统（上半）并置：观测器极点在 $-4,-5$，速度反馈增益取 $K=[-3,-4]$；闭环矩阵的左上块仍是原系统 $A$（不可控模态），模态归属由分块结构直接读出。','> 极点归属须对完整闭环作能控、能观检查；传函中的消去模态不一定不可观，也可能只是不能由参考输入激发。')
rep(25,'（3）结构图为',r'''将四维闭环矩阵记为 $F$，输入列、输出行分别记为 $B_{\mathrm{cl}}$、$C_{\mathrm{cl}}$。为辨认极点，令估计误差 $e=x-\hat x$，则

$$
\begin{bmatrix}\dot x\\\dot e\end{bmatrix}
=\begin{bmatrix}A+bk&-bk\\0&A-hc\end{bmatrix}
\begin{bmatrix}x\\e\end{bmatrix}
+\begin{bmatrix}b\\0\end{bmatrix}v
$$

控制闭环 $A+bk$ 的极点为 $-1,-3$，误差系统 $A-hc$ 的极点为 $-4,-5$。传递函数按零初态计算，此时 $e(0)=0$ 导致 $e(t)=0$，于是

$$
G_{vy}(s)=c[sE-(A+bk)]^{-1}b=\frac1{s+1}
$$

原题给定的非零 $x(0)$ 影响零输入响应，但不改变传递函数。对完整四维实现进行 PBH 检查：

| 模态 $\lambda$ | $r[\lambda E-F,\ B_{\mathrm{cl}}]$ | $r\begin{bmatrix}\lambda E-F\\C_{\mathrm{cl}}\end{bmatrix}$ | 归属 |
| :-- | :-- | :-- | :-- |
| $-1$ | $4$ | $4$ | 能控、能观 |
| $-3$ | $3$ | $4$ | 不能控、能观 |
| $-4$ | $3$ | $4$ | 不能控、能观 |
| $-5$ | $3$ | $4$ | 不能控、能观 |

因此 **$-3,-4,-5$ 为不可控模态，无不可观模态**。也可验证完整能控矩阵秩为 $1$、能观矩阵秩为 $4$。

（3）结构图为''')
# Reference input is v throughout the augmented model.
rep(25,r'\end{pmatrix}u(t)',r'\end{pmatrix}v(t)')
rep(25,'∴ 状态观测阵为 $h=\\begin{pmatrix}8.5\\\\-0.5\\end{pmatrix}$',r'''因此

$$
h=\begin{bmatrix}\frac{17}{2}\\-\frac12\end{bmatrix}
$$

$$
\dot{\hat x}=\begin{bmatrix}-\frac{13}{2}&-\frac{15}{2}\\\frac12&-\frac52\end{bmatrix}\hat x
+\begin{bmatrix}1\\0\end{bmatrix}u
+\begin{bmatrix}\frac{17}{2}\\-\frac12\end{bmatrix}y
$$''')
rep(27,'所以对角形为','令新的状态为 $z=T^{-1}x$，所以对角形为')
rep(27,r'\dot x=\begin{pmatrix}-1&0\\0&-2\end{pmatrix}x+\begin{pmatrix}1\\-1\end{pmatrix}u,\qquad y=(-1\ \ -3)x',r'\dot z=\begin{pmatrix}-1&0\\0&-2\end{pmatrix}z+\begin{pmatrix}1\\-1\end{pmatrix}u,\qquad y=(-1\ \ -3)z')
rep(27,'特征值两两互异时可对角化，否则化约当型','特征值两两互异时一定可对角化；有重根时还须检查独立特征向量数')
body(28,r'''（考点：广义特征向量链与约当变换）

原题输出式遗漏状态向量，按 $y=[1,0,0]x$ 理解。由

$$
\det(\lambda E-A)=(\lambda+1)^2(\lambda+2)
$$

得特征值 $-1$（二重）与 $-2$。解 $(A+E)p_1=0$，取

$$
p_1=\begin{bmatrix}-1\\0\\1\end{bmatrix}
$$

由于 $r(A+E)=2$，$-1$ 只有一个独立特征向量，需要再求广义特征向量。由 $(A+E)p_2=p_1$，可取

$$
p_2=\begin{bmatrix}1\\0\\0\end{bmatrix}
$$

再解 $(A+2E)p_3=0$，取

$$
p_3=\begin{bmatrix}-4\\\frac12\\1\end{bmatrix}
$$

因此

$$
T=[p_1\ p_2\ p_3]=\begin{bmatrix}-1&1&-4\\0&0&\frac12\\1&0&1\end{bmatrix}
$$

$$
\det T=\frac12\ne0
$$

由 $x=T\bar x$，须按 $T^{-1}AT$、$T^{-1}B$、$CT$ 三个方向分别变换：

$$
\bar A=\begin{bmatrix}-1&1&0\\0&-1&0\\0&0&-2\end{bmatrix}
$$

$$
\bar B=\begin{bmatrix}1\\1\\0\end{bmatrix}
$$

$$
\bar C=[-1\ 1\ -4]
$$

故变换后的状态空间表达式为

$$
\dot{\bar x}=\bar A\bar x+\bar Bu
$$

$$
y=\bar C\bar x
$$

回代检查 $AT=T\bar A$、$T\bar B=B$、$\bar C=CT$ 均成立。

> [!warning] 原答案的广义特征向量有误
> 原书 $p_2=(\frac34,0,-\frac12)^T$ 实际满足 $(A+E)p_2=\frac14p_1$，不能与超对角元为 $1$ 的约当块配用。本题选取上面的简单向量，重新计算输入、输出矩阵；不再照录不自洽的结果。
''')
for n in [30,31]:
    s=ans[n][1]; start=s.index('（3）'); tail=s.find('> [!note] 本题总结',start)
    s=s[:start]+r'''（3）按零阶保持离散化，采样周期 $T=0.1\,\mathrm s=\frac1{10}\,\mathrm s$。令 $q=e^{-T}=e^{-1/10}$，则

$$
G=e^{AT}=\begin{bmatrix}-q+2q^2&-2q+2q^2\\q-q^2&2q-q^2\end{bmatrix}
$$

输入矩阵必须对 $e^{At}B$ 的两个分量分别积分：

$$
H=\int_0^T e^{At}B\,\mathrm dt
$$

$$
H=\begin{bmatrix}\displaystyle\int_0^T(-2e^{-t}+2e^{-2t})\,\mathrm dt\\[6pt]\displaystyle\int_0^T(2e^{-t}-e^{-2t})\,\mathrm dt\end{bmatrix}
$$

$$
H=\begin{bmatrix}-(1-q)^2\\\frac{3-4q+q^2}{2}\end{bmatrix}
$$

于是精确离散模型为

$$
x(k+1)=Gx(k)+Hu(k)
$$

$$
y(k)=[1\ 4]x(k)
$$

> [!note] 精确值口径
> 原书给出的舍入矩阵以及 $H=[0,0.1]^T$ 不能写作精确等式；尤其 $H$ 第一分量并不为零。本题保留指数形式，手算无需展开多位小数。

'''+s[tail:]
    ans[n][1]=s
# Correct original statement transcription from rendered PDF.
qs[22][1]=qs[22][1].replace(r'\end{bmatrix}\n',r'\end{bmatrix}\n')
qs[22][1]=qs[22][1].replace(r'0&e^{-3t}\end{bmatrix}',r'0&e^{-3t}\end{bmatrix}^{-1}')
qs[28][1]=qs[28][1].replace(r'y=(1\ \ 0\ \ 0)',r'y=(1\ \ 0\ \ 0)x')+'\n> [!note] 题面补字\n> 原书输出式漏写末尾状态向量 $x$，这里按 $y=Cx$ 补全。\n'
qh=qh.replace('modify: 2026-10-01','modify: 2026-10-07')
ah=ah[:ah.index('> [!abstract]')]+'> [!abstract] 答案与解析\n> 本专题 31 题按原书十个题型保留，每题附题设、原图及必要推导。题号可直达；原题与原答案的差异随题注明。\n> 本轮重点修正电路与框图列式、状态转移矩阵题设逆号、观测器精确增益、约当变换与离散输入矩阵，并补齐 1-25 的传递函数和模态归属。\n\n'
ah=ah.replace('modify: 2026-10-01','modify: 2026-10-07')
def nav(kind):
    s='## 🔎 题号直达\n\n| 题号范围 | 直达'+kind+' |\n| :-- | :-- |\n'
    for k in range(1,32,5):
        stop=min(k+4,31); links=' · '.join(f'[[#✏️ 1-{i}　{kind}\\|1-{i}]]' for i in range(k,stop+1))
        s+=f'| 1-{k}～1-{stop} | {links} |\n'
    return s+'\n'
# Keep original topic heading after inserting navigation.
qh=qh.replace('## 【题型1】',nav('题目')+'## 【题型1】')
summaries=[
'两状态电路；$\\dot x_2=(-x_1-R_1x_2+u_1-u_2)/L$',
'双质量系统；$B_2$ 作用在 $M_2$，方程见解析',
'输入为电流源；输出 $y=R_3(x_1+x_2)$',
'四状态、双输入；输出为两质量块的速度',
'四阶模型完全能控且能观；可用全维观测器重构',
'三积分器模型，$A$ 为上三角阵；$y=x_1+du$',
'极点 $-2$、$(-3\\pm\\mathrm j\\sqrt7)/2$（按原题正增益支路）',
'$G(s)=\\frac{s+1}{s^3+2s^2+4s-1}$；不是 BIBO 稳定',
'$W(s)=\\frac{s^3+5s^2+7s+3}{s^4+5s^3+10s^2+10s+2}$',
'$W(s)=\\frac2{s^3-7s-6}$；存在极点 $3$，不渐近稳定',
'$W(s)=\\frac{3s-1}{s(s-1)(s-2)}$；完全能控、完全能观',
'特征值 $-1,-2$；不完全能控、完全能观',
'$G(s)=2+\\frac1{(s+1)(s+6)}$；最小阶数 $2$',
'三阶实现非最小；最小传函 $1/[(s+1)(s+3)]$',
'按三阶实现理解，$a=1$ 或 $2$ 时非最小',
'对角阵 $A=\\mathrm{diag}(-4,-1,-2)$；指数逐项求',
'完全能控、完全能观；$y(t)=9e^{-2t}-6e^{-3t}$',
'完全能控；二阶状态转移矩阵见解析',
'不渐近稳定但 BIBO 稳定；$G(s)=1/(s+3)$',
'$B=[1,-1]^T$，能控秩 $1$',
'不渐近稳定且不 BIBO 稳定；$y(t)=(e^{2t}-e^{-t})/3$',
'完全能观当且仅当 $\\rho\\ne0$；$y(3)=1-6e^{-3}$',
'$h=[5.990888,2.9892,-1.99]^T$，精确满足题给极点',
'取 $u=v-Kx$，$K=[9,4]$',
'$h=[\\frac{17}{2},-\\frac12]^T$；$G_{vy}=1/(s+1)$；$-3,-4,-5$ 不可控，全模态可观',
'直通项 $D=1$；对角极点 $-1,-3$',
'$G(s)=\\frac{2s+1}{(s+1)(s+2)}$；三种标准型见解析',
'$-1$ 二阶约当块与 $-2$ 一阶块；变换方向 $x=T\\bar x$',
'$G=e^A$；$H=[(1-e^{-2})/2,0,0,0]^T$',
'令 $q=e^{-1/10}$，$H=[-(1-q)^2,(3-4q+q^2)/2]^T$',
'与 1-30 同题，保留完整结果；$H$ 第一分量非零']
ah+=nav('解析')+'## 答案速查\n\n| 题号 | 结论与关键结果 |\n| :-- | :-- |\n'
for n,txt in enumerate(summaries,1): ah+=f'| [[#✏️ 1-{n}　解析\\|1-{n}]] | {txt} |\n'
ah+='\n## 【题型1】数学建模列写状态空间表达式\n\n'
qout=qh; aout=ah
for n in range(1,32):
    old,s,tail=qs[n]; label=old[old.index('（'):].removesuffix('**')
    qout+=f'#### ✏️ 1-{n}　题目\n\n[[{base}（答案与解析）#✏️ 1-{n}　解析|查看解析]] · [[#🔎 题号直达|返回题号导航]]\n\n'+label+s+tail
    imgs=re.findall(r'^!\[\[.*?\]\]$',s,re.M)
    stmt=re.sub(r'^!\[\[.*?\]\]\n?','',s,flags=re.M).strip()
    # Avoid nested original callouts inside the folded statement.
    stmt=re.sub(r'^> \[!\w+\].*\n','',stmt,flags=re.M);stmt=re.sub(r'^> ?', '',stmt,flags=re.M)
    statement=label+'\n\n'+stmt
    callout='> [!note]- 本题题设\n'+'\n'.join('> '+ln if ln else '>' for ln in statement.splitlines())
    content=ans[n][1].strip(); end=ans[n][2]
    if n==16: end=''
    if n==31: end=''
    aout+=f'#### ✏️ 1-{n}　解析\n\n[[{base}（题目）#✏️ 1-{n}　题目|原题]] · [[#🔎 题号直达|返回题号导航]]\n\n'+callout+'\n\n'+'\n\n'.join(imgs)+ ('\n\n' if imgs else '')+content+'\n\n'+end
for p,t in [(qp,qout),(ap,aout)]:
    t=t.replace('|330]]','|430]]')
    p.write_bytes(t.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
print('written',len(qout.splitlines()),len(aout.splitlines()))

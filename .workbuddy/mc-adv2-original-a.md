---
create: 2026-10-01
modify: 2026-10-01
tags:
  - 777习题集
  - 考研真题
  - 现代控制理论
book: 现控200题强化
chapter: 2
type: exam-solutions
---

> 返回：[[777习题集目录]] ｜ 题目：[[现控200题强化 专题二 线性系统的能控能观性及稳定性分析（题目）]] ｜ 勘误：[[777习题集官方勘误摘录]]

# 现控200题强化 专题二 线性系统的能控能观性及稳定性分析（答案与解析）

> [!abstract] 答案与解析
> 本专题 29 题（2-1—2-29）的答案与解析，按题号连续排列。原书答案册（现控册）只给**考点**与**本题总结**、不标难度星级，本页一并保留（总结按库内口径压缩为一两句）。
>
> **本页已录 2-1—2-29 全部 29 题**（题型 1—7）。

> **本批落实的官方勘误与复算发现（均经 sympy 复算确认）**：
> **2-8**（题面，$x_2$ 的一阶导）——原书 $\Sigma_2$ 左端印 $\dot x_1$，题目页已按勘误改 $\dot x_2$，本页解析按 $\dot x_2=-2x_2+u_2$ 进行。
> **2-13**（改图，题面补控制律）——原书（3）只写 $u=k_1x_1+k_2x_2$，官方勘误图补为 $u=v+k_1x_1+k_2x_2$（正反馈约定），与答案册 $A+bK$ 的解法配套（题目页已落实）。
> **2-14**（改图）——原书 $V$ 的第三行 $CA^2$ 印 $[-2,-3,-4]$，复算应为 $[-2,3,-4]$（照原书则 $\det V\ne0$，与 $\mathrm{rank}\,V=2$ 矛盾）；官方勘误图改用 $V=\begin{bmatrix}c\\cA\end{bmatrix}$ 判别，本页按勘误转写。
> **2-20**（改图）——原书 $\Phi(t)$ 的 $(2,2)$ 元印 $e^{-t}$、$x(t)$ 第二分量为 $\frac12+e^{-t}+\frac12e^{-2t}$，官方勘误图（红框）更正为 $e^{-2t}$ 与 $\frac12-e^{-t}+\frac52e^{-2t}$，复算确认，本页按勘误转写。
> **2-28**（BIBO 结论）——官方勘误把 $G$ 的印刷误 $1/(s^2(s+1))$ 更正为 $1/(s(s+1))$（复算成立），但随之把结论翻转为「是 BIBO 稳定」——复算**不支持**：$G=\frac1{s(s+1)}$ 含 $s=0$ 极点，阶跃输入下输出无界。本页维持原书「不是 BIBO 系统」的结论（详见 2-28 的 ⚠️）。
>
> 全批矩阵结论均经 sympy/numpy 独立复算（`_verify_xq2.py`，80 项全过；见各题尾注与文末录入说明）。

## 答案速查

| 题号 | 答案 | 题号 | 答案 |
| :-- | :-- | :-- | :-- |
| 2-1 | $\dot x=\begin{bmatrix}0&1&0\\-3&-4&0\\2&1&-2\end{bmatrix}x+\begin{bmatrix}0\\1\\0\end{bmatrix}u$，$y=[0\ \ 0\ \ 1]x$；rank $M=2$ 不能控、rank $N=3$ 能观；$W(s)=\frac{1}{(s+1)(s+3)}$ ⚠️ | 2-16 | $V=x_1^2+x_2^2$ 正定，$\dot V=-2\left[x_1^2+x_2^2+(x_1^2+x_2^2)^2\right]$ 负定，大范围渐近稳定 |
| 2-2 | 能控标准形实现；原书按 $u=v+Kx$ 得 $K=[-4\ \ -4\ \ -1]$（若按 $u=v-Kx$ 则 $K=[4\ \ 4\ \ 1]$，闭环极点相同） | 2-17 | $P=\begin{bmatrix}2.78&7.94\\7.94&95.07\end{bmatrix}$ 正定（原书 $(2,2)$ 元印 95.4），$x_e=0$ 大范围渐近稳定 |
| 2-3 | $\dot x=\begin{bmatrix}-2&3\\1&0\end{bmatrix}x+\begin{bmatrix}1\\1\end{bmatrix}u$，$y=[1\ \ 0]x$；不能控、能观；$W(s)=\frac{1}{s-1}$；$x(1)=[0.434\ \ 0.334]^T$ | 2-18 | $V=x_1^2+x_2^2$ 正定，$\dot V=-2(x_1^2+x_2^2)^2$ 负定，大范围渐近稳定 |
| 2-4 | 能控：$a\ne0$ 且 $a\ne3$；能观：$a\ne1$；$W(s)=\frac{s+1-a}{(s-2)\left[(s+1)^2-a\right]}$，$a=0,3$ 不能控、$a=1$ 不能观处均出现零极点对消 | 2-19 | $A=\cfrac{\partial f}{\partial x}\Big|_{0}=\begin{bmatrix}1&-3\\2&3\end{bmatrix}$，$\lambda=2\pm\sqrt5\,\mathrm j$ 有正实部，不稳定 |
| 2-5 | 对任何 $b$ 均不能控（$\det M\equiv 0$） | 2-20 | $x(t)=\begin{bmatrix}1-e^{-t}\\[2pt]\frac12-e^{-t}+\frac52e^{-2t}\end{bmatrix}$ ⚠️；$P=\begin{bmatrix}\frac{7}{12}&\frac{1}{12}\\[2pt]\frac{1}{12}&\frac14\end{bmatrix}$ 正定渐近稳定；$K=[-1\ \ 2]$ ⚠️图 |
| 2-6 | 不稳定、能控、能观；$K=[5\ \ \frac{13}{2}]$；$\frac{Y(s)}{V(s)}=\frac{s+1}{(s+2)(s+4)}$，稳态输出 $=$ 稳态增益 $=\frac18$；取 $\beta=8$ | 2-21 | $e^{At}=\begin{bmatrix}2e^{-t}-e^{-2t}&e^{-t}-e^{-2t}\\2e^{-2t}-2e^{-t}&2e^{-2t}-e^{-t}\end{bmatrix}$；$P=\begin{bmatrix}1.25&0.25\\0.25&0.25\end{bmatrix}$ 正定，大范围渐近稳定 |
| 2-7 | rank $M=2$ 不可控；$\lambda=1,1,-1$ 不渐近稳定；$\lambda=1$ 不可控且不稳定 ⇒ 不可镇定 | 2-22 | 平衡点 $(0,0)$；$V=x_1^4+2x_2^2$，$\dot V=-4x_2^2$，大范围渐近稳定 |
| 2-8 | $\Sigma_1$、$\Sigma_2$ 均能控能观；串联后不能控、能观；$W(s)=\frac{1}{(s+1)(s+3)}$ 存在 $(s+2)$ 对消 | 2-23 | $x_{e1}=(-2,1)$ 处 $\lambda=\frac{-1\pm\sqrt7\,\mathrm j}{2}$ 渐近稳定；$x_{e2}=(0,-1)$ 处 $\lambda=1,-2$ 不稳定 |
| 2-9 | 闭环 $W(s)=\frac{s}{(s+1)^2}$；能控（rank $S=3$）；闭环不能观（rank $Q=2$） | 2-24 | $P=\mathrm{diag}\left(\frac43,-\frac13\right)$ 不正定，不渐近稳定；$x(1)=[\frac32\ \ 3]^T$，$x(2)=[\frac74\ \ -5]^T$ |
| 2-10 | rank $Q_c=2<3$ 不完全能控；$\bar A=\begin{bmatrix}1&0&2\\1&2&-2\\0&0&3\end{bmatrix}$、$\bar B=\begin{bmatrix}1&0\\0&1\\0&0\end{bmatrix}$；不能控子系统 $\lambda=3>0$ ⇒ 不能镇定 | 2-25 | $x_e=0$（唯一）；$P=\frac43E$ 正定，大范围渐近稳定 |
| 2-11 | $\dot x=\begin{bmatrix}-0.38&0\\0&-2.62\end{bmatrix}x+\begin{bmatrix}1\\1\end{bmatrix}u$，$y=[0.45\ \ -0.45]x$（约当/对角型实现） | 2-26 | $e^{At}=\begin{bmatrix}\cos2t&\frac12\sin2t\\-2\sin2t&\cos2t\end{bmatrix}$；能控；$G=e^{AT}$、$H=\begin{bmatrix}-\frac12\cos2T+\frac12\\ \sin2T\end{bmatrix}$；$T\ne\frac{k\pi}{2}$ 时离散化后仍完全能控 |
| 2-12 | $\Phi(t)=\begin{bmatrix}2e^{-t}-e^{-2t}&e^{-t}-e^{-2t}\\2e^{-2t}-2e^{-t}&2e^{-2t}-e^{-t}\end{bmatrix}$；$a\ne1,\frac12$；能观Ⅱ型 $\dot x=\begin{bmatrix}0&-2\\1&-3\end{bmatrix}x+\begin{bmatrix}1\\a\end{bmatrix}u$，$y=[0\ \ 1]x$；$P=\begin{bmatrix}\frac54&\frac14\\[2pt]\frac14&\frac14\end{bmatrix}$ 渐近稳定 | 2-27 | $\lambda=-1,\pm2$ 不渐近稳定；$W(s)=\frac{2(s-2m)}{(s+2)(s-2)}$，$m=1$ 时对消不稳定极点，$W=\frac{2}{s+2}$ BIBO 稳定 |
| 2-13 | $W(s)=\frac{s+1}{s^2+s-1}$；能控Ⅰ型 $\bar A=\begin{bmatrix}0&1\\1&-1\end{bmatrix}$、$\bar c=[1\ \ 1]$；$u=v+k_1x_1+k_2x_2$ 口径下 $k_1=-3$、$k_2=2$ | 2-28 | 三阶口径 $G(s)=\frac{s-1}{s(s+1)(s-1)}=\frac{1}{s(s+1)}$；实现特征值 $0,\pm1$ 不稳定；极点含 $0$ ⇒ **不是 BIBO 系统** ⚠️；最小实现 $\dot x=\begin{bmatrix}0&1\\0&-1\end{bmatrix}x+\begin{bmatrix}0\\1\end{bmatrix}u$，$y=[1\ \ 0]x$ |
| 2-14 | 不可控（rank $S=2$）、不可观测（rank $V=2$）；可控/可观分解见正文 ⚠️ | 2-29 | $x_e=0$；$P=\begin{bmatrix}\frac34&-\frac14\\[2pt]-\frac14&-\frac14\end{bmatrix}$ 不定 ⇒ 不稳定；$G(s)=\frac{1}{s+1}$ BIBO 稳定；$K=[11\ \ 7]$ |
| 2-15 | 与 2-14 同一系统；$T_c$ 分解后能控子系统 $\dot{\hat x}_1=\begin{bmatrix}0&-1\\1&-2\end{bmatrix}\hat x_1+\begin{bmatrix}-1\\-2\end{bmatrix}\bar x+\begin{bmatrix}1\\0\end{bmatrix}u$，$y_1=[1\ \ -1]\hat x_1$ | — | — |

## 【题型1】能控性与能观性的判别

**2-1　答案**（考点：①串联组合子系统的状态空间表达式；②能控秩判据与能观秩判据；③串联组合子系统的传递函数）

（1）串联时 $u_1=u$、$u_2=y_1=c_1^Tx_1$、$y=y_2=c_2x_2$，按串联公式

$$
\begin{bmatrix}\dot x_1\\\dot x_2\end{bmatrix}=\begin{bmatrix}A_1&0\\b_2c_1^T&A_2\end{bmatrix}\begin{bmatrix}x_1\\x_2\end{bmatrix}+\begin{bmatrix}b_1\\0\end{bmatrix}u_1
$$

代入数据：

$$
\dot x=\begin{bmatrix}0&1&0\\-3&-4&0\\2&1&-2\end{bmatrix}x+\begin{bmatrix}0\\1\\0\end{bmatrix}u,\qquad y=[0\ \ 0\ \ 1]x
$$

（2）能控性判别矩阵：

$$
M=[b\ \ Ab\ \ A^2b]=\begin{bmatrix}0&1&-4\\1&-4&13\\0&1&-4\end{bmatrix}
$$

> [!warning] ⚠️ 复算提示
> 原书 $A^2b$ 的中间元印 $3$，复算为 $13$（$A^2b=[-4\ \ 13\ \ -4]^T$）。第一行与第三行相同，$\mathrm{rank}\,M=2<3$，**串联系统不能控**的结论不受影响。

能观性判别矩阵：

$$
N=\begin{bmatrix}c\\cA\\cA^2\end{bmatrix}=\begin{bmatrix}0&0&1\\2&1&-2\\-7&-4&4\end{bmatrix},\qquad \mathrm{rank}\,N=3
$$

故串联系统**不能控、能观测**。

（3）子系统传递函数：

$$
W_1(s)=c_1^T(sI-A_1)^{-1}b_1=\frac{s+2}{(s+1)(s+3)},\qquad W_2(s)=c_2(sI-A_2)^{-1}b_2=\frac{1}{s+2}
$$

$$
W(s)=W_1(s)W_2(s)=\frac{1}{(s+1)(s+3)}
$$

$W_1$ 的零点 $s=-2$ 与 $W_2$ 的极点相消，与「不能控」相互印证。

> [!note] 本题总结
> 串联组合按 $\begin{bmatrix}A_1&0\\b_2c_1^T&A_2\end{bmatrix}$ 拼装；传递函数出现零极点对消时，串联系统必然不完全能控或不完全能观。

**2-2　答案**（考点：状态反馈极点配置）

把 $W(s)=\dfrac{10}{s(s+1)(s+2)}=\dfrac{10}{s^3+3s^2+2s}$ 写成能控标准形：

$$
\dot x=\begin{bmatrix}0&1&0\\0&0&1\\0&-2&-3\end{bmatrix}x+\begin{bmatrix}0\\0\\1\end{bmatrix}u,\qquad y=[10\ \ 0\ \ 0]x
$$

$\mathrm{rank}\,U_c=3=n$，完全能控，可任意配置极点。设 $K=[k_1\ \ k_2\ \ k_3]$，期望特征多项式

$$
f^*(\lambda)=(\lambda+2)(\lambda+1-\mathrm j)(\lambda+1+\mathrm j)=\lambda^3+4\lambda^2+6\lambda+4
$$

原书取闭环 $\lambda I-(A+bK)$（即 $u=v+Kx$ 的正反馈口径）：

$$
f(\lambda)=\lambda^3+(3-k_3)\lambda^2+(2-k_2)\lambda-k_1
$$

对比系数得 $3-k_3=4$、$2-k_2=6$、$-k_1=4$，即

$$
K=[-4\ \ -4\ \ -1]
$$

> [!note] 两种符号口径
> 原书按 $u=v+Kx$（闭环 $A+bK$）解得 $K=[-4\ \ -4\ \ -1]$；若按本库常规口径 $u=v-Kx$（闭环 $A-bK$），同一组期望极点解得 $K=[4\ \ 4\ \ 1]$，两者只差一个正负号，闭环极点同为 $-1\pm\mathrm j,-2$。

> [!note] 本题总结
> 极点配置三步：能控标准形（或直接算 $A-bK$ 特征式）→ 写期望特征多项式 → 对比系数解 $K$。

**2-3　答案**（考点：①能控性秩判据与能观性秩判据；②公式法求传递函数；③非齐次状态方程的输出响应）

（1）由结构图：主综合点输出 $\frac{1}{s+2}$ 的输入为 $u+3x_2$，即 $sX_1=U+3X_2-2X_1$；右综合点输出为 $\frac1s$ 的输入 $x_1+u$，即 $sX_2=X_1+U$。于是

$$
\dot x=\begin{bmatrix}-2&3\\1&0\end{bmatrix}x+\begin{bmatrix}1\\1\end{bmatrix}u,\qquad y=[1\ \ 0]x
$$

能控性：

$$
M=[b\ \ Ab]=\begin{bmatrix}1&1\\1&1\end{bmatrix},\qquad \mathrm{rank}\,M=1<2
$$

不能控。能观性：

$$
N=\begin{bmatrix}c\\cA\end{bmatrix}=\begin{bmatrix}1&0\\-2&3\end{bmatrix},\qquad \mathrm{rank}\,N=2
$$

能观测。

（2）$\det(sI-A)=s^2+2s-3=(s-1)(s+3)$，

$$
W(s)=c(sI-A)^{-1}b=\frac{s+3}{(s-1)(s+3)}=\frac{1}{s-1}
$$

（3）$A$ 的特征值为 $1,-3$，

$$
\Phi(t)=e^{At}=\begin{bmatrix}\frac14e^{t}+\frac34e^{-3t}&\frac34e^{t}-\frac34e^{-3t}\\[4pt]\frac14e^{t}-\frac14e^{-3t}&\frac34e^{t}+\frac14e^{-3t}\end{bmatrix}
$$

$x(t)=\Phi(t)x_0+\displaystyle\int_0^t\Phi(t-\tau)bu(\tau)\,\mathrm d\tau$，其中积分项 $=A^{-1}\left(\Phi(t)-E\right)b=[e^t-1\ \ e^t-1]^T$，故

$$
x(t)=\begin{bmatrix}\frac12e^{t}+\frac32e^{-3t}-1\\[4pt]\frac12e^{t}-\frac12e^{-3t}-1\end{bmatrix},\qquad x(1)=\begin{bmatrix}0.434\\0.334\end{bmatrix}
$$

输出值 $y(1)=x_1(1)=0.434$。

> [!note] 本题总结
> 结构图列状态方程要盯住每个综合点的输入代数和；非齐次定常方程可用 $x(t)=\Phi(t)x_0+A^{-1}(\Phi(t)-E)bu$（$u$ 为常值）直接算。

**2-4　答案**（考点：①能控性秩判据与能观性秩判据；②传递函数与能控性、能观性的关系）

（1）能控性判别矩阵：

$$
M=[b\ \ Ab\ \ A^2b]=\begin{bmatrix}0&1&1-a\\0&a&-2a\\1&-1&a+1\end{bmatrix},\qquad |M|=a^2-3a
$$

完全能控要求 $a^2-3a\ne0$，即 $a\ne0$ 且 $a\ne3$。

能观性判别矩阵：

$$
N=\begin{bmatrix}c\\cA\\cA^2\end{bmatrix}=\begin{bmatrix}1&0&0\\2&-1&1\\4&0&1-a\end{bmatrix},\qquad |N|=a-1
$$

完全能观要求 $a\ne1$。故**完全能控能观：$a\ne0$ 且 $a\ne1$ 且 $a\ne3$**。

（2）传递函数：

$$
W(s)=c(sI-A)^{-1}b=\frac{s+1-a}{(s-2)\left[(s+1)^2-a\right]}
$$

- $a=0$：$W(s)=\dfrac{s+1}{(s-2)(s+1)^2}$，出现 $(s+1)$ 对消 ⇒ 不能控；
- $a=3$：$W(s)=\dfrac{s-2}{(s-2)\left[(s+1)^2-3\right]}$，出现 $(s-2)$ 对消 ⇒ 不能控；
- $a=1$：$W(s)=\dfrac{s}{(s-2)(s+2)s}$，出现 $s$ 对消 ⇒ 不能观。

> [!note] 本题总结
> 单输入单输出系统完全能控且完全能观的充要条件是传递函数无零极点对消；参数扫描型题目把「判据行列式为零的参数值」与「对消发生的参数值」一一对应验证。

**2-5　答案**（考点：能控性秩判据）

设 $b=[b_1\ \ b_2\ \ b_3]^T$，则

$$
Ab=\begin{bmatrix}\lambda b_1\\\lambda b_2+b_3\\\lambda b_3\end{bmatrix},\qquad A^2b=\begin{bmatrix}\lambda^2b_1\\\lambda^2b_2+2\lambda b_3\\\lambda^2b_3\end{bmatrix}
$$

对 $M=[b\ \ Ab\ \ A^2b]$ 做列变换：第 2 列减 $\lambda$ 倍第 1 列得 $[0\ \ b_3\ \ 0]^T$，第 3 列减 $\lambda$ 倍第 2 列得 $[0\ \ \lambda b_3\ \ 0]^T$（又 $\lambda\ne0$，可再约出 $[0\ \ b_3\ \ 0]^T$）：

$$
M\sim\begin{bmatrix}b_1&0&0\\b_2&b_3&b_3\\b_3&0&0\end{bmatrix}
$$

第 2、3 列相同，$\det M\equiv0$（复算确认对任意 $b$ 恒成立），$\mathrm{rank}\,M\le2<3$。

**不论如何选取 $b$，系统都不能控。** 理由：$A$ 的约当标准形中特征值 $\lambda$ 对应两个约当块（一个 2 阶、一个 1 阶），重根 $\lambda$ 有两个约当块而输入只有一个，无法同时"接通"两个块。

> [!note] 本题总结
> 同一特征值多个约当块 + 单输入 ⇒ 该特征值方向必然不能控；列变换把 $M$ 化成显式奇异性是书面证明的标准做法。

**2-6　答案**（考点：①能控性秩判据与能观性秩判据；②李二法；③状态反馈极点配置；④闭环传递函数求取）

（1）$M=[b\ \ Ab]=\begin{bmatrix}1&0\\0&2\end{bmatrix}$、$N=\begin{bmatrix}c\\cA\end{bmatrix}=\begin{bmatrix}1&0\\0&5\end{bmatrix}$ 均满秩，能控且能观。

李雅普诺夫方程 $A^TP+PA=-I$，取 $P=\begin{bmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{bmatrix}$：

$$
\begin{bmatrix}4p_{12}&5p_{11}-p_{12}+2p_{22}\\5p_{11}-p_{12}+2p_{22}&10p_{12}-2p_{22}\end{bmatrix}=\begin{bmatrix}-1&0\\0&-1\end{bmatrix}
$$

即

$$
4p_{12}=-1,\quad 5p_{11}-p_{12}+2p_{22}=0,\quad 10p_{12}-2p_{22}=-1
$$

解得 $p_{11}=\frac14$、$p_{12}=-\frac14$、$p_{22}=-\frac34$：

$$
P=\begin{bmatrix}\frac14&-\frac14\\[2pt]-\frac14&-\frac34\end{bmatrix},\qquad \Delta_1=\frac14>0,\quad \Delta_2=-\frac14<0
$$

$P$ 不正定，**系统在原点处不稳定**（特征值 $\frac{-1\pm\sqrt{41}}{2}$ 确有一个正根）。

（2）设 $K=[K_0\ \ K_1]$，$u=v-Kx$：

$$
|\lambda I-(A-bK)|=\lambda^2+(K_0+1)\lambda+K_0+2K_1-10
$$

期望 $(\lambda+2)(\lambda+4)=\lambda^2+6\lambda+8$，解得

$$
K=\begin{bmatrix}5&\dfrac{13}{2}\end{bmatrix}
$$

（3）此时 $A-bK=\begin{bmatrix}-5&-\frac32\\2&-1\end{bmatrix}$，

$$
\frac{Y(s)}{V(s)}=c[sI-(A-bK)]^{-1}b=\frac{s+1}{(s+2)(s+4)}
$$

$v(t)=1(t)$ 时 $Y(s)=\dfrac{s+1}{s(s+2)(s+4)}=\dfrac18\cdot\dfrac1s+\dfrac14\cdot\dfrac1{s+2}-\dfrac38\cdot\dfrac1{s+4}$：

$$
y(t)=\frac18+\frac14e^{-2t}-\frac38e^{-4t}
$$

闭环稳态输出 $y(\infty)=\dfrac18$，稳态增益 $=\dfrac{Y(s)}{V(s)}\Big|_{s=0}=\dfrac18$。

（4）改用 $u=\beta v-Kx$（即输入通道增益 $\beta$），则 $\dfrac{Y(s)}{V(s)}=\dfrac{\beta(s+1)}{(s+2)(s+4)}$，稳态增益 $\dfrac{\beta}{8}=1$，取

$$
\beta=8
$$

> [!note] 本题总结
> 李二法判稳不满秩正定时结论是"不稳定"而非"不确定"时，可用特征值直接佐证；非零稳态误差用输入通道增益 $\beta$ 补偿，$\beta=1/(\text{稳态增益})$。

**2-7　答案**（考点：①能控性秩判据；②渐近稳定判据；③可镇定性）

（1）能控性判别矩阵：

$$
M=[B\ \ AB\ \ A^2B]=\begin{bmatrix}1&0&-1&0&1&0\\1&2&3&2&1&2\\1&0&-1&0&1&0\end{bmatrix}
$$

第一行与第三行相同，$\mathrm{rank}\,M=2<3$，**系统不完全能控**。

（2）特征多项式：

$$
\det(\lambda I-A)=(\lambda-1)^2(\lambda+1)
$$

特征值 $\lambda_{1,2}=1$、$\lambda_3=-1$，有正实部特征值，**系统不是渐近稳定的**。

（3）判可镇定：对不稳定特征值 $\lambda=1$ 检验

$$
\mathrm{rank}\,[\lambda I-A\ \ B]=\mathrm{rank}\begin{bmatrix}1&0&1&1&0\\-1&0&-1&1&2\\1&0&1&1&0\end{bmatrix}=2<3
$$

$\lambda=1$ 不可控且不稳定，**系统不可镇定**。

> [!note] 本题总结
> 可镇定 ⇔ 所有不稳定特征值都可控（$\mathrm{rank}[\lambda I-A\ \ B]=n$ 对每个 $\mathrm{Re}\,\lambda\ge0$ 成立）；不可控子系统的特征值全部在左半平面才行。

**2-8　答案**（考点：①子系统能控能观判别；②串联组合的能控能观；③传递函数判别法）

（1）$\Sigma_1$：$M_1=[b_1\ \ A_1b_1]=\begin{bmatrix}0&1\\1&-4\end{bmatrix}$，$|M_1|=-1\ne0$ 能控；$N_1=\begin{bmatrix}c_1\\c_1A_1\end{bmatrix}=\begin{bmatrix}2&1\\-3&-2\end{bmatrix}$，$|N_1|=-1\ne0$ 能观。$\Sigma_2$ 为一阶系统，$b_2=1\ne0$、$c_2=1\ne0$，能控且能观。

（2）串联（$\Sigma_1$ 在前、$y_1=u_2$）后的组合系统与 2-1 相同：

$$
\dot x=\begin{bmatrix}0&1&0\\-3&-4&0\\2&1&-2\end{bmatrix}x+\begin{bmatrix}0\\1\\0\end{bmatrix}u,\qquad y=[0\ \ 0\ \ 1]x
$$

$$
\mathrm{rank}\,M=2<3\ \text{不能控}，\qquad \mathrm{rank}\,N=3\ \text{能观测}
$$

（3）用传递函数分析：

$$
W_1(s)=\frac{s+2}{(s+1)(s+3)},\qquad W_2(s)=\frac{1}{s+2},\qquad W(s)=W_1(s)W_2(s)=\frac{1}{(s+1)(s+3)}
$$

串联后传递函数出现 $(s+2)$ 的零极点对消，**不满足既能控又能观**（与（2）"不能控但能观"一致）。

> [!note] 本题总结
> 传递函数出现零极点对消 ⇒ 串联系统不能控（零点在公子系统）或不能观；本例对消发生在前一个子系统的零点与后一个子系统的极点之间，故不能控。

**2-9　答案**（考点：①能控性秩判据、能观性秩判据；②状态反馈极点配置；③公式法求传递函数）

取状态反馈控制律 $u=v-Kx$（$K=[1\ \ 1\ \ 3]$），闭环系统矩阵：

$$
A-BK=\begin{bmatrix}0&1&0\\0&0&1\\0&-1&-2\end{bmatrix}
$$

闭环传递函数：

$$
W(s)=c[sI-(A-BK)]^{-1}b=\frac{s^2}{s(s+1)^2}=\frac{s}{(s+1)^2}
$$

能控性（状态反馈不改变能控性）：

$$
S=[b\ \ Ab\ \ A^2b]=\begin{bmatrix}0&0&1\\0&1&0\\1&0&0\end{bmatrix},\qquad \mathrm{rank}\,S=3
$$

完全能控。能观性（对闭环系统）：

$$
Q=\begin{bmatrix}c\\c(A-BK)\\c(A-BK)^2\end{bmatrix}=\begin{bmatrix}0&0&1\\0&-1&-2\\0&2&3\end{bmatrix},\qquad \mathrm{rank}\,Q=2<3
$$

**闭环系统不能观测**（状态反馈改变了 $cA^i$ 的行向量，可能破坏能观性——开环 $Q=[c;cA;cA^2]$ 满秩能观）。

> [!note] 本题总结
> 状态反馈不改变系统的能控性，但一般会改变能观性——本题闭环 $Q$ 的第一列全零。

**2-10　答案**（考点：①能控性结构分解；②状态反馈可镇定问题）

（1）能控性判别矩阵：

$$
Q_c=[B\ \ AB\ \ A^2B]=\begin{bmatrix}2&1&3&2&5&4\\1&1&2&2&4&4\\-1&-1&-2&-2&-4&-4\end{bmatrix},\qquad \mathrm{rank}\,Q_c=2<3
$$

（第三行 $=$ 负的第二行）系统不完全能控，按能控性分解。取 $Q_c$ 的两个线性无关列再补一列 $e_3$：

$$
P^{-1}=\begin{bmatrix}2&1&0\\1&1&0\\-1&-1&1\end{bmatrix},\qquad P=(P^{-1})^{-1}=\begin{bmatrix}1&-1&0\\-1&2&0\\0&1&1\end{bmatrix}
$$

$$
\bar A=PAP^{-1}=\begin{bmatrix}1&0&2\\1&2&-2\\0&0&3\end{bmatrix},\qquad \bar B=PB=\begin{bmatrix}1&0\\0&1\\0&0\end{bmatrix}
$$

即二维能控子系统 $\dot{\bar x}_c=\begin{bmatrix}1&0\\1&2\end{bmatrix}\bar x_c+\begin{bmatrix}2\\-2\end{bmatrix}x_3+\begin{bmatrix}1&0\\0&1\end{bmatrix}u$ 与一维不能控子系统 $\dot x_3=3x_3$。

（2）$A$ 的特征值为 $1,2,3$（互异），对应特征向量 $P_1=(1,0,0)^T$、$P_2=(1,1,-1)^T$、$P_3=(0,0,1)^T$，可对角化为 $\mathrm{diag}(1,2,3)$。不能控子系统的特征值为 $3>0$，位于右半平面，故**该系统不能通过状态反馈镇定**。

> [!note] 本题总结
> 能控性分解的变换矩阵取 $[Q_c\text{ 的无关列}|\text{补列}]$；可镇定性看**不能控子系统**的特征值是否全在左半平面。

**2-11　答案**（考点：既能控又能观的约当（对角）标准型实现）

$$
G(s)=\frac{1}{s^2+3s+1}=\frac{0.45}{s+0.38}-\frac{0.45}{s+2.62}
$$

（极点 $s_{1,2}=\frac{-3\pm\sqrt5}{2}\approx-0.38,-2.62$；留数 $\approx\pm0.45$。）

取状态变量 $x_1(s)=\dfrac{1}{s+0.38}u(s)$、$x_2(s)=\dfrac{1}{s+2.62}u(s)$，则

$$
\dot x=\begin{bmatrix}-0.38&0\\0&-2.62\end{bmatrix}x+\begin{bmatrix}1\\1\end{bmatrix}u,\qquad y=[0.45\ \ -0.45]x
$$

$B$ 无零行、$C$ 无零列，**既能控又能观**。

> [!note] 本题总结
> 单实极点对角型实现：留数法拆部分分式，$B$ 全 1、$C$ 取留数；能控能观 ⇔ 留数全非零。

**2-12　答案**（考点：①状态转移矩阵；②能观性参数条件；③能观规范形；④李二法）

（1）$\det(sI-A)=(s+1)(s+2)$，

$$
\Phi(t)=e^{At}=\mathcal L^{-1}\left[(sI-A)^{-1}\right]=\begin{bmatrix}2e^{-t}-e^{-2t}&e^{-t}-e^{-2t}\\2e^{-2t}-2e^{-t}&2e^{-2t}-e^{-t}\end{bmatrix}
$$

（2）能观性矩阵：

$$
N=\begin{bmatrix}c\\cA\end{bmatrix}=\begin{bmatrix}1&a\\-2a&1-3a\end{bmatrix},\qquad |N|=1-3a+2a^2=(2a-1)(a-1)
$$

$a\ne1$ 且 $a\ne\frac12$ 时满秩，故 $a\ne1$、$a\ne\frac12$。

（3）$W(s)=c(sI-A)^{-1}b=\dfrac{as+1}{s^2+3s+2}$，其能观标准Ⅱ型：

$$
\dot x=\begin{bmatrix}0&-2\\1&-3\end{bmatrix}x+\begin{bmatrix}1\\a\end{bmatrix}u,\qquad y=[0\ \ 1]x
$$

（4）李雅普诺夫方程 $A^TP+PA=-I$，解得

$$
P=\begin{bmatrix}\frac54&\frac14\\[2pt]\frac14&\frac14\end{bmatrix},\qquad \Delta_1=\frac54>0,\quad \Delta_2=\frac14>0
$$

$P$ 正定，系统在平衡状态处**渐近稳定**（特征值 $-1,-2$ 佐证）。

> [!note] 本题总结
> 能观Ⅱ型 = 能控Ⅰ型的对偶转置；李二法解出的 $P$ 与传递函数极点判稳互相印证。

**2-13　答案**（考点：①公式法求传递函数；②化能控标准Ⅰ型；③状态反馈极点配置）

（1）$\det(sI-A)=s^2+s-1$，

$$
W(s)=c(sI-A)^{-1}b=\frac{s+1}{s^2+s-1}
$$

（2）$M=[b\ \ Ab]=\begin{bmatrix}1&0\\1&-1\end{bmatrix}$ 满秩能控。$|\lambda I-A|=\lambda^2+\lambda-1$，即 $a_1=1$、$a_0=-1$；分子 $s+1$ 即 $b_1=1$、$b_0=1$。能控标准Ⅰ型：

$$
\bar A=\begin{bmatrix}0&1\\-a_0&-a_1\end{bmatrix}=\begin{bmatrix}0&1\\1&-1\end{bmatrix},\qquad \bar b=\begin{bmatrix}0\\1\end{bmatrix},\qquad \bar c=[b_0\ \ b_1]=[1\ \ 1]
$$

（3）按勘误口径 $u=v+k_1x_1+k_2x_2$，$A+bk=\begin{bmatrix}1+k_1&-1+k_2\\1+k_1&-2+k_2\end{bmatrix}$：

$$
f(\lambda)=|\lambda I-(A+bk)|=\lambda^2+(1-k_1-k_2)\lambda-1-k_1
$$

期望 $f^*(\lambda)=(\lambda+1-\mathrm j)(\lambda+1+\mathrm j)=\lambda^2+2\lambda+2$，对比系数：

$$
1-k_1-k_2=2,\qquad -1-k_1=2\ \Rightarrow\ k_1=-3,\ k_2=2
$$

> [!note] 本题总结
> 本题的 $A+bK$ 与 2-2 同为正反馈口径（勘误题面 $u=v+k_1x_1+k_2x_2$ 已挑明）；若换成 $u=v-Kx$ 口径，$K$ 取正负号相反的解。

**2-14　答案**（考点：能控性与能观性判别 + 可控/可观结构分解）

（1）能控性判别矩阵：

$$
S=[b\ \ Ab\ \ A^2b]=\begin{bmatrix}1&0&-1\\1&1&-3\\0&1&-2\end{bmatrix},\qquad \mathrm{rank}\,S=2<3
$$

不可控。能观性判别（按勘误图口径取 $V=\begin{bmatrix}c\\cA\end{bmatrix}$）：

$$
V=\begin{bmatrix}0&1&-2\\1&-2&3\end{bmatrix},\qquad \mathrm{rank}\,V=2<3
$$

不可观测。

> [!warning] ⚠️ 勘误 + 复算
> 原书判能观性时列了第三行 $cA^2=[-2\ \ -3\ \ -4]$，复算 $cA^2=[-2\ \ 3\ \ -4]$（照原书则 $\det V=12\ne0$，与其 $\mathrm{rank}\,V=2$ 自相矛盾）。官方勘误图直接改用 $V=[c;cA]$（秩已饱和），本页按勘误转写。

（2）可控性分解：取 $S$ 的两个无关列加补列，

$$
P^{-1}=\begin{bmatrix}1&0&0\\1&1&0\\0&1&1\end{bmatrix},\qquad P=\begin{bmatrix}1&0&0\\-1&1&0\\0&-1&1\end{bmatrix}
$$

$$
\bar A=PAP^{-1}=\begin{bmatrix}0&-1&-1\\1&-2&-2\\0&0&-1\end{bmatrix},\qquad \bar B=PB=\begin{bmatrix}1\\0\\0\end{bmatrix},\qquad \bar C=CP^{-1}=[1\ \ -1\ \ \vdots\ \ -2]
$$

可控子系统与不可控子系统：

$$
\dot x_c=\begin{bmatrix}0&-1\\1&-2\end{bmatrix}x_c+\begin{bmatrix}-1\\-2\end{bmatrix}x_{\bar c}+\begin{bmatrix}1\\0\end{bmatrix}u,\qquad y_1=[1\ \ -1]x_c
$$

$$
\dot x_{\bar c}=-x_{\bar c},\qquad y_2=-2x_{\bar c}
$$

可观性分解：取 $T=\begin{bmatrix}c\\cA\\e_1^T\end{bmatrix}=\begin{bmatrix}0&1&-2\\1&-2&3\\1&0&0\end{bmatrix}$，$T^{-1}=\begin{bmatrix}0&0&1\\-3&-2&2\\-2&-1&1\end{bmatrix}$：

$$
\bar A=TAT^{-1}=\begin{bmatrix}0&1&0\\-1&-2&0\\2&1&-1\end{bmatrix},\qquad \bar B=TB=\begin{bmatrix}1\\-1\\1\end{bmatrix},\qquad \bar C=CT^{-1}=[1\ \ 0\ \ 0]
$$

可观子系统与不可观子系统：

$$
\dot x_o=\begin{bmatrix}0&1\\-1&-2\end{bmatrix}x_o+\begin{bmatrix}1\\-1\end{bmatrix}u,\qquad y_1=[1\ \ 0]x_o
$$

$$
\dot x_{\bar o}=-x_{\bar o}+u+[2\ \ 1]x_o,\qquad y_2=0
$$

> [!warning] ⚠️ 复算提示
> 原书可观分解的 $\bar A$ 印 $\begin{bmatrix}0&3&0\\-1&-2&0\\2&1&-1\end{bmatrix}$，复算 $(1,2)$ 元应为 $1$（可观子系统 $\begin{bmatrix}0&1\\-1&-2\end{bmatrix}$，特征值 $-1$ 二重；原书的 $3$ 使其变成 $-1\pm\sqrt2\,\mathrm j$，渐近稳定的结论不受影响）。

> [!note] 本题总结
> 结构分解的变换矩阵按"判别矩阵无关行/列 + 补齐"拼装；可控与可观两个分解各自独立做，得到的是"可控性分解形式"与"可观性分解形式"两套坐标系（卡尔曼四分解需分解两次）。

**2-15　答案**（考点：线性定常连续系统的能控性分解）

与 2-14 为同一系统（$A$、$b$、$c$ 全同），$\gamma(Q_c)=2<3$ 不完全能控。取

$$
T_c=\begin{bmatrix}1&0&0\\1&1&0\\0&1&1\end{bmatrix},\qquad T_c^{-1}=\begin{bmatrix}1&0&0\\-1&1&0\\1&-1&1\end{bmatrix}
$$

$$
\tilde A=T_c^{-1}AT_c=\begin{bmatrix}0&-1&-1\\1&-2&-2\\0&0&-1\end{bmatrix},\qquad \tilde B=T_c^{-1}b=\begin{bmatrix}1\\0\\0\end{bmatrix},\qquad \tilde C=cT_c=[1\ \ -1\ \ -2]
$$

（2）能控子系统为

$$
\dot{\hat x}_1=\begin{bmatrix}0&-1\\1&-2\end{bmatrix}\hat x_1+\begin{bmatrix}-1\\-2\end{bmatrix}\bar x+\begin{bmatrix}1\\0\end{bmatrix}u(t),\qquad y_1=[1\ \ -1]\hat x_1
$$

不可控子系统：$\dot{\bar x}=-\bar x$，$y_2=-2\bar x$。

> [!note] 本题总结
> 与 2-14 同题（分标 2009 哈工程 810 / 2009 山东大学 847），$T_c$ 列序与 2-14 的 $P^{-1}$ 一致；能控子系统的 $y_1$ 只取 $\tilde C$ 的前两元。

## 【题型4】李雅普诺夫判稳方法

**2-16　答案**（考点：非线性系统的能量函数法（即李二法））

令 $\dot x_1=\dot x_2=0$ 解得唯一平衡点 $(0,0)$。取

$$
V(x)=x_1^2+x_2^2
$$

$V(x)$ 正定，且

$$
\dot V(x)=2x_1\dot x_1+2x_2\dot x_2=-2\left[x_1^2+x_2^2+\left(x_1^2+x_2^2\right)^2\right]
$$

$\dot V(x)$ 负定；又 $\|\boldsymbol x\|\to\infty$ 时 $V(x)\to\infty$，故系统在 $(0,0)$ 处**大范围渐近稳定**。

> [!note] 本题总结
> 径向对称的非线性阻尼系统选 $V=\|\boldsymbol x\|^2$，$\dot V$ 会自动配方成 $-r^2-r^4$ 型负定函数。

**2-17　答案**（考点：线性定常离散系统的李雅普诺夫方程法（即李二法））

取 $Q=I$，$P=\begin{bmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{bmatrix}$，由 $G^TPG-P=-Q$ 解得

$$
P=\begin{bmatrix}2.78&7.94\\7.94&95.07\end{bmatrix}
$$

> [!warning] ⚠️ 复算提示
> 原书 $P$ 的 $(2,2)$ 元印 $95.4$，复算精确值为 $\frac{1138}{63}\approx95.07$（解方程 $-0.36p_{11}=-1$、$0.8p_{11}-0.28p_{12}=0$、$p_{11}+1.8p_{12}-0.19p_{22}=-1$）。顺序主子式 $\Delta_1>0$、$\Delta_2>0$ 的结论不变。

$P$ 正定，系统在平衡状态 $x_e=0$ 处**大范围渐近稳定**。

> [!note] 本题总结
> 离散李雅普诺夫方程是 $G^TPG-P=-Q$（连续系统是 $A^TP+PA=-Q$，别混）；特征值 $0.8,0.9$ 均在单位圆内，与结论一致。

**2-18　答案**（考点：非线性系统的能量函数法（即李二法））

令 $\dot x_1=\dot x_2=0$，$(x_1,x_2)=(0,0)$ 为系统唯一平衡点。取

$$
V(x)=x_1^2+x_2^2
$$

$V(x)$ 正定，且

$$
\dot V(x)=2x_1\left[x_2-x_1\left(x_1^2+x_2^2\right)\right]+2x_2\left[-x_1-x_2\left(x_1^2+x_2^2\right)\right]=-2\left(x_1^2+x_2^2\right)^2
$$

$\dot V(x)$ 负定；又 $\|\boldsymbol x\|\to\infty$ 时 $V(x)\to\infty$，故系统在原点处**大范围渐近稳定**。

> [!note] 本题总结
> 与 2-16 同型：交叉项 $2x_1x_2-2x_1x_2$ 抵消后剩纯 $-r^4$ 型负定项。

**2-19　答案**（考点：非线性系统的李一法）

$$
\frac{\partial f}{\partial x}=\begin{bmatrix}\dfrac{\partial f_1}{\partial x_1}&\dfrac{\partial f_1}{\partial x_2}\\[6pt]\dfrac{\partial f_2}{\partial x_1}&\dfrac{\partial f_2}{\partial x_2}\end{bmatrix}=\begin{bmatrix}1&1-4\cos x_2\\3-e^{x_1}&3\end{bmatrix}
$$

在平衡点 $X=0$ 处线性化：

$$
A=\frac{\partial f}{\partial x}\bigg|_{X=0}=\begin{bmatrix}1&-3\\2&3\end{bmatrix}
$$

特征方程 $\lambda^2-4\lambda+9=0$，得 $\lambda_{1,2}=2\pm\sqrt5\,\mathrm j$，实部为正。并非所有特征值均具有负实部，**系统在平衡点 $X=0$ 处不稳定**。

> [!note] 本题总结
> 李一法：平衡点处泰勒展开取雅可比矩阵 $A$，按 $\mathrm{Re}\,\lambda_i$ 判线性化系统，进而下非线性系统的结论（负实部⇒渐近稳定；有正实部⇒不稳定；临界情形不能下结论）。

**2-20　答案**（考点：①非齐次状态方程的状态响应；②李雅普诺夫方程法（李二法）；③状态反馈极点配置）

（1）$\Phi(t)=e^{At}=\begin{bmatrix}e^{-t}&0\\e^{-t}-e^{-2t}&e^{-2t}\end{bmatrix}$，则

$$
x(t)=\Phi(t)x(0)+\int_0^t\Phi(t-\tau)bu(\tau)\,\mathrm d\tau=\begin{bmatrix}1-e^{-t}\\[4pt]\dfrac12-e^{-t}+\dfrac52e^{-2t}\end{bmatrix}
$$

> [!warning] ⚠️ 勘误
> 原书 $\Phi$ 的 $(2,2)$ 元印 $e^{-t}$，并随之把 $x(t)$ 第二分量印成 $\frac12+e^{-t}+\frac12e^{-2t}$；官方勘误图更正为 $e^{-2t}$ 与 $\frac12-e^{-t}+\frac52e^{-2t}$，复算确认（原式在 $t=0$ 之外不满足 $\dot x_2=x_1-2x_2$）。

（2）$A^TP+PA=-I$（$Q=I$），解得

$$
P=\begin{bmatrix}\frac{7}{12}&\frac{1}{12}\\[2pt]\frac{1}{12}&\frac14\end{bmatrix},\qquad \Delta_1=\frac{7}{12}>0,\quad \Delta_2=\frac14\times\frac{7}{12}-\frac{1}{144}=\frac14>0
$$

$P$ 正定，系统**渐近稳定**。

（3）设 $u=v-Kx$，$K=[k_1\ \ k_2]$：

$$
|\lambda I-(A-bK)|=\lambda^2+(3+k_1)\lambda+2k_1+k_2+2
$$

期望 $f^*(\lambda)=(\lambda+1-\mathrm j)(\lambda+1+\mathrm j)=\lambda^2+2\lambda+2$，对比系数 $3+k_1=2$、$2k_1+k_2+2=2$，得

$$
k_1=-1,\qquad k_2=2,\qquad K=[-1\ \ 2]
$$

> [!warning] ⚠️ 复算提示（两处）
> ① 原书特征式常数项印 $2k_2+k_1+2$，展开 $\det(\lambda I-(A-bK))$ 应为 $2k_1+k_2+2$（其 $K=[-1\ \ 2]$ 的结论按正确式成立）。② 原书答案的状态变量图（下图照录）给出 $\dot x_1=v-x_1+2x_2$、$\dot x_2=x_1-3x_2$，闭环矩阵 $\begin{bmatrix}-1&2\\1&-3\end{bmatrix}$ 的极点为 $-2\pm\sqrt3$，与 $K=[-1\ \ 2]$ 应有闭环 $\dot x_1=v-2x_2$、$\dot x_2=x_1-2x_2$（极点 $-1\pm\mathrm j$）不一致，图中反馈系数疑有排印错误，引用时注意。

![[附件/现控强化2-20-ans-状态变量图.png|430]]

> [!note] 本题总结
> 非零初始条件 + 常值输入：$x(t)=\Phi(t)x_0+A^{-1}(\Phi(t)-E)b$；极点配置后画状态变量图，反馈系数就是 $K$ 的分量（符号看综合点处的正负号约定）。

**2-21　答案**（考点：①拉氏反变换法求状态转移矩阵；②李雅普诺夫方程法（李二法））

（1）$e^{At}=\mathcal L^{-1}\left[(sI-A)^{-1}\right]$：

$$
(sI-A)^{-1}=\begin{bmatrix}\dfrac{s+3}{(s+1)(s+2)}&\dfrac{1}{(s+1)(s+2)}\\[6pt]\dfrac{-2}{(s+1)(s+2)}&\dfrac{s}{(s+1)(s+2)}\end{bmatrix}
$$

$$
e^{At}=\begin{bmatrix}2e^{-t}-e^{-2t}&e^{-t}-e^{-2t}\\2e^{-2t}-2e^{-t}&2e^{-2t}-e^{-t}\end{bmatrix}
$$

（2）系统为线性系统，则只有 $x_e=0$ 一个平衡状态。取 $Q=I$，解 $A^TP+PA=-I$：

$$
P=\begin{bmatrix}1.25&0.25\\0.25&0.25\end{bmatrix}
$$

$P$ 正定，系统在 $x_e=0$ 处**大范围渐近稳定**。

> [!warning] ⚠️ 复算提示
> 原书此步印「由 $A^TPA-P=0$」，应为 $A^TP+PA=-I$ 之排印错误——其解出的 $P=\begin{bmatrix}1.25&0.25\\0.25&0.25\end{bmatrix}$ 恰满足 $A^TP+PA=-I$（复算确认），$P$ 的数值可放心引用。

> [!note] 本题总结
> $(sI-A)^{-1}$ 每元部分分式后再反变换；连续系统李雅普诺夫方程别写成离散形式。

**2-22　答案**（考点：非线性系统的能量函数法（即李二法））

令 $\dot x_1=\dot x_2=0$，可得唯一平衡点 $(0,0)$。取

$$
V(x)=x_1^4+2x_2^2
$$

$V(x)$ 正定，且

$$
\dot V(x)=4x_1^3\dot x_1+4x_2\dot x_2=4x_1^3x_2+4x_2\left(-x_1^3-x_2\right)=-4x_2^2
$$

$\dot V(x)=0$ 当且仅当 $x_2=0$；而在 $x_2=0$ 上 $\dot x_2=-x_1^3$，只有 $x_1=0$ 处系统能停留，即 $\dot V(x)$ 仅在平衡点 $(0,0)$ 处为零。又 $\|\boldsymbol x\|\to\infty$ 时 $V(x)\to\infty$，故系统在平衡点处**大范围渐近稳定**。

> [!note] 本题总结
> $\dot V=-4x_2^2$ 严格说是半负定，"仅在原点为零"要借 $\dot x_2=-x_1^3$ 把 $x_2=0$ 线上的运动赶出该线（即拉萨尔不变集思路的初等版本）。

**2-23　答案**（考点：非线性系统的李一法）

（1）令 $\dot x_1=\dot x_2=0$，得

$$
x_2^2-1=0,\qquad -x_1-x_2-1=0
$$

解得两组平衡状态 $x_{e1}=(-2,1)$、$x_{e2}=(0,-1)$。

（2）雅可比矩阵：

$$
J(x)=\begin{bmatrix}\dfrac{\partial f_1}{\partial x_1}&\dfrac{\partial f_1}{\partial x_2}\\[6pt]\dfrac{\partial f_2}{\partial x_1}&\dfrac{\partial f_2}{\partial x_2}\end{bmatrix}=\begin{bmatrix}0&2x_2\\-1&-1\end{bmatrix}
$$

① 在 $x_{e1}=(-2,1)$ 处：

$$
A=J(x)\big|_{x_e=(-2,1)}=\begin{bmatrix}0&2\\-1&-1\end{bmatrix},\qquad |\lambda I-A|=\lambda^2+\lambda+2=0
$$

$\lambda_{1,2}=\dfrac{-1\pm\sqrt7\,\mathrm j}{2}$，实部均为负，故该平衡状态**渐近稳定**。

② 在 $x_{e2}=(0,-1)$ 处：

$$
A=J(x)\big|_{x_e=(0,-1)}=\begin{bmatrix}0&-2\\-1&-1\end{bmatrix},\qquad |\lambda I-A|=\lambda^2+\lambda-2=0
$$

$\lambda_1=1$、$\lambda_2=-2$，存在正实部特征值，故该平衡状态**不稳定**。

> [!note] 本题总结
> 多平衡点逐点线性化、逐点下结论；$x_2^2-1=0$ 给 $x_2=\pm1$，代回第二式得 $x_1=-x_2-1$。

## 【题型5】离散系统李雅普诺夫判稳方法

**2-24　答案**（考点：线性定常离散系统的李雅普诺夫方程法（即李二法））

取 $P=\begin{bmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{bmatrix}$，由 $G^TPG-P=-Q$（取 $Q=I$）：

$$
P=\begin{bmatrix}\frac43&0\\0&-\frac13\end{bmatrix},\qquad \Delta_2=-\frac49<0
$$

$P$ 不是正定矩阵，**系统不是渐近稳定系统**（特征值 $0.5,-2$，$|-2|>1$ 佐证）。

再算状态响应：$x(1)=Gx(0)+bu=\begin{bmatrix}\frac32\\3\end{bmatrix}$，

$$
x(2)=Gx(1)+bu=\begin{bmatrix}\frac74\\-5\end{bmatrix}
$$

> [!note] 本题总结
> 离散系统平衡状态渐近稳定 ⇔ 存在唯一正定对称 $P$ 满足 $G^TPG-P=-Q$；本题 $-2$ 的特征值在单位圆外，$P$ 出现负对角元是必然。

**2-25　答案**（考点：线性定常离散系统的李雅普诺夫方程法）

（1）$|G|=\begin{vmatrix}0&0.5\\0.5&0\end{vmatrix}=-0.25\ne0$，故该系统存在唯一平衡状态 $x_e=0$。

（2）设 $P=\begin{bmatrix}p_1&p_2\\p_3&p_4\end{bmatrix}$，令 $Q=-I$，由 $G^TPG-P=Q$ 得 $G^TPG-P=-I$：

$$
0.25p_3-p_1=-1,\qquad -0.75p_2=0,\qquad 0.25p_1-p_3=-1
$$

解得 $p_1=p_4=\frac43$、$p_2=p_3=0$：

$$
P=\begin{bmatrix}\frac43&0\\0&\frac43\end{bmatrix},\qquad \Delta_1=\frac43>0,\quad \Delta_2=\frac{16}{9}>0
$$

$P$ 正定，系统在唯一平衡状态 $x_e=0$ 处**大范围渐近稳定**。

> [!note] 本题总结
> $G$ 的特征值 $\pm0.5$ 都在单位圆内，李二法给出 $P=\frac43E$；对称 $G$ 解出对角 $P$ 是常态。

## 【题型6】线性定常系统的离散化

**2-26　答案**（考点：①拉氏反变换法求状态转移矩阵；②能控性秩判据；③线性定常系统的离散化；④离散系统能控性）

（1）$A=\begin{bmatrix}0&1\\-4&0\end{bmatrix}$，$\det(sI-A)=s^2+4$，

$$
e^{At}=\mathcal L^{-1}\left[(sI-A)^{-1}\right]=\begin{bmatrix}\cos2t&\frac12\sin2t\\-2\sin2t&\cos2t\end{bmatrix}
$$

（2）能控性判别矩阵 $Q_c=[b\ \ Ab]=\begin{bmatrix}0&2\\2&0\end{bmatrix}$，$\mathrm{rank}\,Q_c=2$，**完全能控**。

（3）离散化：

$$
G=e^{AT}=\begin{bmatrix}\cos2T&\frac12\sin2T\\-2\sin2T&\cos2T\end{bmatrix},\qquad H=\int_0^Te^{At}b\,\mathrm dt=\begin{bmatrix}-\frac12\cos2T+\frac12\\ \sin2T\end{bmatrix}
$$

$$
x(k+1)=Gx(k)+Hu(k)
$$

（4）离散化后能控性判别矩阵：

$$
Q_d=[H\ \ GH]=\begin{bmatrix}-\frac12\cos2T+\frac12&\frac12(1-\cos2T)\cos2T+\frac12\sin^22T\\ \sin2T&\sin2T(\cos2T-1)+\cos2T\sin2T\end{bmatrix}
$$

$$
|Q_d|=-\sin2T\left(1-\cos2T\right)
$$

$|Q_d|\ne0$ 要求 $\sin2T\ne0$ 且 $\cos2T\ne1$。综上，当

$$
T\ne\frac{k\pi}{2}\qquad (k=0,1,2,\cdots)
$$

时，离散化后系统完全能控。

> [!warning] ⚠️ 复算提示
> 原书 $|Q_d|$ 印为 $\sin2T(\cos2T-1)$，与复算 $-\sin2T(1-\cos2T)$ 相同（只差提出负号），零点条件 $\sin2T=0$ 或 $\cos2T=1$ 一致，$T\ne k\pi/2$ 的结论正确。

> [!note] 本题总结
> 连续系统能控 ⇏ 任意采样后仍能控：振荡模态 $\pm\mathrm j2$ 在 $T=k\pi/2$ 时采样"踩空"，离散化后丢能控性；这是采样周期选取的经典考点。

## 【题型7】输出稳定性判别

**2-27　答案**（考点：①李一法；②BIBO 稳定性判据）

（1）$u=0$ 时令 $\dot x=0$，系统存在唯一平衡状态 $x_e=(0,0,0)$。特征值：

$$
|\lambda I-A|=(\lambda+1)\left(\lambda^2-4\right)=0\ \Rightarrow\ \lambda_1=-1,\ \lambda_2=-2,\ \lambda_3=2
$$

存在正实部特征值，**系统不是渐近稳定的**。

（2）开环传递函数：

$$
W(s)=c(sI-A)^{-1}b=\frac{2\left[s^2+s-m(2s+2)\right]}{(s+1)(s+2)(s-2)}=\frac{2(s+1)(s-2m)}{(s+1)(s+2)(s-2)}=\frac{2(s-2m)}{(s+2)(s-2)}
$$

极点 $s_1=2$、$s_2=-2$，其中 $s=2$ 具有正实部。要使系统 BIBO 稳定，须消去不稳定极点：当 $m=1$ 时零点 $s=2m=2$ 与不稳定极点对消，此时

$$
W(s)=\frac{2}{s+2}
$$

系统 BIBO 稳定，故 **$m=1$**。

> [!note] 本题总结
> 状态稳定性看 $A$ 的特征值；BIBO 稳定看 $W(s)$ 的极点（对消后）。零点对消掉不稳定极点只能"骗过"输入输出，内部状态仍发散——工程上要慎用。

**2-28　答案**（考点：①BIBO 稳定性判定；②系统最小实现）

> [!warning] ⚠️ 题面与阶数
> 原书题目册题面印二阶 $\ddot y-\dot y=\dot u-u$，但答案册全程按**三阶** $\dddot y-\dot y=\dot u-u$ 求解（实现为三维、$G$ 分母含 $(s+1)$ 因子），两者不一致，疑题面漏印一个微分点；本页按答案册三阶口径转写。

（1）对微分方程进行拉氏变换：

$$
s^3Y(s)-sY(s)=sU(s)-U(s)
$$

$$
G(s)=\frac{Y(s)}{U(s)}=\frac{s-1}{s^3-s}=\frac{s-1}{s(s+1)(s-1)}
$$

能控标准形实现（按未约简的 $G$，$n=3$，$a_2=0$、$a_1=-1$、$a_0=0$；分子 $b_2=0$、$b_1=1$、$b_0=-1$）：

$$
\dot x=\begin{bmatrix}0&1&0\\0&0&1\\0&1&0\end{bmatrix}x+\begin{bmatrix}0\\0\\1\end{bmatrix}u,\qquad y=[-1\ \ 1\ \ 0]x
$$

$$
|\lambda I-A|=\lambda\left(\lambda^2-1\right)=0,\qquad \lambda_1=0,\ \lambda_{2,3}=\pm1
$$

故系统在平衡状态下**不稳定**。消去对消因子 $(s-1)$ 后

$$
G(s)=\frac{1}{s(s+1)},\qquad p_1=0,\ p_2=-1
$$

极点含 $s=0$，**不是 BIBO 系统**（阶跃输入下 $y=t-1+e^{-t}$ 无界）。

> [!warning] ⚠️ 勘误与复算
> 原书此步 $G$ 印 $1/(s^2(s+1))$，官方勘误更正为 $1/(s(s+1))$（复算成立），但随之把结论改为「故系统是 BIBO 稳定」——复算**不支持**：$\frac1{s(s+1)}$ 的极点为 $0$ 与 $-1$，$s=0$ 极点使阶跃响应无界，按 BIBO 定义**不是 BIBO 稳定**。本页维持原书印刷版「不是 BIBO 系统」的结论，仅采纳勘误的 $G$ 表达式。

（2）求最小实现：约简后 $G(s)=\dfrac{1}{s^2+s}=\dfrac{1}{s(s+1)}$（二阶、无对消），其能控标准形实现即最小实现：

$$
\dot x=\begin{bmatrix}0&1\\0&-1\end{bmatrix}x+\begin{bmatrix}0\\1\end{bmatrix}u,\qquad y=[1\ \ 0]x
$$

（二维实现既能控又能观，为最小实现。）

> [!note] 本题总结
> ①当且仅当传递函数无零极点对消时系统为 BIBO 稳定——有对消时要看**约简后**的极点；②最小实现必须完全能控且完全能观，取约简传递函数的标准形实现即可。

**2-29　答案**（考点：①BIBO 稳定性判定；②状态反馈极点配置）

（1）$|A|=\begin{vmatrix}0&1\\2&1\end{vmatrix}=-2\ne0$，可知平衡状态 $x_e=0$（唯一）。

（2）设 $P=\begin{bmatrix}p_1&p_2\\p_3&p_4\end{bmatrix}$，由 $A^TP+PA=-I$：

$$
\begin{bmatrix}0&2\\1&1\end{bmatrix}P+P\begin{bmatrix}0&1\\2&1\end{bmatrix}=\begin{bmatrix}-1&0\\0&-1\end{bmatrix}
$$

整理得 $p_1=\frac34$、$p_2=p_3=-\frac14$、$p_4=-\frac14$：

$$
P=\begin{bmatrix}\frac34&-\frac14\\[2pt]-\frac14&-\frac14\end{bmatrix},\qquad |P|=-\frac{3}{16}-\frac{1}{16}=-\frac14<0
$$

$P$ 不定，**系统不稳定**（特征值 $2,-1$ 佐证）。

（3）$G(s)=c(sI-A)^{-1}b=[-2\ \ 1]\cdot\dfrac{1}{s^2-s-2}\begin{bmatrix}s-1&1\\2&s\end{bmatrix}\begin{bmatrix}0\\1\end{bmatrix}=\dfrac{s-2}{s^2-s-2}=\dfrac{1}{s+1}$

系统传递函数极点具有负实部，故系统**是 BIBO 稳定的**。

（4）取 $u=v-Kx$，$K=[k_1\ \ k_2]$，闭环特征多项式：

$$
|\lambda I-(A-BK)|=\lambda^2+(k_2-1)\lambda+(k_1-2)
$$

期望 $f^*(\lambda)=(\lambda+3)^2=\lambda^2+6\lambda+9$，对比系数：

$$
k_2-1=6\ \Rightarrow\ k_2=7,\qquad k_1-2=9\ \Rightarrow\ k_1=11
$$

即状态反馈矩阵 $K=[11\ \ 7]$。

> [!note] 本题总结
> $|A|\ne0$ 只保证原点是唯一平衡状态，不保证稳定；$G(s)=\frac{s-2}{(s-2)(s+1)}$ 有对消——内部不稳定（$\lambda=2$）但输出 BIBO 稳定，正是"内部 vs 外部稳定性"的经典对照。

## 录入说明

> [!note] 覆盖范围（专题二全 29 题已录完）
> 本页已录 **2-1—2-29** 全部 29 题（题型 1—7），2026-10-01 完成（题目页与本页同日收官）。
>
> **官方勘误 17 条已全部处理**：题面级 2 条——**2-8**（$\Sigma_2$ 左端 $\dot x_1\to\dot x_2$）与 **2-13**（(3) 控制律补 $u=v+k_1x_1+k_2x_2$）在题目页落实；解析侧文字类 4 条——2-9、2-10、2-12「优化答案」经与勘误图（`img067`/`img068`/`img069`）逐条对照，与印刷版内容一致（2-9 勘误版补的「取状态反馈控制律 $u=v-Kx$」表述已体现在解析中），**2-28**「系统是 BIBO 稳定」经复算不成立（见 2-28 ⚠️，维持原书结论）。
>
> 改图类 11 条（2-1、2-3、2-13、2-14、2-15、2-20、2-21、2-26、2-29 等，勘误图 `img064`—`img080`）：**2-14**（能观性判别改用 $V=[c;cA]$）、**2-20**（$\Phi_{(2,2)}$ 与 $x(t)$ 第二分量更正）两处实质改动了答案内容；其余经对照勘误图与复算，印刷版答案无需改动。
>
> **复算另核出 6 处**（非官方勘误，均已在正文标注）：
>
> 2-1 的 $A^2b$ 中元应为 $13$（原书印 $3$）；2-14 可观分解 $\bar A_{(1,2)}$ 应为 $1$（原书印 $3$，可观子系统特征值随之由 $-1\pm\sqrt2\,\mathrm j$ 变为 $-1$ 二重）；2-17 的 $P_{22}=95.07$（原书印 $95.4$）；2-20(3) 特征式常数项应为 $2k_1+k_2+2$（原书印 $2k_2+k_1+2$，$K=[-1\ \ 2]$ 不变）、其状态变量图与 $K$ 不自洽（照录）；2-21 的「$A^TPA-P=0$」应为 $A^TP+PA=-I$（$P$ 值不受影响）；2-28 题面（二阶）与答案（三阶）阶数不一致。
>
> 全部矩阵结论经 sympy 独立复算（`.workbuddy\_verify_xq2.py`，80 项全过）。


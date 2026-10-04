---
create: 2026-09-26
modify: 2026-10-03
tags: [知识点, 自动控制原理, 公式速查]
type: cheatsheet
cssclasses: [big-table]
aliases: [z变换速查, 离散化速查, 脉冲传递函数, ZOH, 差分方程]
---

> 返回：[[07 第7章 线性离散系统的分析与校正]] | 返回目录：[[自动控制原理]]

# 附录 z 变换与离散化速查

> [!abstract] 附录定位
> 第7章离散部分的**纯公式速查**，一页查完：**基本定理**（线性·位移·复位移·初值·终值·卷积）、**由 $F(s)$ 求 $F(z)$ 换算表 20 行**（部分分式／留数）、**带 ZOH 的 $G(s)\to G_d(z)$ 四行表**、差分方程与脉冲传函互化、控制器离散化的替换公式、$z$ 反变换三法，末节附判稳、稳态误差与易错点。
>
> **符号口径**：§(1) 按**青大 825 的序列写法**（输出 $c[k]$、输入 $r[k]$、位移拍数记 $m$），并附**连续写法**（课本式 $e(t\pm mT)$、$f(t)$、$T$）对照——两者由 $c[k]=f(kT)$ 对应。
>
> **变换对表（$f(t)\leftrightarrow F(z)$）与拉氏表并列在本库 [[附录 拉氏变换表与z变换表]]**；推导与例题见 [[07-1-b z变换计算与反变换例题]]、[[07-1-c 采样与z变换综合例题]]。所有含 $T$ 的式子都以**采样周期 $T$ 为已知常数**处理。

## 🧮 (1) 基本定理（单边 z 变换；因果序列 $k<0$ 取零）

**线性**：

$$
\mathcal Z\bigl\{a\,c_1[k]+b\,c_2[k]\bigr\}=aC_1(z)+bC_2(z)
$$

**实数位移（滞后／超前）**——**考试就背这两条**（青大口径：输出 $c[k]$、输入 $r[k]$，位移拍数记 $m$）：

$$
\mathcal Z\bigl[c(k-m)\bigr]=z^{-m}C(z)
$$

$$
\mathcal Z\bigl[c(k+m)\bigr]=z^{m}\Bigl[C(z)-c[0]-c[1]z^{-1}-\cdots-c[m-1]z^{-(m-1)}\Bigr]
$$

紧凑写法：

$$
z^{m}\Bigl[C(z)-\sum\limits_{i=0}^{m-1}c[i]z^{-i}\Bigr]
$$

乘开形（手写常用，与 [[07-2 差分方程与系统稳定性]] 同）：

$$
z^{m}C(z)-z^{m}c[0]-z^{m-1}c[1]-\cdots-z\,c[m-1]
$$

$m=2$ 就是

$$
\mathcal Z[c(k+2)]=z^{2}C(z)-z^{2}c(0)-zc(1)
$$

**连续写法对照**（课本式 $e(t\pm mT)$，$c[k]=f(kT)$；与拉氏并列、由 $F(s)$ 求 $F(z)$ 时用）：

$$
\mathcal Z\bigl[f(t-mT)\bigr]=z^{-m}F(z)
$$

$$
\mathcal Z\bigl[f(t+mT)\bigr]=z^{m}\Bigl[F(z)-f(0)-f(T)z^{-1}-\cdots-f\bigl((m-1)T\bigr)z^{-(m-1)}\Bigr]
$$

> [!tip] 背法就两句
> **滞后就一项：只乘一个 $z^{-m}$（没有初值项，不是漏写）**；**超前乘 $z^{m}$ 之后要减掉前 $m$ 个初值**（$m=1$ 减 $c[0]$，$m=2$ 减 $c[0]+c[1]z^{-1}$），零初值时才退化成 $z^{m}C(z)$。
>
> 滞后为什么干净：换元后下标 $-m,\dots,-1$ 那 $m$ 项落在 $k<0$，**被"因果信号零延拓"直接抹掉**；超前那前 $m$ 项是真实存在的，只能补回再减。
>
> 代 $a=1$ 自检：超前式给 $z/(z-1)$，滞后式给 $1/(z-1)$（延迟一拍，正是位移式的含义），与查表一致。

> [!derivation]- 推导（不做要求，想看再展开）
> 定义式 $C(z)=\sum\limits_{k=0}^{\infty}c[k]z^{-k}$，两条都靠换元（下标记 $k$、位移拍数记 $m$）。
>
> **① 滞后 $m$ 拍：$c[k-m]$**
>
> $$
> \mathcal Z\bigl[c(k-m)\bigr]=\sum_{k=0}^{\infty}c[k-m]z^{-k}\ \overset{i=k-m}{=}\ \sum_{i=-m}^{\infty}c[i]z^{-(i+m)}=z^{-m}\sum_{i=-m}^{\infty}c[i]z^{-i}
> $$
>
> 写开前几项（$m=1$，$i=-1$ 那项 $c[-1]$ 按零延拓为零）：
>
> $$
> \mathcal Z\bigl[c(k-1)\bigr]=0+c[0]z^{-1}+c[1]z^{-2}+\cdots=z^{-1}\bigl[c[0]+c[1]z^{-1}+c[2]z^{-2}+\cdots\bigr]=z^{-1}C(z)
> $$
>
> **② 超前 $m$ 拍：$c[k+m]$**
>
> $$
> \mathcal Z\bigl[c(k+m)\bigr]=\sum_{k=0}^{\infty}c[k+m]z^{-k}\ \overset{i=k+m}{=}\ \sum_{i=m}^{\infty}c[i]z^{-(i-m)}=z^{m}\sum_{i=m}^{\infty}c[i]z^{-i}
> $$
>
> 写开前几项（$m=1$，$i=0$ 那项 $c[0]$ 被换元换走了）：
>
> $$
> \mathcal Z\bigl[c(k+1)\bigr]=c[1]+c[2]z^{-1}+c[3]z^{-2}+\cdots
> $$
>
> $$
> =z\bigl[c[0]+c[1]z^{-1}+c[2]z^{-2}+\cdots\bigr]-z\,c[0]=z\bigl[C(z)-c[0]\bigr]
> $$
>
> **差别只在换元后的求和下限**：滞后下限是 $-m$，负标号项按零延拓全为零，只剩乘 $z^{-m}$；超前下限是 $m$，前 $m$ 项被换掉了，得补回再减。
>
> 换成连续字母（$c[k]=f(kT)$）就是上面"连续写法对照"那一行——写法不同，换元完全一样。

> [!derivation]- 代 $c[k]=a^{k}$ 走一遍（一阶 / 二阶，不做要求）
> 序列 $c[k]=a^{k}$（$k\ge0$），$C(z)=\dfrac{z}{z-a}=1+az^{-1}+a^{2}z^{-2}+\cdots$；$c[0]=1$、$c[1]=a$。
>
> **滞后 $m=1$**：序列 $\{c[k-1]\}=0,\,1,\,a,\,a^{2},\dots$（$k=0$ 那项按零延拓为 $0$）
>
> $$
> \mathcal Z\bigl[c(k-1)\bigr]=0+z^{-1}+az^{-2}+\cdots=z^{-1}\cdot\frac{z}{z-a}=\frac{1}{z-a}
> $$
>
> **超前 $m=1$**：序列 $\{c[k+1]\}=a,\,a^{2},\,a^{3},\dots$
>
> $$
> \mathcal Z\bigl[c(k+1)\bigr]=a+a^{2}z^{-1}+a^{3}z^{-2}+\cdots=a\cdot\frac{z}{z-a}=\frac{az}{z-a}
> $$
>
> 走公式同结果：$z\bigl[C(z)-c[0]\bigr]=z\bigl[\frac{z}{z-a}-1\bigr]=\frac{az}{z-a}$。
>
> **滞后 $m=2$**：序列 $\{c[k-2]\}=0,\,0,\,1,\,a,\dots$
>
> $$
> \mathcal Z\bigl[c(k-2)\bigr]=0+0+z^{-2}+az^{-3}+\cdots=z^{-2}\cdot\frac{z}{z-a}=\frac{1}{z(z-a)}
> $$
>
> **超前 $m=2$**：序列 $\{c[k+2]\}=a^{2},\,a^{3},\,a^{4},\dots$
>
> $$
> \mathcal Z\bigl[c(k+2)\bigr]=a^{2}+a^{3}z^{-1}+a^{4}z^{-2}+\cdots=a^{2}\cdot\frac{z}{z-a}=\frac{a^{2}z}{z-a}
> $$
>
> 走公式同结果：$z^{2}\bigl[C(z)-c[0]-c[1]z^{-1}\bigr]=z^{2}\bigl[\frac{z}{z-a}-1-\frac{a}{z}\bigr]=\frac{a^{2}z}{z-a}$。

**考场上的用法（由差分方程写脉冲传函）**：一阶把 $c[k-1]$ 换成 $z^{-1}C(z)$，

$$
c[k]-ac[k-1]=br[k]
$$

$$
G(z)=\frac{C(z)}{R(z)}=\frac{b}{1-az^{-1}}=\frac{bz}{z-a}
$$

二阶同理（$c[k-2]\to z^{-2}C(z)$），

$$
c[k]-a_1c[k-1]-a_2c[k-2]=b_0r[k]+b_1r[k-1]
$$

$$
G(z)=\frac{b_0+b_1z^{-1}}{1-a_1z^{-1}-a_2z^{-2}}
$$

**复位移**（时域乘 $\lambda^{k}$ ↔ z 域宗量除以 $\lambda$）：

$$
\mathcal Z\bigl\{\lambda^{k}c[k]\bigr\}=C\!\left(\frac z\lambda\right)
$$

连续写法（$\lambda=e^{\mp aT}$，衰减 ↔ 宗量放大）：

$$
\mathcal Z\bigl[e^{\mp at}f(t)\bigr]=F\bigl(ze^{\pm aT}\bigr)
$$

**初值**：

$$
c[0]=\lim_{z\to\infty}C(z)
$$

**终值**（先判稳，条件见下）：

$$
\lim_{k\to\infty}c[k]=\lim_{z\to1}(z-1)C(z)
$$

**卷积**：

$$
\mathcal Z\bigl\{c_1[k]*c_2[k]\bigr\}=C_1(z)C_2(z)
$$

> [!warning] 终值定理的适用条件（825 在这里设卡）
> 约分后的 $(z-1)C(z)$ **全部极点严格在单位圆内**：$C(z)$ 允许在 $z=1$ 处有单极点，但不能另有单位圆上或圆外的极点。
> 2019 第 6 题就是直接问「能否定义稳态误差」——先判稳、再代终值，顺序反了就没分。

> [!note] 定义式在这儿（写开就是一条 $z^{-1}$ 的幂级数）
> $E(z)=e(0)+e(T)z^{-1}+e(2T)z^{-2}+\cdots$，也就是 $E(z)=\sum\limits_{n=0}^{\infty}e(nT)z^{-n}$（序列口径 $E(z)=\sum_k e[k]z^{-k}$，$e[k]=e(kT)$）——**长除法商出来的系数依次就是 $e(0),e(T),e(2T),\dots$**。
>
> 采样拉氏变换同理：$E^*(s)=e(0)+e(T)e^{-Ts}+e(2T)e^{-2Ts}+\cdots$，令 $z=e^{sT}$ 即得（左半平面 ↔ 单位圆内）。
>
> **变换对表在 [[07-1 采样与z变换]] §7.3（拉氏表与 z 表并列版见 [[附录 拉氏变换表与z变换表]]），本页不重复。**
>
> **考试范围**：只要会用 $E(z)$ 这一条（长除法读系数、$z\to\infty$ 取初值、$z\to1$ 取终值）；$e^*(t)=\sum e(nT)\delta(t-nT)$ 与 $E^*(s)=\sum e(nT)e^{-nTs}$ 仅作"采样 → 冲激串 → 令 $z=e^{sT}$"的理解链，**825 不考这两种写法**。

## 🧮 (2) 由 $F(s)$ 求 $F(z)$：两条路

**部分分式法（首选）**：把 $F(s)$ 拆成 $\frac{A}{s+a}$、$\frac{A}{(s+a)^2}$、$\frac{Bs+C}{s^2+\omega^2}$ 这类项，逐项查下表相加（注意别漏掉除以 $s$ 的积分项）。

| $F(s)$ | $F(z)$ |
| :-- | :-- |
| $\dfrac{1}{s}$ | $\dfrac{z}{z-1}$ |
| $\dfrac{1}{s^2}$ | $\dfrac{Tz}{(z-1)^2}$ |
| $\dfrac{1}{s^3}$ | $\dfrac{T^2z(z+1)}{2(z-1)^3}$ |
| $\dfrac{1}{s+a}$ | $\dfrac{z}{z-e^{-aT}}$ |
| $\dfrac{1}{(s+a)^2}$ | $\dfrac{Te^{-aT}z}{(z-e^{-aT})^2}$ |
| $\dfrac{1}{(s+a)^3}$ | $\dfrac{T^2e^{-aT}z(z+e^{-aT})}{2(z-e^{-aT})^3}$ |
| $\dfrac{a}{s(s+a)}$ | $\dfrac{(1-e^{-aT})z}{(z-1)(z-e^{-aT})}$ |
| $\dfrac{a}{s^2(s+a)}$ | $\dfrac{Tz}{(z-1)^2}-\dfrac{(1-e^{-aT})z}{a(z-1)(z-e^{-aT})}$ |
| $\dfrac{\omega}{s^2+\omega^2}$ | $\dfrac{z\sin\omega T}{z^2-2z\cos\omega T+1}$ |
| $\dfrac{s}{s^2+\omega^2}$ | $\dfrac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}$ |
| $\dfrac{\omega}{s^2-\omega^2}$ | $\dfrac{z\sinh\omega T}{z^2-2z\cosh\omega T+1}$ |
| $\dfrac{s}{s^2-\omega^2}$ | $\dfrac{z(z-\cosh\omega T)}{z^2-2z\cosh\omega T+1}$ |
| $\dfrac{\omega^2}{s(s^2+\omega^2)}$ | $\dfrac{z}{z-1}-\dfrac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}$ |
| $\dfrac{\omega}{(s+a)^2+\omega^2}$ | $\dfrac{ze^{-aT}\sin\omega T}{z^2-2ze^{-aT}\cos\omega T+e^{-2aT}}$ |
| $\dfrac{s+a}{(s+a)^2+\omega^2}$ | $\dfrac{z(z-e^{-aT}\cos\omega T)}{z^2-2ze^{-aT}\cos\omega T+e^{-2aT}}$ |
| $\dfrac{b-a}{(s+a)(s+b)}$ | $\dfrac{z}{z-e^{-aT}}-\dfrac{z}{z-e^{-bT}}$ |
| $\dfrac{1}{(s+a)(s+b)(s+c)}$ | $\dfrac{z}{(b-a)(c-a)(z-e^{-aT})}+\dfrac{z}{(a-b)(c-b)(z-e^{-bT})}+\dfrac{z}{(a-c)(b-c)(z-e^{-cT})}$ |
| $\dfrac{s+d}{(s+a)(s+b)(s+c)}$ | $\dfrac{(d-a)z}{(b-a)(c-a)(z-e^{-aT})}+\dfrac{(d-b)z}{(a-b)(c-b)(z-e^{-bT})}+\dfrac{(d-c)z}{(a-c)(b-c)(z-e^{-cT})}$ |
| $\dfrac{abc}{s(s+a)(s+b)(s+c)}$ | $\dfrac{z}{z-1}-\dfrac{bcz}{(b-a)(c-a)(z-e^{-aT})}-\dfrac{caz}{(c-b)(a-b)(z-e^{-bT})}-\dfrac{abz}{(a-c)(b-c)(z-e^{-cT})}$ |
| $\dfrac{a^2b^2}{s^2(s+a)(s+b)}$ | $\dfrac{abTz}{(z-1)^2}-\dfrac{(a+b)z}{z-1}-\dfrac{b^2z}{(a-b)(z-e^{-aT})}+\dfrac{a^2z}{(a-b)(z-e^{-bT})}$ |

> [!tip] 带 $e^{-at}$ 的两行是 $\sin/\cos$ 两行的母式
> 第 14、15 行（带 $e^{-at}$ 的 $\dfrac{\omega}{(s+a)^2+\omega^2}$ 与 $\dfrac{s+a}{(s+a)^2+\omega^2}$）是第 9、10 行 $\sin\omega t$／$\cos\omega t$ 的母式；令 $a=0$ 就退化成那两行——**记两行母式等于记四行**。
>
> 第 17—20 行是**多极点部分分式**的现成结果（三极点一族与 $\dfrac{a^2b^2}{s^2(s+a)(s+b)}$），对应的 $e(t)$、$F(s)$ 三栏并列写法和系数次序自检见 [[附录 拉氏变换表与z变换表]]。

**留数法（重根、不肯拆式时用）**：设 $F(s)$ 的极点为 $p_i$（$m$ 重极点按 $m$ 重留数算），则

$$
F(z)=\sum_i\operatorname{Res}_{s=p_i}\left[F(s)\,\frac{z}{z-e^{sT}}\right]
$$

> [!derivation] 留数法一句话推
> $\mathcal Z\{f(kT)\}=\sum_k f(kT)z^{-k}$，把 $f(kT)$ 写成 $s$ 域留数和 $f(t)=\sum_i\operatorname{Res}\bigl[F(s)e^{st}\bigr]$。
>
> 代入后对 $k$ 求几何级数 $\sum_k e^{p_i kT}z^{-k}=\frac{z}{z-e^{p_iT}}$，即得。$\frac{z}{z-e^{sT}}$ 与有些书写的 $\frac{1}{1-e^{sT}z^{-1}}$ 是同一个东西。

## 📋 (3) 带零阶保持器：常见 $G(s)\to G(z)$

保持器与环节一起离散化时的**脉冲传递函数**是

$$
G_d(z)=\left(1-z^{-1}\right)\mathcal Z\left[\frac{G(s)}{s}\right]=\frac{z-1}{z}\,\mathcal Z\Bigl[\mathcal L^{-1}\Bigl\{\frac{G(s)}{s}\Bigr\}_{t=kT}\Bigr]
$$

四行常用对照（$K/s$、$K/(s+a)$、$K/[s(s+a)]$、$K/s^2$）：

| $G(s)$ | $G_d(z)$ |
| :-- | :-- |
| $\dfrac{K}{s}$ | $\dfrac{KT}{z-1}$ |
| $\dfrac{K}{s+a}$ | $\dfrac{K\left(1-e^{-aT}\right)}{a\left(z-e^{-aT}\right)}$ |
| $\dfrac{K}{s(s+a)}$ | $\dfrac{K\Bigl[\left(aT-1+e^{-aT}\right)z+\left(1-e^{-aT}-aTe^{-aT}\right)\Bigr]}{a^2(z-1)\left(z-e^{-aT}\right)}$ |
| $\dfrac{K}{s^2}$ | $\dfrac{KT^2(z+1)}{2(z-1)^2}$ |

> [!warning] 两个 $G(z)$ 不是一回事（825 的分岔点）
> **理想脉冲采样**（无保持器）：$G(z)=\mathcal Z[G(s)]$，用第 (2) 节的表——题面写"采样器仅在偏差之后／中间没有采样器，也没有零阶保持器"时用它（2009·7、2013·7、2024 选择5）。
>
> **带零阶保持器**：多一个 $1/s$ 再乘 $(1-z^{-1})$，用本节表——题面给 $G_h(s)=\frac{1-\mathrm e^{-Ts}}{s}$ 或 `c2d(sys,T,'zoh')` 时用它（2007、2008、2014、2017、2018、2019、2022、2023、2025）。
>
> 另记一条：**加 ZOH 不改变系统阶数与开环极点，只改变开环零点**；$G(s)$ 分母 $n$ 次则 $G_d(z)$ 分母仍 $n$ 次（多出的 $z=1$ 极点被 $(1-z^{-1})$ 约掉），次数变高就是漏乘或没约分。

## 🔁 (4) 差分方程 ↔ 脉冲传函

$$
c[k]+a_1c[k-1]+\cdots+a_nc[k-n]=b_0r[k]+b_1r[k-1]+\cdots+b_mr[k-m]
$$

零初值下两边取 $z$ 变换（$\mathcal Z[c(k-i)]=z^{-i}C(z)$）：

$$
G(z)=\frac{C(z)}{R(z)}=\frac{b_0+b_1z^{-1}+\cdots+b_mz^{-m}}{1+a_1z^{-1}+\cdots+a_nz^{-n}}
$$

分子分母同乘 $z^{\max(m,n)}$ 即得正幂形式。反向由 $G(z)$ 写差分方程，就是交叉相乘后把 $z^{-n}$ 读成「延迟 $n$ 拍」（位移定理见 **(1)**）。

> [!tip] 825 只认后向式，前向式二十年没出现过
> 2006 第 6(3) 题面直接写「**后向**差分方程式」；2010、2011、2015、2016 的第 7(2) 题与 2020、2024 第 6 题，答案全部是 $z^{-1}$ 幂次。
>
> 移项写成减号形也对（青大解析惯用），只是符号约定：
>
> $$
> c[k]-a_1c[k-1]-\cdots-a_nc[k-n]=b_0r[k]+\cdots
> $$
>
> 反推时先同上把正幂形式同除 $z^n$ 对齐，否则容易把 $r[k-1]$ 误写成 $r[k+1]$。

> [!warning] 超前那一项的初值不能丢
> 滞后式 $z^{-n}C(z)$ 干净；**超前式多一个减去前 $n$ 个初值的括号**。零初值时括号里的和为零，才退化成 $z^nC(z)$。

## ⚙️ (5) 连续 → 离散的替换（控制器离散化）

| 方法 | 替换式 | 特点 |
| :-- | :-- | :-- |
| 前向差分（欧拉） | $s=\dfrac{z-1}{T}$ | 最简；$T$ 偏大时可能把稳定系统算成不稳定 |
| 后向差分 | $s=\dfrac{z-1}{Tz}$ | 稳定域比前向大，但仍有畸变 |
| 双线性（Tustin） | $s=\dfrac{2}{T}\cdot\dfrac{z-1}{z+1}$ | **最常用**；左半平面 ↔ 单位圆内一一对应 |
| 预畸变双线性 | $s=\dfrac{\omega_0}{\tan\left(\omega_0T/2\right)}\cdot\dfrac{z-1}{z+1}$ | 在指定 $\omega_0$ 处频率精确，用于截止频率附近 |
| 零极点匹配 | $z=e^{sT}$，增益按静态增益配 | 保持零极点位置，适合滤波器 |
| 阶跃响应不变（ZOH） | $G_d=(1-z^{-1})\mathcal Z\bigl[\frac{G(s)}{s}\bigr]$ | 采样瞬时的阶跃响应与原系统一致 |
| 脉冲响应不变 | $G_d=T\,\mathcal Z\bigl[G(s)\bigr]$ | 前面的 $T$ 不能省，否则增益对不上 |

> [!note] 双线性有频率畸变
> $s$ 域频率 $\omega$ 与 $z$ 域频率 $\omega_a$ 的关系是 $\omega_a=\frac{2}{T}\tan\frac{\omega T}{2}$（或反写 $\omega=\frac{2}{T}\arctan\frac{\omega_aT}{2}$）。
>
> $\omega T$ 不大时 $\omega_a\approx\omega$；高频段必须按预畸变那一行修正。PID 位置式／增量式的完整写法见 [[07-3-c 数字PID与控制器离散化]]。

## ↩️ (6) $z$ 反变换三法

| 方法 | 做法 | 什么时候用 |
| :-- | :-- | :-- |
| 长除法 | $F(z)$ 按 $z^{-1}$ 升幂相除，商的系数依次是 $c[0],c[1],c[2],\dots$ | 只要前几项／某一拍；或分母不便因式分解 |
| 部分分式 | 对 $\dfrac{F(z)}{z}$ 分解，再乘回 $z$ 查变换对表 | **常规首选**；注意除的是 $z$ 不是 $F$ |
| 留数法 | $c[k]=\sum\operatorname{Res}\bigl[F(z)z^{k-1}\bigr]$（遍历 $F(z)$ 的极点） | 有重极点、或要闭式通项 |

> [!tip] 825 实际考到这一步
> 20 年**没有单独设问"求 $z$ 反变换"**，但"求输出序列／输出响应"型要用它：**2010 第7(3)** 求 $c[0],c[1],c[2]$ 并给闭式（部分分式）、**2017 第6题与 2018 第6题**（同一道题）求输出响应并读超调量、峰值时间（要序列或闭式包络）、**2024 选择9** 求 $c(6T)$（差分方程递推更快）；2015 解析另用长除法展 $G(z)=3+17z^{-1}+67z^{-2}+\cdots$ 作核对。
>
> 结论：**长除法（读点）+ 部分分式（要闭式／包络）练熟就够**；留数法没出现过非用不可的场合，把结果写成冲激串 $e^*(t)=\sum e(nT)\delta(t-nT)$ 也从来没要求过。

## ✅ (7) 判稳与稳态误差：一行结论

- **稳定** ⟺ 闭环特征根全在单位圆内：$\lvert z_i\rvert<1$（映射 $z=e^{sT}$：左半平面 ↔ 单位圆内）。
- **二阶速判**：$F(z)=z^2+a_1z+a_0$ 稳定 ⟺ $F(1)>0$、$F(-1)>0$、$\lvert a_0\rvert<1$（朱利判据的特例）。
- **高阶**：$z=\dfrac{w+1}{w-1}$（即 $w=\dfrac{z+1}{z-1}$），则 $\lvert z\rvert<1\Leftrightarrow\operatorname{Re}w<0$，对 $w$ 域特征方程用**劳斯判据**；或直接在 $z$ 域用朱利判据。
- **稳态误差**（单位反馈、闭环稳定、误差采样）：

$$
K_p=\lim_{z\to1}\bigl[1+G(z)\bigr],\qquad K_v=\lim_{z\to1}(z-1)G(z),\qquad K_a=\lim_{z\to1}(z-1)^2G(z)
$$

| 型别 | 阶跃 $A\cdot1(t)$ | 斜坡 $At$ | 加速度 $\frac{A}{2}t^2$ |
| :-- | :-- | :-- | :-- |
| 0 型 | $\dfrac{A}{K_p}$ | $\infty$ | $\infty$ |
| Ⅰ 型 | $0$ | $\dfrac{AT}{K_v}$ | $\infty$ |
| Ⅱ 型 | $0$ | $0$ | $\dfrac{AT^2}{K_a}$ |

> [!warning] 离散的 $K_p$ 与连续差一个 1
> 教材第八版离散系统 **$K_p=\lim\limits_{z\to1}[1+G(z)]$（含 1）**，阶跃误差写成 $\frac{A}{K_p}$；连续系统是 $K_p=\lim G(s)$、误差 $\frac{R}{1+K_p}$，查表时别混用。
>
> 另外误差都带 $T$ 的幂，而 $K_v,K_a$ 的定义里**不含** $T$（$T$ 只在误差式子里出现）。详见 [[07-3 稳态误差与数字控制]]。

## ⚠️ (8) 易错点清单

- **保持器的两个 $G(z)$ 别混**：$\mathcal Z[G(s)]$ 与 $(1-z^{-1})\mathcal Z\bigl[\frac{G(s)}{s}\bigr]$ 差一个积分环节。
- **$T$ 藏在哪**：$1/s$ 类式子显式带 $T$；$1/(s+a)$ 类表面没有 $T$，实际全在 $e^{-aT}$ 里，**$T$ 一变整个式子都变**。
- **终值定理前先判稳定**：要确认约分后的 $(z-1)F(z)$ 全部极点严格在单位圆内，否则 $\lim_{z\to1}(z-1)F(z)$ 没有意义（式子与条件见 **(1)**）。
- **部分分式除的是 $z$**：$F(z)$ 直接分解会丢一个 $z$，商序列就错了。
- **超前位移的初值项**、**差分方程的零初值前提**，这两处最常漏。
- **双线性高频畸变**：只做替换不做预畸变， cutoff 附近会偏。

> 相关：[[附录 拉氏变换表与z变换表\|拉氏表与 z 表并列]] · [[07 第7章 线性离散系统的分析与校正]] · [[07-1 采样与z变换\|变换对表 §7.3]] · [[07-1-b z变换计算与反变换例题\|计算与反变换例题]] · [[07-2-b 稳定性分析与综合例\|判稳例题]] · [[07-3-c 数字PID与控制器离散化\|PID 离散化]] · 速查 [[自动控制原理]]

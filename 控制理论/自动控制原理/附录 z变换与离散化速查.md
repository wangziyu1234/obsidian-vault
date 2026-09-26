---
create: 2026-09-26
modify: 2026-09-26
tags: [知识点, 自动控制原理, 公式速查]
type: cheatsheet
aliases: [z变换速查, 离散化速查, 脉冲传递函数, ZOH, 差分方程]
---

> 返回：[[07 第7章 线性离散系统的分析与校正]] | 返回目录：[[自动控制原理]]

# 附录 z 变换与离散化速查

> [!abstract] 附录定位
> 第7章离散部分的**纯公式速查**，只收"由 $s$ 域到 $z$ 域"的换算与套路：**由 $F(s)$ 求 $F(z)$**（部分分式／留数）、**带零阶保持器的常见 $G(s)\to G(z)$ 对照**、差分方程与脉冲传函互化、控制器离散化的替换公式、$z$ 反变换三法，末节附判稳与稳态误差的一行结论。
>
> **基本变换对表（$f(t)\leftrightarrow F(z)$）在 [[07-1 采样与z变换]] §7.3，本页不重复**；推导与例题见 [[07-1-b z变换计算与反变换例题]]、[[07-1-c 采样与z变换综合例题]]。所有含 $T$ 的式子都以**采样周期 $T$ 为已知常数**处理。

## 🧮 (1) 由 $F(s)$ 求 $F(z)$：两条路

**部分分式法（首选）**：把 $F(s)$ 拆成 $\frac{A}{s+a}$、$\frac{A}{(s+a)^2}$、$\frac{Bs+C}{s^2+\omega^2}$ 这类项，逐项查下表相加。

| $F(s)$ | $F(z)$ |
| :-- | :-- |
| $\dfrac{1}{s}$ | $\dfrac{z}{z-1}$ |
| $\dfrac{1}{s^2}$ | $\dfrac{Tz}{(z-1)^2}$ |
| $\dfrac{1}{s+a}$ | $\dfrac{z}{z-e^{-aT}}$ |
| $\dfrac{1}{(s+a)^2}$ | $\dfrac{Te^{-aT}z}{(z-e^{-aT})^2}$ |
| $\dfrac{a}{s(s+a)}$ | $\dfrac{(1-e^{-aT})z}{(z-1)(z-e^{-aT})}$ |
| $\dfrac{\omega}{s^2+\omega^2}$ | $\dfrac{z\sin\omega T}{z^2-2z\cos\omega T+1}$ |
| $\dfrac{s}{s^2+\omega^2}$ | $\dfrac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}$ |
| $\dfrac{\omega}{(s+a)^2+\omega^2}$ | $\dfrac{ze^{-aT}\sin\omega T}{z^2-2ze^{-aT}\cos\omega T+e^{-2aT}}$ |
| $\dfrac{s+a}{(s+a)^2+\omega^2}$ | $\dfrac{z(z-e^{-aT}\cos\omega T)}{z^2-2ze^{-aT}\cos\omega T+e^{-2aT}}$ |

**留数法（重根、不肯拆式时用）**：设 $F(s)$ 的极点为 $p_i$（$m$ 重极点按 $m$ 重留数算），则

$$
F(z)=\sum_i\operatorname{Res}_{s=p_i}\left[F(s)\,\frac{z}{z-e^{sT}}\right]
$$

> [!derivation] 留数法一句话推
> $\mathcal Z\{f(kT)\}=\sum_k f(kT)z^{-k}$，把 $f(kT)$ 写成 $s$ 域留数和 $f(t)=\sum_i\operatorname{Res}\bigl[F(s)e^{st}\bigr]$。
>
> 代入后对 $k$ 求几何级数 $\sum_k e^{p_i kT}z^{-k}=\frac{z}{z-e^{p_iT}}$，即得。$\frac{z}{z-e^{sT}}$ 与有些书写的 $\frac{1}{1-e^{sT}z^{-1}}$ 是同一个东西。

## 📋 (2) 带零阶保持器：常见 $G(s)\to G(z)$

保持器与环节一起离散化时的**脉冲传递函数**是

$$
G_d(z)=\left(1-z^{-1}\right)\mathcal Z\left[\frac{G(s)}{s}\right]=\frac{z-1}{z}\,\mathcal Z\Bigl[\mathcal L^{-1}\Bigl\{\frac{G(s)}{s}\Bigr\}_{t=kT}\Bigr]
$$

| $G(s)$ | $G_d(z)$ |
| :-- | :-- |
| $\dfrac{K}{s}$ | $\dfrac{KT}{z-1}$ |
| $\dfrac{K}{s+a}$ | $\dfrac{K\left(1-e^{-aT}\right)}{a\left(z-e^{-aT}\right)}$ |
| $\dfrac{K}{s(s+a)}$ | $\dfrac{K\Bigl[\left(aT-1+e^{-aT}\right)z+\left(1-e^{-aT}-aTe^{-aT}\right)\Bigr]}{a^2(z-1)\left(z-e^{-aT}\right)}$ |
| $\dfrac{K}{s^2}$ | $\dfrac{KT^2(z+1)}{2(z-1)^2}$ |

> [!warning] 两个 $G(z)$ 不是一回事
> **理想脉冲采样**（无保持器）：$G(z)=\mathcal Z[G(s)]$，用第 (1) 节的表。
>
> **带零阶保持器**：多一个 $1/s$ 再乘 $(1-z^{-1})$，用本节表。考题说"离散化后的脉冲传递函数"通常指后者；只说"求 $G(z)$"要看清有没有保持器。

## 🔁 (3) 差分方程 ↔ 脉冲传函

$$
y(k)+a_1y(k-1)+\cdots+a_ny(k-n)=b_0u(k)+b_1u(k-1)+\cdots+b_mu(k-m)
$$

零初值下两边取 $z$ 变换：

$$
G(z)=\frac{Y(z)}{U(z)}=\frac{b_0+b_1z^{-1}+\cdots+b_mz^{-m}}{1+a_1z^{-1}+\cdots+a_nz^{-n}}
$$

分子分母同乘 $z^{\max(m,n)}$ 即得正幂形式。反过来由 $G(z)$ 写差分方程，就交叉相乘再逐项反变换。

**实数位移定理**（单边 $z$ 变换，$t<0$ 延拓为零）：

$$
\mathcal Z\bigl[f(k-n)\bigr]=z^{-n}F(z)
$$

$$
\mathcal Z\bigl[f(k+n)\bigr]=z^{n}\Bigl[F(z)-\sum_{i=0}^{n-1}f(i)z^{-i}\Bigr]
$$

> [!warning] 超前那一项的初值不能丢
> 滞后式 $z^{-n}F(z)$ 干净；**超前式多一个减去前 $n$ 个初值的括号**。零初值时括号里的和为零，才退化成 $z^nF(z)$。

## ⚙️ (4) 连续 → 离散的替换（控制器离散化）

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

## ↩️ (5) $z$ 反变换三法

| 方法 | 做法 | 什么时候用 |
| :-- | :-- | :-- |
| 长除法 | $F(z)$ 按 $z^{-1}$ 升幂相除，商的系数依次是 $f(0),f(T),f(2T),\dots$ | 只要前几项；或分母不便因式分解 |
| 部分分式 | 对 $\dfrac{F(z)}{z}$ 分解，再乘回 $z$ 查变换对表 | **常规首选**；注意除的是 $z$ 不是 $F$ |
| 留数法 | $f(kT)=\sum\operatorname{Res}\bigl[F(z)z^{k-1}\bigr]$（遍历 $F(z)$ 的极点） | 有重极点、或要闭式通项 |

## ✅ (6) 判稳与稳态误差：一行结论

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

## ⚠️ (7) 易错点清单

- **保持器的两个 $G(z)$ 别混**：$\mathcal Z[G(s)]$ 与 $(1-z^{-1})\mathcal Z\bigl[\frac{G(s)}{s}\bigr]$ 差一个积分环节。
- **$T$ 藏在哪**：$1/s$ 类式子显式带 $T$；$1/(s+a)$ 类表面没有 $T$，实际全在 $e^{-aT}$ 里，**$T$ 一变整个式子都变**。
- **终值定理前先判稳定**：要确认约分后的 $(z-1)F(z)$ 全部极点严格在单位圆内，否则 $\lim_{z\to1}(z-1)F(z)$ 没有意义。
- **部分分式除的是 $z$**：$F(z)$ 直接分解会丢一个 $z$，商序列就错了。
- **超前位移的初值项**、**差分方程的零初值前提**，这两处最常漏。
- **双线性高频畸变**：只做替换不做预畸变， cutoff 附近会偏。

> 相关：[[07 第7章 线性离散系统的分析与校正]] · [[07-1 采样与z变换\|基本变换对表 §7.3]] · [[07-1-b z变换计算与反变换例题\|计算与反变换例题]] · [[07-2-b 稳定性分析与综合例\|判稳例题]] · [[07-3-c 数字PID与控制器离散化\|PID 离散化]] · 速查 [[自动控制原理]]

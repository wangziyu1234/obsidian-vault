---
create: 2026-10-03
modify: 2026-10-03
tags: [知识点, 自动控制原理, 公式速查]
type: cheatsheet
aliases: [s域到z域对照表, sz对照表, 脉冲传递函数对照表, ZOH离散化对照表]
---

> 返回：[[07 第7章 线性离散系统的分析与校正]] | 返回目录：[[自动控制原理]]

# 附录 s 域到 z 域对照表

> [!abstract] 附录定位
> 两张"$s$ 域 → $z$ 域"的**查表页**，从 [[附录 z变换与离散化速查]] 单独拆出，做题时单开一页对着查：
>
> - **(1) 理想（脉冲）采样**：$G(z)=\mathcal Z[G(s)]$ —— 题面写"没有保持器／采样器只在偏差处"时用；
> - **(2) 带零阶保持器（ZOH）**：$G_d(z)=(1-z^{-1})\mathcal Z\bigl[\frac{G(s)}{s}\bigr]$ —— 题面给 $G_h(s)=\frac{1-\mathrm e^{-Ts}}{s}$ 或 `c2d(sys,T,'zoh')` 时用。
>
> 方法与定理（部分分式／留数、位移与终值定理、判稳与稳态误差）见 [[附录 z变换与离散化速查]]；基本变换对表（$f(t)\leftrightarrow F(z)$，14 行）见 [[07-1 采样与z变换]] §7.3。

## 📋 (1) 理想（脉冲）采样：$G(z)=\mathcal Z[G(s)]$

**用法**：把 $G(s)$ 拆成 $\frac{A}{s+a}$、$\frac{A}{(s+a)^2}$、$\frac{Bs+C}{s^2+\omega^2}$ 这类项，**逐项查下表相加**——注意别漏掉除以 $s$ 的积分项（$1/s$、$1/s^2$ 两行就干这个）。

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

> [!tip] 后两行是前两行的母式
> $\dfrac{\omega}{(s+a)^2+\omega^2}$ 与 $\dfrac{s+a}{(s+a)^2+\omega^2}$ 是 $e^{-at}\sin\omega t$／$e^{-at}\cos\omega t$ 的像；令 $a=0$ 就退化成 $\sin\omega t$／$\cos\omega t$ 那两行。**记两行母式，等于记四行。**

**重根、不肯拆式时**：留数法

$$
F(z)=\sum_i\operatorname{Res}_{s=p_i}\left[F(s)\,\frac{z}{z-e^{sT}}\right]
$$

（推导与例题见 [[附录 z变换与离散化速查]] §(2) 与 [[07-1-b z变换计算与反变换例题]]。）

## 🎯 (2) 带零阶保持器（ZOH）：$G_d(z)=(1-z^{-1})\mathcal Z\bigl[\frac{G(s)}{s}\bigr]$

**用法**：先给 $G(s)$ 补一个 $\frac1s$（多一个积分环节）查上表，再整体乘 $(1-z^{-1})=\frac{z-1}{z}$。

$$
G_d(z)=\left(1-z^{-1}\right)\mathcal Z\left[\frac{G(s)}{s}\right]
$$

| $G(s)$ | $G_d(z)$ |
| :-- | :-- |
| $\dfrac{K}{s}$ | $\dfrac{KT}{z-1}$ |
| $\dfrac{K}{s+a}$ | $\dfrac{K\left(1-e^{-aT}\right)}{a\left(z-e^{-aT}\right)}$ |
| $\dfrac{K}{s(s+a)}$ | $\dfrac{K\Bigl[\left(aT-1+e^{-aT}\right)z+\left(1-e^{-aT}-aTe^{-aT}\right)\Bigr]}{a^2(z-1)\left(z-e^{-aT}\right)}$ |
| $\dfrac{K}{s^2}$ | $\dfrac{KT^2(z+1)}{2(z-1)^2}$ |

> [!warning] 两个 $G(z)$ 别混——825 的分岔点就在这里
> 同一道题，**有没有保持器，答案差一个积分环节**：
> - 题面写"采样器仅在偏差之后／中间没有采样器，也没有零阶保持器"→ 用 **(1)**，$G(z)=\mathcal Z[G(s)]$（2009·7、2013·7、2024 选择5）；
> - 题面给 $G_h(s)=\frac{1-\mathrm e^{-Ts}}{s}$ 或 `c2d(sys,T,'zoh')` → 用 **(2)**（2007、2008、2014、2017、2018、2019、2022、2023、2025 都是这种）。
>
> 另记一条：**加 ZOH 不改变系统阶数与开环极点，只改变开环零点。**

> [!note] 查表前的 10 秒自检（数阶数）
> $G(s)$ 分母是 $n$ 次，$G_d(z)$ 分母仍是 $n$ 次——多出来的那个 $1/s$ 导致的 $z=1$ 极点，正好被 $(1-z^{-1})$ 的 $z=1$ 零点约掉。
> 若算出的分母次数比 $n$ 高，多半是 $(1-z^{-1})$ 漏乘、或没有约掉 $z=1$ 那对零极点（$K/s$ 与 $K/s^2$ 两行最容易踩）。

> 相关：[[附录 z变换与离散化速查]]（定理·留数法·判稳·稳态误差·控制器离散化） · [[07-1 采样与z变换]]（§7.3 基本变换对表） · [[07-2 差分方程与系统稳定性]]（脉冲传函与结构图） · [[07-3 稳态误差与数字控制]] · 速查 [[自动控制原理]]

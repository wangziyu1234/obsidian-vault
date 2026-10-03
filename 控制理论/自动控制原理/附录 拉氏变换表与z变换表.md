---
create: 2026-10-03
modify: 2026-10-03
tags: [知识点, 自动控制原理, 公式速查]
type: cheatsheet
aliases: [拉氏变换表, z变换表, 变换对速查, 变换对表, 常用变换对]
---

> 返回：[[00 拉普拉斯变换（数学基础）]] · [[07 第7章 线性离散系统的分析与校正]] | 返回目录：[[自动控制原理]]

# 附录 拉氏变换表与 z 变换表

> [!abstract] 附录定位
> **两张对偶变换对表并列一页**：连续域查 $\mathcal L$、离散域查 $\mathcal Z$，同一列 $f(t)$ 对齐，方便互相印证。
>
> **和 [[附录 s域到z域对照表]] 的区别**（别混）：
> - **本页**＝「$f(t)$ 是哪一类信号 → 它的像函数是什么」，用于**求正变换、查反变换**；
> - **那一页**＝「已知 $F(s)$，采样后 $F(z)$ 或 $G_d(z)$ 是什么」，用于**把 $s$ 域系统离散化**（含 ZOH 表）。
>
> 正本分别在 [[00-1 拉普拉斯变换定义、变换对与定理]] 与 [[07-1 采样与z变换]] §7.3；本页只做并列速查，**两处改动要同步**。

## 📘 (1) 拉氏变换对：$f(t)\leftrightarrow F(s)$

单边变换 $F(s)=\int_0^\infty f(t)\mathrm e^{-st}\,dt$；普通函数取 $0^-$ 冲激约定时对 $\delta(t)$ 也成立。

| 时域 $f(t)$ | 复频域 $F(s)$ |
| :-- | :-- |
| 单位脉冲 $\delta(t)$ | $1$ |
| 单位阶跃 $1(t)$ | $\dfrac{1}{s}$ |
| 斜坡 $t$ | $\dfrac{1}{s^{2}}$ |
| $t^{n}\ (n=1,2,\dots)$ | $\dfrac{n!}{s^{n+1}}$ |
| 指数 $\mathrm e^{-at}$ | $\dfrac{1}{s+a}$ |
| $t\,\mathrm e^{-at}$ | $\dfrac{1}{(s+a)^2}$ |
| $t^{n}\mathrm e^{-at}$ | $\dfrac{n!}{(s+a)^{n+1}}$ |
| $1-\mathrm e^{-at}$ | $\dfrac{a}{s(s+a)}$ |
| $\dfrac{\mathrm e^{-at}-\mathrm e^{-bt}}{b-a}\ (a\ne b)$ | $\dfrac{1}{(s+a)(s+b)}$ |
| $\sin\omega t$ | $\dfrac{\omega}{s^{2}+\omega^{2}}$ |
| $\cos\omega t$ | $\dfrac{s}{s^{2}+\omega^{2}}$ |
| $\mathrm e^{-at}\sin\omega t$ | $\dfrac{\omega}{(s+a)^{2}+\omega^{2}}$ |
| $\mathrm e^{-at}\cos\omega t$ | $\dfrac{s+a}{(s+a)^{2}+\omega^{2}}$ |

## 📗 (2) $z$ 变换对：$f(t)\leftrightarrow F(z)$

单边 z 变换 $F(z)=\sum\limits_{n=0}^{\infty}f(nT)z^{-n}$，$z=\mathrm e^{sT}$，因果信号 $t<0$ 延拓为零。

| 时域 $f(t)$ | 复域 $F(z)$ |
| :-- | :-- |
| $\delta(t)$ | $1$ |
| $1(t)$ | $\dfrac{z}{z-1}$ |
| $t$ | $\dfrac{Tz}{(z-1)^2}$ |
| $\dfrac{t^2}{2}$ | $\dfrac{T^2z(z+1)}{2(z-1)^3}$ |
| $\dfrac{t^3}{6}$ | $\dfrac{T^3z(z^2+4z+1)}{6(z-1)^4}$ |
| $a^{k}$（序列） | $\dfrac{z}{z-a}$ |
| $\mathrm e^{-at}$ | $\dfrac{z}{z-\mathrm e^{-aT}}$ |
| $\sin\omega t$ | $\dfrac{z\sin\omega T}{z^2-2z\cos\omega T+1}$ |
| $\cos\omega t$ | $\dfrac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}$ |
| $t\,\mathrm e^{-at}$ | $\dfrac{T\mathrm e^{-aT}z}{(z-\mathrm e^{-aT})^2}$ |
| $\dfrac{t^2}{2}\mathrm e^{-at}$ | $\dfrac{T^2\mathrm e^{-aT}z(z+\mathrm e^{-aT})}{2(z-\mathrm e^{-aT})^3}$ |
| $1-\mathrm e^{-at}$ | $\dfrac{z(1-\mathrm e^{-aT})}{(z-1)(z-\mathrm e^{-aT})}$ |
| $\mathrm e^{-at}\sin\omega t$ | $\dfrac{z\mathrm e^{-aT}\sin\omega T}{z^2-2z\mathrm e^{-aT}\cos\omega T+\mathrm e^{-2aT}}$ |
| $\mathrm e^{-at}\cos\omega t$ | $\dfrac{z(z-\mathrm e^{-aT}\cos\omega T)}{z^2-2z\mathrm e^{-aT}\cos\omega T+\mathrm e^{-2aT}}$ |

> [!tip] 两表怎么对照记（这是并列的意义）
> **极点映到 $z=\mathrm e^{sT}$**：$s=-a\Rightarrow z=\mathrm e^{-aT}$；$s=0\Rightarrow z=1$。所以左边每出现一个 $(s+a)$，右边就出现一个 $(z-\mathrm e^{-aT})$：
>
> | 项 | $F(s)$ | $F(z)$ |
> | :-- | :-- | :-- |
> | 阶跃 | $\dfrac1s$ | $\dfrac{z}{z-1}$ |
> | 斜坡 | $\dfrac1{s^2}$ | $\dfrac{Tz}{(z-1)^2}$ |
> | 指数 | $\dfrac1{s+a}$ | $\dfrac{z}{z-\mathrm e^{-aT}}$ |
> | 振荡 | $\dfrac{\omega}{s^2+\omega^2}$ | $\dfrac{z\sin\omega T}{z^2-2z\cos\omega T+1}$ |
>
> **$s=0$ 处的重极点会多出 $T^k$ 因子**（$1/s^2\to Tz/(z-1)^2$、$t^2/2\to T^2z(z+1)/[2(z-1)^3]$）——这是"连续积分变成离散累加"留下的痕迹，**查 z 表时最容易漏这个 $T$**。

> [!warning] 两个"阶跃"别写反
> $\mathcal L[1(t)]=\dfrac1s$ 而 $\mathcal Z[1(t)]=\dfrac{z}{z-1}$：**连续域是 $1/s$，离散域是 $\dfrac{z}{z-1}$（不是 $\dfrac1{z-1}$，也不是 $\dfrac1{z+1}$）**。同理 $\mathcal Z[\mathrm e^{-at}]=\dfrac{z}{z-\mathrm e^{-aT}}$ 分子上的 $z$ 不能丢——丢一个 $z$ 就错整道题（部分分式法除 $z$ 的坑也在这个 $z$ 上）。

> 相关：[[附录 s域到z域对照表]]（由 $F(s)$ 求 $F(z)$／ZOH 四行表） · [[附录 z变换与离散化速查]]（定理·留数法·判稳·稳态误差） · [[00-1 拉普拉斯变换定义、变换对与定理]]（拉氏定理与使用边界） · [[07-1 采样与z变换]]（§7.3 基本变换对表） · 速查 [[自动控制原理]]

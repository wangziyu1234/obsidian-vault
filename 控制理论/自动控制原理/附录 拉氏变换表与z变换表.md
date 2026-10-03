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
> **一张合并总表**：同一列 $f(t)$ 对齐，左栏查 $\mathcal L$、右栏查 $\mathcal Z$——两张表合成一张，**同行即可对照**（$\frac1s$ 对 $\frac{z}{z-1}$、$\frac1{s+a}$ 对 $\frac{z}{z-e^{-aT}}$、$\frac{\omega}{s^2+\omega^2}$ 对 $\frac{z\sin\omega T}{z^2-2z\cos\omega T+1}$）。
>
> **和 [[附录 z变换与离散化速查]] 的分工**：本页是"$f(t)$ 是哪类信号 → 它的像函数是什么"，用于**求正变换、查反变换**；那一页管"已知 $F(s)$，采样后 $F(z)$ 或带 ZOH 的 $G_d(z)$ 是什么"（其 §(2) 九行表、§(3) 四行表），另有定理、留数法、判稳与稳态误差。
>
> 正本在 [[00-1 拉普拉斯变换定义、变换对与定理]] 与 [[07-1 采样与z变换]] §7.3；本页只做合并速查，**改动要同步**。

## 📋 (1) 变换对总表

单边变换：$F(s)=\int_0^\infty f(t)\mathrm e^{-st}\,dt$；$F(z)=\sum\limits_{n=0}^{\infty}f(nT)z^{-n}$，$z=\mathrm e^{sT}$，因果信号 $t<0$ 延拓为零。

| $f(t)$ | $F(s)$（拉氏） | $F(z)$（z 变换） |
| :-- | :-- | :-- |
| $\delta(t)$ | $1$ | $1$ |
| $1(t)$ | $\frac1s$ | $\frac{z}{z-1}$ |
| $t$ | $\frac1{s^2}$ | $\frac{Tz}{(z-1)^2}$ |
| $\frac{t^2}{2}$ | $\frac1{s^3}$ | $\frac{T^2z(z+1)}{2(z-1)^3}$ |
| $\frac{t^3}{6}$ | $\frac1{s^4}$ | $\frac{T^3z(z^2+4z+1)}{6(z-1)^4}$ |
| $t^n$ | $\frac{n!}{s^{n+1}}$ | 无 $n$ 阶简式，查上两行 |
| $\mathrm e^{-at}$ | $\frac1{s+a}$ | $\frac{z}{z-\mathrm e^{-aT}}$ |
| $t\,\mathrm e^{-at}$ | $\frac1{(s+a)^2}$ | $\frac{T\mathrm e^{-aT}z}{(z-\mathrm e^{-aT})^2}$ |
| $\frac{t^2}{2}\mathrm e^{-at}$ | $\frac1{(s+a)^3}$ | $\frac{T^2\mathrm e^{-aT}z(z+\mathrm e^{-aT})}{2(z-\mathrm e^{-aT})^3}$ |
| $t^{n}\mathrm e^{-at}$ | $\frac{n!}{(s+a)^{n+1}}$ | 无 $n$ 阶简式，同上行 |
| $a^{k}$（序列） | 无连续对应 | $\frac{z}{z-a}$ |
| $1-\mathrm e^{-at}$ | $\frac{a}{s(s+a)}$ | $\frac{z(1-\mathrm e^{-aT})}{(z-1)(z-\mathrm e^{-aT})}$ |
| $\frac{\mathrm e^{-at}-\mathrm e^{-bt}}{b-a}\ (a\ne b)$ | $\frac{1}{(s+a)(s+b)}$ | $\frac{1}{b-a}\Bigl[\frac{z}{z-\mathrm e^{-aT}}-\frac{z}{z-\mathrm e^{-bT}}\Bigr]$ |
| $\sin\omega t$ | $\frac{\omega}{s^2+\omega^2}$ | $\frac{z\sin\omega T}{z^2-2z\cos\omega T+1}$ |
| $\cos\omega t$ | $\frac{s}{s^2+\omega^2}$ | $\frac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}$ |
| $\mathrm e^{-at}\sin\omega t$ | $\frac{\omega}{(s+a)^2+\omega^2}$ | $\frac{z\mathrm e^{-aT}\sin\omega T}{z^2-2z\mathrm e^{-aT}\cos\omega T+\mathrm e^{-2aT}}$ |
| $\mathrm e^{-at}\cos\omega t$ | $\frac{s+a}{(s+a)^2+\omega^2}$ | $\frac{z(z-\mathrm e^{-aT}\cos\omega T)}{z^2-2z\mathrm e^{-aT}\cos\omega T+\mathrm e^{-2aT}}$ |

## 📌 (2) 三条查表要点

1. **极点映射**：$s=-a\Rightarrow z=\mathrm e^{-aT}$、$s=0\Rightarrow z=1$——左栏每出现一个 $(s+a)$，右栏就出现一个 $(z-\mathrm e^{-aT})$（看指数行与两行衰减振荡）。
2. **$s=0$ 的 $k$ 重极点会带出 $T^k$ 因子**：$\frac1{s^2}\to\frac{Tz}{(z-1)^2}$、$\frac1{s^3}\to\frac{T^2z(z+1)}{2(z-1)^3}$——这是"连续积分变成离散累加"的痕迹，**查右栏最容易漏这个 $T$**。
3. **两个"阶跃"别写反**：$\mathcal L[1(t)]=\frac1s$，而 $\mathcal Z[1(t)]=\frac{z}{z-1}$（不是 $\frac1{z-1}$）；$\mathcal Z[\mathrm e^{-at}]=\frac{z}{z-\mathrm e^{-aT}}$ 分子上的 $z$ 不能丢——部分分式法"除 $z$"的坑也在这个 $z$ 上。

> [!tip] 表里为什么有的格子不写式子
> $t^n$、$t^n\mathrm e^{-at}$ 的 z 变换带欧拉多项式，$n=2,3$ 的具体式子已在上面两行列出，工程上够用；$a^{k}$ 是序列，没有连续信号的拉氏对应。**空着的那格不是漏抄，是本来就没有简式。**

> [!note] 合并后少了一列的原理在这儿
> 两张表能同行并列，是因为离散化只做一件事：**把每个 $s$ 域极点 $p$ 换成 $\mathrm e^{pT}$，并把 $s=0$ 处的重极点计数换成 $T^k$ 因子**。所以"左侧 $(s+a)$ 的幂次"与"右侧 $(z-\mathrm e^{-aT})$ 的幂次"始终一样。

> 相关：[[附录 z变换与离散化速查]]（$F(s)\to F(z)$ 九行表／ZOH 四行表·定理·留数法·判稳·稳态误差） · [[00-1 拉普拉斯变换定义、变换对与定理]]（拉氏定理与使用边界） · [[07-1 采样与z变换]]（§7.3 变换对表） · 速查 [[自动控制原理]]

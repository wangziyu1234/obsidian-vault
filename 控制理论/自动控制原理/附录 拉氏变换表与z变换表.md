---
create: 2026-10-03
modify: 2026-10-04
tags: [知识点, 自动控制原理, 公式速查]
type: cheatsheet
cssclasses: [big-table, wide-table]
aliases: [拉氏变换表, z变换表, 变换对速查, 变换对表, 常用变换对]
---

> 返回：[[00 拉普拉斯变换（数学基础）]] · [[07 第7章 线性离散系统的分析与校正]] | 返回目录：[[自动控制原理]]

# 附录 拉氏变换表与 z 变换表

> [!abstract] 附录定位
> **一张合并总表，教材附录原表 24 行全收**：同一行 $f(t)$ 对齐，左栏查 $\mathcal L$、右栏查 $\mathcal Z$——**同行即可对照**（$\frac1s$ 对 $\frac{z}{z-1}$、$\frac1{s+a}$ 对 $\frac{z}{z-\mathrm e^{-aT}}$、$\frac{\omega}{s^2+\omega^2}$ 对 $\frac{z\sin\omega T}{z^2-2z\cos\omega T+1}$）。
>
> 相对讲义正本，本页多收两类行：**双曲行**（$\sinh\omega t$、$\cosh\omega t$，分母是 $s^2-\omega^2$）与**多极点部分分式行**（三极点 $\frac{1}{(s+a)(s+b)(s+c)}$ 一族、$\frac{a^2b^2}{s^2(s+a)(s+b)}$）——这些都能直接查表出结果，不必现推留数。
>
> **和 [[附录 z变换与离散化速查]] 的分工**：本页是"$f(t)$ 是哪类信号 → 它的像函数是什么"，用于**求正变换、查反变换**；那一页管"已知 $F(s)$，采样后 $F(z)$ 或带 ZOH 的 $G_d(z)$ 是什么"（其 §(2) 换算表、§(3) 四行表），另有定理、留数法、判稳与稳态误差。
>
> 正本在 [[00-1 拉普拉斯变换定义、变换对与定理]] 与 [[07-1 采样与z变换]] §7.3（常用 14 行）；本页在其上补足教材原表，**同一行式子的写法两处必须一致**。

## 📋 (1) 变换对总表

单边变换：$F(s)=\int_0^\infty f(t)\mathrm e^{-st}\,dt$；$F(z)=\sum\limits_{n=0}^{\infty}f(nT)z^{-n}$，$z=\mathrm e^{sT}$，因果信号 $t<0$ 延拓为零；$a,b,c,d$ 为互不相等的实常数。

| $f(t)$ | $F(s)$（拉氏） | $F(z)$（z 变换） |
| :-- | :-- | :-- |
| $\delta(t)$ | $1$ | $1$ |
| $\delta(t-nT)$ | $\mathrm e^{-nTs}$ | $z^{-n}$ |
| $1(t)$ | $\frac1s$ | $\frac{z}{z-1}$ |
| $t$ | $\frac1{s^2}$ | $\frac{Tz}{(z-1)^2}$ |
| $\frac{t^2}{2}$ | $\frac1{s^3}$ | $\frac{T^2z(z+1)}{2(z-1)^3}$ |
| $\frac{t^3}{6}$ | $\frac1{s^4}$ | $\frac{T^3z(z^2+4z+1)}{6(z-1)^4}$ |
| $t^n$ | $\frac{n!}{s^{n+1}}$ | 无 $n$ 阶简式，查上两行 |
| $a^{t/T}$（采样即 $a^n$） | $\frac{1}{s-\frac1T\ln a}$ | $\frac{z}{z-a}$ |
| $\mathrm e^{-at}$ | $\frac1{s+a}$ | $\frac{z}{z-\mathrm e^{-aT}}$ |
| $t\,\mathrm e^{-at}$ | $\frac1{(s+a)^2}$ | $\frac{T\mathrm e^{-aT}z}{(z-\mathrm e^{-aT})^2}$ |
| $\frac{t^2}{2}\mathrm e^{-at}$ | $\frac1{(s+a)^3}$ | $\frac{T^2\mathrm e^{-aT}z(z+\mathrm e^{-aT})}{2(z-\mathrm e^{-aT})^3}$ |
| $t^n\mathrm e^{-at}$ | $\frac{n!}{(s+a)^{n+1}}$ | 无 $n$ 阶简式，同上行 |
| $1-\mathrm e^{-at}$ | $\frac{a}{s(s+a)}$ | $\frac{(1-\mathrm e^{-aT})z}{(z-1)(z-\mathrm e^{-aT})}$ |
| $t-\frac1a(1-\mathrm e^{-at})$ | $\frac{a}{s^2(s+a)}$ | $\frac{Tz}{(z-1)^2}-\frac{(1-\mathrm e^{-aT})z}{a(z-1)(z-\mathrm e^{-aT})}$ |
| $\sin\omega t$ | $\frac{\omega}{s^2+\omega^2}$ | $\frac{z\sin\omega T}{z^2-2z\cos\omega T+1}$ |
| $\cos\omega t$ | $\frac{s}{s^2+\omega^2}$ | $\frac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}$ |
| $\sinh\omega t$ | $\frac{\omega}{s^2-\omega^2}$ | $\frac{z\sinh\omega T}{z^2-2z\cosh\omega T+1}$ |
| $\cosh\omega t$ | $\frac{s}{s^2-\omega^2}$ | $\frac{z(z-\cosh\omega T)}{z^2-2z\cosh\omega T+1}$ |
| $1-\cos\omega t$ | $\frac{\omega^2}{s(s^2+\omega^2)}$ | $\frac{z}{z-1}-\frac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}$ |
| $\mathrm e^{-at}\sin\omega t$ | $\frac{\omega}{(s+a)^2+\omega^2}$ | $\frac{z\mathrm e^{-aT}\sin\omega T}{z^2-2z\mathrm e^{-aT}\cos\omega T+\mathrm e^{-2aT}}$ |
| $\mathrm e^{-at}\cos\omega t$ | $\frac{s+a}{(s+a)^2+\omega^2}$ | $\frac{z(z-\mathrm e^{-aT}\cos\omega T)}{z^2-2z\mathrm e^{-aT}\cos\omega T+\mathrm e^{-2aT}}$ |
| $\mathrm e^{-at}-\mathrm e^{-bt}$ | $\frac{b-a}{(s+a)(s+b)}$ | $\frac{z}{z-\mathrm e^{-aT}}-\frac{z}{z-\mathrm e^{-bT}}$ |
| $\frac{\mathrm e^{-at}}{(b-a)(c-a)}+\frac{\mathrm e^{-bt}}{(a-b)(c-b)}+\frac{\mathrm e^{-ct}}{(a-c)(b-c)}$ | $\frac{1}{(s+a)(s+b)(s+c)}$ | $\frac{z}{(b-a)(c-a)(z-\mathrm e^{-aT})}+\frac{z}{(a-b)(c-b)(z-\mathrm e^{-bT})}+\frac{z}{(a-c)(b-c)(z-\mathrm e^{-cT})}$ |
| $\frac{d-a}{(b-a)(c-a)}\mathrm e^{-at}+\frac{d-b}{(a-b)(c-b)}\mathrm e^{-bt}+\frac{d-c}{(a-c)(b-c)}\mathrm e^{-ct}$ | $\frac{s+d}{(s+a)(s+b)(s+c)}$ | $\frac{(d-a)z}{(b-a)(c-a)(z-\mathrm e^{-aT})}+\frac{(d-b)z}{(a-b)(c-b)(z-\mathrm e^{-bT})}+\frac{(d-c)z}{(a-c)(b-c)(z-\mathrm e^{-cT})}$ |
| $1-\frac{bc}{(b-a)(c-a)}\mathrm e^{-at}-\frac{ca}{(c-b)(a-b)}\mathrm e^{-bt}-\frac{ab}{(a-c)(b-c)}\mathrm e^{-ct}$ | $\frac{abc}{s(s+a)(s+b)(s+c)}$ | $\frac{z}{z-1}-\frac{bcz}{(b-a)(c-a)(z-\mathrm e^{-aT})}-\frac{caz}{(c-b)(a-b)(z-\mathrm e^{-bT})}-\frac{abz}{(a-c)(b-c)(z-\mathrm e^{-cT})}$ |
| $abt-(a+b)-\frac{b^2}{a-b}\mathrm e^{-at}+\frac{a^2}{a-b}\mathrm e^{-bt}$ | $\frac{a^2b^2}{s^2(s+a)(s+b)}$ | $\frac{abTz}{(z-1)^2}-\frac{(a+b)z}{z-1}-\frac{b^2z}{(a-b)(z-\mathrm e^{-aT})}+\frac{a^2z}{(a-b)(z-\mathrm e^{-bT})}$ |

## 📌 (2) 五条查表要点

1. **极点映射**：$s=-a\Rightarrow z=\mathrm e^{-aT}$、$s=0\Rightarrow z=1$——左栏每出现一个 $(s+a)$，右栏就出现一个 $(z-\mathrm e^{-aT})$（指数行、衰减振荡行、三极点行都守这条）。
2. **$s=0$ 的 $k$ 重极点会带出 $T^k$ 因子**：$\frac1{s^2}\to\frac{Tz}{(z-1)^2}$、$\frac1{s^3}\to\frac{T^2z(z+1)}{2(z-1)^3}$——这是"连续积分变成离散累加"的痕迹，**查右栏最容易漏这个 $T$**。
3. **两个"阶跃"别写反**：$\mathcal L[1(t)]=\frac1s$，而 $\mathcal Z[1(t)]=\frac{z}{z-1}$（不是 $\frac1{z-1}$）；$\mathcal Z[\mathrm e^{-at}]=\frac{z}{z-\mathrm e^{-aT}}$ 分子上的 $z$ 不能丢——部分分式法"除 $z$"的坑也在这个 $z$ 上。
4. **双曲行的分母是 $\cosh$ 不是 $\cos$**：$\frac{\omega}{s^2-\omega^2}$ 对应 $z^2-2z\cosh\omega T+1$，写成 $\cos$ 就把双曲信号当成振荡信号了。
5. **多极点行的系数就是留数**：$\frac{1}{(s+a)(s+b)(s+c)}$ 拆出的系数依次是 $\frac{1}{(b-a)(c-a)}$、$\frac{1}{(a-b)(c-b)}$、$\frac{1}{(a-c)(b-c)}$——分母是"该极点与其他极点之差的乘积"，**写成 $a-b$ 还是 $b-a$ 靠这条自检**（带 $t=0$ 验证三项之和为零最省事）。

> [!tip] 表里为什么有的格子不写式子
> $t^n$、$t^n\mathrm e^{-at}$ 的 z 变换带欧拉多项式，$n=2,3$ 的具体式子已在上面两行列出，工程上够用；**空着的那格不是漏抄，是本来就没有简式。**

> [!note] 教材原表把 $\frac{t^2}{2}\mathrm e^{-at}$ 那一格拆成两项写
> 上表给的是通分后的紧凑式，教材附录原表写的是分项式，两者恒等：
>
> $$
> \frac{T^2\mathrm e^{-aT}z}{2(z-\mathrm e^{-aT})^2}+\frac{T^2z\mathrm e^{-2aT}}{(z-\mathrm e^{-aT})^3}=\frac{T^2\mathrm e^{-aT}z(z+\mathrm e^{-aT})}{2(z-\mathrm e^{-aT})^3}
> $$
>
> 查表按紧凑式抄不容易错；碰到答案写成前一种，通分即可对上。

> [!note] $\frac{\mathrm e^{-at}-\mathrm e^{-bt}}{b-a}$ 与 $\frac{b-a}{(s+a)(s+b)}$ 是同一件事的两种配法
> 本表按教材原表配：$f(t)=\mathrm e^{-at}-\mathrm e^{-bt}$ 对 $F(s)=\frac{b-a}{(s+a)(s+b)}$；若把 $f(t)$ 除以 $b-a$（写成 $\frac{\mathrm e^{-at}-\mathrm e^{-bt}}{b-a}$），$F(s)$ 就是干净的 $\frac{1}{(s+a)(s+b)}$，$F(z)$ 也整体除以 $b-a$。**看题面给的是哪一个，别把因子漏在外头。**

> [!note] 合并后少了一列的原理在这儿
> 两张表能同行并列，是因为离散化只做一件事：**把每个 $s$ 域极点 $p$ 换成 $\mathrm e^{pT}$，并把 $s=0$ 处的重极点计数换成 $T^k$ 因子**。所以"左侧 $(s+a)$ 的幂次"与"右侧 $(z-\mathrm e^{-aT})$ 的幂次"始终一样。

> 相关：[[附录 z变换与离散化速查]]（$F(s)\to F(z)$ 换算表／ZOH 四行表·定理·留数法·判稳·稳态误差） · [[00-1 拉普拉斯变换定义、变换对与定理]]（拉氏定理与使用边界） · [[07-1 采样与z变换]]（§7.3 变换对表） · 速查 [[自动控制原理]]

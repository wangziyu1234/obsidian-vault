---
create: 2026-10-03
modify: 2026-10-06
tags: [知识点, 自动控制原理, 公式速查]
type: cheatsheet
cssclasses: [transform-reference]
aliases: [拉氏变换表, z变换表, 变换对速查, 变换对表, 常用变换对]
---

> 返回：[[附录目录]] | 原文：[[00 拉普拉斯变换（数学基础）]] · [[07 第7章 线性离散系统的分析与校正]] | 返回目录：[[自动控制原理]]

# 附录 拉氏变换表与 z 变换表

> [!abstract] 本讲定位
> 26 个拉氏与 z 变换对；常用短式在前，多极点与双曲函数在后。

[[#(1) 冲激、阶跃与幂函数|冲激与幂函数]] · [[#(2) 指数函数|指数]] · [[#(3) 三角函数|三角]] · [[#(4) 衰减振荡与组合信号|衰减与组合]]

[[#(5) 五条查表要点|查表要点]] · [[#(6) 多极点部分分式|多极点]] · [[#(7) 双曲函数|双曲]]

**单边变换；$T>0$；因果信号在 $t<0$ 时为零；各式按收敛范围使用，分母中的参数差非零。**

$$
F(s)=\int_0^\infty f(t)\mathrm e^{-st}\,dt
$$

$$
F(z)=\sum_{n=0}^{\infty}f(nT)z^{-n}
$$

## (1) 冲激、阶跃与幂函数

| $f(t)$ | 拉氏 $F(s)$ | z 变换 $F(z)$ |
| :-- | :-- | :-- |
| $\delta(t)$ | $1$ | $1$ |
| $\delta(t-nT)$ | $\mathrm e^{-nTs}$ | $z^{-n}$ |
| $1(t)$ | $\frac1s$ | $\frac{z}{z-1}$ |
| $t$ | $\frac1{s^2}$ | $\frac{Tz}{(z-1)^2}$ |
| $\frac{t^2}{2}$ | $\frac1{s^3}$ | $\frac{T^2z(z+1)}{2(z-1)^3}$ |
| $\frac{t^3}{6}$ | $\frac1{s^4}$ | $\frac{T^3z(z^2+4z+1)}{6(z-1)^4}$ |
| $t^n$ | $\frac{n!}{s^{n+1}}$ | 一般阶数未展开，低阶见上表 |

## (2) 指数函数

| $f(t)$ | 拉氏 $F(s)$ | z 变换 $F(z)$ |
| :-- | :-- | :-- |
| $a^{t/T}$ | $\frac{1}{s-\frac1T\ln a}$ | $\frac{z}{z-a}$ |
| $\mathrm e^{-at}$ | $\frac1{s+a}$ | $\frac{z}{z-\mathrm e^{-aT}}$ |
| $t\,\mathrm e^{-at}$ | $\frac1{(s+a)^2}$ | $\frac{T\mathrm e^{-aT}z}{(z-\mathrm e^{-aT})^2}$ |
| $\frac{t^2}{2}\mathrm e^{-at}$ | $\frac1{(s+a)^3}$ | $\frac{T^2\mathrm e^{-aT}z(z+\mathrm e^{-aT})}{2(z-\mathrm e^{-aT})^3}$ |
| $t^n\mathrm e^{-at}$ | $\frac{n!}{(s+a)^{n+1}}$ | 一般阶数未展开，低阶见上表 |
| $1-\mathrm e^{-at}$ | $\frac{a}{s(s+a)}$ | $\frac{(1-\mathrm e^{-aT})z}{(z-1)(z-\mathrm e^{-aT})}$ |

**首行 $a>0$；幂次 $n\in\mathbb N_0$。**

## (3) 三角函数

| $f(t)$ | 拉氏 $F(s)$ | z 变换 $F(z)$ |
| :-- | :-- | :-- |
| $\sin\omega t$ | $\frac{\omega}{s^2+\omega^2}$ | $\frac{z\sin\omega T}{z^2-2z\cos\omega T+1}$ |
| $\cos\omega t$ | $\frac{s}{s^2+\omega^2}$ | $\frac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}$ |

## (4) 衰减振荡与组合信号

**① 指数衰减正弦**

$$
f(t)=\mathrm e^{-at}\sin\omega t
$$

$$
F(s)=\frac{\omega}{(s+a)^2+\omega^2}
$$

$$
F(z)=\frac{z\mathrm e^{-aT}\sin\omega T}{z^2-2z\mathrm e^{-aT}\cos\omega T+\mathrm e^{-2aT}}
$$

---

**② 指数衰减余弦**

$$
f(t)=\mathrm e^{-at}\cos\omega t
$$

$$
F(s)=\frac{s+a}{(s+a)^2+\omega^2}
$$

$$
F(z)=\frac{z(z-\mathrm e^{-aT}\cos\omega T)}{z^2-2z\mathrm e^{-aT}\cos\omega T+\mathrm e^{-2aT}}
$$

---

**③ 斜坡减去指数过渡项（$a\ne0$）**

$$
f(t)=t-\frac1a(1-\mathrm e^{-at})
$$

$$
F(s)=\frac{a}{s^2(s+a)}
$$

$$
\begin{aligned}
F(z)&=\frac{Tz}{(z-1)^2}\\
&\quad-\frac{(1-\mathrm e^{-aT})z}{a(z-1)(z-\mathrm e^{-aT})}
\end{aligned}
$$

---

**④ 阶跃减去余弦**

$$
f(t)=1-\cos\omega t
$$

$$
F(s)=\frac{\omega^2}{s(s^2+\omega^2)}
$$

$$
\begin{aligned}
F(z)&=\frac{z}{z-1}\\
&\quad-\frac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}
\end{aligned}
$$

---

**⑤ 两个指数之差（$a\ne b$）**

$$
f(t)=\mathrm e^{-at}-\mathrm e^{-bt}
$$

$$
F(s)=\frac{b-a}{(s+a)(s+b)}
$$

$$
F(z)=\frac{z}{z-\mathrm e^{-aT}}-\frac{z}{z-\mathrm e^{-bT}}
$$

## (5) 五条查表要点

1. 按 $F(s)$ 或 $f(t)$ 定位；极点映射只校验分母，分子与系数照表。
2. $1/s^k$ 的采样周期因子为 $T^{k-1}$。
3. z 反变换：先除 $z$ → 部分分式展开 → 乘回 $z$ → 查表。
4. 三角项用 $\cos$，双曲项用 $\cosh$。
5. 第 (6) 节①：留数系数之和为零。

## (6) 多极点部分分式

**$a,b,c\in\mathbb R$ 且互异，$d\in\mathbb R$；分母中的参数差非零。**

**① 三个一阶因子 · 常数分子**

$$
F(s)=\frac{1}{(s+a)(s+b)(s+c)}
$$

$$
\begin{aligned}
f(t)&=\frac{\mathrm e^{-at}}{(b-a)(c-a)}\\
&\quad+\frac{\mathrm e^{-bt}}{(a-b)(c-b)}\\
&\quad+\frac{\mathrm e^{-ct}}{(a-c)(b-c)}
\end{aligned}
$$

$$
\begin{aligned}
F(z)&=\frac{z}{(b-a)(c-a)(z-\mathrm e^{-aT})}\\
&\quad+\frac{z}{(a-b)(c-b)(z-\mathrm e^{-bT})}\\
&\quad+\frac{z}{(a-c)(b-c)(z-\mathrm e^{-cT})}
\end{aligned}
$$

---

**② 三个一阶因子 · 一次分子**

$$
F(s)=\frac{s+d}{(s+a)(s+b)(s+c)}
$$

$$
\begin{aligned}
f(t)&=\frac{d-a}{(b-a)(c-a)}\mathrm e^{-at}\\
&\quad+\frac{d-b}{(a-b)(c-b)}\mathrm e^{-bt}\\
&\quad+\frac{d-c}{(a-c)(b-c)}\mathrm e^{-ct}
\end{aligned}
$$

$$
\begin{aligned}
F(z)&=\frac{(d-a)z}{(b-a)(c-a)(z-\mathrm e^{-aT})}\\
&\quad+\frac{(d-b)z}{(a-b)(c-b)(z-\mathrm e^{-bT})}\\
&\quad+\frac{(d-c)z}{(a-c)(b-c)(z-\mathrm e^{-cT})}
\end{aligned}
$$

---

**③ 一个积分因子与三个一阶因子**

$$
F(s)=\frac{abc}{s(s+a)(s+b)(s+c)}
$$

$$
\begin{aligned}
f(t)&=1\\
&\quad-\frac{bc}{(b-a)(c-a)}\mathrm e^{-at}\\
&\quad-\frac{ca}{(c-b)(a-b)}\mathrm e^{-bt}\\
&\quad-\frac{ab}{(a-c)(b-c)}\mathrm e^{-ct}
\end{aligned}
$$

$$
\begin{aligned}
F(z)&=\frac{z}{z-1}\\
&\quad-\frac{bcz}{(b-a)(c-a)(z-\mathrm e^{-aT})}\\
&\quad-\frac{caz}{(c-b)(a-b)(z-\mathrm e^{-bT})}\\
&\quad-\frac{abz}{(a-c)(b-c)(z-\mathrm e^{-cT})}
\end{aligned}
$$

---

**④ 二重积分因子与两个一阶因子（$a\ne b$）**

$$
F(s)=\frac{a^2b^2}{s^2(s+a)(s+b)}
$$

$$
\begin{aligned}
f(t)&=abt\\
&\quad-(a+b)\\
&\quad-\frac{b^2}{a-b}\mathrm e^{-at}\\
&\quad+\frac{a^2}{a-b}\mathrm e^{-bt}
\end{aligned}
$$

$$
\begin{aligned}
F(z)&=\frac{abTz}{(z-1)^2}\\
&\quad-\frac{(a+b)z}{z-1}\\
&\quad-\frac{b^2z}{(a-b)(z-\mathrm e^{-aT})}\\
&\quad+\frac{a^2z}{(a-b)(z-\mathrm e^{-bT})}
\end{aligned}
$$

## (7) 双曲函数

| $f(t)$ | 拉氏 $F(s)$ | z 变换 $F(z)$ |
| :-- | :-- | :-- |
| $\sinh\omega t$ | $\frac{\omega}{s^2-\omega^2}$ | $\frac{z\sinh\omega T}{z^2-2z\cosh\omega T+1}$ |
| $\cosh\omega t$ | $\frac{s}{s^2-\omega^2}$ | $\frac{z(z-\cosh\omega T)}{z^2-2z\cosh\omega T+1}$ |

---

> 相关：[[附录 z变换与离散化速查]] · [[00-1 拉普拉斯变换定义、变换对与定理]] · [[07-1 采样与z变换]] · [[自动控制原理]]

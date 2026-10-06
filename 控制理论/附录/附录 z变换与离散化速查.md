---
create: 2026-09-26
modify: 2026-10-06
tags: [知识点, 自动控制原理, 公式速查]
type: cheatsheet
cssclasses: [big-table]
aliases: [z变换速查, 离散化速查, 脉冲传递函数, ZOH, 差分方程]
---

> 返回：[[附录目录]] | 原文：[[07 第7章 线性离散系统的分析与校正]] | 返回目录：[[自动控制原理]]

# 附录 z 变换与离散化速查

> [!abstract] 本讲定位
> 采样变换、ZOH、差分方程、反变换、判稳与基本定理速查。

**约定**：单边 z 变换；$T>0$；$c[k]=f(kT)$；负序号零延拓。

| 要求 | 直达 |
| :-- | :-- |
| 无保持器的采样结果 | [[#🧮 (1) 常用变换与采样结果\|变换表]] |
| 带零阶保持器 | [[#📋 (2) 带零阶保持器的离散化\|ZOH]] |
| 差分方程与传函互写 | [[#🔁 (3) 差分方程与脉冲传函互化\|互化]] |
| 输出前几拍或通项 | [[#↩️ (4) 反变换与输出序列\|反变换]] |
| 判稳与稳态误差 | [[#✅ (5) 判稳与稳态误差\|判稳与误差]] |

[[#🧮 (6) 基本定理|基本定理]] · [[#⚠️ (7) 易错点清单|计算自检]] · [[#🧩 (8) 双曲函数与多极点|双曲与多极点]] · [[#⚙️ (9) 控制器离散化扩展|离散化]] · [[#📖 (10) 留数法|留数法]]

## 🧮 (1) 常用变换与采样结果

**步骤**：部分分式展开 → 逐项查表 → 相加。

| $F(s)$ | $F(z)$ |
| :-- | :-- |
| $\frac{1}{s}$ | $\frac{z}{z-1}$ |
| $\frac{1}{s^2}$ | $\frac{Tz}{(z-1)^2}$ |
| $\frac{1}{s^3}$ | $\frac{T^2z(z+1)}{2(z-1)^3}$ |
| $\frac{1}{s+a}$ | $\frac{z}{z-e^{-aT}}$ |
| $\frac{1}{(s+a)^2}$ | $\frac{Te^{-aT}z}{(z-e^{-aT})^2}$ |
| $\frac{1}{(s+a)^3}$ | $\frac{T^2e^{-aT}z(z+e^{-aT})}{2(z-e^{-aT})^3}$ |
| $\frac{a}{s(s+a)}$ | $\frac{(1-e^{-aT})z}{(z-1)(z-e^{-aT})}$ |
| $\frac{a}{s^2(s+a)}$ | $\frac{Tz}{(z-1)^2}-\frac{(1-e^{-aT})z}{a(z-1)(z-e^{-aT})}$ |
| $\frac{\omega}{s^2+\omega^2}$ | $\frac{z\sin\omega T}{z^2-2z\cos\omega T+1}$ |
| $\frac{s}{s^2+\omega^2}$ | $\frac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}$ |
| $\frac{\omega^2}{s(s^2+\omega^2)}$ | $\frac{z}{z-1}-\frac{z(z-\cos\omega T)}{z^2-2z\cos\omega T+1}$ |
| $\frac{\omega}{(s+a)^2+\omega^2}$ | $\frac{ze^{-aT}\sin\omega T}{z^2-2ze^{-aT}\cos\omega T+e^{-2aT}}$ |
| $\frac{s+a}{(s+a)^2+\omega^2}$ | $\frac{z(z-e^{-aT}\cos\omega T)}{z^2-2ze^{-aT}\cos\omega T+e^{-2aT}}$ |
| $\frac{b-a}{(s+a)(s+b)}$ | $\frac{z}{z-e^{-aT}}-\frac{z}{z-e^{-bT}}$ |

## 📋 (2) 带零阶保持器的离散化

**ZOH；零初值。**

$$
\begin{aligned}
G_d(z)&=\left(1-z^{-1}\right)\mathcal Z\left[\frac{G(s)}{s}\right]\\
&=\frac{z-1}{z}\,\mathcal Z\Bigl[\mathcal L^{-1}\Bigl\{\frac{G(s)}{s}\Bigr\}_{t=kT}\Bigr]
\end{aligned}
$$

**参数**：含 $a$ 的两式取 $a\ne0$；$a=0$ 分别查 $K/s$、$K/s^2$。

| $G(s)$ | $G_d(z)$ |
| :-- | :-- |
| $\frac{K}{s}$ | $\frac{KT}{z-1}$ |
| $\frac{K}{s+a}$ | $\frac{K\left(1-e^{-aT}\right)}{a\left(z-e^{-aT}\right)}$ |
| $\frac{K}{s^2}$ | $\frac{KT^2(z+1)}{2(z-1)^2}$ |

**积分与惯性环节串联**

$$
G(s)=\frac{K}{s(s+a)}
$$

$$
\begin{aligned}
G_d(z)&=\frac{K}{a^2(z-1)(z-e^{-aT})}\\
&\quad\cdot\Bigl[\left(aT-1+e^{-aT}\right)z\\
&\qquad+\left(1-e^{-aT}-aTe^{-aT}\right)\Bigr]
\end{aligned}
$$

## 🔁 (3) 差分方程与脉冲传函互化

$$
c[k]+a_1c[k-1]+\cdots+a_nc[k-n]=b_0r[k]+b_1r[k-1]+\cdots+b_mr[k-m]
$$

**零初值；滞后 $i$ 拍对应 $z^{-i}$。**

$$
G(z)=\frac{C(z)}{R(z)}=\frac{b_0+b_1z^{-1}+\cdots+b_mz^{-m}}{1+a_1z^{-1}+\cdots+a_nz^{-n}}
$$

**正幂式**：分子分母同乘 $z^{\max(m,n)}$。

**反求差分方程**：化为 $z^{-1}$ 幂次 → 交叉相乘 → 读出各拍。

## ↩️ (4) 反变换与输出序列

| 方法 | 必要步骤 | 适用 |
| :-- | :-- | :-- |
| 长除法 | 按 $z^{-1}$ 升幂相除 → 依次读 $c[0],c[1],c[2],\dots$ | 前几拍 |
| 部分分式 | 先除 $z$ → 展开 → 乘回 $z$ → 查表 | 闭式通项 |
| 留数法 | $c[k]=\sum\operatorname{Res}\bigl[F(z)z^{k-1}\bigr]$ | 重极点或通项 |

## ✅ (5) 判稳与稳态误差

**渐近稳定**：闭环特征根 $\lvert z_i\rvert<1$。

**二阶实系数式**：$F(z)=z^2+a_1z+a_0$；稳定 ⟺ $F(1)>0$、$F(-1)>0$、$\lvert a_0\rvert<1$。

**高阶**：$z=\dfrac{w+1}{w-1}$（即 $w=\dfrac{z+1}{z-1}$），则 $\lvert z\rvert<1\Leftrightarrow\operatorname{Re}w<0$；变换后用劳斯判据。

**采样稳态误差**：单位负反馈、闭环稳定；有限值须满足第 (6) 节终值条件。$G(z)$ 为开环脉冲传函。

$$
K_p=\lim_{z\to1}\bigl[1+G(z)\bigr]
$$

$$
K_v=\lim_{z\to1}(z-1)G(z)
$$

$$
K_a=\lim_{z\to1}(z-1)^2G(z)
$$

| 型别 | 阶跃 $A\cdot1(t)$ | 斜坡 $At$ | 加速度 $\frac{A}{2}t^2$ |
| :-- | :-- | :-- | :-- |
| 0 型 | $\frac{A}{K_p}$ | $\infty$ | $\infty$ |
| Ⅰ 型 | $0$ | $\frac{AT}{K_v}$ | $\infty$ |
| Ⅱ 型 | $0$ | $0$ | $\frac{AT^2}{K_a}$ |

## 🧮 (6) 基本定理

**单边、因果；$m\in\mathbb N_0$，$c[k]=f(kT)$。**

$$
C(z)=\sum\limits_{k=0}^{\infty}c[k]z^{-k}
$$

**线性**

$$
\mathcal Z\bigl\{a\,c_1[k]+b\,c_2[k]\bigr\}=aC_1(z)+bC_2(z)
$$

**滞后 / 超前 $m$ 拍**

$$
\mathcal Z\bigl[c(k-m)\bigr]=z^{-m}C(z)
$$

$$
\mathcal Z\bigl[c(k+m)\bigr]=z^{m}\Bigl[C(z)-c[0]-c[1]z^{-1}-\cdots-c[m-1]z^{-(m-1)}\Bigr]
$$

**连续写法**

$$
\mathcal Z\bigl[f(t-mT)\bigr]=z^{-m}F(z)
$$

$$
\mathcal Z\bigl[f(t+mT)\bigr]=z^{m}\Bigl[F(z)-f(0)-f(T)z^{-1}-\cdots-f\bigl((m-1)T\bigr)z^{-(m-1)}\Bigr]
$$

**复位移；$\lambda\ne0$。**

$$
\mathcal Z\bigl\{\lambda^{k}c[k]\bigr\}=C\!\left(\frac z\lambda\right)
$$

**$\lambda=e^{\mp aT}$。**

$$
\mathcal Z\bigl[e^{\mp at}f(t)\bigr]=F\bigl(ze^{\pm aT}\bigr)
$$

**初值**

$$
c[0]=\lim_{z\to\infty}C(z)
$$

**终值：约分后 $(z-1)C(z)$ 的全部极点严格在单位圆内。**

$$
\lim_{k\to\infty}c[k]=\lim_{z\to1}(z-1)C(z)
$$

**卷积**

$$
\mathcal Z\bigl\{c_1[k]*c_2[k]\bigr\}=C_1(z)C_2(z)
$$

## ⚠️ (7) 易错点清单

- 无保持器查第 (1) 节；ZOH 先除 $s$，变换后乘 $(1-z^{-1})$。
- 超前位移保留初值项；差分方程求传函取零初值。
- 离散 $K_p$ 含 $1$；误差中的 $T,T^2$ 不并入 $K_v,K_a$。
- 多极点部分分式：检查参数差、符号与系数。

## 🧩 (8) 双曲函数与多极点

**双曲函数**

| $F(s)$ | $F(z)$ |
| :-- | :-- |
| $\frac{\omega}{s^2-\omega^2}$ | $\frac{z\sinh\omega T}{z^2-2z\cosh\omega T+1}$ |
| $\frac{s}{s^2-\omega^2}$ | $\frac{z(z-\cosh\omega T)}{z^2-2z\cosh\omega T+1}$ |

**多极点部分分式**

![[附录 拉氏变换表与z变换表#(6) 多极点部分分式]]

自检： [[附录 拉氏变换表与z变换表#(5) 五条查表要点|五条查表要点]]。

## ⚙️ (9) 控制器离散化扩展

**$T>0$；预畸变指定频率 $0<\omega_0<\pi/T$。**

| 方法 | 替换式 |
| :-- | :-- |
| 前向差分（欧拉） | $s=\frac{z-1}{T}$ |
| 后向差分 | $s=\frac{z-1}{Tz}$ |
| 双线性（Tustin） | $s=\frac{2}{T}\cdot\frac{z-1}{z+1}$ |
| 预畸变双线性 | $s=\frac{\omega_0}{\tan\left(\omega_0T/2\right)}\cdot\frac{z-1}{z+1}$ |
| 零极点匹配 | $z=e^{sT}$，增益按静态增益配 |
| 阶跃响应不变（ZOH） | $G_d=(1-z^{-1})\mathcal Z\bigl[\frac{G(s)}{s}\bigr]$ |
| 脉冲响应不变 | $G_d=T\,\mathcal Z\bigl[G(s)\bigr]$ |

**双线性频率换算**：$s=\mathrm j\omega_a$，$z=e^{\mathrm j\omega T}$；连续频率 $\omega_a$、离散等效角频率 $\omega$，$|\omega|<\pi/T$。

$$
\omega_a=\frac{2}{T}\tan\frac{\omega T}{2}
$$

$$
\omega=\frac{2}{T}\arctan\frac{\omega_aT}{2}
$$

数字 PID：[[07-3-c 数字PID与控制器离散化]]。

## 📖 (10) 留数法

**$p_i$ 为 $F(s)$ 的极点；$m$ 重极点取 $m$ 重留数。**

$$
F(z)=\sum_i\operatorname{Res}_{s=p_i}\left[F(s)\,\frac{z}{z-e^{sT}}\right]
$$

推导与例题：[[07-1-b z变换计算与反变换例题]] · [[07-1-c 采样与z变换综合例题]]。

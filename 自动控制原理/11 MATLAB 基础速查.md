---
create: 2026-07-25
modify: 2026-07-26
tags: [知识点, 自动控制原理, 公式速查]
---

> 返回目录：[[自动控制原理]]

# MATLAB 基础速查（对应教材附录 B）

> [!info] ℹ️
> 只列基础命令，按"建模 → 连接 → 分析"三步使用；命令均出自教材附录 B。离散模型在建模命令末尾多传采样周期 `Ts`。

**① 建模与模型转换**

| 用途 | 命令 |
| :-- | :-- |
| 传递函数模型 | `sys = tf(num, den)`——num/den 为分子/分母**降幂**系数向量，如 `tf([1],[1 1 0])` ↔ $\dfrac{1}{s^2+s}$ |
| 因式相乘展开 | `den = conv([0.1 1],[1 3])`（多项式卷积 = 相乘） |
| 零极点模型 | `sys = zpk(z, p, k)`——零/极点向量与增益，无零点用 `[]`，如 `zpk([-2],[0 -1],1)` |
| 状态空间模型 | `sys = ss(A, B, C, D)` |
| 模型互转 | `[z,p,k] = tf2zp(num,den)`、`[num,den] = zp2tf(z,p,k)`、`[A,B,C,D] = tf2ss(num,den)` |
| 连续 → 离散 | `sysd = c2d(sys, Ts, 'zoh')`（零阶保持器离散化，第 7 章求 $G(z)$ 可代替查表） |
| 最小实现 | `sysr = minreal(sys)`（自动消零极点对消，验证"最小实现⇔能控能观"） |

**② 结构图连接**：串联 `series(G1,G2)`（等价 `G1*G2`）、并联 `parallel(G1,G2)`（等价 `G1+G2`）、反馈 `feedback(G,H,sign)`——`sign` 缺省为 $-1$（负反馈），单位负反馈闭环即 `feedback(G,1)`。

**③ 分章分析命令**

| 章 | 任务 | 命令 |
| :-- | :-- | :-- |
| 3 | 阶跃 / 脉冲 / 任意输入 / 零输入响应 | `step(sys)`、`impulse(sys)`、`lsim(sys,u,t,x0)`、`initial(sys,x0,t)` |
| 3 | 特征根 / 零极点分布 | `roots(den)`、`pzmap(sys)`、`eig(A)` |
| 4 | 根轨迹 | `rlocus(G)`（图上单击轨迹可读出该点 $K^*$ 与闭环极点） |
| 5 | Bode / 奈氏 / 尼科尔斯图 | `bode(sys)`、`nyquist(sys)`、`nichols(sys)` |
| 5 | 稳定裕度 | `[Gm,Pm,Wcg,Wcp] = margin(sys)`——$Gm=h$（**倍数**，$20\lg Gm$ 才是 dB 值）、$Pm=\gamma$、$Wcg=\omega_g$、$Wcp=\omega_c$ |
| 7 | 离散系统响应 | `c2d` 离散化后直接 `step(sysd)` 等 |
| 8 | 非线性方程数值解（画相轨迹） | `[t,x] = ode45(@fun, t, x0)`（推荐用函数句柄 `@fun`，旧式字符串传函数已弃用） |
| 9 | 可控 / 可观判定 | `S = ctrb(A,B)`、`V = obsv(A,C)`，再 `rank(S)`、`rank(V)` 与 $n$ 比较 |
| 9 | 结构分解 | `[Ac,Bc,Cc,T] = ctrbf(A,B,C)`（按可控性）、`obsvf(...)`（按可观测性） |
| 9 | 极点配置 | `K = place(A,B,P)` 或 `K = acker(A,b,P)`——`P` 为期望极点向量；观测器增益用对偶：`L = acker(A',C',P)'` |
| 9 | 李雅普诺夫方程 | `P = lyap(A',Q)` |

> [!warning] ⚠️ 两个易错
> ① `margin` 返回的幅值裕度 `Gm` 是**倍数**不是 dB，报告 $h(\mathrm{dB})=20\lg Gm$。
> ② MATLAB 的 `lyap(M,Q)` 解的是 $MX+XM^{T}=-Q$，所以求 $A^TP+PA=-Q$ 必须传**转置** `lyap(A',Q)`（教材附录 B 同此写法）。

---
create: 2026-07-25
modify: 2026-07-26
tags: [知识点, 自动控制原理, 公式速查]
---

> 返回目录：[[自动控制原理]]

# MATLAB 基础速查（对应教材附录 B）

> [!abstract] 本讲定位
> MATLAB 基础命令速查（对应教材附录 B），按「建模 → 连接 → 分析」三步组织。

> [!info]
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
| 离散 → 连续 | `sysc = d2c(sysd)`（与 `c2d` 互逆；也可 `d2c(sysd,'zoh')` 指定保持器） |
| 最小实现 | `sysr = minreal(sys)`（自动消零极点对消，验证"最小实现⇔能控能观"） |
| 部分分式展开 | `[r,p,k] = residue(num,den)`（$\dfrac{\text{num}}{\text{den}}=\sum\dfrac{r_i}{s-p_i}+k$，拉氏反变换直接查表，00 章配） |
| 延迟环节有理近似 | `sysp = pade(sys, n)`（$e^{-Ts}$ 用 $n$ 阶 Pade 逼近，含纯延迟系统频域/奈氏分析用） |
| 相似变换 | `sysT = ss2ss(sys, T)`（$x_\text{新}=T\,x_\text{旧}$ 坐标变换，现控 2.6 线性变换） |
| 标准型变换 | `csys = canon(sys,'companion')`（能控标准型）、`msys = canon(sys,'modal')`（约当/对角型，现控 2.3/2.5） |

**② 结构图连接**：串联 `series(G1,G2)`（等价 `G1*G2`）、并联 `parallel(G1,G2)`（等价 `G1+G2`）、反馈 `feedback(G,H,sign)`——`sign` 缺省为 $-1$（负反馈），**正反馈用 `feedback(G,H,+1)`**；单位负反馈闭环即 `feedback(G,1)`。

**③ 分章分析命令**

| 章 | 任务 | 命令 |
| :-- | :-- | :-- |
| 3 | 阶跃 / 脉冲 / 任意输入 / 零输入响应 | `step(sys)`、`impulse(sys)`、`lsim(sys,u,t,x0)`、`initial(sys,x0,t)`；配合 `gensig` 生成正弦/方波测试信号：`[u,t] = gensig('sin', Tp, Tf)` |
| 3 | 特征根 / 零极点分布 | `roots(den)`、`pzmap(sys)`、`eig(A)` |
| 3 | 阻尼比 / 自然频率 | `[Wn,Zeta] = damp(sys)`（三阶及以上直接给出各极点对应 $\zeta,\omega_n$，判别欠/过阻尼） |
| 3 | 阶跃性能指标 | `S = stepinfo(sys)`——`S.Peak`（$M_p$）、`S.PeakTime`（$t_p$）、`S.SettlingTime`（$t_s$，2%）、`S.RiseTime`（$t_r$）、`S.Overshoot`（$\sigma\%$） |
| 3 | 稳态增益 | `K = dcgain(sys)`（$=\lim_{s\to0}G(s)$，求静态误差系数/终值用） |
| 4 | 根轨迹 | `rlocus(G)`（图上单击轨迹可读出该点 $K^*$ 与闭环极点） |
| 4 | 根轨迹选点求 $K^*$ | `[K,p] = rlocfind(G)`（需先画出 `rlocus` 图，再在图窗单击轨迹，返回该点增益与闭环极点） |
| 4 | 等 $\zeta$ / 等 $\omega_n$ 网格 | `sgrid`（叠加网格，配 rlocus 按阻尼比/频率定主导极点） |
| 5 | Bode / 奈氏 / 尼科尔斯图 | `bode(sys)`、`nyquist(sys)`、`nichols(sys)` |
| 5 | 稳定裕度 | `[Gm,Pm,Wcg,Wcp] = margin(sys)`——$Gm=h$（**倍数**，$20\lg Gm$ 才是 dB 值）、$Pm=\gamma$、$Wcg=\omega_g$、$Wcp=\omega_c$ |
| 5 | 带宽 | `Wb = bandwidth(sys)`（幅值降 3 dB 处频率；也可 `bandwidth(sys,dbdrop)`） |
| 5 | 指定频率点频率响应 | `H = freqresp(sys, w)`（任意 $\omega$ 的复数响应，验证奈氏穿越点/谐振点） |
| 7 | 离散系统响应 | `c2d` 离散化后直接 `step(sysd)`，或经典命令 `dstep(sysd)` / `dimpulse(sysd)` |
| 7 | 离散等 $\zeta$ / 等 $\omega_n$ 网格 | `zgrid`（z 域网格，配离散根轨迹 `rlocus(sysd)` 用） |
| 8 | 非线性方程数值解（画相轨迹） | `[t,x] = ode45(@fun, t, x0)`（推荐用函数句柄 `@fun`，旧式字符串传函数已弃用） |
| 9 | 可控 / 可观判定 | `S = ctrb(A,B)`、`V = obsv(A,C)`，再 `rank(S)`、`rank(V)` 与 $n$ 比较 |
| 9 | 可控性 / 可观性格拉姆矩阵 | `Wc = gram(sys,'c')`、`Wo = gram(sys,'o')`（对应现控 4.1.4 格拉姆判据；奇异时判不完全能控/可观） |
| 9 | 矩阵指数 $e^{At}$ | `Phi = expm(A*t)`（数值计算，与现控 3 章拉氏/对角化/凯莱-哈密顿三法对照） |
| 9 | 结构分解 | `[Ac,Bc,Cc,T] = ctrbf(A,B,C)`（按可控性）、`obsvf(...)`（按可观测性） |
| 9 | 极点配置 | `K = place(A,B,P)` 或 `K = acker(A,b,P)`——`P` 为期望极点向量；观测器增益用对偶：`L = acker(A',C',P)'` |
| 9 | 李雅普诺夫方程 | `P = lyap(A',Q)` |

> [!warning] 四个易错
> ① `margin` 返回的幅值裕度 `Gm` 是**倍数**不是 dB，报告 $h(\mathrm{dB})=20\lg Gm$。
> ② MATLAB 的 `lyap(M,Q)` 解的是 $MX+XM^{T}=-Q$，所以求 $A^TP+PA=-Q$ 必须传**转置** `lyap(A',Q)`（教材附录 B 同此写法）。
> ③ `acker` 只适用于 **SISO** 且对重极点敏感（数值不稳），多输入/重极点优先用 `place`。
> ④ `ss2ss(sys,T)` 中 $T$ 是 $x_\text{新}=T\,x_\text{旧}$——方向反了会得到错误状态方程；`canon` 的 `'companion'` 输出为能控标准型（对照现控 2.5 记号时注意）。

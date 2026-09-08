---
create: 2026-07-25
modify: 2026-09-09
tags: [知识点, 自动控制原理, 公式速查]
---

> 返回目录：[[自动控制原理]]

# MATLAB 基础速查（对应教材附录 B）

> [!abstract] 本讲定位
> 按“建模 → 连接 → 分析 → 回验”查命令；对应教材附录 B 的分析任务，并注明 MATLAB 指标口径、模型类型与函数限制。

## 🔧 建模与模型转换

| 用途 | 命令与条件 |
|:--|:--|
| 传递函数 | `sys = tf(num,den)`；系数按降幂排列，例如 `tf(1,[1 1 0])` 表示 $\frac{1}{s^2+s}$ |
| 因式相乘 | `den = conv([0.1 1],[1 3])` |
| 零极点模型 | `sys = zpk(z,p,k)`；无零点用 `[]` |
| 状态空间 | `sys = ss(A,B,C,D)`；离散模型增加采样周期 `Ts` |
| 模型互转 | `tf2zp`、`zp2tf`、`tf2ss`；LTI 对象可直接用 `tf(sys)`、`ss(sys)`、`zpk(sys)` |
| 连续 → 离散 | `sysd = c2d(sys,Ts,'zoh')`，对应零阶保持输入假设 |
| 离散 → 连续 | `sysc = d2c(sysd,'zoh')`；是指定方法下的等效还原，**不是无条件唯一的逆运算** |
| 最小实现 | `sysr = minreal(sys)`；注意数值容差，不要据简化后的模型掩盖内部不稳定模态 |
| 部分分式 | `[r,p,k] = residue(num,den)`；重极点对应高次分母，`k` 是直项多项式的系数向量，不一定是常数 |
| 纯延迟近似 | `sysp = pade(sys,n)`；用于含时延模型的 $n$ 阶有理近似，不能当成精确时延 |
| 坐标变换 | `sysT = ss2ss(sys,T)`，约定 $x_{\rm 新}=T x_{\rm 旧}$ |
| 标准型 | `csys = canon(sys,'companion')`；查看实际返回的 `A,B,C,D`，不要预设输入/输出向量 |
| 模态形式 | `msys = canon(sys,'modal')`；实模态块与复极点的实二阶块，不能一概当成任意系统的对角阵 |

> [!note] 连续与离散模型要分清
> `tf`、`zpk`、`ss` 的离散形式需提供 `Ts`；采样只保留采样点信息，$z=e^{sT}$ 的反求存在频率混叠，不能由 `d2c` 无条件恢复唯一的原连续系统。

## 🔗 结构图连接

- **串联**：输入先经过 `G1`，再经过 `G2`，用 `series(G1,G2)`。SISO 可写 `G1*G2`；MIMO 的矩阵乘法次序是 `G2*G1`。
- **并联**：`parallel(G1,G2)`，即维数相容时的 `G1+G2`。
- **反馈**：`feedback(G,H)` 默认负反馈；正反馈用 `feedback(G,H,+1)`。
- **单位负反馈**：`Phi = feedback(G,1)`。先分清传入的是开环 `G` 还是闭环 `Phi`。

## 📊 分章分析命令

| 章 | 任务 | 命令与条件 |
|:--|:--|:--|
| 3 | 阶跃 / 脉冲 / 任意输入 | `step(sys)`、`impulse(sys)`、`lsim(sys,u,t)` |
| 3 | 非零初始状态 | `lsim(sys,u,t,x0)`、`initial(sys,x0,t)`；`x0` 必须属于所用状态空间模型的坐标 |
| 3 | 生成测试输入 | `[u,t] = gensig('sin',Tp,Tf)` |
| 3 | 特征根 / 零极点 | `roots(den)`、`pzmap(sys)`、`eig(A)` |
| 3 | 极点的阻尼参数 | `[Wn,Zeta,p] = damp(sys)`；按**每个极点**输出，不能直接据此给整个高阶系统定阻尼类型 |
| 3 | 阶跃指标 | `S = stepinfo(sys)`；`Peak` 为峰值，`Overshoot` 为超调百分数，另有 `PeakTime`、`SettlingTime`、`RiseTime` |
| 3/7 | 直流增益 | `dcgain(sys)`；连续模型在 $s=0$，离散模型在 $z=1$ 求值；稳态解释仍需稳定性条件 |
| 4 | 根轨迹 | `rlocus(G)`；`[K,p] = rlocfind(G)` 可在图中选点求增益 |
| 4 | 连续极点网格 | `sgrid`，等阻尼比/等自然频率网格 |
| 5 | 频率特性 | `bode(sys)`、`nyquist(sys)`、`nichols(sys)` |
| 5 | 稳定裕度 | `[Gm,Pm,Wcg,Wcp] = margin(G)`；`Gm` 为倍数，`Pm` 为度，`Wcg` 为相位穿越频率，`Wcp` 为增益交越频率 |
| 5 | 闭环带宽 | `Wb = bandwidth(Phi)`；相对闭环**直流幅值**下降 3 dB 的频率 |
| 5 | 指定频率响应 | `H = freqresp(sys,w)`，返回复数响应，单位通常为 rad/s |
| 7 | 离散响应 | 对 `sysd` 直接使用 `step`、`impulse`、`lsim`；不要把旧式 `dstep`/`dimpulse` 当作 LTI 对象接口 |
| 7 | 离散极点网格 | `zgrid`，可配合 `rlocus(sysd)` |
| 8 | 非线性微分方程 | `[t,x] = ode45(@fun,tspan,x0)`；函数句柄见 [[08-1 非线性系统基本概念与相平面法\|相平面法]] |
| 9 | 能控 / 能观判据 | `rank(ctrb(A,B))`、`rank(obsv(A,C))` 与状态维数 $n$ 比较 |
| 9 | 格拉姆矩阵 | `gram(sys,'c')`、`gram(sys,'o')` 返回稳定模型的无限时域格拉姆矩阵；不稳定系统不要直接套此接口 |
| 9 | 状态转移矩阵 | `expm(A*t)`，见 [[控制理论/现代控制理论/02 状态空间表达式的解\|状态空间解]] |
| 9 | 结构分解 | `[Ac,Bc,Cc,T] = ctrbf(A,B,C)`，可观测分解用 `obsvf` |
| 9 | 极点配置 | `K = place(A,B,P)`；单输入也可用 `acker(A,b,P)`；观测器用对偶 `L = place(A',C',P)'` |
| 9 | 李雅普诺夫方程 | `P = lyap(A',Q)`，解 $A^TP+PA=-Q$ |

## ⚠️ 口径与适用条件

> [!warning] `stepinfo` 默认值不等于教材所有口径
> 默认上升时间按最终变化量的 **10%–90%** 计算，调节时间默认 **2%** 误差带。与欠阻尼二阶系统“首次到达终值”的上升时间、或 5% 调节时间比较时，要显式设置参数。

```matlab
Phi = tf(4,[1 2 4]);
S = stepinfo(Phi,'RiseTimeLimits',[0 1], ...
    'SettlingTimeThreshold',0.05);
```

这里的 0%–100% 上升时间用于会在有限时间到达终值的响应；单调渐近响应通常仍用 10%–90% 口径。性能公式见 [[03-2 二阶系统的动态指标与极点位置]]。

> [!warning] `damp` 的两个“1”不代表临界阻尼
> 对 `tf(1,[1 3 2])`，极点为 $-1,-2$，`damp` 对两个负实极点均给出阻尼参数 1；但二阶分母的整体阻尼比为 $\frac{3}{2\sqrt2}>1$，系统是过阻尼而不是临界阻尼。见 [[04-2-4 开环重极点与闭环临界阻尼]]。

> [!warning] 裕度、重根与李雅普诺夫方程
> - 幅值裕度换算为 dB：$h_{\rm dB}=20\lg Gm$；若存在多个交越点，结合完整奈氏曲线或 `allmargin` 判断，勿仅凭一个正裕度判稳。
> - `place` 不能配置重数超过 `rank(B)` 的极点；`acker` 用于单输入。重根设计可比较特征多项式系数，再用 `eig(A-B*K)` 回验。
> - `lyap(M,Q)` 解 $MX+XM^T=-Q$，因此此处必须传 `A'`。当 $A$ 渐近稳定且 $Q>0$ 时，所得对称解 $P>0$。

## 🧪 标准型反例与回验

> [!example] ✏️ `canon` 不能固定写成 $C=e_n^T$
> 对 $G(s)=\frac{2s+3}{s^2+4s+5}$，在 MATLAB R2026a 执行：
>
> ```matlab
> sys = ss(tf([2 3],[1 4 5]));
> csys = canon(sys,'companion');
> [A,B,C,D] = ssdata(csys);
> ```
>
> 得到
>
> $$
> A=\begin{bmatrix}0&-5\\1&-4\end{bmatrix}
> $$
>
> $$
> B=\begin{bmatrix}1\\0\end{bmatrix}
> $$
>
> $$
> C=\begin{bmatrix}2&-5\end{bmatrix}
> $$
>
> $$
> D=0
> $$
>
> 此时 $C\ne e_2^T$；直接验证
>
> $$
> C(sE-A)^{-1}B+D=\frac{2s+3}{s^2+4s+5}
> $$
>
> 所以“$A$ 系数在末列”不意味着 $B,C$ 都固定，也不能只凭 $A$ 的外观就套用教材另一种能控/能观标准型。

> [!tip] 每次变换都回验
> 坐标变换检查 $A_{\rm 新}=TAT^{-1}$、$B_{\rm 新}=TB$、$C_{\rm 新}=CT^{-1}$；传函用 `tf(sys)` 对照，反馈用 `eig(A-B*K)` 对照，李雅普诺夫方程检查残差 `A'*P+P*A+Q`。

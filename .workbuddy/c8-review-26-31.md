**8-26　解析**（2021 年广东工业大学，考点：新定义的描述函数问题，难度 ★★☆）

解：按原题结构图，线性部分为

$$
G(s)=\frac4{s^2+2s+4}.
$$

（1）先求负倒描述函数。

$$
N(A)=\frac{A+\mathrm jb}{A^2+b^2}.
$$

$$
-\frac1{N(A)}=-A+\mathrm jb.
$$

因此，固定 $b<0$ 时，负倒描述函数轨迹是从 $\mathrm jb$ 向左延伸的水平射线；随 $A$ 增大向左移动。非零自振要求 $A>0$，不能将射线起点算作自振。

令

$$
D(\omega)=(4-\omega^2)^2+4\omega^2.
$$

则

$$
G(\mathrm j\omega)
=\frac{4(4-\omega^2)}{D(\omega)}
-\mathrm j\frac{8\omega}{D(\omega)}.
$$

交点的实部为 $-A<0$，故只需研究 $\omega>2$ 的一段，不能把右半平面的曲线也算入。

$$
G(\mathrm j2)=-\mathrm j.
$$

$$
\lim_{\omega\to\infty}G(\mathrm j\omega)=0.
$$

为确认此段虚部没有折返，令

$$
v(\omega)=-\operatorname{Im}G(\mathrm j\omega)
=\frac{8\omega}{\omega^4-4\omega^2+16}.
$$

$$
v'(\omega)=
\frac{8(-3\omega^4+4\omega^2+16)}{(\omega^4-4\omega^2+16)^2}<0,
\qquad \omega>2.
$$

于是 $\operatorname{Im}G$ 在这一段从 $-1$ 严格增至 $0$，与水平射线恰有一个正振幅交点的条件为

$$
\boxed{-1<b<0}.
$$

交点稳定性也须检查。相位平衡给出

$$
A=\frac{(-b)(\omega^2-4)}{2\omega},
\qquad \omega>2.
$$

右端随 $\omega$ 严格增大；在满足相位平衡的频率上，环路幅值为

$$
\lvert N(A)G(\mathrm j\omega)\rvert
=\frac{v(\omega)}{-b}.
$$

由于 $v$ 随频率递减，振幅略增时环路幅值小于1、振幅趋于减小；振幅略减时环路幅值大于1、振幅趋于增大。因此描述函数法预测该交点为稳定自振点。

当 $b=-1$ 时，交点为 $A=0$、$\omega=2$，不是非零周期运动；$b<-1$ 或 $b\ge0$ 均不属于上述自振范围（原题本就限定 $b<0$）。

（2）$b=-0.5=-\frac12$ 在上述范围内，因此预测存在稳定自振。原题仅要求列方程，可写成

$$
\begin{cases}
\dfrac{8\omega}{(4-\omega^2)^2+4\omega^2}=\dfrac12,\\[6pt]
A=\dfrac{4(\omega^2-4)}{(4-\omega^2)^2+4\omega^2},
\end{cases}
\qquad \omega>2.
$$

也可以化为适合手算保留的形式：

$$
\boxed{\omega^4-4\omega^2-16\omega+16=0,
\qquad \omega>2}.
$$

$$
\boxed{A=\frac{\omega^2-4}{4\omega}}.
$$

由前述单调性，此区间内频率根唯一，无须用计算器求小数或写四次方程根式。

> [!tip] 本题关键
> “曲线有交点”还须满足 $A>0$；先由实部筛出 $\omega>2$，再讨论参数范围，能避免把零振幅边界或错误频率根当作自振。

**8-27　解析**（2024 年杭州电子科技大学，考点：新定义的描述函数问题，难度 ★★☆）

解：描述函数为正实数，定义域为 $A>0$。

$$
N(A)=A+\frac1A.
$$

$$
-\frac1{N(A)}=-\frac{A}{A^2+1}.
$$

该轨迹在负实轴上：随 $A$ 从0增至1，由 $0^-$ 移到 $-\frac12$；随 $A$ 从1增至无穷，再返回 $0^-$。因此同一几何交点可能对应两个不同振幅。

线性部分为

$$
G(s)=\frac{\frac12}{s(s+1)(4s+1)}.
$$

其频率响应的分母为

$$
(\mathrm j\omega)(1+\mathrm j\omega)(1+4\mathrm j\omega)
=-5\omega^2+\mathrm j\omega(1-4\omega^2).
$$

令虚部为0，取正频率，得到

$$
\omega_x=\frac12\,\mathrm{rad/s}.
$$

$$
G\left(\mathrm j\frac12\right)=-\frac25.
$$

由幅值平衡求所有候选振幅：

$$
\frac{A}{A^2+1}=\frac25.
$$

$$
2A^2-5A+2=0.
$$

$$
(2A-1)(A-2)=0.
$$

$$
A_1=\frac12,\qquad A_2=2.
$$

不能只凭“大振幅”或图上的字母给两根判稳。把描述函数暂视为实增益 $n>0$，闭环特征方程为

$$
4s^3+5s^2+s+\frac n2=0.
$$

由三阶劳斯条件得

$$
5>4\cdot\frac n2.
$$

即等效线性系统在 $n<\frac52$ 时稳定，在 $n>\frac52$ 时不稳定。代回 $n=N(A)$：

$$
N(A)<\frac52
\quad\Longleftrightarrow\quad
\frac12<A<2.
$$

- 在 $A_1=\frac12$ 附近：振幅稍小时等效增益过大，振幅增长；振幅稍大时进入等效稳定区，振幅衰减。两侧均回到 $A_1$，故为稳定周期解。
- 在 $A_2=2$ 附近：振幅稍小时趋于减小，振幅稍大时趋于增大。两侧均远离 $A_2$，故为不稳定周期解。

所以，描述函数法预测稳定自激振荡的参数为

$$
\boxed{A=\frac12,\qquad \omega=\frac12\,\mathrm{rad/s}}.
$$

另一个候选 $A=2$、$\omega=\frac12\,\mathrm{rad/s}$ 应标为不稳定周期解，不应写成“无解”，更不能把它当作稳定自振答案。

> [!warning] 一个几何交点，两个候选振幅
> 描述函数曲线在复平面上只与奈氏曲线交于同一点 $-\frac25$，但振幅参数有两个原像，必须分别检查稳定性，不能按振幅大小直接取舍。

**8-28　解析**（2024 年南京航天大学，考点：非线性求振幅和频率，难度 ★★☆）

解：（1）由原题

$$
N(A)=\frac1A\mathrm e^{-\mathrm j\pi/3},
\qquad A>0.
$$

可得

$$
-\frac1{N(A)}
=-A\mathrm e^{\mathrm j\pi/3}
=A\mathrm e^{-\mathrm j2\pi/3}.
$$

负倒描述函数轨迹是辐角 $-120^\circ$ 的射线，随 $A$ 增大从原点向外移动。

线性部分为

$$
G(s)=\frac{15}{s(0.5s+1)}.
$$

$$
\lvert G(\mathrm j\omega)\rvert
=\frac{15}{\omega\sqrt{1+\omega^2/4}}.
$$

$$
\arg G(\mathrm j\omega)
=-90^\circ-\arctan\frac\omega2.
$$

正频率相角从 $-90^\circ$ 严格降至 $-180^\circ$，故必有且仅有一个频率满足相角 $-120^\circ$；对应幅值为正，因此有一个周期解候选。

（2）相位平衡给出

$$
-90^\circ-\arctan\frac\omega2=-120^\circ.
$$

$$
\frac\omega2=\tan30^\circ=\frac1{\sqrt3}.
$$

$$
\boxed{\omega=\frac2{\sqrt3}\,\mathrm{rad/s}}.
$$

再由幅值平衡得

$$
A=\lvert G(\mathrm j\omega)\rvert.
$$

$$
A=\frac{15}{\frac2{\sqrt3}\sqrt{1+\frac13}}
=\boxed{\frac{45}{4}}.
$$

本题描述函数相角不随振幅改变，因此相位平衡频率不随振幅改变。在该频率处

$$
\lvert N(A)G(\mathrm j\omega)\rvert
=\frac{45}{4A}.
$$

振幅稍大时环路幅值小于1，振幅衰减；振幅稍小时环路幅值大于1，振幅增长。按描述函数法的局部振幅判据，该周期解稳定，即预测存在稳定自振。

由于 $r=0$ 且为单位负反馈，非线性输入与输出满足 $e=-c$，输出振幅也为 $\frac{45}{4}$。

## 【知识点七】系统输出振幅和自振频率

**8-29　解析**（2024 年中国矿业大学（徐州），考点：系统输出自振幅值与频率分析，难度 ★★☆）

解：（1）先按原图区分前向通道与反馈通道：

$$
P(s)=\frac1{s(0.5s+1)}.
$$

$$
H(s)=\frac5{s+2}.
$$

环路等效线性部分须包含二者，故

$$
G(s)=P(s)H(s)
=\frac5{s(0.5s+1)(s+2)}.
$$

由于 $s+2=2(0.5s+1)$，也可写成

$$
\boxed{G(s)=\frac{\frac52}{s(0.5s+1)^2}}.
$$

设非线性输入 $e(t)$ 的基波振幅为 $A_e$。理想继电器的描述函数为

$$
N(A_e)=\frac4{\pi A_e}.
$$

$$
-\frac1{N(A_e)}=-\frac{\pi A_e}{4}.
$$

线性部分相位为

$$
\arg G(\mathrm j\omega)
=-90^\circ-2\arctan\frac\omega2.
$$

令其等于 $-180^\circ$，得

$$
\omega_x=2\,\mathrm{rad/s}.
$$

$$
G(\mathrm j2)=-\frac58.
$$

所以候选振幅为

$$
\frac{\pi A_e}{4}=\frac58.
$$

$$
\boxed{A_e=\frac5{2\pi}}.
$$

检验周期解稳定性：把描述函数暂视为实增益 $n>0$，等效闭环特征方程为

$$
\frac12s^3+2s^2+2s+5n=0.
$$

劳斯条件为

$$
2\cdot2>\frac12\cdot5n.
$$

即

$$
n<\frac85.
$$

$N(A_e)$ 随振幅严格递减。在交点处 $N=\frac85$；振幅稍增时进入等效稳定区，振幅稍减时进入等效不稳定区，故振幅扰动有恢复趋势。描述函数法预测该周期运动稳定。

（2）题目要求的是输出振幅，而非 $A_e$。由原图在 $r=0$ 时有

$$
E(s)=-H(s)C(s)=-\frac5{s+2}C(s).
$$

因此在自振频率处，基波振幅满足

$$
\frac{A_e}{A_c}
=\lvert H(\mathrm j2)\rvert
=\frac5{\sqrt{2^2+2^2}}
=\frac5{2\sqrt2}.
$$

$$
A_c=A_e\frac{2\sqrt2}{5}
=\frac5{2\pi}\frac{2\sqrt2}{5}.
$$

故输出自振参数为

$$
\boxed{A_c=\frac{\sqrt2}{\pi},
\qquad \omega=2\,\mathrm{rad/s}}.
$$

还可用前向通道独立复核：继电器输出基波振幅为 $\frac4\pi$，而

$$
\lvert P(\mathrm j2)\rvert=\frac1{2\sqrt2}.
$$

$$
A_c=\frac4\pi\cdot\frac1{2\sqrt2}
=\frac{\sqrt2}{\pi}.
$$

> [!warning] 两个不能漏的地方
> 环路传递函数中有两个同时间常数的惯性因子，不能漏平方；输出换算必须使用 $e=-Hc$，不是把环路等效增益误当作反馈通道。

**8-30　解析**（2025 年济南大学，考点：系统输出自振幅值与频率分析，难度 ★☆☆）

解：（1）负倒描述函数为

$$
-\frac1{N(A)}=-\frac{\pi A}{6},
\qquad A>0.
$$

在复平面上画负实轴射线，箭头随 $A$ 增大指向左方；原点只是 $A\to0^+$ 的极限。

线性部分为

$$
G(s)=\frac{K}{s(s+1)(2s+1)},
\qquad K>0.
$$

其频率响应可写成

$$
G(\mathrm j\omega)
=\frac{K}{-3\omega^2+\mathrm j\omega(1-2\omega^2)}.
$$

为便于手绘，分离实虚部：

$$
\operatorname{Re}G(\mathrm j\omega)
=-\frac{3K}{(1+\omega^2)(1+4\omega^2)}.
$$

$$
\operatorname{Im}G(\mathrm j\omega)
=-\frac{K(1-2\omega^2)}{\omega(1+\omega^2)(1+4\omega^2)}.
$$

正频率奈氏曲线的关键点与方向如下：

- $\omega\to0^+$ 时，实部趋于 $-3K$，虚部趋于 $-\infty$，相角趋于 $-90^\circ$。
- 虚部在 $\omega=\frac1{\sqrt2}$ 时为零，此时穿过负实轴。
- 随后进入第二象限，最后从上方趋于原点，相角连续取值趋于 $-270^\circ$。
- 负频率曲线关于实轴对称；在正频率曲线上标出 $\omega$ 增大方向。若画完整奈氏围线，原点积分极点须按惯例绕行。

负实轴交点为

$$
\omega_x=\frac1{\sqrt2}\,\mathrm{rad/s}.
$$

$$
G(\mathrm j\omega_x)=-\frac{2K}{3}.
$$

（2）负倒描述函数射线对任意 $K>0$ 均经过该点。幅值平衡给出

$$
\frac{\pi A}{6}=\frac{2K}{3}.
$$

$$
A=\frac{4K}{\pi}.
$$

为判断稳定性，以实增益 $n=N(A)$ 替代非线性部分，则闭环特征方程为

$$
2s^3+3s^2+s+Kn=0.
$$

劳斯稳定条件为

$$
3>2Kn.
$$

即 $Kn<\frac32$ 时等效线性系统稳定，$Kn>\frac32$ 时不稳定。由于 $N(A)=\frac6{\pi A}$ 随振幅递减，候选点两侧的振幅变化均指向该点，因此描述函数法预测存在稳定自振。

当题设 $K=0.75\pi=\frac{3\pi}{4}$ 时，

$$
A=\frac4\pi\cdot\frac{3\pi}{4}=3.
$$

原图为单位负反馈且 $r=0$，所以 $e=-c$，两者振幅相等。因此

$$
\boxed{A_c=3,
\qquad \omega=\frac1{\sqrt2}\,\mathrm{rad/s}}.
$$

> [!tip] 手绘要点
> 画图时标出低频渐近线 $\operatorname{Re}G=-3K$、负实轴交点 $-\frac{2K}{3}$、高频趋近原点的方向，再画随振幅向左移动的负倒描述函数射线即可。不要仅凭“有交点”省略稳定性判断。

**8-31　解析**（2012 年南京航空航天大学，考点：系统输出自振幅值与频率分析，难度 ★☆☆）

解：（1）按原题 $M=1$、$K=0.5$，非线性环节描述函数为

$$
N(A)=\frac4{\pi A}+\frac12
=\frac{\pi A+8}{2\pi A}.
$$

因此负倒数为

$$
\boxed{-\frac1{N(A)}=-\frac{2\pi A}{\pi A+8}}.
$$

其导数为

$$
\frac{\mathrm d}{\mathrm dA}
\left(-\frac1{N(A)}\right)
=-\frac{16\pi}{(\pi A+8)^2}<0.
$$

随 $A$ 从 $0^+$ 增至无穷，该点沿负实轴从 $0^-$ 移向 $-2$。轨迹取值范围为 $(-2,0)$，两个端点均不在有限正振幅处取得。

线性部分为

$$
G(s)=\frac4{(s+1)^3}.
$$

$$
G(\mathrm j\omega)
=\frac4{(1-3\omega^2)+\mathrm j\omega(3-\omega^2)}.
$$

取负实轴交点，得到

$$
\omega_x=\sqrt3\,\mathrm{rad/s}.
$$

$$
G(\mathrm j\sqrt3)=-\frac12.
$$

该点位于 $(-2,0)$ 内，因此存在唯一正振幅候选。若需手绘奈氏图，另有

$$
G(0)=4.
$$

$$
G\left(\frac{\mathrm j}{\sqrt3}\right)
=-\mathrm j\frac{3\sqrt3}{2}.
$$

正频率曲线从实轴上的4出发，进入第四象限，穿过上述虚轴点后进入第三象限，再经 $-\frac12$ 进入第二象限，最终从上方趋于原点。

判稳时将 $N(A)$ 暂记为实增益 $n$，闭环特征方程为

$$
(s+1)^3+4n=0.
$$

$$
s^3+3s^2+3s+(1+4n)=0.
$$

劳斯条件为

$$
3\cdot3>1+4n.
$$

故 $n<2$ 时等效线性系统稳定，$n>2$ 时不稳定。由于 $N(A)$ 随振幅递减，交点处的振幅扰动有恢复趋势，描述函数法预测该周期运动稳定。

（2）由幅值平衡

$$
\frac{2\pi A}{\pi A+8}=\frac12.
$$

$$
4\pi A=\pi A+8.
$$

得到

$$
\boxed{A=\frac8{3\pi},
\qquad \omega=\sqrt3\,\mathrm{rad/s}}.
$$

无外部周期激励时，自振相位由初始条件决定。若取非线性输入基波为

$$
e(t)\approx\frac8{3\pi}\sin(\sqrt3t+\varphi),
$$

由单位负反馈、$r=0$ 得精确的信号关系 $c=-e$，所以输出基波近似为

$$
\boxed{c(t)\approx-\frac8{3\pi}\sin(\sqrt3t+\varphi)}.
$$

选择时间原点使 $\varphi=0$，便得到原答案采用的形式

$$
c(t)\approx-\frac8{3\pi}\sin(\sqrt3t).
$$

> [!warning] 倒数与近似号
> $-\frac{\pi A+8}{2\pi A}$ 是 $-N(A)$，不是负倒描述函数；用这一错误式不可能解出有限的 $A=\frac8{3\pi}$。此外，描述函数法得到的是基波近似，不能将上式称作原系统的精确正弦解。

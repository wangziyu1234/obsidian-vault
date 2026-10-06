from pathlib import Path
p=next(Path('控制理论/777习题集').glob('现控200题基础 第5章*答案*.md'))
raw=p.read_bytes();nl='\r\n' if b'\r\n' in raw else '\n';s=raw.decode('utf-8').replace('\r\n','\n')
def rep(old,new):
    global s
    assert old in s,old[:90]
    s=s.replace(old,new)
def section(start,end,new):
    global s
    i=s.index(start);j=s.index(end,i);s=s[:i]+new.rstrip()+'\n\n'+s[j:]
rep('modify: 2026-09-28','modify: 2026-10-06')
section('> 现控基础册第五章','## 答案速查',r'''> 本章 34 题，按原题逐题核对状态反馈、观测器与组合系统。原书勘误在对应题下说明；2026-10-06 补正矩阵元素、反馈与注入项、参数边界及题面转录，答案速查同步更新。指数、根式与对数保留适合手算的精确形式。''')
rep(r'f(\lambda)=\lambda^3-3\lambda^2+12\lambda',r'f(\lambda)=\lambda^3+17\lambda^2+12\lambda')
rep(r'取 $K=[k_1\ k_2\ 0]$（不加到不能控通道），可以验证',r'取分解坐标中的增益 $\tilde K=[4\ \ 8\ \ 0]$，再由 $K=\tilde K P^{-1}$ 换回原坐标，可以验证')
rep(r'\begin{bmatrix}1&0\\0&-6\end{bmatrix}',r'\begin{bmatrix}1&0\\0&-3\end{bmatrix}')
rep(r'\approx[-3.59\ \ -4.31]','')
rep(r'\approx-3.586','');rep(r'\approx-4.310','')
section('> 原书答案 $K=[-3.59','**5-6',r'''> 保留精确解 $K=[\sqrt2-5\ \ \frac{5\sqrt2-20}{3}]$，代回特征多项式恰为 $\lambda^2+\sqrt2\lambda+1$，无需先舍入再求后续系数。''')
rep(r'$k=[1\ \ 0.561]$',r'$k_1=1$，$k_2=\frac{\sqrt2 q}{\sqrt{\pi^2+q^2}}-\frac12$，$q=-\ln(0.02835)$')
section(r'超调量 $\sigma','> [!note] 本题总结',r'''题给超调量为 $2.835\%$。令 $q=-\ln(0.02835)>0$，则

$$
\frac{\pi\xi}{\sqrt{1-\xi^2}}=q
$$

$$
\xi=\frac{q}{\sqrt{\pi^2+q^2}}
$$

由 $\omega_n^2=2k_1=2$ 得 $\omega_n=\sqrt2$，比较一次项：

$$
2k_2+1=2\xi\omega_n
$$

$$
\boxed{k_1=1,\qquad k_2=\frac{\sqrt2 q}{\sqrt{\pi^2+q^2}}-\frac12}
$$

原书采用近似 $\xi\approx3/4$，相应 $k_2\approx3\sqrt2/4-1/2$；该近似不能与题给超调量的精确关系混写成等号。''')
rep(r'\lambda^3+(3-k_3)\lambda^2+(2-k_2)\lambda-k_0',r'\lambda^3+(3-k_2)\lambda^2+(2-k_1)\lambda-k_0')
old=r'\begin{bmatrix}0&1&0\\0&0&1\\-4&-6&-4\end{bmatrix}x+\begin{bmatrix}0\\0\\1\end{bmatrix}v,\quad y=[1\ \ 0\ \ 0]x'
rep(old,old.replace('y=[1','y=[10'))
rep('稳定条件不受影响。',r'可通过状态反馈镇定的结论不变；正确增益范围为 $K_1<0$、$K_2>-1$，漏掉常数 $1$ 会错误缩小该范围。')
rep('特征根要么一对纯虚根、要么一正一负实根',r'特征根在 $F<1$ 时为一对纯虚根、$F=1$ 时为双零根、$F>1$ 时为一正一负实根')
rep(r'\frac{s+1}{\lambda^3+5s^2+9s+5}',r'\frac{s+1}{s^3+5s^2+9s+5}') if r'\frac{s+1}{\lambda^3+5s^2+9s+5}' in s else rep(r'\dfrac{s+1}{\lambda^3+5s^2+9s+5}',r'\dfrac{s+1}{s^3+5s^2+9s+5}')
rep('指定闭环传函分母比分子低一阶时','目标传递函数的分母次数比原系统阶数低一阶时')
rep(r'故能设计全维观测器 $\iff b\ne0$（$a$ 任意）。',r'''故能任意配置全维观测器极点 $\iff b\ne0$（$a$ 任意）。

> [!note] 观测器存在与任意极点配置
> 若只要求估计误差渐近趋零，条件是可检测性，还允许 $b=0,a<0$。此时取 $L=[-1\ \ 0]^T$，便有 $A-LC=\mathrm{diag}(a,-1)$。因此“渐近观测器存在”的完整条件为 $b\ne0$ 或 $b=0,a<0$。''')
rep(r'BIBO 要求 $b\gt0$',r'独立讨论时 BIBO 要求 $b\ge0$')
rep(r'(3) $b\gt0$',r'(3) $b\ge0$（独立讨论）') if r'(3) $b\gt0$' in s else None
old='故 BIBO 稳定条件为\n\n$$\nb\\gt0\n$$'
rep(old,r'''以上先讨论 $b\ne0$ 的非零传递函数。另当 $b=0$ 时，$W(s)\equiv0$，零初态下输出不受输入影响，仍满足 BIBO 稳定。因此第三问独立讨论时，完整范围为

$$
b\ge0
$$

若要求同时满足第二问的任意观测器极点配置条件 $b\ne0$，交集才是 $b>0$。''')
rep('（$a$ 任意，例如 $a=2$ 时 $K=[3\\ \\ -1]$。）',r'（$a$ 任意。若 $b=0$，第二个系数方程不再限制 $k_2$，全部解为 $K=[a+1\ \ k_2]$；因此上面的 $K=[a+1\ \ -1]$ 对 $b=0$ 也有效。）')
rep('前馈通道参数 $a$ 不影响能观性与 BIBO 判稳的主导项，配置时它只平移 $k_1$；而 $b$ 同时管能控、能观与开环增益——一个参数卡三条判据是小题眼。',r'$a$ 不影响能观性的满秩条件，配置时平移 $k_1$；第三问是在 $a=0$ 下单独讨论 BIBO 稳定，不能将其条件直接推广到任意 $a$。')
rep(r'能控子系统 $\dot x_c=\begin{bmatrix}1&0\\1&2\end{bmatrix}x_c+\begin{bmatrix}1&0\\0&1\end{bmatrix}u$（特征值 $1,2$），不能控子系统 $\dot{\bar x}_c=3\bar x_c$。',r'''分解后的完整方程为

$$
\dot x_c=\begin{bmatrix}1&0\\1&2\end{bmatrix}x_c+\begin{bmatrix}2\\-2\end{bmatrix}\bar x_c+u
$$

$$
\dot{\bar x}_c=3\bar x_c
$$

能控块特征值为 $1,2$；只有限制在 $\bar x_c=0$ 的能控子空间内，才可省去上式耦合项。''')
p.write_bytes(s.replace('\n',nl).encode('utf-8'))
pq=next(p.parent.glob('现控200题基础 第5章*题目*.md'));raw=pq.read_bytes();s=raw.decode('utf-8');start=s.index('**5-11');end=s.index('**5-12',start);chunk=s[start:end];assert r'y=[1\ \ 0\ \ 0]' in chunk;chunk=chunk.replace(r'y=[1\ \ 0\ \ 0]',r'y=[10\ \ 0\ \ 0]');s=s[:start]+chunk+s[end:];s=s.replace('modify: 2026-09-28','modify: 2026-10-06');pq.write_bytes(s.encode('utf-8'));print('chapter5 first half updated')

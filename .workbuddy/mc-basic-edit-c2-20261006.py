from pathlib import Path
import re
p=next(Path('控制理论/777习题集').glob('现控200题基础 第2章*答案*.md'))
raw=p.read_bytes(); nl='\r\n' if b'\r\n' in raw else '\n'; s=raw.decode('utf-8').replace('\r\n','\n')
def rep(old,new):
    global s
    assert old in s,old[:100]
    s=s.replace(old,new)
def section(start,end,new):
    global s
    i=s.index(start);j=s.index(end,i);s=s[:i]+new.rstrip()+'\n\n'+s[j:]
rep('modify: 2026-09-27','modify: 2026-10-06')
section('> 一处与原书答案不同','## 答案速查',r'''> 2-9 原书及官方修正仍有闭环特征多项式漏项，本页给出保留指数的精确反馈增益。2026-10-06 回看原题并逐题复算，另修正 2-1 导数符号、2-5 重根情形、2-8 零输出解释、2-10 采样周期说明和 2-11 系数匹配笔误；2-7 原题未给具体时刻，答案保留该时刻为参数。''')
rep(r'A=\Phi(t)|_{t=0}',r'A=\dot\Phi(t)|_{t=0}')
rep(r'\begin{bmatrix}c\\ca\end{bmatrix}',r'\begin{bmatrix}c\\cA\end{bmatrix}')
rep(r'$x(t)=\begin{bmatrix}e^{at}&\frac{e^{at}-e^{bt}}{a-b}\\0&e^{bt}\end{bmatrix}x(0)$',r'$x(t)=e^{At}x(0)$；$a=b$ 时 $e^{At}=e^{at}\begin{bmatrix}1&t\\0&1\end{bmatrix}$，$a\ne b$ 见解析')
rep('上三角矩阵的 $e^{At}$（sympy 复验）：',r'先设 $a\ne b$，上三角矩阵的 $e^{At}$ 为：')
rep(r'> 上三角 $A$ 的 $e^{At}$ 保持上三角；非对角元 $\frac{e^{at}-e^{bt}}{a-b}$ 在 $a\to b$ 时取极限 $te^{at}$（重根情形）。',r'''> 上三角 $A$ 的 $e^{At}$ 保持上三角；题设没有排除 $a=b$，此时应取重根形式：
>
> $$
> e^{At}=e^{at}\begin{bmatrix}1&t\\0&1\end{bmatrix}
> $$
>
> $$
> x(t)=e^{at}\begin{bmatrix}x_1(0)+t x_2(0)\\x_2(0)\end{bmatrix}
> $$''')
rep('**2-5　答案 $x(t)=',r'**2-5　答案（$a\ne b$；重根见题末）$x(t)=')
section('**2-8　答案','**2-9　答案',r'''**2-8　答案 $\lambda=-\frac32$，$x(0)=[-2\ \ 2]^T$**（考点：零输出轨迹与非齐次状态方程）

若输出恒为零，则

$$
x_2(t)=-x_1(t)
$$

对 $y=x_1+x_2$ 求导并代入状态方程：

$$
0=\dot y=-x_1-2x_2+2u=x_1+2u
$$

因此必须有

$$
x_1(t)=-2e^{\lambda t}
$$

$$
x_2(t)=2e^{\lambda t}
$$

代回第一条状态方程：

$$
-2\lambda e^{\lambda t}=2e^{\lambda t}+e^{\lambda t}
$$

从而

$$
\lambda=-\frac32,\qquad x(0)=\begin{bmatrix}-2\\2\end{bmatrix}
$$

代入第二条状态方程同样成立，且 $y(t)\equiv0$。

> [!note] 本题总结
> 这是指定非零初态与输入共同形成的零输出轨迹；零输入响应和零状态响应的输出相互抵消。先用 $y=0$、$\dot y=0$ 消元，可避免对 $\lambda=-1,-2$ 另行讨论。''')
rep(r'$\lambda=-1.5$',r'$\lambda=-\frac32$')
section('**2-9　答案','## 【题型3】',r'''**2-9　答案：精确离散模型及反馈增益如下**（考点：零阶保持离散化、离散状态反馈极点配置）

（1）按原图，$x_2$ 为 $1/(s+2)$ 的输出，$x_1=y$ 为积分器输出：

$$
\dot x_1=x_2
$$

$$
\dot x_2=-2x_2+u
$$

$$
A=\begin{bmatrix}0&1\\0&-2\end{bmatrix},\qquad B=\begin{bmatrix}0\\1\end{bmatrix}
$$

$$
\Phi(t)=\begin{bmatrix}1&\frac{1-e^{-2t}}2\\0&e^{-2t}\end{bmatrix}
$$

题设 $T=0.5\,\mathrm{s}$。本题记 $q=e^{-1}$，保留指数精确值：

$$
G=e^{AT}=\begin{bmatrix}1&\frac{1-q}2\\0&q\end{bmatrix}
$$

$$
H=\int_0^T\Phi(\tau)B\,d\tau=\begin{bmatrix}\frac q4\\\frac{1-q}2\end{bmatrix}
$$

$$
x(k+1)=Gx(k)+Hu(k)
$$

（2）采用负反馈 $u=r-K_dx$，$K_d=[k_1\ \ k_2]$。展开闭环特征多项式：

$$
\begin{aligned}
f(z)&=\det[zI-(G-HK_d)]\\
&=z^2-\left(1+q-\frac q4k_1-\frac{1-q}2k_2\right)z\\
&\quad+q+\frac{1-2q}4k_1-\frac{1-q}2k_2
\end{aligned}
$$

目标极点为题给的 $0.5\pm0.2i$，故

$$
f^*(z)=(z-0.5-0.2i)(z-0.5+0.2i)=z^2-z+0.29
$$

比较系数：

$$
\frac q4k_1+\frac{1-q}2k_2=q
$$

$$
\frac{1-2q}4k_1-\frac{1-q}2k_2=\frac{29}{100}-q
$$

两式相加后求解，得

$$
k_1=\frac{29}{25(1-q)}
$$

$$
k_2=\frac{q(71-100q)}{50(1-q)^2}
$$

$$
K_d=\begin{bmatrix}\dfrac{29}{25(1-q)}&\dfrac{q(71-100q)}{50(1-q)^2}\end{bmatrix},\qquad q=e^{-1}
$$

回代后严格得到 $f(z)=z^2-z+0.29$。

> [!warning] 原书与官方修正的漏项
> 原书答案册书内 29—30 页把目标常数写成 $0.65$，应为 $0.29$；闭环多项式常数项还漏掉了 $q$（书中近似为 $0.368$）。官方修正虽把目标多项式改为 $z^2-z+0.29$，仍沿用了漏项的闭环方程，因此其 $K_d=[4.165\ \ -0.048]$ 仍不满足目标极点。
>
> 旧笔记中的 $[1.835\ \ 0.630]$ 也是基于先行舍入所得的近似增益，不能称为严格配置结果。本页以以上精确式为准。''')
rep(r'(1) $G=\begin{bmatrix}1&0.316\\0&0.368\end{bmatrix}$，$H=\begin{bmatrix}0.092\\0.316\end{bmatrix}$；(2) $K_d\approx[1.835\ \ 0.630]$ ⚠️复算',r'$q=e^{-1}$；$K_d=[\frac{29}{25(1-q)}\ \ \frac{q(71-100q)}{50(1-q)^2}]$；精确 $G,H$ 见解析')
rep(r'$T\ne\dfrac{k\pi}{4}$（$k=\pm1,\pm2,\dots$）',r'$T>0$ 且 $T\ne\frac{k\pi}{4}$（$k=1,2,\dots$）')
rep(r'$T\ne\dfrac{k\pi}{4}$（$k=\pm1,\pm2,\dots$）',r'$T>0$ 且 $T\ne\frac{k\pi}{4}$（$k=1,2,\dots$）') if r'$T\ne\dfrac{k\pi}{4}$（$k=\pm1,\pm2,\dots$）' in s else None
rep(r'（原书印作「$A=\dot\Phi(t)|_{t=0}$」，漏了导数点，数值按 $\dot\Phi(0)$ 给出，结果无误。）',r'（原书答案册书内 30 页写的是 $A=\dot\Phi(0)$，导数点存在；此处按原式转写。）')
rep(r'T\ne\frac{k\pi}{4}\qquad (k=\pm1,\pm2,\pm3,\dots)',r'T>0,\qquad T\ne\frac{k\pi}{4}\quad(k=1,2,3,\dots)')
rep('的整数分之一处','的正整数倍处')
rep(r'$2b_1+b_2=0$',r'$2b_1+b_2=1$')
section('**2-12　答案', '\n\x00', '') if False else None
i=s.index('**2-12　答案')
s=s[:i]+r'''**2-12　答案：保留 $e^{-2}$ 的精确离散模型**（考点：零阶保持离散化）

$$
\Phi(t)=\begin{bmatrix}1&\frac{1-e^{-2t}}2\\0&e^{-2t}\end{bmatrix}
$$

题设 $T=1\,\mathrm{s}$，本题记 $q=e^{-2}$，则

$$
G=\Phi(1)=\begin{bmatrix}1&\frac{1-q}2\\0&q\end{bmatrix}
$$

$$
H=\int_0^1\Phi(t)B\,dt=\begin{bmatrix}\frac{1+q}4\\\frac{1-q}2\end{bmatrix}
$$

因此

$$
x(k+1)=\begin{bmatrix}1&\frac{1-q}2\\0&q\end{bmatrix}x(k)+\begin{bmatrix}\frac{1+q}4\\\frac{1-q}2\end{bmatrix}u(k)
$$

$$
y(k)=[1\ \ 0]x(k),\qquad q=e^{-2}
$$

> [!note] 本题总结
> 与 2-9(1) 的连续对象相同。一般采样周期下 $H$ 的第一分量为 $\frac T2+\frac{e^{-2T}-1}4$，本题代入 $T=1$ 即得 $\frac{1+e^{-2}}4$。
'''
rep(r'$G=\begin{bmatrix}1&0.4323\\0&0.1353\end{bmatrix}$，$H=\begin{bmatrix}0.2838\\0.4323\end{bmatrix}$',r'$q=e^{-2}$，$G=\begin{bmatrix}1&\frac{1-q}2\\0&q\end{bmatrix}$，$H=\begin{bmatrix}\frac{1+q}4\\\frac{1-q}2\end{bmatrix}$')
p.write_bytes(s.replace('\n',nl).encode('utf-8'))
qfile=next(p.parent.glob('现控200题基础 第2章*题目*.md'))
data=qfile.read_bytes(); txt=data.decode('utf-8').replace('modify: 2026-09-27','modify: 2026-10-06').replace('单人单出','单入单出');qfile.write_bytes(txt.encode('utf-8'))
print('updated chapter 2')

from pathlib import Path
p=next(Path('控制理论/777习题集').glob('现控200题基础 第1章*答案*.md'))
raw=p.read_bytes();nl='\r\n' if b'\r\n' in raw else '\n';s=raw.decode('utf-8').replace('\r\n','\n')
def rep(old,new):
 global s
 assert old in s,old[:90]
 s=s.replace(old,new)
def section(start,end,new):
 global s
 i=s.index(start);j=s.index(end,i);s=s[:i]+new.rstrip()+'\n\n'+s[j:]
rep(r'取 $x_i=\dfrac{1}{s+\lambda_i}u$，三个一阶环节并联：',r'''将三个并联支路的输出分别定义为状态（以下为零初值下的拉氏域定义）：

$$
X_1(s)=\frac{U(s)}{s+1}
$$

$$
X_2(s)=-\frac{2U(s)}{s+2}
$$

$$
X_3(s)=\frac{3U(s)}{s+3}
$$

于是''')
rep(r'模拟结构图：三个一阶环节 $\frac{1}{s+\lambda_i}$ 并联，输入同为 $u$，输出按 $1,-2,3$ 加权求和。',r'模拟结构对应三个支路 $1/(s+1)$、$-2/(s+2)$、$3/(s+3)$ 并联；支路输出就是 $x_1,x_2,x_3$，再按 $y=x_1+x_2+x_3$ 求和。')
rep(r'\begin{bmatrix}s+1&1\\-3&s+5\end{bmatrix}',r'\begin{bmatrix}s+1&-1\\3&s+5\end{bmatrix}')
section('**1-21　答案','**1-22　答案',r'''**1-21　答案：$x_1x_2x_3$ 能控能观，$x_4$ 能观不能控，$x_5x_6$ 能控不能观；$W(s)=1/[(s+1)(s+2)(s+3)]$**（考点：分块结构的能控能观性与传递函数）

> [!note] 官方修正图核对
> 官方修正的是左端第 4 个状态导数的下标，应为 $\dot x_4$；输入向量仍为 $B=[0,0,1,0,0,4]^T$。旧笔记误读成末分量“$4\to0$”，并据此把末两态判成“双不能”，现按原题和官方图恢复。

（1）按结构分成三块：

- $x_1,x_2,x_3$ 构成三阶能控标准形，输入从链尾进入，输出包含链首 $x_1$，完全能控且完全能观。
- $\dot x_4=-5x_4$ 没有输入驱动，但输出包含 $x_4$，故能观、不能控。
- $x_5,x_6$ 构成二阶约当块，输入从链尾 $x_6$ 以增益 $4$ 进入，但二者均不出现在输出中，故能控、不能观。

末两态的能控矩阵可直接验算：

$$
\begin{bmatrix}B_J&A_JB_J\end{bmatrix}=\begin{bmatrix}0&4\\4&-28\end{bmatrix}
$$

其行列式为 $-16\ne0$。整个系统的能控秩为 $5$，能观秩为 $4$。

![[现控1-21-模拟变量图.png|430]]

（2）零初态下，$x_4$ 没有输入响应；$x_5,x_6$ 虽受输入驱动，但不影响输出。故传递函数仅来自前三态：

$$
W(s)=\frac{1}{s^3+6s^2+11s+6}=\frac{1}{(s+1)(s+2)(s+3)}
$$

> [!note] 本题总结
> 互异对角模态可逐行、逐列检查输入输出；约当块要看链尾输入与链首输出，不能把“每个 $B_i,C_i$ 非零”机械套到链中每个状态。不能控或不能观的模态都可能不出现在传递函数中。''')
s=s.replace(r'$x_5x_6$ 既不能控也不能观',r'$x_5x_6$ 能控不能观')
s=s.replace(r'\Phi(s)=\begin{bmatrix}\frac{3s^2+9s+4}{(s+2)D} & -\frac{s+1}{D}\\ -\frac{2s(s+1)}{D}',r'\Phi(s)=\begin{bmatrix}\frac{3s^2+9s+4}{(s+2)D} & -\frac{s+1}{D}\\ \frac{2s(s+1)}{D}')
rep(r'\\[8pt]-\dfrac{2s(s+1)}',r'\\[8pt]\dfrac{2s(s+1)}')
old=r'[I+G(s)H(s)]^{-1}=\frac{1}{(s+2)(s^2+5s+2)}\begin{bmatrix}s(s+1)(s+3)&s+1\\-2s(s+1)&s(s+2)\end{bmatrix}'
new=r'''[I+G(s)H(s)]^{-1}=\begin{bmatrix}
\dfrac{s(s+1)(s+3)}{(s+2)D}&\dfrac{s+1}{D}\\[6pt]
-\dfrac{2s(s+1)}{D}&\dfrac{s(s+2)}{D}
\end{bmatrix},\qquad D=s^2+5s+2'''
rep(old,new)
needle='模拟结构图：两个积分器串联'
i=s.index(needle);j=s.index('\n\n',i);s=s[:j]+'\n\n![[现控1-5-模拟结构图.png|430]]'+s[j:]
needle='模拟结构图：三个积分器串联';i=s.index(needle);j=s.index('\n\n',i);s=s[:j]+'\n\n![[现控1-9-模拟结构图.png|520]]'+s[j:]
p.write_bytes(s.replace('\n',nl).encode('utf-8'))
pq=next(p.parent.glob('现控200题基础 第1章*题目*.md'));s=pq.read_bytes().decode('utf-8');i=s.index('**1-21');j=s.index('**1-22',i);chunk=s[i:j];chunk=chunk.replace(r'\begin{bmatrix}0\\ 0\\ 1\\ 0\\ 0\\ 0\end{bmatrix}u',r'\begin{bmatrix}0\\ 0\\ 1\\ 0\\ 0\\ 4\end{bmatrix}u');start=chunk.index('> [!note] 勘误');end=chunk.index('（1）判断',start);chunk=chunk[:start]+'> [!note] 官方修正图核对\n> 左端第4个状态导数修正为 $\\dot x_4$；输入向量末分量仍是 $4$。旧笔记“改为0”的说明系误读，已纠正。\n\n'+chunk[end:];s=s[:i]+chunk+s[j:];i=s.index('**1-19');j=s.index('**1-20',i);chunk=s[i:j].replace(r'$x=\begin{bmatrix}',r'$\dot x=\begin{bmatrix}');s=s[:i]+chunk+s[j:];s=s.replace('\r\n','\n').replace('\n','\r\n') if b'\r\n' in pq.read_bytes() else s;pq.write_bytes(s.encode('utf-8'));print('chapter1 second half updated')

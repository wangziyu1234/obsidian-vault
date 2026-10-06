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
rep(r'$\dot x(k+1)=Gx(k)$',r'$x(k+1)=Gx(k)$')
rep(r'$\det G=-\alpha\ne0$（$\alpha\ne0$），唯一平衡状态 $x_e=0$。',r'平衡状态满足 $(I-G)x_e=0$，而 $\det(I-G)=2-\alpha$。当 $\alpha\ne2$ 时原点唯一；$\alpha=2$ 时 $x_1=x_2$ 上的所有点均为平衡状态，均不渐近稳定。')
rep(r'\begin{bmatrix}-17&1\\-23.5&-3\end{bmatrix}',r'\begin{bmatrix}-17&1\\-49&-3\end{bmatrix}')
rep(r'\begin{bmatrix}-5&0\\0.5&-2\end{bmatrix}',r'\begin{bmatrix}-5&-8\\\frac12&-1\end{bmatrix}')
rep(r'取 $u=v+bk$',r'配置时先取理想状态反馈 $u=v+Kx$，实际实现使用 $u=v+K\hat x$')
rep(r'\begin{bmatrix}4\\1\\-2\end{bmatrix}(y-\hat x_1)',r'\begin{bmatrix}4\\1\\-2\end{bmatrix}y')
rep('① 状态不可观测（不可直接测量）时，先按输出',r'① 状态不能全部直接测量时，先检查能观性。本题 $C=[1,0,0,0]$ 的能观矩阵满秩，可以按输出')
rep('观测器只改变观测误差动态，不改变闭环传函与极点配置结果。',r'零初态下，观测器不改变参考输入到输出的闭环传递函数；完整内部系统的极点由反馈极点与观测器极点共同组成。')
rep('（2）$U_o=\\begin{bmatrix}0&0&1&0',r'（2）本题卫星角速度 $\omega>0$。$U_o=\begin{bmatrix}0&0&1&0')
rep(r'$\dot w=-10w+100u$',r'$\dot w=-10w-50y+100u$')
old=r'\dot w=(\bar A_{22}-g\bar A_{12})w+(\bar A_{21}-g\bar A_{11})y+(\bar B_2-g\bar B_1)u=-10w+100u'
new=r'''\begin{aligned}
\dot w&=(\bar A_{22}-g\bar A_{12})w\\
&\quad+\big[(\bar A_{22}-g\bar A_{12})g+\bar A_{21}-g\bar A_{11}\big]y\\
&\quad+(\bar B_2-g\bar B_1)u\\
&=-10w-50y+100u
\end{aligned}'''
rep(old,new)
rep(r'\hat x_2=w+gy=w+5y',r'''\hat x_2=w+gy=w+5y
$$

验算：真实辅助量 $\eta=x_2-5y$ 满足 $\dot\eta=-10\eta-50y+100u$，因此

$$
\frac{d}{dt}(x_2-\hat x_2)=-10(x_2-\hat x_2)''')
rep(r'\hat x_1=w+\begin{bmatrix}3\\4\end{bmatrix}y,\qquad \hat x=T\begin{bmatrix}\hat x_1\\ y\end{bmatrix}',r'\hat x_c=w+\begin{bmatrix}3\\4\end{bmatrix}y,\qquad \hat x=T\begin{bmatrix}\hat x_c\\ y\end{bmatrix}')
rep(r'（否则 $\lambda$ 系数变 $-2g_2-6$ 型错值）','')
section('（3）① 状态反馈：','**5-33',r'''（3）构造实际使用估计状态的反馈系统：

$$
u=v-7\hat x_1-\hat x_2
$$

受控对象与观测器共用同一个实际输入 $u$，观测器为

$$
\dot{\hat x}_1=\hat x_2+8(y-\hat x_1)
$$

$$
\dot{\hat x}_2=2\hat x_1-\hat x_2+u+14(y-\hat x_1)
$$

![[现控5-32-观测器反馈状态框图.png|430]]

> [!note] 反馈信号的选择
> 原书图将真实状态 $x_1,x_2$ 直接反馈，同时在旁路运行观测器。上图给出基于观测器的实际实现：反馈使用 $\hat x_1,\hat x_2$，观测器同时接收 $u$ 与 $y$。''')
i=s.index(r'（2）令 $\bar x=x-\hat x$');j=s.index('（3）系统矩阵',i);chunk=s[i:j];old=r'\begin{bmatrix}B\\ B\end{bmatrix}v';assert old in chunk;chunk=chunk.replace(old,r'\begin{bmatrix}B\\ 0\end{bmatrix}v');s=s[:i]+chunk+s[j:]
rep('（3）系统矩阵已成上三角分块，传递函数只由左上块决定：',r'（3）系统矩阵已成上三角分块，且输入不直接驱动误差子系统；在传递函数所用的零初态条件下，误差恒为零，故输入输出传递函数只由左上块决定：')
p.write_bytes(s.replace('\n',nl).encode('utf-8'))
pq=next(p.parent.glob('现控200题基础 第5章*题目*.md'));s=pq.read_bytes().decode('utf-8')
s=s.replace(r'$K\in R^{n\times n}$',r'$K\in R^{1\times n}$').replace(r'$P\in R^{2n}$',r'$P\in R^{2n\times2n}$')
s += '\n> [!note] 5-34 维数订正\n> 原题将反馈矩阵写作 $K\\in R^{n\\times n}$、变换矩阵写作 $P\\in R^{2n}$。按单输入系统的乘法维数，分别应为 $K\\in R^{1\\times n}$ 和 $P\\in R^{2n\\times2n}$，上文已订正。\n'
pq.write_bytes(s.encode('utf-8'));print('chapter5 second half updated')

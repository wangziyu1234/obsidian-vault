from pathlib import Path
import re
base=Path('D:/obsidian/控制理论/777习题集')
ap=next(base.glob('现控200题强化 专题三*答案*.md')); qp=next(base.glob('现控200题强化 专题三*题目*.md'))
a=ap.read_text(encoding='utf-8-sig');q=qp.read_text(encoding='utf-8-sig')
def get(n):return re.search(rf'^\*\*3-{n}　答案.*?(?=^\*\*3-\d+　答案|^## |\Z)',a,re.M|re.S)[0]
def change(n,old,new):
    global a
    b=get(n);assert old in b,(n,old[:100]);a=a.replace(b,b.replace(old,new))
def append(n,new):
    global a
    b=get(n); idx=b.find('> [!note] 本题总结'); idx=idx if idx>=0 else len(b)
    a=a.replace(b,b[:idx].rstrip()+'\n\n'+new.strip()+'\n\n'+b[idx:])
def put(n,new):
    global a
    b=get(n);a=a.replace(b,b.split('\n',1)[0]+'\n\n'+new.strip()+'\n\n')
change(1,'闭环状态空间描述：','取控制律 $u=v-kx$，其中 $v$ 为闭环参考输入。闭环状态空间描述：')
change(1,r'\dot x=(A-Bk)x+Bu=',r'\dot x=(A-Bk)x+Bv=')
change(1,r'\begin{bmatrix}0\\1\end{bmatrix}u,\qquad y=[3\ \ 1]x\n',r'\begin{bmatrix}0\\1\end{bmatrix}u,\qquad y=[3\ \ 1]x\n') if False else None
# Only the second occurrence is the closed loop.
b=get(1); idx=b.index('取控制律');b=b[:idx]+b[idx:].replace(r'\begin{bmatrix}0\\1\end{bmatrix}u',r'\begin{bmatrix}0\\1\end{bmatrix}v');a=a.replace(get(1),b)
change(2,'得同一个 $K=','得到另一组坐标下的 $K=')
append(3,r'''
把镇定条件写成参数关系：若 $b+c=0$，不能控模态包含原点，不能镇定；若 $a=b+c\ne0$，不能控模态为 $-a$，必须已有 $a>0$。故完整条件为

$$
b+c\ne0
$$

$$
a\ne b+c\quad\text{或}\quad a>0
$$
''')
change(4,'故可进行零极点配置','故可进行极点配置')
change(5,'（1）设 $k=(k_1,k_2)$，闭环系统为','（1）记原题状态矩阵、控制输入列、扰动输入列和输出行为 $A,B,D,C$。设 $K=(k_1,k_2)$，闭环系统为')
change(7,'三条极点里有一条 $-1$ 是与**零点 $-1$ 对消**的多余极点（由把原系统补成 3 阶能控标准形引入），这正是"补零极点"技巧：把多引入的极点放在原系统零点处。','原系统本来就是三阶。配置后把一个极点放在零点 $-1$ 处，使外部传递函数约成二阶；内部状态仍是三维，不能据约分后的分母把内部极点漏掉。')
append(8,r'''
本题约定静态输出反馈 $u=Hy$。也可保留原来的稳定因子 $s+2$，直接考察余下二阶多项式：

$$
\det[sE-(A+BHC)]=(s+2)[s^2-(h_1+2)s+h_1+1-h_2]
$$

由二阶稳定判据，只需 $h_1<-2$、$h_2<h_1+1$。取 $H=[-4,-5]^T$ 后，余下因子为 $s^2+2s+2$，全部极点实部为负。
''')
change(10,'（1）由题可知，系统的能观Ⅱ型如下：','（1）题面只给传递函数，未指明初值所在的状态坐标。以下沿答案册选能观Ⅱ型，并把 $x(0)=[4,1]^T$ 理解为这一实现下的初值；换状态坐标时初值也须同步变换。')
change(10,r'f(\lambda)=\det(\lambda I-A+bk)=s^2+(4+2k_2+k_1)s+4k_1+k_2',r'f(\lambda)=\det(\lambda I-A+BK)=\lambda^2+(4+2k_2+k_1)\lambda+4k_1+k_2')
change(12,'可以通过设计全维状态观测器对系统极点进行任意配置','可以对观测误差系统的极点进行任意配置')
change(12,'而闭环系统的特征多项式','而观测误差系统的特征多项式')
change(13,'题面取 $u=v+Kx$','题面取 $u=Kx$（加入参考输入时写 $u=v+Kx$）')
append(13,r'''
完整观测器取 $\hat y=C\hat x$：

$$
\dot{\hat x}=A\hat x+Bu+G(y-C\hat x)
$$

$$
\dot{\hat x}=\begin{bmatrix}-21&-10\\24&10\end{bmatrix}\hat x
+\begin{bmatrix}1\\1\end{bmatrix}u
+\begin{bmatrix}11\\-12\end{bmatrix}y
$$
''')
put(15,r'''
记原题矩阵为 $A,B,C$。有

$$
Q_c=[B\ \ AB]=\begin{bmatrix}0&100\\100&-500\end{bmatrix}
$$

$$
Q_o=\begin{bmatrix}C\\CA\end{bmatrix}=E_2
$$

两者均满秩，能分别配置状态反馈与观测误差的极点。

**先设计观测器。** 取 $\dot{\hat x}=A\hat x+Bu+G(y-C\hat x)$，令 $G=[g_1,g_2]^T$。比较

$$
\det[sE-(A-GC)]=s^2+(5+g_1)s+5g_1+g_2
$$

$$
(s+50)^2=s^2+100s+2500
$$

得

$$
G=\begin{bmatrix}95\\2025\end{bmatrix}
$$

**再设计状态反馈。** 令 $a=7.07$，严格保留题给小数；控制律取 $u=v-K\hat x$，$K=[k_1,k_2]$。题目所要求的多项式是

$$
f^*(s)=(s+a)^2+a^2=s^2+2as+2a^2
$$

而

$$
\det[sE-(A-BK)]=s^2+(5+100k_2)s+100k_1
$$

逐项比较，得到适合手算的精确关系

$$
k_1=\frac{a^2}{50}
$$

$$
k_2=\frac{2a-5}{100}
$$

完整实现为

$$
u=v-\frac{a^2}{50}\hat x_1-\frac{2a-5}{100}\hat x_2
$$

$$
\dot{\hat x}=\begin{bmatrix}-95&1\\-2025&-5\end{bmatrix}\hat x
+\begin{bmatrix}0\\100\end{bmatrix}u
+\begin{bmatrix}95\\2025\end{bmatrix}y
$$

设 $e=x-\hat x$，则 $\dot e=(A-GC)e$，$\dot x=(A-BK)x+BK e+Bv$。因而完整闭环的四个极点为题给的一对极点与两个 $-50$。

> [!warning] 题面与官方勘误的目标不同
> 题目 PDF 113 页给 $-7.07\pm\mathrm j7.07$；官方勘误图却给期望式 $s^2+\sqrt2s+1$，且使用 $u=v+K\hat x$，对应 $K=[-\frac1{100},\frac{5-\sqrt2}{100}]$。两者的目标极点和反馈符号均不同。本解按题面作答，不把 $7.07$ 擅自替换成 $5\sqrt2$，也不把勘误目标混入计算。

> [!note] 分离原理
> 分离原理是精确的矩阵结论，不需要观测器极点“足够快”才近似成立。较快的观测器只是在瞬态速度方面的设计选择。
''')
change(16,r'=\frac{s-a+2}{s^2-(2a+1)s+(a+3)(a-2)}',r'=\frac{s-a+2}{(s-a-3)(s-a+2)}=\frac1{s-a-3}')
change(16,'显然系统存在两个特征值都有正实部，故该系统无法通过设计全维状态观测器将闭环系统极点配置到 $-2,-6$ 处。',r'''取 $G=[g_1,g_2]^T$，则

$$
A-GC=\begin{bmatrix}7-g_1&0\\3-g_2&2\end{bmatrix}
$$

不能观模态 $2$ 始终不变，因此不能把观测误差极点配置到 $-2,-6$；原系统存在正极点本身并不是不能设计观测器的理由。''')
append(17,r'''
按题设选择的观测器完整方程为

$$
\dot{\hat x}=\begin{bmatrix}3&1\\-20&-6\end{bmatrix}\hat x
+\begin{bmatrix}0\\1\end{bmatrix}u
+\begin{bmatrix}-3\\15\end{bmatrix}y
$$

使用状态估计实现控制时取 $u=v-43\hat x_1-8\hat x_2$。这里观测器极点按原题取 $-1,-2$，不自行改成更快的极点。
''')
change(18,r'\begin{bmatrix}\frac{23}{2}\\[2pt]\frac{167}{2}\end{bmatrix}(y-\hat y)',r'\begin{bmatrix}\frac{23}{2}\\[2pt]\frac{167}{2}\end{bmatrix}y')
append(18,r'''
题目第（3）问要求完整闭环状态方程。由 $u=v+K\hat x$，原系统与观测器分别为

$$
\dot x=Ax+BK\hat x+Bv
$$

$$
\dot{\hat x}=GCx+(A-GC+BK)\hat x+Bv
$$

合并即得

$$
\begin{bmatrix}\dot x\\\dot{\hat x}\end{bmatrix}
=\begin{bmatrix}0&1&0&0\\-2&3&-6&-7\\23&0&-23&1\\167&0&-175&-4\end{bmatrix}
\begin{bmatrix}x\\\hat x\end{bmatrix}
+\begin{bmatrix}0\\1\\0\\1\end{bmatrix}v
$$

$$
y=[2\ \ 0\ \ 0\ \ 0]\begin{bmatrix}x\\\hat x\end{bmatrix}
$$

> [!warning] 观测误差只能注入一次
> 已写 $(A-GC)\hat x$ 后，应加 $Gy$；若同时再加 $G(y-\hat y)$，就会重复减去一次 $GC\hat x$，观测器极点随之改变。
''')
change(18,'（考点：①线性定常连续系统的李一法；','（考点：①李雅普诺夫方程判稳；')
put(19,r'''
记原题矩阵为 $A,B,C$，题给 $\zeta=0.707$、$\omega_n=1.414$。

（1）能控矩阵为

$$
Q_c=\begin{bmatrix}0&1\\1&-1\end{bmatrix}
$$

其秩为 $2$。设理想状态反馈为 $u=v-Kx$，$K=[k_1,k_2]$，则

$$
\det[sE-(A-BK)]=s^2+(1+k_2)s+k_1
$$

与 $s^2+2\zeta\omega_ns+\omega_n^2$ 比较，得

$$
k_1=\omega_n^2
$$

$$
k_2=2\zeta\omega_n-1
$$

这是题给小数下的精确关系，不必把乘积展开为多位小数。原书取 $K\approx[2,1]$ 是舍入结果，不与精确等号混用。

（2）能观矩阵为 $Q_o=[C;CA]=E_2$，满秩。取 $G=[g_1,g_2]^T$，有

$$
\det[sE-(A-GC)]=s^2+(g_1+1)s+g_1+g_2
$$

与 $(s+10)^2$ 比较得到

$$
G=\begin{bmatrix}19\\81\end{bmatrix}
$$

（3）实际控制律使用估计状态：

$$
u=v-k_1\hat x_1-k_2\hat x_2
$$

观测器状态方程为

$$
\dot{\hat x}=\begin{bmatrix}-19&1\\-81&-1\end{bmatrix}\hat x
+\begin{bmatrix}0\\1\end{bmatrix}u
+\begin{bmatrix}19\\81\end{bmatrix}y
$$

将控制律同时代入原系统和观测器，得完整闭环：

$$
\begin{bmatrix}\dot x\\\dot{\hat x}\end{bmatrix}
=\begin{bmatrix}A&-BK\\GC&A-GC-BK\end{bmatrix}
\begin{bmatrix}x\\\hat x\end{bmatrix}
+\begin{bmatrix}B\\B\end{bmatrix}v
$$

$$
\begin{aligned}
\begin{bmatrix}\dot x\\\dot{\hat x}\end{bmatrix}
&=\begin{bmatrix}0&1&0&0\\0&-1&-k_1&-k_2\\19&0&-19&1\\81&0&-81-k_1&-1-k_2\end{bmatrix}
\begin{bmatrix}x\\\hat x\end{bmatrix}\\
&\quad+\begin{bmatrix}0\\1\\0\\1\end{bmatrix}v
\end{aligned}
$$

$$
y=[1\ \ 0\ \ 0\ \ 0]\begin{bmatrix}x\\\hat x\end{bmatrix}
$$

取 $e=x-\hat x$ 后，状态矩阵分块上三角，特征多项式为 $(s^2+2\zeta\omega_ns+\omega_n^2)(s+10)^2$，可回验两组设计均成立。
''')
change(21,r'$|\lambda I-(A+HC)|=\lambda^2+(5+H_2)\lambda+5H_2+6H_1+6$',r'$|\lambda I-(A+HC)|=\lambda^2+(5-H_2)\lambda-5H_2-6H_1+6$')
append(21,r'''
以解法一实现实际控制，取 $u=v-K\hat x$，完整观测器为

$$
\dot{\hat x}=\begin{bmatrix}-5&-\frac{125}{6}\\6&-15\end{bmatrix}\hat x
+\begin{bmatrix}0\\2\end{bmatrix}u
+\begin{bmatrix}\frac{119}{6}\\15\end{bmatrix}y
$$

解法二若把 $H$ 同时取反，应写 $\dot{\hat x}=A\hat x+Bu-H(y-C\hat x)$，其误差矩阵才是 $A+HC$。状态反馈的正负号并不强迫观测器增益也换号，必须看各自的控制律。
''')
change(22,r'按 $|sI-(A-GC)|$ 正确展开为',r'按本图约定的 $|sI-(A+GC)|$ 正确展开为')
change(22,'（2）由分离定理可得，状态观测器的引入不改变原状态反馈系统的传递函数，则系统传递函数为',r'''（2）令 $e=x-\hat x$。按图中负号，观测误差满足 $\dot e=(A+GC)e$，且 $\dot x=(A-BK)x+BK e+Bv$。传递函数采用零初始条件，因此 $e(t)=0$，系统传递函数为''')
def write(p,t):
    raw=p.read_bytes();bom=b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    p.write_bytes(bom+t.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
write(ap,a)
print('adv3 first mathematical completion applied')

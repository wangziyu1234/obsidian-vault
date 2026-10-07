from pathlib import Path
import re
base=Path('D:/obsidian/控制理论/777习题集')
ap=next(base.glob('现控200题强化 专题三*答案*.md'));qp=next(base.glob('现控200题强化 专题三*题目*.md'))
a=ap.read_text(encoding='utf-8-sig');q=qp.read_text(encoding='utf-8-sig')
def get(n):return re.search(rf'^\*\*3-{n}　答案.*?(?=^\*\*3-\d+　答案|^## |\Z)',a,re.M|re.S)[0]
def change(n,old,new):
    global a
    b=get(n);assert old in b,(n,old[:100]);a=a.replace(b,b.replace(old,new))
def append(n,new):
    global a
    b=get(n);idx=b.find('> [!note] 本题总结');idx=idx if idx>=0 else len(b)
    a=a.replace(b,b[:idx].rstrip()+'\n\n'+new.strip()+'\n\n'+b[idx:])
def put(n,new):
    global a
    b=get(n);a=a.replace(b,b.split('\n',1)[0]+'\n\n'+new.strip()+'\n\n')
b=get(23); cut=b.index('（2）构造'); a=a.replace(b,b[:cut]+r'''
（2）本实现中 $y=x_3$ 已可测，需要估计的是 $z=[x_1,x_2]^T$。无需变换（取 $T=E_3$），直接分块：

$$
\dot z=A_{11}z+A_{12}y+b_1u
$$

$$
\dot y=A_{21}z+A_{22}y+b_2u
$$

$$
A_{11}=\begin{bmatrix}0&0\\1&0\end{bmatrix},\qquad
A_{12}=\begin{bmatrix}0\\-2\end{bmatrix}
$$

$$
A_{21}=[0\ \ 1],\qquad A_{22}=-3
$$

$$
b_1=\begin{bmatrix}1\\0\end{bmatrix},\qquad b_2=0
$$

设 $G=[g_1,g_2]^T$。估计误差矩阵为 $F=A_{11}-GA_{21}$，要求

$$
\det(sE-F)=s^2+g_2s+g_1=(s+6)^2
$$

故

$$
G=\begin{bmatrix}36\\12\end{bmatrix}
$$

为了避免对测量输出求导，引入二维观测器状态 $\omega=\hat z-Gy$。于是

$$
\dot\omega=F\omega+(FG+A_{12}-GA_{22})y+(b_1-Gb_2)u
$$

代入得到可直接实现的方程

$$
\dot\omega=\begin{bmatrix}0&-36\\1&-12\end{bmatrix}\omega
+\begin{bmatrix}-324\\-74\end{bmatrix}y
+\begin{bmatrix}1\\0\end{bmatrix}u
$$

状态还原为

$$
\hat x=\begin{bmatrix}\omega_1+36y\\\omega_2+12y\\y\end{bmatrix}
$$

用第（1）问的正反馈口径实现 $u=v+K\hat x$，即

$$
u=v-3\omega_1+\omega_2-101y
$$

回代误差 $z-\hat z$ 的微分方程为 $\dot e=Fe$，特征式为 $(s+6)^2$。

（3）一般先令 $T^{-1}=\begin{bmatrix}R\\C\end{bmatrix}$，使最后一组新坐标就是可测输出；再从与 $C$ 行空间互补的行向量中选 $R$，保证 $T^{-1}$ 可逆。这样的 $R$ 不唯一，故 $T$ 不唯一；仅说“任意非奇异矩阵均可”还不足以保证所需的输出分块。

> [!note] 状态分块
> 本题直接可测的是 $x_3$，不是 $x_1$；二维向量 $z$ 和单个状态分量应分开记。原答案含 $\dot y$ 的中间式还需代入 $\hat z=\omega+Gy$，才能得到以上无需输出微分器的实现。

''')
change(24,'设 $\\mathrm{rank}(M)=3$','算得 $\\mathrm{rank}(M)=3$')
change(24,r'\bar B=T^{-1}B=\begin{bmatrix}\bar B_1\\\bar B_2\end{bmatrix}=\begin{bmatrix}0\\0\\1\end{bmatrix}',r'\bar B=T^{-1}B=\begin{bmatrix}\bar B_1\\\bar B_2\end{bmatrix}=\begin{bmatrix}1\\0\\0\end{bmatrix}')
change(24,'降维观测器方程为',r'取 $\bar x=T^{-1}x=[x_3,x_2,x_1]^T$，将前两项记为 $z$，最后一项为 $y=x_1$。定义 $\omega=\hat z-Gy$；下式中的 $\hat{\bar x}_1$ 指前两项组成的向量 $\hat z$。降维观测器方程为')
append(24,r'''
控制律为 $u=v-K\hat x$，代入状态还原式可得

$$
u=v-\omega_1-2\omega_2-19y
$$

由 $\bar B=[1,0,0]^T$ 可见控制输入进入 $\dot\omega_1$，不能在状态变量图中漏掉。传递函数采用对象和观测器均为零初始条件；任意初始估计误差还会产生衰减的自由响应。
''')
change(24,r'\omega(s)=C',r'W(s)=C')
put(25,r'''
用 $P_0=x(0)$ 统一表示原题给定的 $n\times n$ 初值矩阵。令

$$
X(t)=e^{At}P_0e^{A^Tt}
$$

先验初值：$X(0)=P_0$。再按矩阵乘积求导，保留乘法顺序：

$$
\dot X=Ae^{At}P_0e^{A^Tt}+e^{At}P_0A^Te^{A^Tt}
$$

由于 $A^T$ 与它自身的矩阵指数可交换，得到

$$
\dot X=AX+XA^T
$$

所以 $X(t)$ 满足原方程和初值。该线性矩阵微分方程的初值解唯一，故

$$
x(t)=e^{At}P_0e^{A^Tt}
$$

这里没有把 $P_0$ 与 $A$ 或矩阵指数交换；三者通常不能交换。
''')
put(26,r'''
设 $B\in\mathbb R^{n\times m}$、$K\in\mathbb R^{m\times n}$。对任意复数 $\lambda$，有块矩阵恒等式

$$
[\lambda E_n-A\ \ B]
\begin{bmatrix}E_n&0\\-K&E_m\end{bmatrix}
=[\lambda E_n-(A+BK)\ \ B]
$$

右乘的块三角矩阵可逆（逆阵把 $-K$ 换为 $K$），因此

$$
r[\lambda E_n-A\ \ B]=r[\lambda E_n-(A+BK)\ \ B]
$$

由 PBH 判据，若 $(A,B)$ 完全能控，则对任意 $K$，$(A+BK,B)$ 都完全能控。反之，若后者对所有 $K$ 完全能控，取 $K=0$ 就得 $(A,B)$ 完全能控。充要性得证。
''')
put(28,r'''
令 $Q_c=[b,Ab,\ldots,A^{n-1}b]$。系统不完全能控，故存在状态变换 $z=Px$，使

$$
\bar A=PAP^{-1}=\begin{bmatrix}A_c&A_{12}\\0&A_u\end{bmatrix}
$$

$$
\bar b=Pb=\begin{bmatrix}b_c\\0\end{bmatrix}
$$

其中不能控块 $A_u$ 的维数至少为 $1$。在复数域取它的一个左特征向量 $w^T\ne0$，满足

$$
w^TA_u=\lambda w^T
$$

块三角性保证 $\lambda$ 也是 $A$ 的特征值。构造非零行向量

$$
q^T=[0\ \ w^T]P
$$

分别相乘可得

$$
q^TA=[0\ \ w^TA_u]P=\lambda q^T
$$

$$
q^Tb=[0\ \ w^T]\bar b=0
$$

所以

$$
q^T[\lambda E-A\ \ b]=0
$$

因 $q^T\ne0$，该矩阵的行线性相关，故 $r[\lambda E-A\ \ b]<n$，正是所需结论。

> [!note] 判据的反向也成立
> 若存在这样的 $q^T$，则 $q^TA^kb=\lambda^kq^Tb=0$，于是 $q^TQ_c=0$，系统不完全能控。这里是“存在一个特征值”，并非每个特征值均不满秩。
''')
put(29,r'''
系统不完全能观，可以选非奇异变换 $z=Px$，把能观部分放在前面：

$$
\bar A=PAP^{-1}=\begin{bmatrix}A_o&0\\A_{21}&A_u\end{bmatrix}
$$

$$
\bar C=CP^{-1}=[C_o\ \ 0]
$$

不能观块 $A_u$ 非空。在复数域取它的一个非零右特征向量 $w$，使 $A_uw=\lambda w$；块三角性保证 $\lambda$ 也是 $A$ 的特征值。构造

$$
q=P^{-1}\begin{bmatrix}0\\w\end{bmatrix}\ne0
$$

于是

$$
Aq=P^{-1}\begin{bmatrix}0\\A_uw\end{bmatrix}=\lambda q
$$

$$
Cq=[C_o\ \ 0]\begin{bmatrix}0\\w\end{bmatrix}=0
$$

合起来即

$$
\begin{bmatrix}\lambda E-A\\C\end{bmatrix}q=0
$$

因为 $q\ne0$，该矩阵的列线性相关，秩小于 $n$，得证。

> [!note] 判据的反向也成立
> 由 $Aq=\lambda q$、$Cq=0$，可得 $CA^kq=\lambda^kCq=0$，从而 $Q_oq=0$，系统不完全能观。右特征向量 $q,w$ 是列向量，不能写成与维数不符的行向量。
''')
append(32,r'''
这里采用控制律 $u=Kx+Fv$。代回原系统，

$$
A+BK=0
$$

$$
CBF=E_2
$$

因此 $\dot y=v$，零初始条件下

$$
Y(s)=\begin{bmatrix}\frac1s&0\\0&\frac1s\end{bmatrix}V(s)
$$

这验证了两个通道确实各为一个积分器。积分型解耦的极点在原点，不应另外宣称它渐近稳定；若改用 $u=Fv-Kx$ 的定义，反馈阵应取 $-E_2$。
''')
change(32,'系统可动态解耦','可通过状态反馈及输入变换实现积分型解耦')
change(33,r'10P_{12}-2P_{22}=0',r'10P_{12}-2P_{22}=-1')
change(33,r'含正实部 $\approx2.70$',r'包含正根 $\frac{-1+\sqrt{41}}2>0$')
needle='（2）设 $K=[K_0\\ \\ K_1]$，'
change(33,needle,r'''
能控、能观性也需要分别回答：

$$
Q_c=[b\ \ Ab]=\begin{bmatrix}1&0\\0&2\end{bmatrix}
$$

$$
Q_o=\begin{bmatrix}c\\cA\end{bmatrix}=\begin{bmatrix}1&0\\0&5\end{bmatrix}
$$

两者均满秩，因此系统完全能控、完全能观。

（2）设 $K=[K_0\ \ K_1]$，''')
append(33,r'''
第（3）问的闭环极点为 $-2,-4$，满足终值定理条件。因此

$$
y(\infty)=\lim_{s\to0}sY(s)=\frac18
$$

单位阶跃下稳态输出和稳态增益都为 $\frac18$；第（4）问乘前置增益 $\beta=8$ 后，稳态输出变为 $1$，闭环极点不变。
''')
def write(p,t):
    raw=p.read_bytes();bom=b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    p.write_bytes(bom+t.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
write(ap,a)
print('adv3 remaining mathematics completed')

from pathlib import Path
import re
base=Path('D:/obsidian/控制理论/777习题集')
ap=next(base.glob('现控200题强化 专题三*答案*.md'));qp=next(base.glob('现控200题强化 专题三*题目*.md'))
def read(p):return p.read_text(encoding='utf-8-sig')
def write(p,t):
    raw=p.read_bytes();p.write_bytes(t.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
a=read(ap);q=read(qp)
def get(n):return re.search(rf'^\*\*3-{n}　答案.*?(?=^\*\*3-\d+　答案|^## |\Z)',a,re.M|re.S)[0]
def put(n,body):
    global a
    old=get(n);head=old.split('\n',1)[0];a=a.replace(old,head+'\n\n'+body.strip()+'\n\n')
def qfix(n,old,new):
    global q
    m=re.search(rf'^\*\*3-{n}[（ ].*?(?=^\*\*3-\d+|^## |\Z)',q,re.M|re.S)
    assert m and old in m[0]
    q=q[:m.start()]+m[0].replace(old,new)+q[m.end():]
qfix(11,r'\begin{bmatrix}1\\0\\1\\1\\1\end{bmatrix}',r'\begin{bmatrix}1\\0\\0\\1\\1\end{bmatrix}')
qfix(12,r'\begin{bmatrix}1\\0\\0\end{bmatrix}',r'\begin{bmatrix}1\\1\\0\end{bmatrix}')
put(11,r'''
原题输入列为 $B=[1,0,0,1,1]^T$，第三分量是 $0$。矩阵 $A$ 由 $-2$ 的二阶约当块与 $+1$ 的三阶约当块组成。

前一块只驱动链首，能控维数为 $1$；后一块输入链尾非零，能控维数为 $3$。两块特征值不同，故总能控维数为 $4$。唯一不能控模态为 $-2$，已经稳定，所以系统可镇定。

取负反馈 $u=v-Kx$。为保留前一块的两个 $-2$，先选 $k_1=0$；$x_2$ 满足 $\dot x_2=-2x_2$，$k_2$ 只产生块间耦合，不改变极点。

余下三个状态的矩阵与输入列为

$$
J=\begin{bmatrix}1&1&0\\0&1&1\\0&0&1\end{bmatrix}
$$

$$
b_J=\begin{bmatrix}0\\1\\1\end{bmatrix}
$$

直接展开 $\det[sI-J+b_J(k_3,k_4,k_5)]$：

$$
\begin{aligned}
f_J(s)&=(s-1)^3+k_3s+k_4s(s-1)+k_5(s-1)^2\\
&=s^3+(k_4+k_5-3)s^2\\
&\quad+(k_3-k_4-2k_5+3)s+k_5-1
\end{aligned}
$$

余下目标为 $-1,-1,-2$，所以

$$
f_J^*(s)=(s+1)^2(s+2)=s^3+4s^2+5s+2
$$

先比常数项，再比二次项、一次项：

$$
k_5=3
$$

$$
k_4=4
$$

$$
k_3=12
$$

因此可取

$$
K=[0\ \ k_2\ \ 12\ \ 4\ \ 3],\qquad k_2\in\mathbb R
$$

回代得到完整特征多项式 $(s+2)^2f_J(s)=(s+1)^2(s+2)^3$。

> [!note] 题面回查与旧录入订正
> 原题 PDF 111 页明确给 $B_3=0$，不是 $1$。旧笔记按错误输入列把 $k_5=3$ 改成 $-9$，现撤销该误判。$-2$ 的二重块也不是整块不能控，而是其中一个模态不能控；$+1$ 的三重块完全能控。
''')
b=get(12);a=a.replace(b,b.replace(r'\begin{bmatrix}1\\0\\0\end{bmatrix}u',r'\begin{bmatrix}1\\1\\0\end{bmatrix}u'))
b=get(5);b=b.replace(r'W(s)=C(sI-A)^{-1}B=',r'W_{wy}(s)=C[sI-(A-BK)]^{-1}D=')
b=b.replace('（2）取 $k_1=2$',r'代入 $k_1=2k_2-4$，闭环特征式为 $(s+2)(s+k_2-2)$；若还要求内部渐近稳定，须 $k_2>2$。'+'\n\n'+'（2）取 $k_1=2$');a=a.replace(get(5),b)
b=get(7).replace(r'\lambda-k_3',r'\lambda+k_3');a=a.replace(get(7),b)
b=get(17).replace(r'\begin{bmatrix}c\\Ac\end{bmatrix}',r'\begin{bmatrix}c\\cA\end{bmatrix}');a=a.replace(get(17),b)
b=get(18);marker=r'平衡点 $x_e=\begin{bmatrix}0\\0\end{bmatrix}$。'
addition=r'''

按题目指定的李雅普诺夫方程法，取 $Q=I$、$P=\begin{bmatrix}p&r\\r&q\end{bmatrix}$。展开 $A^TP+PA=-I$ 得

$$
-4r=-1
$$

$$
p+3r-2q=0
$$

$$
2r+6q=-1
$$

依次求得

$$
P=\begin{bmatrix}-\frac54&\frac14\\\frac14&-\frac14\end{bmatrix}
$$

$P$ 负定，故 $V=-x^TPx$ 正定，且 $\dot V=x^Tx>0$。原点不稳定。再用特征值作独立核对：
'''
assert marker in b;a=a.replace(get(18),b.replace(marker,marker+addition))
put(27,r'''
讨论零输入内部稳定性，令 $u=0$。取 $V=x^TPx$，由 $P$ 对称正定，$V$ 正定且径向无界。

$$
\dot V=x^T(A^TP+PA)x=-x^TC^TCx=-\|Cx\|^2\le0
$$

这里通常只能说**半负定**；$x\ne0$ 并不保证 $Cx\ne0$，完全能观也不意味着 $C^TC$ 正定。

考察 $\dot V=0$ 中的最大不变集。若一条轨迹始终在此集合，则

$$
Ce^{At}x(0)=0\qquad(t\ge0)
$$

在 $t=0$ 处依次求导得到

$$
Cx(0)=CAx(0)=\cdots=CA^{n-1}x(0)=0
$$

即 $Q_ox(0)=0$。由完全能观，$r(Q_o)=n$，只能有 $x(0)=0$。

因此最大不变集只有原点。$V$ 的各子水平集闭、有界、正向不变，LaSalle 不变集定理给出原点大范围渐近稳定。
''')
b=get(28).replace('非零 $n$ 维常行向量 $\alpha$','非零 $n$ 维列向量 $\alpha$');a=a.replace(get(28),b)
b=get(29).replace('q_o^T','q_o').replace('q^T','q').replace(r'\bar A q',r'Aq').replace(r'\bar Aq',r'Aq');a=a.replace(get(29),b)
put(30,r'''
（1）设 $x=Tz$，其中 $T$ 为常数非奇异矩阵。新状态矩阵为 $\bar A=T^{-1}AT$，且

$$
\begin{aligned}
\det(sI-\bar A)&=\det[T^{-1}(sI-A)T]\\
&=\det(T^{-1})\det(sI-A)\det T\\
&=\det(sI-A)
\end{aligned}
$$

两矩阵的特征值相同，因此渐近稳定性不变。

（2）题目要求的是**保持同一个 $A$，构造一个输出行 $c$**。仅引用对偶系统 $(A^T,b^T)$ 的能观性不能完成这个证明。

由 $(A,b)$ 能控，方阵

$$
Q_c=[b\ \ Ab\ \cdots\ A^{n-1}b]
$$

可逆。令 $e_n$ 为第 $n$ 个单位列向量，取

$$
c=e_n^TQ_c^{-1}
$$

则 $cQ_c=e_n^T$，即

$$
cA^ib=0\quad(0\le i\le n-2)
$$

$$
cA^{n-1}b=1
$$

设 $Q_o=[c;cA;\ldots;cA^{n-1}]$，其与 $Q_c$ 乘积的 $(i,j)$ 元为 $cA^{i+j-2}b$。反对角线上均为 $1$，反对角线上方均为 $0$。倒序排列各列后即为单位对角的下三角矩阵，因此

$$
\det(Q_oQ_c)=(-1)^{n(n-1)/2}\ne0
$$

所以 $Q_o$ 可逆，构造出的 $(A,c)$ 完全能观。
''')
put(31,r'''
> [!warning] 第（1）问原题条件漏项
> 原题 PDF 122 页写 $i=1,2,\ldots,n-2$，没有 $i=0$。按此字面条件，结论不成立，不能直接证明 $Q_oQ_c$ 满秩。以下先给反例，再给补足条件后的证明。

（1）取 $n=3$，

$$
A=\operatorname{diag}(1,-1,0)
$$

$$
b=[1\ \ 1\ \ 0]^T,\qquad c=[1\ \ 1\ \ 0]
$$

有 $cAb=0$、$cA^2b=2\ne0$，符合原题条件；但 $Q_c$ 第三行、$Q_o$ 第三列均为零，且两者秩均为 $2$。所以原命题为假。

若补上 $cb=0$，即改成 $cA^ib=0$（$i=0,1,\ldots,n-2$），令 $\mu=cA^{n-1}b\ne0$，则

$$
Q_c=[b\ \ Ab\ \cdots\ A^{n-1}b]
$$

$$
Q_o=\begin{bmatrix}c\\cA\\\vdots\\cA^{n-1}\end{bmatrix}
$$

$Q_oQ_c$ 的反对角线上为 $\mu$，其上方全为零。将列次序反转后是对角元全为 $\mu$ 的下三角矩阵，故

$$
\det(Q_oQ_c)=(-1)^{n(n-1)/2}\mu^n\ne0
$$

于是 $Q_c,Q_o$ 都满秩，修正后的命题成立。

（2）这个传递函数恒等式本身不需要第（1）问的条件。对 $sI-A$ 可逆的 $s$，由秩一行列式恒等式，

$$
\begin{aligned}
\det(sI-A-bc)&=\det(sI-A)\det[I-(sI-A)^{-1}bc]\\
&=\det(sI-A)[1-c(sI-A)^{-1}b]
\end{aligned}
$$

移项即得有理函数恒等式

$$
G(s)=c(sI-A)^{-1}b=\frac{\det(sI-A)-\det(sI-A-bc)}{\det(sI-A)}
$$

若用正反馈解释，$u=v+y$ 给 $W_0=W/(1-W)$，反解应为 $W=W_0/(1+W_0)$；旧解反解式中的负号不对。
''')
write(ap,a);write(qp,q)
print('adv3 confirmed mathematical repairs applied')

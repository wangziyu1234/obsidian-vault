from pathlib import Path
import re

p=Path('控制理论/777习题集/现控200题基础 第5章 线性定常系统的综合（答案与解析）.md')
raw=p.read_bytes()
text=raw.decode('utf-8-sig').replace('\r\n','\n')
changed=[]
def edit(n, old, new):
    global text
    start=text.index(f'**5-{n}　答案')
    end=text.find('\n**5-',start+1)
    if end<0: end=len(text)
    part=text[start:end]
    assert old in part, (n,old[:60])
    text=text[:start]+part.replace(old,new,1)+text[end:]
    if n not in changed: changed.append(n)

edit(1,'不能控极点 $\\lambda=-1$ 与期望极点',r'''上述两个秩可直接由 PBH 矩阵看出：

$$
[-2I-A\ \ B]=\begin{bmatrix}0&-1&1\\0&-1&0\end{bmatrix}
$$

后两列构成的二阶子式为 $1$，故秩为 $2$。

$$
[-I-A\ \ B]=\begin{bmatrix}1&-1&1\\0&0&0\end{bmatrix}
$$

第二行全零、第一行非零，故秩为 $1$。

不能控极点 $\lambda=-1$ 与期望极点''')
edit(1,'> [!note] 本题总结',r'''也可直接构造反馈作验证。取 $u=v-Kx$，则

$$
A-BK=\begin{bmatrix}-2-k_1&1-k_2\\0&-1\end{bmatrix}
$$

取 $k_1=4$、$k_2$ 任意，上三角阵的两个对角元就是 $-6,-1$。

> [!note] 本题总结''')
edit(3,'$$\nP^{-1}AP=',r'''由 $x=P\tilde x$ 逐行得到 $x_1=\tilde x_1+2\tilde x_2$、$x_2=\tilde x_3$、$x_3=\tilde x_2$，反解即得上面的 $P^{-1}$。逐列乘 $A$：

$$
AP=\begin{bmatrix}2&3&1\\0&0&-1\\1&2&0\end{bmatrix}
$$

左乘 $P^{-1}$ 就是依次取 $AP$ 的“第一行减两倍第三行、第三行、第二行”，故

$$
P^{-1}AP=''')
edit(3,'（复算：$A-BK=',r'''增益换回原坐标时逐列相乘：

$$
K=[4\ \ 8\ \ 0]P^{-1}=[4\ \ 0\ \ -8+8]=[4\ \ 0\ \ 0]
$$

（复算：$A-BK=''')
edit(5,'比较系数：',r'''行列式的展开过程为

$$
\lambda I-(A-BK)=\begin{bmatrix}\lambda+k_1&k_2-2\\3&\lambda+5\end{bmatrix}
$$

$$
f(\lambda)=(\lambda+k_1)(\lambda+5)-3(k_2-2)
$$

比较系数：''')
edit(7,'比较系数：',r'''这里二阶行列式可先保留因式，避免漏掉 $k_1$ 的常数项：

$$
\lambda I-(A+BK)=\begin{bmatrix}\lambda+1-2k_1&-2k_2\\3&\lambda+\frac32\end{bmatrix}
$$

$$
f(\lambda)=(\lambda+1-2k_1)\left(\lambda+\frac32\right)+6k_2
$$

比较系数：''')
edit(8,'$Q_c$ 满秩，完全能控。',r'''先算能控矩阵：

$$
Q_c=[B\ \ AB]=\begin{bmatrix}0&1\\1&-4\end{bmatrix}
$$

$$
\det Q_c=-1\ne0
$$

故完全能控。''')
edit(14,'（2）PBH 判据：$\\lambda=1$ 时 $\\mathrm{rank}[\\lambda I-A\\ \\ B]=4$（能控），$\\lambda=-1$ 时 $\\mathrm{rank}=3\\lt4$（不能控）。两个不能控极点 $-1,-1$ 恰为期望极点，故能配置。',r'''（2）按列计算能控矩阵：

$$
Q_c=[B\ \ AB\ \ A^2B\ \ A^3B]
=\begin{bmatrix}0&1&2&3\\1&1&1&1\\0&0&0&0\\0&0&0&0\end{bmatrix}
$$

左上二阶子式为 $-1$，后两行全零，故秩恰为 $2$。前两个状态构成能控块，后两个状态的自治矩阵为 $\begin{bmatrix}-1&1\\0&-1\end{bmatrix}$。两个不能控极点 $-1,-1$ 恰为期望极点，故能配置。''')
edit(14,'要 $f(s)=(s+1)^4$，需',r'''因为反馈只改变 $A$ 的第二行，闭环矩阵保持上三角分块，特征行列式等于两个对角块的行列式之积；上面的二阶因子展开为

$$
(s-1)(s-1-k_2)-k_1=s^2-(2+k_2)s+1+k_2-k_1
$$

要 $f(s)=(s+1)^4$，需''')
edit(16,'$$\n\\bar A=R_c^{-1}AR_c=',r'''逆矩阵可以由 $x_1=2\bar x_1+\bar x_2$、$x_2=\bar x_1+\bar x_2$、$x_3=-\bar x_1-\bar x_2+\bar x_3$ 反解：

$$
R_c^{-1}=\begin{bmatrix}1&-1&0\\-1&2&0\\0&1&1\end{bmatrix}
$$

先逐列计算

$$
AR_c=\begin{bmatrix}3&2&2\\2&2&0\\-2&-2&3\end{bmatrix}
$$

左乘 $R_c^{-1}$ 时，依次取第一行减第二行、负第一行加两倍第二行、第二行加第三行，得到

$$
\bar A=R_c^{-1}AR_c=''')
edit(17,'② $W(s)=',r'''② 先求输入对应的逆矩阵列：

$$
sI-A=\begin{bmatrix}s+2&-4\\-1&s-1\end{bmatrix}
$$

$$
(sI-A)^{-1}B=\frac{1}{s^2+s-6}\begin{bmatrix}s-1\\1\end{bmatrix}
$$

再乘 $C=[1\ \ -1]$，分子为 $(s-1)-1=s-2$，因此 $W(s)=''')
edit(19,'与 $(\\lambda+10)^2=\\lambda^2+20\\lambda+100$ 比较：$h_1=8.5$，$h_2=23.5$。观测器：',r'''展开时先用二阶行列式：

$$
f(\lambda)=(\lambda+2h_1)(\lambda+3)+(2+2h_2)
$$

与 $(\lambda+10)^2=\lambda^2+20\lambda+100$ 比较：

$$
2h_1+3=20\quad\Rightarrow\quad h_1=\frac{17}{2}
$$

$$
6h_1+2h_2+2=100\quad\Rightarrow\quad 2h_2=100-51-2=47
$$

故 $H=[\frac{17}{2}\ \ \frac{47}{2}]^T$。观测器：''')
edit(21,'设 $G=[g_1\\ g_2\\ g_3]^T$，',r'''能观矩阵沿第一行展开，非零项对应的二阶子式为 $\begin{vmatrix}0&2\\6&-2\end{vmatrix}=-12$，故 $\det U_o=-12\ne0$。

设 $G=[g_1\ g_2\ g_3]^T$，''')
edit(21,'与 $(\\lambda+5)^3=',r'''沿 $\lambda I-(A-GC)$ 第一行展开可保留为

$$
\begin{aligned}
f(\lambda)
&=(\lambda-1)\big[(\lambda+1)(\lambda+g_3)+2g_2-2\big]\\
&\quad-6(\lambda+g_3)+6g_1.
\end{aligned}
$$

展开各次幂即得到前式。与 $(\lambda+5)^3=''')
edit(24,'（2）$U_o$ 满秩（$\\mathrm{rank}=3$）。',r'''（2）由 $C=[1\ \ 0\ \ 0]$，依次右乘 $A$ 得 $CA=[0\ \ 1\ \ 0]$、$CA^2=[0\ \ 0\ \ 1]$，故

$$
U_o=\begin{bmatrix}C\\CA\\CA^2\end{bmatrix}=I_3
$$

秩为 $3$。''')
edit(24,'期望 $(\\lambda+3)^3=',r'''沿特征矩阵第一行展开：

$$
f(\lambda)=(\lambda+g_1)\big[\lambda(\lambda+5)+6\big]+g_2(\lambda+5)+g_3
$$

期望 $(\lambda+3)^3=''')
edit(24,'（3）$U_c$ 满秩。',r'''（3）逐列计算可得

$$
U_c=\begin{bmatrix}0&0&1\\0&1&-5\\1&-5&19\end{bmatrix}
$$

沿第一行展开得 $\det U_c=-1$，故满秩。''')
edit(25,'> [!note] 复算提示',r'''逐次乘 $A$ 时，前两步为

$$
AB=\begin{bmatrix}0\\0\\20\\-4\end{bmatrix}
$$

$$
A^2B=\begin{bmatrix}0\\240\\-4\\-2399.2\end{bmatrix}
$$

第三步中的两个容易算错的分量分别是

$$
(A^3B)_2=-0.02\times240+12\times(-4)=-52.8
$$

$$
(A^3B)_4=-120\times(-4)-0.2\times(-2399.2)=959.84
$$

将 $Q_c$ 的列顺序倒排，得到下三角矩阵；四列倒排相当于 $6$ 次对换，不改变行列式符号，所以

$$
\det Q_c=240\times240\times20\times20=23040000\ne0
$$

> [!note] 复算提示''')
edit(25,'末元 sympy 精确计算为', '末元按上述乘法得到')
edit(25,'（3）基于重构状态设计控制器的要点：',r'''作为下问能观性的依据，先算

$$
U_o=\begin{bmatrix}
1&0&0&0\\
0&1&0&0\\
-12&-0.02&12&0\\
0.24&-11.9996&-0.24&12
\end{bmatrix}
$$

这是下三角阵，$\det U_o=1\times1\times12\times12=144\ne0$。

（3）基于重构状态设计控制器的要点：''')
edit(27,'设 $G=[g_1\\ g_2\\ g_3\\ g_4]^T$，',r'''为手算判秩，沿第一行第三列、再沿剩余矩阵第一行第三列展开，得到

$$
\det U_o=-12\omega^4\ne0
$$

设 $G=[g_1\ g_2\ g_3\ g_4]^T$，''')
edit(27,'期望：',r'''按增益分量收集行列式展开项，也可写成

$$
\begin{aligned}
f(\lambda)
&=\lambda^2(\lambda^2+\omega^2)
+g_3\lambda(\lambda^2+\omega^2)\\
&\quad+g_4(\lambda^2-3\omega^2)
-2\omega g_2\lambda-6\omega^3g_1.
\end{aligned}
$$

期望：''')
edit(29,'原系统状态估计：',r'''这里 $w$ 的方程不需要测量 $\dot y$。令未测状态 $z=[x_2,x_3]^T$，真实辅助量为 $\eta=z-Gy$。由分块方程相减：

$$
\begin{aligned}
\dot\eta
&=\dot z-G\dot y\\
&=(\bar A_{11}-G\bar A_{21})z
+(\bar A_{12}-G\bar A_{22})y
+(\bar B_1-G\bar B_2)u.
\end{aligned}
$$

记 $F=\bar A_{11}-G\bar A_{21}$，再代入 $z=\eta+Gy$，得到

$$
\dot\eta=F\eta+(FG+\bar A_{12}-G\bar A_{22})y+(\bar B_1-G\bar B_2)u
$$

本题的 $y$ 系数逐项相加为

$$
FG=\begin{bmatrix}2\times10-10\times7\\10-4\times7\end{bmatrix}
=\begin{bmatrix}-50\\-18\end{bmatrix}
$$

$$
FG+\bar A_{12}-G\bar A_{22}
=\begin{bmatrix}-50+1+30\\-18+0+21\end{bmatrix}
=\begin{bmatrix}-19\\3\end{bmatrix}
$$

以 $w$ 复制 $\eta$ 的动态方程，就得到上面的降维观测器。误差满足 $\frac{d}{dt}(\eta-w)=F(\eta-w)$，其极点为 $-1\pm\mathrm j$。

原系统状态估计：''')
edit(30,'$U_o$ 满秩，完全能观；',r'''先逐行计算能观矩阵：

$$
U_o=\begin{bmatrix}0&0&1\\0&2&0\\4&2&6\end{bmatrix}
$$

沿第一行展开得 $\det U_o=-8\ne0$，故完全能观；''')
edit(30,'状态估计：',r'''辅助变量的来源同样是消去输出导数：令 $z=[x_1,x_2]^T$、$\eta=z-Gy$，并记 $F=\bar A_{11}-G\bar A_{21}$，则

$$
\dot\eta=F\eta+(FG+\bar A_{12}-G\bar A_{22})y+(\bar B_1-G\bar B_2)u
$$

代入 $G=[3,4]^T$ 后，两个输入通道分别为

$$
FG+\bar A_{12}-G\bar A_{22}
=\begin{bmatrix}-20\\6-28\end{bmatrix}+\begin{bmatrix}0\\3\end{bmatrix}
=\begin{bmatrix}-20\\-19\end{bmatrix}
$$

$$
\bar B_1-G\bar B_2=\begin{bmatrix}0\\0\end{bmatrix}-2\begin{bmatrix}3\\4\end{bmatrix}
=\begin{bmatrix}-6\\-8\end{bmatrix}
$$

以 $w$ 复制 $\eta$ 的方程，误差满足 $\frac{d}{dt}(\eta-w)=F(\eta-w)$，故无需直接使用 $\dot y$。

状态估计：''')
edit(31,'（3）$\\Phi(t)=',r'''上述标准型也可通过具体坐标变换得到。能控坐标取

$$
z_{c1}=x_1,\qquad z_{c2}=x_2-4x_1
$$

于是 $\dot z_{c1}=z_{c2}$，且

$$
\dot z_{c2}=\dot x_2-4\dot x_1=16x_1-8x_2+u=-16z_{c1}-8z_{c2}+u
$$

能观坐标取

$$
z_{o1}=4x_1+x_2,\qquad z_{o2}=x_1
$$

于是

$$
\dot z_{o1}=4\dot x_1+\dot x_2=-16x_1+u=-16z_{o2}+u
$$

$$
\dot z_{o2}=-4x_1+x_2=z_{o1}-8z_{o2}
$$

两变换均可逆，而原矩阵本来就是约当块，无需再变换。

（3）$\Phi(t)=''')
edit(31,'（sympy 复核 ✓；',r'''其中 $A=-4I+N$，$N^2=0$，故 $e^{At}=e^{-4t}(I+tN)$。积分令 $r=t-\tau$，分部积分得到

$$
\begin{aligned}
\int_0^t re^{-4r}\,\mathrm dr
&=\left[-\frac r4e^{-4r}\right]_0^t+\frac14\int_0^t e^{-4r}\,\mathrm dr\\
&=\frac1{16}-\left(\frac t4+\frac1{16}\right)e^{-4t}.
\end{aligned}
$$

与零输入项 $e^{-4t}(1+t)$ 合并，常数系数为 $1-\frac1{16}=\frac{15}{16}$，$t$ 的系数为 $1-\frac14=\frac34$。

（''')
edit(31,'（4）$\\mathrm{rank}\\,Q_c=2$。',r'''（4）能控矩阵为

$$
Q_c=\begin{bmatrix}0&1\\1&-4\end{bmatrix},\qquad \det Q_c=-1\ne0
$$

故 $\mathrm{rank}\,Q_c=2$。''')
edit(31,'（5）$\\mathrm{rank}\\,Q_o=2$。',r'''（5）能观矩阵为

$$
Q_o=\begin{bmatrix}1&0\\-4&1\end{bmatrix},\qquad \det Q_o=1\ne0
$$

故 $\mathrm{rank}\,Q_o=2$。''')
edit(32,'（1）$\\mathrm{rank}\\,Q_c=2$。',r'''（1）$AB=[1,-1]^T$，所以

$$
Q_c=\begin{bmatrix}0&1\\1&-1\end{bmatrix},\qquad \det Q_c=-1\ne0
$$

故 $\mathrm{rank}\,Q_c=2$。''')
edit(32,'（2）$\\mathrm{rank}\\,Q_o=2$。',r'''（2）$CA=[0,1]$，所以 $Q_o=I_2$，故 $\mathrm{rank}\,Q_o=2$。''')
edit(33,'由分离定理，全维观测器的引入不改变闭环传递函数：',r'''传递函数须取对象与观测器的零初态。令 $e=x-\hat x$，两套状态方程相减得

$$
\dot e=(A-G_oC)e
$$

因 $e(0)=0$，有 $e(t)\equiv0$，故 $\hat x=x$。对象方程因而化为

$$
\dot x_1=x_2
$$

$$
\dot x_2=-2x_1-2x_2+v
$$

又 $y=x_1$，消去 $x_2$ 得

$$
\ddot y+2\dot y+2y=v
$$

取零初态拉普拉斯变换即有 $(s^2+2s+2)Y=V$。因此''')
edit(33,'（sympy 直接对上述四阶复合系统求 $C[sI-\\tilde A]^{-1}\\tilde B$ 验证，结果同为 $\\dfrac{1}{s^2+2s+2}$ ✓。）','非零初始估计误差会产生额外的暂态响应，但不属于零初态传递函数。')

# Keep original encoding and line endings.
out=text.replace('\n','\r\n') if b'\r\n' in raw else text
p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+out.encode('utf-8'))
print('Supplemented:', sorted(changed))

from pathlib import Path
import re
root=Path('D:/obsidian');folder=root/'控制理论/777习题集'
src=(root/'.workbuddy/mc-adv1-format.py').read_text(encoding='utf-8')
ns={'re':re};exec(src[src.index('def split_top'):src.index('# Keep complete')],ns)
ap=next(folder.glob('现控200题强化 专题二*答案与解析*.md'))
qp=next(folder.glob('现控200题强化 专题二*题目*.md'))
a=ap.read_text(encoding='utf-8');q=qp.read_text(encoding='utf-8')
# Keep the answer index narrow enough for vertical reading.
answers=[
r'不能控、能观；$W=\frac1{(s+1)(s+3)}$',
r'$u=v+Kx$ 时 $K=[-4\ \ -4\ \ -1]$',
r'不能控、能观；$W=\frac1{s-1}$；$y(1)=\frac{\mathrm e}{2}+\frac{3\mathrm e^{-3}}2-1$',
r'能控：$a\ne0,3$；能观：$a\ne1$',
r'对任意 $b$，$r(M)\le2$，不能控',
r'不稳定、能控能观；$K=[5\ \ \frac{13}{2}]$；单位稳态增益取 $\beta=8$',
r'不能控，不能镇定；不能控模态含 $\lambda=1$',
r'两子系统均能控能观；串联后不能控、能观',
r'$W=\frac{s}{(s+1)^2}$；能控、闭环不能观',
r'能控秩为 $2$；不能控模态 $\lambda=3$，不能镇定',
r'精确极点 $\frac{-3\pm\sqrt5}{2}$、留数 $\pm\frac1{\sqrt5}$；对角型实现能控能观',
r'$a\ne1,\frac12$ 时能观并可作能观规范形变换；原系统渐近稳定',
r'$W=\frac{s+1}{s^2+s-1}$；正反馈约定下 $k_1=-3,k_2=2$',
r'能控秩与能观秩均为 $2$；两种结构分解见正文',
r'与 2-14 同一系统；能控子系统及耦合项见正文',
r'$V=x_1^2+x_2^2$；大范围渐近稳定',
r'$P_{11}=\frac{25}{9}$、$P_{12}=\frac{500}{63}$、$P_{22}=\frac{113800}{1197}$；大范围渐近稳定',
r'$V=x_1^2+x_2^2$；$\dot V=-2(x_1^2+x_2^2)^2$；大范围渐近稳定',
r'原题 $f(0)\ne0$，原点不是平衡点；改常数项为 $+1$ 后原点不稳定',
r'$K=[-1\ \ 2]$；响应与正确状态变量图见正文；原系统渐近稳定',
r'$P=\frac14\begin{bmatrix}5&1\\1&1\end{bmatrix}$；大范围渐近稳定',
r'$\dot V=-4x_2^2$；最大不变集只有原点，大范围渐近稳定',
r'$(-2,1)$ 渐近稳定；$(0,-1)$ 不稳定',
r'$P=\mathrm{diag}(\frac43,-\frac13)$；不稳定；$x(1)=[\frac32\ \ 3]^T$、$x(2)=[\frac74\ \ -5]^T$',
r'$\det(E-G)=\frac34$，唯一平衡点为原点；$P=\frac43E$，大范围渐近稳定',
r'$T>0$ 且 $T\ne\frac{k\pi}{2}$ 时离散化后能控（$k=1,2,\ldots$）',
r'内部不稳定；$m=1$ 时 $W=\frac2{s+2}$，BIBO 稳定',
r'原题三阶；约简 $G=\frac1{s(s+1)}$，非 BIBO 稳定；最小实现二阶',
r'内部不稳定，$G=\frac1{s+1}$ 为 BIBO 稳定；$K=[11\ \ 7]$']
start=a.index('| 题号 | 答案 |');end=a.index('## 【题型1】',start)
table='| 题号 | 核心结论 |\n| :-- | :-- |\n'
table+='\n'.join(f'| [[#✏️ 2-{i}　解析\\|2-{i}]] | {x} |' for i,x in enumerate(answers,1))+'\n\n'
a=a[:start]+table+a[end:]
a=a.replace('由 LaSalle 不变集原理，又','又').replace('故系统在平衡点处**大范围渐近稳定**。','由 LaSalle 不变集原理，系统在平衡点处**大范围渐近稳定**。')
a=a.replace('连续有理真有理系统','连续有限维真有理系统')
for p,t in [(ap,a),(qp,q)]:
 t=re.sub(r'(?m)^(> )?\$\$\n(.*?)\n(?:> )?\$\$',ns['fmt'],t,flags=re.S)
 p.write_bytes(t.replace('\n','\r\n').encode('utf-8'))
print('Formatted topic 2 formula blocks and answer index.')

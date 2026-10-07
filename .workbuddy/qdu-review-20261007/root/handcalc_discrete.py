from edit_recent import edit
import re

def a06(t):
    t=t.replace(r'e^{-1}\approx0.367879',r'e^{-1}')
    t=t.replace('数值形式为\n\n$$\n4c[k]-2.471517765c[k-1]+0.367879441c[k-2]=3r[k]\n$$\n\n','')
    return t

def a07(t):
    old='K=2.5时z域和w域均不稳定；全实数稳定范围−1<K<2.163953，正增益时0<K<2.163953；K=2时阶跃稳态误差1/3。'
    new=r'$K=2.5$ 时不稳定；稳定范围 $-1<K<(1+e^{-1})/(1-e^{-1})$，正增益再与 $K>0$ 取交集；$K=2$ 时阶跃稳态误差 $1/3$。'
    assert old in t;t=t.replace(old,new)
    t=t.replace(r'p=3.5e^{-1}-2.5\approx-1.212422',r'p=\frac72e^{-1}-\frac52<-1')
    start=t.index('代入 $p\\approx-1.212422$：');end=t.index('**',start)
    # Preserve the following subsection; replace numerical bilinear verification.
    t=t[:start]+r'''由于 $p<-1$，双线性变换后的根为

$$
w=\frac{p-1}{p+1}>0
$$

因此 $w$ 平面也判为不稳定。这里 $e^{-1}<3/7$，故 $p<-1$ 可直接手算判断。

'''+t[end:]
    t=t.replace(r'\frac{1+e^{-1}}{1-e^{-1}}\approx2.163953',r'\frac{1+e^{-1}}{1-e^{-1}}')
    t=t.replace(r'\boxed{0<K<2.163953}',r'\boxed{0<K<\frac{1+e^{-1}}{1-e^{-1}}}')
    t=t.replace(r'$p=3e^{-1}-2\approx-0.896362$ 在单位圆内',r'$p=3e^{-1}-2$ 满足 $-1<p<1$（由 $1/3<e^{-1}<1$），在单位圆内')
    return t

def a09(t):
    t=t.replace('两极点约−0.283367、−0.003218，系统稳定。','朱利条件均满足，系统稳定。')
    start=t.index('数值形式为\n\n$$\n\\boxed{\\Phi(z)');end=t.index('> [!note]- 题面整理说明',start)
    t=t[:start]+r'''**3. 用精确系数判稳**

令 $a=e^{-1}$，闭环分母为 $z^2+pz+q$，其中

$$
p=\frac{7a^2-13a^5}{3}
$$

$$
q=a^7
$$

由 $0<a<1/2$，得到

$$
0<p=\frac{a^2(7-13a^3)}3<\frac7{12}<1
$$

$$
0<q<\frac1{128}<1
$$

二阶朱利条件逐项成立：

$$
1+p+q>0
$$

$$
1-p+q>1-\frac7{12}>0
$$

$$
1-q>1-\frac1{128}>0
$$

故闭环极点全部位于单位圆内，离散系统渐近稳定；无需先计算指数或极点的小数。

'''+t[end:]
    return t

edit(2006,'答案与解析',a06)
edit(2007,'答案与解析',a07)
edit(2009,'答案与解析',a09)

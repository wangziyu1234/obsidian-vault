from edit_recent import edit
import re

def a18(t):
    t=t.replace(r'3\sqrt5-5\approx1.708204',r'3\sqrt5-5')
    t=t.replace('稳定0<K<70；出现衰减振荡4.060673<K<70',r'稳定 $0<K<70$；衰减振荡 $\frac{38\sqrt{19}-56}{27}<K<70$')
    for val in ['-0.880367','4.060673','-5.239266','1.96350','2.68240','3.44597']:
        t=t.replace(r'\approx'+val,'')
    old='动态性能可由实际闭环阶跃响应进一步核验：'
    start=t.index(old);end=t.index('> [!note]- 题面整理说明',start)
    t=t[:start]+r'''在本题中，超前校正提高截止频率和相角裕度，通常对应响应加快、超调减小；这是对这一具体系统的动态性能判断。无计算器作答以校正前后的频率特性和裕度比较为依据，无需另求密采样阶跃响应的多位小数指标。

'''+t[end:]
    return t

def a19(t):
    t=t.replace('振荡K>16.371932；ζ=0.707时K≈29.866827',r'衰减振荡 $K>42\sqrt{105}-414$；$\zeta=0.707$ 时按根轨迹读图 $K\approx30$，精确关系见正文')
    for val in ['-4.753049','16.371932','-4.183346']:
        t=t.replace(r'\approx'+val,'')
    start=t.index('联立取正增益稳定根，得到');end=t.index('![[附件/青大825-2019',start)
    t=t[:start]+r'''消去 $K$，得

$$
\alpha^3-(40\zeta^2+2)\alpha^2+480\zeta^2\alpha-1440\zeta^2=0
$$

令 $\alpha_*$ 为代入题给 $\zeta=0.707$ 后、符合稳定复极点条件的实根，则

$$
\boxed{K=\frac{\alpha_*^2(24-2\alpha_*)}{20\zeta^2}}
$$

手算作图时沿阻尼比线与根轨迹的交点估读，可取 $K\approx30$。上面的两式给出精确关系，不要求手工求三次方程的多位小数；题给0.707仍保留为原始数据，不另换成 $1/\sqrt2$ 再列一套舍入答案。

'''+t[end:]
    return t

def a24(t):
    t=t.replace('稳定0<k<8.16；分离点−2.288584，k≈4.331570',r'稳定 $0<k<204/25$；分离点由 $4s_b^3+15s_b^2+16s_b+6=0$ 确定')
    t=t.replace(r's_b\approx-2.288584',r'-\frac{23}{10}<s_b<-\frac94')
    t=t.replace(r'k_b\approx4.331570',r'k_b=-s_b(s_b+3)(s_b^2+2s_b+2)')
    return t

edit(2018,'答案与解析',a18)
edit(2019,'答案与解析',a19)
edit(2024,'答案与解析',a24)

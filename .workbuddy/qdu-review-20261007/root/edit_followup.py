from edit_recent import edit
import re

def q20(t):
    old='其中 $K,T_1,T_2$ 均为正数，环内无时滞，非线性环节的描述函数 $N(A)>0$。'
    assert old in t
    return t.replace(old,'其中 $K,T_1,T_2$ 均为正数，非线性环节的描述函数 $N(A)>0$。图中反馈环节为 $H(s)=Ts+1$，本题取 $T=0$，因此按单位负反馈求解。')

def a20(t):
    old='#### （1）展开线性部分的频率响应\n\n按胡寿松'
    assert old in t
    return t.replace(old,'#### （1）展开线性部分的频率响应\n\n图中反馈环节为 $H(s)=Ts+1$，题设取 $T=0$，故 $H(s)=1$。这里的 $T$ 是反馈环节时间常数；“无时滞”并不意味着 $T=0$，两者不能混用。\n\n按胡寿松')

def handcalc(year,t):
    if year==2015:
        t=t.replace(r'$t_p=2\pi/\sqrt3\approx3.628\,\mathrm{s}$，超调量 $16.303\%$；5% 调节时间教材近似 $7.0\,\mathrm{s}$，严格定义为 $5.289093\ldots\,\mathrm{s}$；',r'$t_p=2\pi/\sqrt3\,\mathrm{s}$，超调量 $100e^{-\pi/\sqrt3}\%$；5% 调节时间按课程近似式取 $7\,\mathrm{s}$；')
        t=t.replace(r'\frac{2\pi}{\sqrt3}\approx3.628',r'\frac{2\pi}{\sqrt3}')
        t=t.replace(r'100e^{-\pi\zeta/\sqrt{1-\zeta^2}}\%=16.303\%',r'100e^{-\pi/\sqrt3}\%')
    else:
        t=t.replace(r'$t_p\approx1.21\,\mathrm{s}$；5%调节时间教材近似2.33 s，严格值1.763031… s；',r'$t_p=2\pi/(3\sqrt3)\,\mathrm{s}$；5%调节时间按课程近似式取 $7/3\,\mathrm{s}$；')
        t=t.replace(r'\frac{3\sqrt3}{2}\approx2.598',r'\frac{3\sqrt3}{2}')
        t=t.replace(r'\frac{2\pi}{3\sqrt3}\approx1.21',r'\frac{2\pi}{3\sqrt3}')
        t=t.replace(r'\frac73\approx2.33',r'\frac73')
    start=t.index('若严格定义调节时间' if year==2015 else '若按“此后始终留在最终值')
    end=t.index('**（2）静态误差系数。**',start)
    n='1' if year==2015 else '3'
    replacement=r'''> [!note] 调节时间的口径
> 上式采用课程常用的5%误差带估算公式，属于近似值。若要求实际响应最后一次进入误差带的严格时刻，需由下式确定 $t_s$，不能把估算式当成精确等式：
>
> $$
> c(t_s)=1.05
> $$
>
> $$
> \begin{aligned}
> c(t)&=1-e^{-Nt/2}\biggl[\cos\left(\frac{N\sqrt3}{2}t\right)\\
> &\qquad+\frac1{\sqrt3}\sin\left(\frac{N\sqrt3}{2}t\right)\biggr]
> \end{aligned}
> $$
>
> 取第一峰值之后的最后一个边界交点；无计算器作答保留这一关系，不要求求解超越方程的多位小数。

'''.replace('N',n)
    t=t[:start]+replacement+t[end:]
    t=t.replace('原题未规定调节时间估算口径，同时提供课程常用近似值与严格误差带定义值。','原题未规定调节时间估算口径，采用课程常用近似式；严格误差带定义另列说明。')
    return t

def a25(t):
    t=t.replace(r'$\omega=4$；预测 $A\approx0.55573$ 不稳定、$1.14556$ 稳定',r'$\omega=4$；预测小振幅 $A_-$ 不稳定、大振幅 $A_+$ 稳定（精确式见正文）')
    t=t.replace(r'\frac{\sqrt{8-2\sqrt{16-\pi^2}}}{\pi}\approx0.555729',r'\frac{\sqrt{8-2\sqrt{16-\pi^2}}}{\pi}')
    t=t.replace(r'\frac{\sqrt{8+2\sqrt{16-\pi^2}}}{\pi}\approx1.145559',r'\frac{\sqrt{8+2\sqrt{16-\pi^2}}}{\pi}')
    t=t.replace(r'\sqrt{1-e^{-1}}\approx0.7951<1',r'\sqrt{1-e^{-1}}<1')
    return t

edit(2020,'试题',q20)
edit(2020,'答案与解析',a20)
for year in [2015,2016]:edit(year,'答案与解析',lambda t,y=year:handcalc(y,t))
edit(2025,'答案与解析',a25)

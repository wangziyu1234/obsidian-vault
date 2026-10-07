from edit_recent import edit
import re

def a07(t):
    old='k≈0.336626，tp≈1.75615 s，5%严格调节时间≈2.33854 s（经验3.5公式≈2.60889 s），稳态误差≈1.609878。'
    new=r'令 $\zeta=-\ln(0.0948)/\sqrt{\pi^2+\ln^2(0.0948)}$，则 $k=(2\sqrt5\zeta-1)/5$；$t_p=\pi/(\sqrt5\sqrt{1-\zeta^2})$；$e_{ss}=6\sqrt5\zeta/5$。'
    assert old in t;t=t.replace(old,new)
    for num in ['0.694427','-167.079','0.599966','0.336626','1.75615','2.39932','1.609878']:
        t=t.replace(r'\approx'+num,'')
    start=t.index('取 $|\\varepsilon(t_s)|=0.05$');end=t.index('**（3）稳态误差**',start)
    t=t[:start]+r'''按课程常用5%带近似式，取

$$
t_s\approx\frac{3.5}{\zeta\sqrt5}
$$

若需保证进入误差带的包络界，则

$$
t_{s,\mathrm{env}}=\frac{-\ln(0.05\sqrt{1-\zeta^2})}{\zeta\sqrt5}
$$

严格的最后入带时刻由 $|\varepsilon(t_s)|=0.05$ 的最后一个正根确定。三种口径不同；无计算器作答保留精确参数和关系式，不要求数值求解超越方程。

'''+t[end:]
    return t

def a09(t):
    old=r'$t_r\approx0.06165\,\mathrm{s}$；5% 严格调节时间 $\approx0.23340\,\mathrm{s}$（包络界 $0.25451\,\mathrm{s}$）；$G(s)=1131.915491/[s(s+24.079456)]$。'
    new=r'令 $\ell=-\ln0.3$、$\beta=\arctan(\pi/\ell)$，则 $t_r=(\pi-\beta)/(10\pi)$；$G(s)=100(\pi^2+\ell^2)/[s(s+20\ell)]$。'
    assert old in t;t=t.replace(old,new)
    t=t.replace('记 $\\alpha=\\zeta\\omega_n$，',r'令 $\ell=-\ln0.3>0$。记 $\alpha=\zeta\omega_n$，')
    t=t.replace(r'12.039728\,\mathrm{s}^{-1}',r'10\ell\,\mathrm{s}^{-1}')
    t=t.replace(r'31.415927\,\mathrm{rad/s}',r'10\pi\,\mathrm{rad/s}')
    t=t.replace(r'33.643952\,\mathrm{rad/s}',r'10\sqrt{\ell^2+\pi^2}\,\mathrm{rad/s}')
    t=t.replace(r'\frac{\alpha}{\omega_n}=0.357857',r'\frac{\alpha}{\omega_n}=\frac{\ell}{\sqrt{\ell^2+\pi^2}}')
    t=t.replace(r'\arccos\zeta=1.204824\,\mathrm{rad}',r'\arccos\zeta=\arctan(\pi/\ell)')
    t=t.replace(r'\boxed{t_r\approx0.06165\,\mathrm{s}}',r'\boxed{t_r=\frac{\pi-\arctan(\pi/\ell)}{10\pi}\,\mathrm{s}}')
    t=t.replace('的该区间根，得到\n\n$$\n\\boxed{t_s\\approx0.23340\\,\\mathrm{s}}.\n$$','在 $(0.2,0.3)$ 内的根即为严格调节时间；保留此关系式，不要求手算多位小数。')
    t=t.replace(r'\approx0.25451\,\mathrm{s}','')
    t=t.replace('$0.29070\\,\\mathrm{s}$',r'$7/(20\ell)\,\mathrm{s}$')
    t=t.replace(r'\boxed{G(s)=\frac{1131.915491}{s(s+24.079456)}}',r'\boxed{G(s)=\frac{100(\pi^2+\ell^2)}{s(s+20\ell)}}')
    return t

def a11(t):
    old='tp≈1.963495 s；严格5%ts≈2.614524 s，包络界2.682397 s，经验值2.916667 s。'
    new=r'$t_p=5\pi/8\,\mathrm{s}$；5%调节时间的课程近似为 $35/12\,\mathrm{s}$，包络保证界为 $5\ln25/6\,\mathrm{s}$；严格时刻由响应入带方程确定。'
    assert old in t;t=t.replace(old,new)
    t=t.replace(r'\frac\pi{1.6}\approx1.963495',r'\frac\pi{1.6}=\frac{5\pi}8')
    t=t.replace(r'e^{-1.2\pi/1.6}\approx0.0947802',r'e^{-3\pi/4}')
    t=t.replace(r'$M_p^2\approx0.00898329<0.05$',r'$M_p^2=e^{-3\pi/2}<0.05$')
    t=t.replace('的根，得到\n\n$$\n\\boxed{t_s\\approx2.614524\\,\\mathrm{s}}.\n$$','在上述区间的根即为严格调节时间；无计算器作答保留此关系，不要求求出超越方程的多位小数根。')
    t=t.replace(r'\approx2.682397\,\mathrm{s}',r'=\frac{5\ln25}6\,\mathrm{s}')
    t=t.replace(r'\approx2.916667\,\mathrm{s}',r'=\frac{35}{12}\,\mathrm{s}')
    return t

edit(2007,'答案与解析',a07)
edit(2009,'答案与解析',a09)
edit(2011,'答案与解析',a11)

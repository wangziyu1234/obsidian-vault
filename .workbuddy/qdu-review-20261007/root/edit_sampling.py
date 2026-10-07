from edit_recent import edit
import sympy as S

tau,q=S.symbols('tau q',positive=True)
c=1+q*q-q*q*tau+q*(1-S.exp(-tau))
v=-q*q+q*S.exp(-tau)
assert S.simplify(S.diff(c,tau)-v)==0
assert S.simplify(v.subs(tau,-S.log(q)))==0
assert S.simplify(c.subs(tau,-S.log(q))-(1+q+q*q*S.log(q)))==0

addition=r'''
**连续输出的采样间峰值**

图中输出标为 $c(t)$，并未限定只观察采样时刻。前述结果是序列 $c[k]$ 的指标；连续输出还需计算两个样本之间的变化。

令

$$
q=1-a=1-e^{-1}
$$

$$
v(t)=\dot c(t)
$$

在第 $k$ 个保持区间内，输入保持为 $1-c[k]$，故

$$
\dot v+v=1-c[k]
$$

由零初值递推得

$$
v[1]=q
$$

$$
v[2]=q
$$

$$
v[3]=aq
$$

在 $t=3+\tau$、$0\le\tau\le1$ 内，有

$$
v(3+\tau)=-q^2+q e^{-\tau}
$$

$$
c(3+\tau)=1+q^2-q^2\tau+q(1-e^{-\tau})
$$

此时 $v(3)>0$、$v(4)<0$，且速度在本区间严格递减。令速度为零，得连续输出的首峰时间

$$
\boxed{t_{p,\mathrm{cont}}=3-\ln q}
$$

代回响应：

$$
\boxed{c_{\max}=1+q+q^2\ln q}
$$

$$
\boxed{\sigma_{\mathrm{cont}}\%=(q+q^2\ln q)\times100\%}
$$

该峰值发生在第3、4个样本之间；两个样本等高不表示连续输出在这一秒内保持平台。连续输出和采样序列的终值均为1，因此两种口径的稳态误差均为0。

'''

def answer(year,t):
    old='超调约39.94%；最早峰值3 s；稳态误差0'
    assert old in t
    t=t.replace(old,r'采样序列：超调 $(1-e^{-1})^2\times100\%$、首次峰值3 s；连续输出峰值见正文；稳态误差0')
    t=t.replace('第3、4个样本均达到首峰，按“首次达到峰值”定义', '第3、4个样本均达到采样序列的首峰，按“首次达到峰值”定义')
    needle=('> [!note]- 题面整理说明\n> - 根据图示明确单位阶跃输入、T=1 s；重复最高样本采用首次峰值时间定义。' if year==2017 else '> [!note]- 题面整理说明\n> - 回忆稿明确写“2017年第六题原题”，据此补入该题的完整题面与图。')
    assert needle in t
    t=t.replace(needle,addition+'> [!note]- 题面整理说明\n> - 单位阶跃输入、T=1 s；同时给出采样序列与图示连续输出的峰值指标，避免混用。')
    return t

def question(year,t):
    old='离散系统如下图，求系统的输出响应，确定超调量、峰值时间及系统的稳态误差。'
    assert old in t
    return t.replace(old,'采样控制系统如下图，求系统的输出响应、超调量、峰值时间及稳态误差。分别给出采样序列 $c[k]$ 的指标，并进一步计算图示连续输出 $c(t)$ 在采样间的峰值。')

for y in [2018]:
    edit(y,'答案与解析',lambda t,y=y:answer(y,t))
    edit(y,'试题',lambda t,y=y:question(y,t))
print('Sampling peak identities independently verified; both years updated.')

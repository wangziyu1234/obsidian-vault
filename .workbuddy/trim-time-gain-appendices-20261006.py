from pathlib import Path
import re

root=Path('D:/obsidian')
base=root/'控制理论/附录'
def read(name):
    p=base/name
    raw=p.read_bytes()
    return p,raw,raw.decode('utf-8-sig').replace('\r\n','\n')
def save(p,raw,text):
    text=re.sub(r'^modify: .*$', 'modify: 2026-10-06',text,count=1,flags=re.M)
    p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))

p,raw,text=read('附录 时域分析速查.md')
text=text.replace('> 一阶/二阶系统公式、动态性能指标、稳态误差表、劳斯判据的**纯速查**。先查二阶指标与稳态误差；一阶公式、劳斯表随后，非欠阻尼补充放在末尾。推导与例题见 [[03 第3章 线性系统的时域分析法]]。', '> 时域公式、适用条件与必要步骤；推导和例题见 [[03 第3章 线性系统的时域分析法]]。')
text=text.replace('**适用**：无零点、直流增益为 1 的标准二阶系统，零初始条件、单位阶跃输入；本节动态指标取 $0<\\zeta<1$。', '**无零点、单位直流增益；零初值、单位阶跃；$0<\\zeta<1$。**')
start=text.index('**阻尼比与性能对照**')
end=text.index('## 稳态误差',start)
text=text[:start]+r'''**超调量对照；最后一行为临界阻尼。**

| $\zeta$ | $\sigma\%$ |
| :--: | :--: |
| 0.3 | ≈37% |
| 0.5 | ≈16% |
| $\frac{\sqrt2}{2}$ | ≈4.3% |
| 1 | 0% |

非欠阻尼：[[#极点等值线与非欠阻尼补充|页末公式]]；带零点：[[03-3-2 零点影响与二阶性能改善]]。

'''+text[end:]
start=text.index('> [!warning] 有限终值先查误差极点')
end=text.index('$$',start)
text=text[:start]+r'''**比较点偏差 $e=r-b$；其他独立输入为零。**

1. 先判闭环稳定。
2. 求有限终值：约分后 $sE(s)$ 的极点全在左半平面。
3. 按输入、型别查表；非单位反馈另区分 $r-c$。

'''+text[end:]
text=re.sub(r'\n> \*\*规律\*\*：[^\n]*\n','\n',text)
text=text.replace('时间常数 $T$ 越小，响应越快；手算答案优先保留上表的对数形式。\n\n','')
text=text.replace('**普通劳斯表未遇特殊行时**，最高次项系数取正，首列全正 ⇔ 渐近稳定；按规则处理后，首列变号次数统计右半平面根数。', '**最高次系数取正；普通劳斯表首列全正 ⇔ 渐近稳定。**')
start=text.index('> [!warning] 两种特殊情况')
end=text.index('## 极点等值线与非欠阻尼补充',start)
text=text[:start]+r'''1. 首元为零、该行非全零：以 $\varepsilon>0$ 代替，令 $\varepsilon\to0^+$ 判符号。
2. 全零行：以上一行构造辅助多项式 $P(s)$，用 $P'(s)$ 系数替换。
3. 数首列变号次数得右半平面根数；出现全零行时，另查辅助多项式的虚轴根及重数。

'''+text[end:]
start=text.index('> [!tip] s平面等值线')
end=text.index('**临界阻尼**',start)
text=text[:start]+r'''| 极点位置 | 等值指标 |
| :-- | :-- |
| $\zeta\omega_n=\text{常数}$ | 欠阻尼近似等 $t_s$ |
| $\omega_d=\text{常数}$ | 等 $t_p$ |
| 原点射线 | 等 $\zeta$、等 $\sigma\%$ |
| 原点圆弧 | 等 $\omega_n$ |

'''+text[end:]
text=text.replace('**临界阻尼**：无零点标准二阶取 $\\zeta=1$，相对误差带为 $\\delta$，调节时间由完整响应确定：', '**临界阻尼：无零点标准二阶，$\\zeta=1$；相对误差带 $0<\\delta<1$。**')
text=text.replace('5%与2%分别取 $\\delta=0.05$、$0.02$。手算可保留此精确关系；若题目要求估算，教材式3-26给出5%口径 $t_s\\approx4.75/\\omega_n$，不能套欠阻尼公式。', '**5%/2%：$\\delta=0.05/0.02$；5%估算：$t_s\\approx4.75/\\omega_n$。**')
text=text.replace('**过阻尼**：用慢模态或完整响应计算。完整推导见 [[03-3-2 零点影响与二阶性能改善]]。', '**过阻尼**：[[03-3-2 零点影响与二阶性能改善|慢模态与完整响应]]。')
save(p,raw,text)

p,raw,text=read('附录 开环增益与闭环增益.md')
head=text[:text.index('> [!abstract]')]
body=r'''> [!abstract] 附录定位
> 增益换算、稳态误差、动态参数与灵敏度；只留公式、条件与必要步骤。

[[#定义与换算|增益换算]] · [[#稳态值与误差|稳态]] · [[#增益与动态参数|动态]] · [[#增益与频域|频域]] · [[#校正中的增益|校正]] · [[#参数灵敏度补充|灵敏度]]

## 定义与换算

**负反馈：前向通道 $G(s)$，反馈通道 $H(s)$。**

$$
G_k(s)=G(s)H(s)
$$

$$
\Phi(s)=\frac{G(s)}{1+G(s)H(s)}
$$

**尾一增益 $K$；$\nu$ 为约分后原点极点数。**

$$
G_k(s)=K\frac{\prod\limits_{i=1}^{m}(\tau_i s+1)}{s^{\nu}\prod\limits_{j=1}^{n-\nu}(T_j s+1)}
$$

**首一根轨迹增益 $K^{\ast}$；$p_j,z_i$ 不含原点因子。**

$$
G_k(s)=K^*\frac{\prod\limits_{i=1}^{m}(s-z_i)}{s^{\nu}\prod\limits_{j=1}^{n-\nu}(s-p_j)}
$$

**除原点积分因子外，零极点均在左半平面。**

$$
K=K^*\frac{\prod\limits_{i=1}^{m}\lvert z_i\rvert}{\prod\limits_{j=1}^{n-\nu}\lvert p_j\rvert}
$$

1. 约分，提出原点积分因子。
2. 常数项归一读 $K$；最高次项归一读 $K^*$。
3. 求闭环，再取 $\Phi(0)$；作稳态值时须判稳。

## 稳态值与误差

**单位负反馈、闭环渐近稳定；其他独立输入为零。**

| 型别 | 闭环直流增益 | 匹配输入 | 稳态误差 |
| :-- | :-- | :-- | :-- |
| 0型 | $\Phi(0)=\frac K{1+K}$ | 单位阶跃 | $\frac1{1+K_p}$，$K_p=K$ |
| Ⅰ型 | $\Phi(0)=1$ | 单位斜坡 | $\frac1{K_v}$，$K_v=K$ |
| Ⅱ型 | $\Phi(0)=1$ | 单位加速度 | $\frac1{K_a}$，$K_a=K$ |

输入幅值乘 $A$，对应误差乘 $A$；其余输入与型别见 [[附录 时域分析速查]]。

**非单位反馈：$H(0)$ 有限非零、环路低频增益趋于无穷。**

$$
\Phi(0)=\frac1{H(0)}
$$

比较点偏差 $E=R-HC$；跟踪误差 $R-C$。

## 增益与动态参数

**典型Ⅰ型二阶：单位负反馈，$p>0$、$K^{\ast}>0$。**

$$
G(s)=\frac{K^*}{s(s+p)}
$$

$$
K=\frac{K^*}{p}
$$

$$
s^2+ps+K^*=0
$$

$$
\omega_n=\sqrt{K^*}
$$

$$
\zeta=\frac{p}{2\sqrt{K^*}}
$$

**纯比例缩放：$C_0>0$，$\widehat\Phi(s)$ 固定。**

$$
\Phi(s)=C_0\widehat\Phi(s)
$$

响应同倍缩放；相对超调量、峰值时间、相对误差带调节时间不变。

**实际调参**：求闭环零极点 → 判稳 → 计算目标指标。

## 增益与频域

**其余环节固定，$K_1,K_2>0$。**

$$
\Delta L=20\lg\frac{K_2}{K_1}
$$

低频渐近线：斜率 $-20\nu$ dB/dec；延长至 $\omega=1$ 的高度为 $20\lg|K|$。

**指定负实轴穿越频率 $\omega_x$；多交越逐个核查。**

$$
h=\frac1{A(\omega_x)}
$$

判稳与裕度：[[附录 频域分析速查]]。

## 校正中的增益

**无源超前：$a>1$；补偿放大倍数 $a$。**

$$
G_c(s)=\frac1a\frac{aTs+1}{Ts+1}
$$

$$
G_c(0)=\frac1a
$$

**测速反馈：$P(s)=K_m/[s(T_ms+1)]$，内反馈 $k_ts$；$K_m,T_m,k_t>0$。**

$$
P_t(s)=\frac{K_m}{s(T_ms+1+K_mk_t)}
$$

$$
K_{v,\mathrm{new}}=\frac{K_m}{1+K_mk_t}
$$

**校正后**：重算低频增益 → 截止频率 → 两种裕度。

## 参数灵敏度补充

**固定反馈通道 $H$。**

$$
S_G^\Phi=\frac{G}{\Phi}\frac{\partial\Phi}{\partial G}
$$

$$
S_G^\Phi=\frac1{1+G(s)H(s)}
$$

**$|GH|\gg1$ 的频带：$|S_G^\Phi|\ll1$。**
'''
save(p,raw,head+body)

p=root/'控制理论/自动控制原理/07-1 采样与z变换.md'
raw=p.read_bytes();text=raw.decode('utf-8-sig').replace('\r\n','\n')
assert '双曲、多极点与推导在该页后部' in text
text=text.replace('双曲、多极点与推导在该页后部','双曲、多极点与留数法在该页后部')
save(p,raw,text)

p=base/'附录目录.md';raw,text=(p.read_bytes(),p.read_text(encoding='utf-8-sig'))
text=text.replace('自控与现控的附录集中入口。常用公式在前，概念辨析、备用数值和教材对照在后。','自控与现控附录入口。速查页以公式、适用条件和必要步骤为主；备用数值与教材对照在后。').replace('## 概念与备用','## 基础公式与备用')
save(p,raw,text)

p=root/'AGENTS.md';raw=p.read_bytes();text=raw.decode('utf-8-sig').replace('\r\n','\n')
marker='### 排版与可读性规范\n'
assert text.count(marker)==1
text=text.replace(marker,marker+'- **控制理论速查附录**：以公式、参数定义、适用条件和必要解题步骤为主，不保留长段解释、完整推导与完整例题；幅相等图谱可保留查形状必需的图。目录和教材对照页保留导航用途。\n')
save(p,raw,text)
print('Trimmed time/gain appendices and updated the one prose reference and format guidance.')

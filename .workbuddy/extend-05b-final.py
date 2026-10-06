exec(Path('D:/obsidian/.workbuddy/extend-05b-edit.py').read_text(encoding='utf-8').split("edit('05-3',three)")[0].split('def three')[0])
def zero(s):
 s=trim(s)
 a=s.index('> [!abstract]'); tail=s[s.index('> 相关：'):]
 body=r'''> [!abstract] 本讲定位
> **例5.14〔习题5-16〕**：虚轴零点使曲线连续经过原点，但相角在该点无定义。先分离实虚部，再计穿越；原点极点仍要补弧。

## 🧩 已有四类之外的第五类：虚轴零点

虚轴极点使幅值趋于无穷，需要补弧；虚轴零点使幅值归零，曲线直接经过原点。简单零点两侧相角极限相差 $180^circ$，不能把它误说成纯粹的主值换支。

## ✏️ 例5.14〔习题5-16〕解答

#### ✏️ 题目

单位负反馈系统的开环传递函数为

$$
G(s)=rac{k(s^2+1)}{s(s+5)}
$$

用奈氏判据确定闭环稳定条件。题给 $arctan0.2=11.3^circ$。先对正增益 $k>0$ 画图，再检查边界。

### ① 化标准形，定幅频与相频

$$
G(mathrm jomega)=rac{k(1-omega^2)}{mathrm jomega(mathrm jomega+5)}
$$

$$
|G(mathrm jomega)|=rac{k|1-omega^2|}{omegasqrt{omega^2+25}}
$$

分子在 $omega=1$ 变号，取以下相角分支：

$$
angle G(mathrm jomega)=
egin{cases}
-90^circ-arctanrac{omega}{5}, & 0<omega<1\[4pt]
-270^circ-arctanrac{omega}{5}, & omega>1
end{cases}
$$

两侧极限分别为 $-101.3^circ$、$-281.3^circ$；在 $omega=1$ 处 $G=0$，相角本身无定义。

### ② 实部、虚部（本例题的关键一步）

分母为 $-omega^2+mathrm j5omega$，乘其共轭后得到

$$
operatorname{Re}G=rac{k(omega^2-1)}{omega^2+25}
$$

$$
operatorname{Im}G=rac{5k(omega^2-1)}{omega(omega^2+25)}
$$

| 频率 | 实部、虚部符号 | 位置 |
| :-- | :-- | :-- |
| $0<omega<1$ | 同负 | 第三象限 |
| $omega=1$ | 同时为零 | 经过原点 |
| $omega>1$ | 同正 | 第一象限 |

因此唯一的有限正频率实轴交点是原点，不在 $(-infty,-1)$ 上。

### ③ 起点、终点与实轴交点

$$
lim_{omega	o0^+}operatorname{Re}G=-rac{k}{25}
$$

$$
lim_{omega	o0^+}operatorname{Im}G=-infty
$$

$$
lim_{omega	oinfty}G(mathrm jomega)=k
$$

曲线从竖直渐近线 $operatorname{Re}G=-k/25$ 右侧进入，经原点转入第一象限，最后从上方趋于 $(k,0)$。

### ④ 围线怎么绕：零点不补弧

$s=pmmathrm j$ 是开环零点，$G$ 在此解析，围线可直接通过。

> [!derivation]- 若绕过零点，映射弧为什么会缩小
> 取 $s=mathrm j+arepsilonmathrm e^{mathrm j	heta}$，则
>
> $$
> s^2+1=2mathrm jarepsilonmathrm e^{mathrm j	heta}+O(arepsilon^2)
> $$
>
> $$
> s(s+5)=-1+5mathrm j+O(arepsilon)
> $$
>
> 故
>
> $$
> G(s)=rac{2mathrm jk}{-1+5mathrm j}arepsilonmathrm e^{mathrm j	heta}+O(arepsilon^2)	o0
> $$
>
> 映射弧半径随 $arepsilon$ 缩到零，不需补无穷大弧，也不贡献绕 $-1$ 的圈数。

原点另有开环极点：低频 $G(s)sim k/(5s)$。从 $s$ 平面正实轴绕向正虚轴时，映射沿第四象限顺时针走 $90^circ$，不穿负实轴。教材从 $G(mathrm j0^+)$ 逆时针补画，是同一段弧的反向作图。

### ⑤ 判稳

开环极点为 $0,-5$，虚轴极点不计入 $P$。正常支和补弧都不穿过 $(-infty,-1)$，所以

$$
P=0
$$

$$
N=N_+-N_-=0
$$

$$
Z=P-2N=0
$$

![[频域-奈氏-虚轴零点判稳.png|520]]

*图取 $k=2$：实线为正频率支，虚线为共轭支；纵轴压缩大数值，箭头标出频率方向。曲线经原点连续衔接。*

### ⑥ 劳斯判据复核（一行就能验）

闭环特征方程为

$$
(k+1)s^2+5s+k=0
$$

$k>0$ 时系数全正，二阶特征根全在左半平面，也排除了虚轴闭环根。因此

$$
oxed{k>0}
$$

若允许负增益，二阶稳定条件要求 $5/(k+1)>0$、$k/(k+1)>0$，仍只得 $k>0$；$k=-1$ 使反馈代数环奇异，不作为正常闭环。$k=0$ 时特征式为 $s(s+5)$，含原点根。

## ⚠️ 边界与易错

- **曲线连续不等于相角连续**：零点处相角无定义，两侧极限可差 $180^circ$。
- **不靠“整支在 −1 右侧”判稳**：当 $k>25$，低频实部已小于 $-1$；有效依据仍是负实轴无穿越。
- **判稳写全**：$Z=0$ 只排除右半平面根，还须排除虚轴闭环根。

其余特殊情形见 [[05-4-a 奈氏特殊情形与条件稳定]]；计数规则见 [[05-4-1 奈氏判据]]。

'''
 return s[:a]+body+tail
edit('05-4-c',zero)
def point(s):
 s=trim(s);s=remove_callout(s,'A 点的双重身份');s=remove_callout(s,'B 只是读数校验点');s=remove_callout(s,'和 PPT 的记号对一下');s=remove_callout(s,'延伸')
 s=s.replace('**幅频局部最大 = 离原点最远**','幅频最大对应距离最大').replace('所以"幅频的局部最大值"＝"离原点最远的点"','幅频局部极大对应到原点距离的局部极大；只有全局峰值才对应最远点')
 s=s.replace('$\\omega_c=94.9$','$\\omega_c\\approx99.09$')
 s=s.replace('|620]]','|520]]')
 anchor='### 5.12.2 二阶振荡：$\\omega_r$、$\\omega_n$、$\\omega_c$ 的四个落点\n'
 s=s.replace(anchor,anchor+r'''
与例5.24同用模型 $G(s)=9000/(s^2+12.18s+900)$。截止频率必须由真实幅值求：

$$
(900-omega_c^2)^2+(12.18omega_c)^2=9000^2
$$

正根为 $omega_capprox99.09$。渐近线的 $30sqrt{10}approx94.9$ 只用于估算；在该频率真实幅值约为 $1.10$，尚未落到单位圆上。
''')
 s=s.replace('只有 $\\zeta<1/\\sqrt2$ 才有正频率谐振峰','标准二阶环节仅在 $0<\\zeta<1/\\sqrt2$ 时有正频率谐振峰')
 return s
edit('05-3-a',point)
def overview(s):
 s=trim(s)
 s=s.replace('畫','画').replace('画正频率半支，有虚轴极点时按 $\\nu\\times90°$ 补齐大弧。','画正频率半支；原点 $\\nu$ 重极点按 $\\nu\\times90°$、非零虚轴 $q$ 重极点按 $q\\times180°$ 补弧。')
 a=s.index('> [!tip] 本部分的最小学习闭环');b=s.index('## 🧭',a);s=s[:a]+s[b:]
 return s
edit('05-4',overview)

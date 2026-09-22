# -*- coding: utf-8 -*-
"""自控 02-2（先删重复 warning 腾行）、02-6 加「考点速记」"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

D = r'D:\obsidian\控制理论\自动控制原理'

# ---- 1) 02-2：删掉与「② 两级 RC 直接串联」正文重复的 warning 块（3 行） ----
p22 = os.path.join(D, '02-2 元部件、电路与机械建模.md')
raw = open(p22, 'rb').read()
nl = '\r\n' if b'\r\n' in raw else '\n'
L = raw.decode('utf-8').replace('\r\n', '\n').split('\n')
i = next(k for k, l in enumerate(L) if l.strip() == '> [!warning] 考研简答/选择常考')
j = i
while j < len(L) and L[j].startswith('>'):
    j += 1
if j < len(L) and L[j].strip() == '':
    j += 1
print('02-2 原 %d 行，删除 L%d–%d（%d 行重复 warning）'
      % (len(L) - 1, i + 1, j, j - i))
del L[i:j]

BLOCKS = [
    ('02-2 元部件、电路与机械建模', [
        '- **机械-电路相似系统**：力 $\\leftrightarrow$ 电压、位移 $\\leftrightarrow$ 电荷、速度 $\\leftrightarrow$ 电流；参数 $m\\leftrightarrow L$、$f\\leftrightarrow R$、$K\\leftrightarrow\\frac1C$。弹簧-质量-阻尼器 $m\\ddot x+f\\dot x+Kx=F$ 给出 $\\frac{X}{F}=\\frac1{ms^{2}+fs+K}$（教材例2-3）；分析方子可互借，但**输入输出须对应**。',
        '- **齿轮系折算（口诀）**：**惯量、黏性摩擦按速比平方折算，转矩按一次方折算**——$J_{eq}=J_1+\\frac{J_2}{i^{2}}$、$f_{eq}=f_1+\\frac{f_2}{i^{2}}$、$M\'_c=\\frac{M_c}{i}$（$i=\\frac{\\omega_1}{\\omega_2}>0$）。主动轴动力学：$J_{eq}\\dot\\omega_1+f_{eq}\\omega_1=M_m-M\'_c$。',
        '- **电路建模两法**：① **列微分方程 $\\to$ 拉氏变换**（通用，KVL/KCL + 元件 s 域关系 $R,Ls,\\frac1{Cs}$）；② **复阻抗法**（快捷）——串联相加、并联 $\\frac{Z_1Z_2}{Z_1+Z_2}$，无源二端口输出开路时按**分压** $G=\\frac{Z_2}{Z_1+Z_2}$。常用结果：$R|C$ 得 $\\frac1{RCs+1}$（惯性）、$C|R$ 得 $\\frac{RCs}{RCs+1}$（微分性）、$RLC$ 取电容电压得 $\\frac1{LCs^{2}+RCs+1}$。',
        '- **运放电路**：只在**负反馈、线性未饱和**区才能用**虚短虚断**（不能用于正反馈比较器或饱和）；反相接法 $G=-\\frac{Z_f}{Z_0}$，五条常用结果（比例/积分/惯性/PI/PD）。**两个易错**：① 每一级反相都带负号（偶数级抵消、奇数级留一个）；② 求整个模拟电路传函要**逐级写出 $-Z_f/Z_0$ 再按结构图化简**，跨级反馈引线按比较点处理。',
        '- **负载效应（最常考）**：无源网络传函默认**输出端无穷大负载、输入内阻为零**。① 电位器接负载 $R_l$ 后 $u=\\frac{E\\alpha}{1+\\frac{R_p}{R_l}\\alpha(1-\\alpha)}$，**只有 $R_l\\ge10R_p$ 才近似线性**；② **两级 RC 直接串联 $\\ne$ 两级传函相乘**——分母多出交叉项 $R_1C_2s$（前级电流有一部分直接流入 $C_2$）；③ 消除办法：后级输入阻抗足够大／前级输出阻抗趋于零／中间加**隔离放大器**。',
    ]),
    ('02-6 典型系统模型·常用元部件与过程控制', [
        '- **常用元部件传函**：电位器/电桥 $K$；测速发电机（电压对转角）$K_ts$；电枢控制直流电动机对转速 $\\frac{K_m}{T_ms+1}$、对转角 $\\frac{K_m}{s(T_ms+1)}$；RC 取电容电压 $\\frac1{RCs+1}$；RLC 取电容电压 $\\frac1{LCs^{2}+RCs+1}$。',
        '- **电枢控制直流电动机的三方程**（教材例2-2）：① 电枢电压平衡 $u_a=R_ai_a+L_a\\frac{di_a}{dt}+E_a$（$E_a=C_e\\omega_m$）；② 电磁转矩 $M_m=C_mi_a$；③ 转矩平衡 $J_m\\dot\\omega_m+f_m\\omega_m=M_m-M_c$。忽略 $L_a$ 得一阶模型 $T_m\\dot\\omega_m+\\omega_m=K_mu_a-K_cM_c$，其中 $T_m=\\frac{R_aJ_m}{R_af_m+C_mC_e}$、$K_m=\\frac{C_m}{R_af_m+C_mC_e}$、$K_c=\\frac{R_a}{R_af_m+C_mC_e}$；两通道传函为 $\\frac{K_m}{T_ms+1}$ 与 $-\\frac{K_c}{T_ms+1}$（**扰动通道为负**：负载增大转速下降）。',
        '- **单容水槽（过程控制）**：孔口关系 $Q_o=\\kappa\\sqrt h$ 非线性，取 $h_0>0$ 线性化得 $K_q=\\frac{\\kappa}{2\\sqrt{h_0}}$、**液阻 $R=\\frac1{K_q}$**；以流入量为输入得 $\\frac{\\Delta H}{\\Delta Q_i}=\\frac{1/K_q}{(A/K_q)s+1}$（$T=\\frac A{K_q}$、$K_v=\\frac1{K_q}$）；以阀开度为输入则 $\\frac{K_uR}{ARs+1}$。**纯运输延迟**在传函上乘 $e^{-\\tau s}$。',
        '- **电加热炉**：绝对温度满足 $C\\frac{d\\theta}{dt}=P-K(\\theta-\\theta_0)$，改写成**偏差**形式 $C\\dot x+Kx=p$（稳态常量自动消去），得 $\\frac{X}{P_\\Delta}=\\frac{1/K}{(C/K)s+1}$——**与单容水槽同构**，不是绝对温度除以总功率。若操纵量为电压还要线性化功率：$P=\\frac{u^2}{R_h}\\Rightarrow\\Delta P=\\frac{2u_0}{R_h}\\Delta u$。',
        '- **无耦合双容水槽**：两槽物料平衡消去 $H_1$ 得 $\\frac{H_2}{Q_i}=\\frac{1/K_2}{(T_1s+1)(T_2s+1)}$——两个一阶惯性串联成无零点二阶；**稳态增益只剩末槽 $\\frac1{K_2}$**（中间增益相消），$K_1$ 只进入 $T_1$。若下游液位反过来影响上游流出，就是**容量耦合**，必须重列方程、**不能把两个空载传函相乘**。',
    ]),
]

for name, lines in BLOCKS:
    path = os.path.join(D, name + '.md')
    if name.startswith('02-6'):
        raw = open(path, 'rb').read()
        nl = '\r\n' if b'\r\n' in raw else '\n'
        L = raw.decode('utf-8').replace('\r\n', '\n').split('\n')
    a = next(k for k, l in enumerate(L) if l.startswith('> [!abstract]'))
    e = a + 1
    while e < len(L) and L[e].startswith('>'):
        e += 1
    block = ['> [!tip] 🎯 考点速记'] + ['> ' + x for x in lines]
    L[e:e] = [''] + block
    for k, l in enumerate(L):
        if l.startswith('modify:'):
            L[k] = 'modify: 2026-09-22'
            break
    open(path, 'wb').write(nl.join(L).encode('utf-8'))
    b2 = open(path, 'rb').read()
    n = len(L) - (1 if L and L[-1] == '' else 0)
    print('=== %s：+%d 行 → %d 行，裸LF=%d' % (name, len(block) + 1, n,
          b2.count(b'\n') - b2.count(b'\r\n')))
    for x in block:
        assert x.startswith('> ')
        print('   %s| %3d%s' % (x[4:22], len(x), '  ← 超 200' if len(x) > 200 else ''))

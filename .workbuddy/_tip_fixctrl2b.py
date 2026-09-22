# -*- coding: utf-8 -*-
"""整块重写自控 02-2 / 02-6 的速记：把 7 条超长行压到 200 以内（保持 5 条以不超 250 行）"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

D = r'D:\obsidian\控制理论\自动控制原理'
BLOCKS = [
    ('02-2 元部件、电路与机械建模', [
        '- **机械-电路相似系统**：力 $\\leftrightarrow$ 电压、位移 $\\leftrightarrow$ 电荷、速度 $\\leftrightarrow$ 电流；$m\\leftrightarrow L$、$f\\leftrightarrow R$、$K\\leftrightarrow\\frac1C$。弹簧-质量-阻尼器 $m\\ddot x+f\\dot x+Kx=F$ 给出 $\\frac XF=\\frac1{ms^{2}+fs+K}$。',
        '- **齿轮系折算口诀**：**惯量、黏性摩擦按速比平方折算，转矩按一次方折算**——$J_{eq}=J_1+\\frac{J_2}{i^{2}}$、$f_{eq}=f_1+\\frac{f_2}{i^{2}}$、$M\'_c=\\frac{M_c}i$（$i=\\frac{\\omega_1}{\\omega_2}>0$）。',
        '- **电路建模两法**：① **列微分方程 $\\to$ 拉氏变换**（通用，KVL/KCL $+$ 元件 s 域关系 $R,Ls,\\frac1{Cs}$）；② **复阻抗法**（快捷）——串联相加、并联 $\\frac{Z_1Z_2}{Z_1+Z_2}$，输出开路时按**分压** $G=\\frac{Z_2}{Z_1+Z_2}$。常用：$R|C$ 得 $\\frac1{RCs+1}$、$C|R$ 得 $\\frac{RCs}{RCs+1}$、$RLC$ 取电容电压得 $\\frac1{LCs^{2}+RCs+1}$。',
        '- **运放电路**：只在**负反馈、线性未饱和**区才能用**虚短虚断**（不能用于正反馈比较器或饱和）；反相接法 $G=-\\frac{Z_f}{Z_0}$，五条常用结果（比例/积分/惯性/PI/PD）。**两个易错**：① 每一级反相都带负号（偶数级抵消、奇数级留一个）；② 求整个模拟电路传函要**逐级写出 $-Z_f/Z_0$ 再按结构图化简**，跨级反馈引线按比较点处理。',
        '- **负载效应（最常考）**：无源网络传函默认**输出端无穷大负载、输入内阻为零**。① 电位器接负载后**只有 $R_l\\ge10R_p$ 才近似线性**；② **两级 RC 直接串联 $\\ne$ 传函相乘**——分母多出交叉项 $R_1C_2s$；③ 消除办法：后级输入阻抗大／前级输出阻抗小／中间加**隔离放大器**。',
    ]),
    ('02-6 典型系统模型·常用元部件与过程控制', [
        '- **常用元部件传函**：电位器/电桥 $K$；测速发电机（电压对转角）$K_ts$；电枢控制直流电动机对转速 $\\frac{K_m}{T_ms+1}$、对转角 $\\frac{K_m}{s(T_ms+1)}$；RC 取电容电压 $\\frac1{RCs+1}$；RLC 取电容电压 $\\frac1{LCs^{2}+RCs+1}$。',
        '- **电枢控制直流电动机**：三方程 $=$ 电压平衡 $u_a=R_ai_a+L_a\\frac{di_a}{dt}+E_a$（$E_a=C_e\\omega_m$）、电磁转矩 $M_m=C_mi_a$、转矩平衡 $J_m\\dot\\omega_m+f_m\\omega_m=M_m-M_c$。忽略 $L_a$ 得 $T_m\\dot\\omega_m+\\omega_m=K_mu_a-K_cM_c$，传函 $\\frac{K_m}{T_ms+1}$ 与 $-\\frac{K_c}{T_ms+1}$（**扰动为负**）。',
        '- **单容水槽**：$Q_o=\\kappa\\sqrt h$ 取 $h_0>0$ 线性化，$K_q=\\frac{\\kappa}{2\\sqrt{h_0}}$、**液阻 $R=\\frac1{K_q}$**；$\\frac{\\Delta H}{\\Delta Q_i}=\\frac{1/K_q}{(A/K_q)s+1}$；以阀开度为输入则 $\\frac{K_uR}{ARs+1}$；**纯运输延迟在传函上乘 $e^{-\\tau s}$**。',
        '- **电加热炉**：$C\\frac{d\\theta}{dt}=P-K(\\theta-\\theta_0)$ 改写成**偏差**形式 $C\\dot x+Kx=p$（稳态常量自动消去），得 $\\frac{X}{P_\\Delta}=\\frac{1/K}{(C/K)s+1}$——**与单容水槽同构**。若操纵量为电压还要线性化功率 $\\Delta P=\\frac{2u_0}{R_h}\\Delta u$。',
        '- **无耦合双容水槽**：消去 $H_1$ 得 $\\frac{H_2}{Q_i}=\\frac{1/K_2}{(T_1s+1)(T_2s+1)}$——两个一阶惯性串联成无零点二阶；**稳态增益只剩末槽 $\\frac1{K_2}$**（中间增益相消），$K_1$ 只进 $T_1$。若下游液位影响上游流出就是**容量耦合**，必须重列方程、**不能把两个空载传函相乘**。',
    ]),
]

for name, lines in BLOCKS:
    path = os.path.join(D, name + '.md')
    raw = open(path, 'rb').read()
    nl = '\r\n' if b'\r\n' in raw else '\n'
    L = raw.decode('utf-8').replace('\r\n', '\n').split('\n')
    a = next(k for k, l in enumerate(L) if '🎯 考点速记' in l)
    e = a + 1
    while e < len(L) and L[e].startswith('>'):
        e += 1
    block = ['> [!tip] 🎯 考点速记'] + ['> ' + x for x in lines]
    L[a:e] = block
    for k, l in enumerate(L):
        if l.startswith('modify:'):
            L[k] = 'modify: 2026-09-22'
            break
    open(path, 'wb').write(nl.join(L).encode('utf-8'))
    b2 = open(path, 'rb').read()
    n = len(L) - (1 if L and L[-1] == '' else 0)
    print('=== %s：%d 行，裸LF=%d' % (name, n, b2.count(b'\n') - b2.count(b'\r\n')))
    for x in block:
        assert x.startswith('> ')
        print('   %s| %3d%s' % (x[4:22], len(x), '  ← 超 200' if len(x) > 200 else ''))

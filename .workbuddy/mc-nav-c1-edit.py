from pathlib import Path
import re, subprocess
root=Path('控制理论/777习题集')
ap=next(root.glob('现控200题基础 第1章*答案*.md'))
qp=next(root.glob('现控200题基础 第1章*题目*.md'))
a=subprocess.check_output(['git','show','HEAD:'+ap.as_posix()]).decode('utf-8'); q=subprocess.check_output(['git','show','HEAD:'+qp.as_posix()]).decode('utf-8')
def write(p,s):
    nl='\r\n' if b'\r\n' in p.read_bytes() else '\n'
    p.write_bytes(s.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
q=q.replace('绘 制','绘制')
# These original titles have no incoming heading links (rg checked before editing).
qs={}
for m in re.finditer(r'^\*\*(1-\d+)([^\n]*?)\*\*(.*?)(?=^\*\*1-\d+|^## |\Z)',q,re.M|re.S):
    text=m.group(3).strip()
    text=re.sub(r'^>.*(?:\n|$)','',text,flags=re.M).strip()
    qs[m.group(1)]=(m.group(2),text)
assert len(qs)==27
q=re.sub(r'^\*\*(1-\d+)([^\n]*?)\*\* ?',lambda m:'#### ✏️ '+m[1]+'　题目\n\n'+(m[2]+'\n\n' if m[2] else ''),q,flags=re.M)
def nav(kind):
    rows=['## 🔎 题号直达','','| 题号范围 | 直达'+kind+' |','| :-- | :-- |']
    for start in range(1,28,5):
        stop=min(start+4,27)
        links=' · '.join(f'[[#✏️ 1-{n}　{kind}\\|1-{n}]]' for n in range(start,stop+1))
        rows.append(f'| 1-{start}～1-{stop} | {links} |')
    return '\n'.join(rows)+'\n\n'
q=q.replace('## 【题型1】',nav('题目')+'## 【题型1】',1)
a=a.replace('## 答案速查',nav('解析')+'## 答案速查',1)
a=re.sub(r'(?<=\| )(1-\d+)(?= \|)',lambda m:f'[[#✏️ {m[1]}　解析\\|{m[1]}]]',a)
def answer(m):
    num,summary,point=m.groups(); source,body=qs[num]
    # The source figures stay visible alongside the derivation.
    figs=re.findall(r'^!\[\[.*?\]\]$',body,re.M)
    body=re.sub(r'^!\[\[.*?\]\]\n?','',body,flags=re.M).strip()
    body=re.sub(r'\n{3,}','\n\n',body)
    if source: body=source+'\n\n'+body
    call='> [!note]- 本题题设\n'+ '\n'.join('> '+line if line else '>' for line in body.splitlines())
    result=f'#### ✏️ {num}　解析\n\n[[{qp.stem}#✏️ {num}　题目|原题]] · [[#🔎 题号直达|返回题号导航]]\n\n{call}\n\n'
    if figs: result+='\n\n'.join(figs)+'\n\n'
    return result+point+ ('\n\n答案：'+summary.removeprefix('答案').removeprefix('：').strip() if num=='1-3' else '')
a=re.sub(r'^\*\*(1-\d+)　(.*?)\*\*([^\n]*)',answer,a,flags=re.M)
# Long inline formulae move to their own display blocks; tables remain compact.
def standalone_inline(s):
    out=[]
    for line in s.splitlines():
        if line.startswith('|') or line.startswith('>') or line.startswith('#'):
            out.append(line);continue
        line=re.sub(r'(?<!\$)\$([^$\n]{65,})\$(?!\$)',lambda m:'\n\n$$\n'+m[1]+'\n$$\n\n',line)
        out.append(line)
    return re.sub(r'\n{3,}','\n\n','\n'.join(out))+'\n'
a=standalone_inline(a);q=standalone_inline(q)
# Split independent display equations previously put side by side.
def split_displays(s):
    def f(m):
        body=m[1]
        if '\\begin{aligned}' in body: return m[0]
        body=re.sub(r',?\s*\\qquad\s*', '\n$$\n\n$$\n', body)
        body=body.replace('\\quad\\Longrightarrow\\quad','\n$$\n\n因此\n\n$$\n')
        return '$$\n'+body.strip()+'\n$$'
    return re.sub(r'^\$\$\n(.*?)\n\$\$',f,s,flags=re.M|re.S)
a=split_displays(a);q=split_displays(q)
brief=[
r'$\dot x_1=x_2$、$\dot x_2=u$，$y=k_1x_1+k_2x_2$',
r'三状态模型见解析；第一条为正反馈 $\dot x_1=x_1+u$',
r'$\dot x_1=x_2$、$\dot x_2=-x_2+2u$，$y=x_1$',
r'$\Phi(s)=\frac2{s+4}$，无超调，$e_{\mathrm{ss}}=\frac12$；三维描述须满足初值约束',
r'$G(s)=1+\frac{5s+3}{s^2+3s+2}$，直通项 $D=1$；实现与图见解析',
r'两电容电压取状态；KCL与矩阵见解析',
r'$\Phi(s)=\frac{R}{RLCs^2+Ls+R}$；电流、电容电压取状态',
r'四状态、双输入双输出；受力方程与矩阵见解析',
r'$G(s)=\frac{ds^2+es+f}{s^3+as^2+bs+c}$；积分链与输出加权图见解析',
r'$W(s)=\frac{(s+1)^2}{s^3+3s^2+2s+1}$；三种实现见解析',
r'离散伴随阵，输入列 $B=[1,-1,1]^T$，$y=x_1$',
r'输入列 $B=[1,-1]^T$；不完全能控、完全能观',
r'$\widetilde A=\mathrm{diag}(-1,-2)$，$\widetilde B=[1,-1]^T$',
r'两组非奇异变换及完整状态模型见解析',
r'三阶约当块，特征值 $3$；$B=[0,0,1]^T$，$C=[37,22,3]$',
r'$A=\mathrm{diag}(-1,-2,-3)$，$B=[1,-2,3]^T$，$C=[1,1,1]$',
r'特征值 $0,-1,3$；变换矩阵与 $\Phi(t)$ 见解析',
r'特征值 $-1,-1,-3$；$-1$ 对应二阶约当块，变换后 $\widetilde B=[\frac12,0,-\frac12]^T$',
r'$W(s)=\frac1{(s+2)(s+3)}$',
r'$W(s)=\frac{12s+59}{(s+2)(s+4)}$',
r'能控秩 $5$、能观秩 $4$；$W(s)=\frac1{(s+1)(s+2)(s+3)}$',
r'闭环传递矩阵见解析，公共二次因子 $D=s^2+5s+2$',
r'$W(s)=\frac{2s-1}{(s+1)(s+2)}$（已与官方修正图对照）',
r'$W(s)=\frac1{(s+1)(s+3)}$；串联系统不完全能控、完全能观',
r'$\alpha(s)=s^3+a_2s^2+a_1s+a_0$',
r'特征值 $3,3,1$；$3$ 对应二阶约当块，变换后输入、输出矩阵见解析',
r'特征值 $1,1,2$；$\lambda=1$ 有两个独立特征向量，可对角化',
]
table='## 答案速查\n\n| 题号 | 结论与关键结果 |\n| :-- | :-- |\n'+'\n'.join(f'| [[#✏️ 1-{i}　解析\\|1-{i}]] | {v} |' for i,v in enumerate(brief,1))+'\n\n'
a=re.sub(r'## 答案速查.*?(?=## 【题型1】)',lambda m:table,a,flags=re.S)
# Remove only blank source lines inside display math (keep space between blocks).
def tidy(s):
    return re.sub(r'(?m)^\$\$\n(.*?)\n\$\$',lambda m:'$$\n'+'\n'.join(x for x in m[1].splitlines() if x.strip())+'\n$$',s,flags=re.S)
a=tidy(a);q=tidy(q)
a=a.replace(r'W(s)=\frac{1+s}{s^3+6s^2+11s+6}',r'\begin{aligned}'+'\n'+r'W(s)&=\frac{1+s}{(s+1)(s+2)(s+3)}\\'+'\n'+r'&=\frac1{(s+2)(s+3)}.'+'\n'+r'\end{aligned}')
a=a.replace('图中两个积分器串联，',r'本题记 $k_1=K_1$、$k_2=K_2$，与原图中的增益对应。图中两个积分器串联，',1)
a=a.replace('三个积分器对应三个状态。',r'将状态写成列向量 $x=[x_1,x_2,x_3]^T$。三个积分器对应三个状态。',1)
a=a.replace('取 $z=[x_1;\\dot x_1;x_2]$：',r'为避免把题面中的二阶状态向量 $x_1$ 与标量混淆，记该向量为 $[\xi_1,\xi_2]^T$，则 $\dot\xi_1=\xi_2$。取 $z=[\xi_1,\xi_2,x_2]^T$：')
a=a.replace(r'$S_1$ 的输出 $y_1=2x_1+\dot x_1$ 作为 $S_2$ 的输入。',r'$S_1$ 的输出作为 $S_2$ 的输入（$u_2=y_1$）。')
write(ap,a);write(qp,q)
write(ap,a);write(qp,q)
print('updated 27 answer/question headings, both navs, 27 quick links, 27 local question statements')

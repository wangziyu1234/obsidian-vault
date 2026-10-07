from pathlib import Path
import re
base=Path('D:/obsidian/控制理论/777习题集')
ap=next(base.glob('现控200题强化 专题三*答案*.md'));qp=next(base.glob('现控200题强化 专题三*题目*.md'))
a=ap.read_text(encoding='utf-8-sig');q=qp.read_text(encoding='utf-8-sig')
q=q.replace('初始状态 $x(0)=Pe$','初始状态 $x(0)=P_0$').replace('x(t)=e^{At}Pe^{A^Tt}','x(t)=e^{At}P_0e^{A^Tt}')
q=q.replace('**3-26（2010', '> [!note] 初值记号\n> 原扫描件初值记号排版不清（印作 $Pe$）；此处统一记 $P_0=x(0)$，解中间的常矩阵也为同一个 $P_0$。\n\n**3-26（2010')
q=q.replace('**3-32（2010', '> [!warning] 第（1）问条件不足\n> 原题的下标从 $i=1$ 开始。缺少 $i=0$ 即 $cb=0$ 时，命题不成立；反例和补足条件后的证明见本题解析。\n\n**3-32（2010')
qs={}
pat=r'^\*\*(3-\d+)(.*?)\*\*\s*(.*?)(?=^\*\*3-\d+|^## |\Z)'
for m in re.finditer(pat,q,re.M|re.S):qs[m[1]]=(m[2],m[3].strip())
assert len(qs)==33
def links(n,peer,label):return f'[[{peer}#✏️ {n}　{label}|'+('原题' if label=='题目' else '查看解析')+']] · [[#🔎 题号直达|返回题号导航]]'
def qrepl(m):
    n=m[1];return f'#### ✏️ {n}　题目\n\n'+links(n,ap.stem,'解析')+'\n\n'+(m[2]+' '+m[3].strip()).strip()+'\n\n'
q=re.sub(pat,qrepl,q,flags=re.M|re.S)
def arepl(m):
    n=m[1];source,body=qs[n]
    imgs=re.findall(r'^!\[\[.*?\]\]\s*$',body,re.M)
    body=re.sub(r'^!\[\[.*?\]\]\s*$', '',body,flags=re.M).strip()
    quoted='\n'.join('> '+line if line else '>' for line in (source+'\n\n'+body).strip().splitlines())
    result=f'#### ✏️ {n}　解析\n\n'+links(n,qp.stem,'题目')+'\n\n> [!note]- 本题题设\n'+quoted+'\n\n'
    if imgs: result+='\n\n'.join(x.strip() for x in imgs)+'\n\n'
    return result+m[2].strip()+'\n\n'
a=re.sub(r'^\*\*(3-\d+)　答案\*\*([^\n]*)\n',arepl,a,flags=re.M)
assert len(re.findall(r'^#### ✏️',a,re.M))==33
def nav(label):
    rows=['## 🔎 题号直达','','| 题号范围 | 直达'+label+' |','| :-- | :-- |']
    for start in range(1,34,5):
        end=min(start+4,33);ns=[f'3-{i}' for i in range(start,end+1)]
        rows.append('| '+ns[0]+('～'+ns[-1] if len(ns)>1 else '')+' | '+' · '.join(f'[[#✏️ {n}　{label}\\|{n}]]' for n in ns)+' |')
    return '\n'.join(rows)+'\n\n'
summary=[
r'$u=v-[5,3]x$；闭环传函 $1/(s+1)$',
r'能控Ⅰ型 $B=e_3$ 时，$K=[154,45,8]$',
r'能控：$(b+c)(a-b-c)\ne0$；镇定边界见解析',
r'$K=[18,21,5]$，内部极点 $-2,-2,-3$',
r'$k_1=2k_2-4$ 可完全抑制扰动；内部稳定还需 $k_2>2$',
r'$y(t)=e^{-2t}(1+t^2/2)$；$K=[6,-4,1]$',
r'$K=[5,11,5]$；内部三阶、闭环传函二阶',
r'完全能控；$u=Hy$ 取 $H=[-4,-5]^T$ 可镇定',
r'$u=v+Kx$ 时 $K=[-4,-4,-1]$',
r'选能观Ⅱ型解释初值；$K=[\frac12,-1]$',
r'能控维数 $4$；可取 $K=[0,k_2,12,4,3]$',
r'$H=[27,23,6]^T$；原题输入列为 $[1,1,0]^T$',
r'$u=Kx$ 时 $K=[-\frac{13}{4},\frac14]$；$G=[11,-12]^T$',
r'完全能观；$G=[3,4]^T$',
r'令 $a=7.07$；$K=[a^2/50,(2a-5)/100]$，$G=[95,2025]^T$',
r'恒不完全能观；$a=4$ 时固定误差极点 $2$ 无法移动',
r'$u=v+K\hat x$，$K=[-43,-8]$；$G=[-3,15]^T$',
r'原系统不稳定；$K=[-6,-7]$，$G=[\frac{23}2,\frac{167}2]^T$；完整四阶闭环见解析',
r'$K=[\omega_n^2,2\zeta\omega_n-1]$；$G=[19,81]^T$；书中 $[2,1]$ 是近似',
r'$K=[10,4]$；$G=[13,22]^T$；完整结构图见解析',
r'$u=v-K\hat x$ 时 $K=[-\frac{19}2,\frac52]$，$H=[\frac{119}6,15]^T$',
r'$K=[4,0,8]$；按原图负注入约定 $G=[-13,-4,-10]^T$',
r'$u=v+K\hat x$，$K=[-3,1,-5]$；二维观测器 $G=[36,12]^T$',
r'$K=[3,2,1]$；$G=[2,7]^T$；变换后 $\bar B=[1,0,0]^T$',
r'$x(t)=e^{At}P_0e^{A^Tt}$；$P_0=x(0)$',
r'可逆块变换保持 PBH 矩阵的秩，状态反馈不改能控性',
r'$\dot V\le0$ 为半负定；用能观性与不变集判渐近稳定',
r'不能控子块的左特征向量给出 PBH 秩亏',
r'不能观子块的右特征向量给出 PBH 秩亏',
r'相似变换保特征值；可取 $c=e_n^TQ_c^{-1}$',
r'第（1）问缺 $cb=0$，原命题不成立；补足后由反三角乘积证明',
r'$u=Kx+Fv$ 时 $K=E_2$，$F=[-2,2;2,-1]$；$\dot y=v$',
r'能控能观但不稳定；$K=[5,\frac{13}2]$，稳态增益 $\frac18$，$\beta=8$'
]
table='## 答案速查\n\n| 题号 | 结论与关键结果 |\n| :-- | :-- |\n'
for i,s in enumerate(summary,1):table+=f'| [[#✏️ 3-{i}　解析\\|3-{i}]] | {s} |\n'
start=a.index('## 答案速查');end=a.index('\n## 【',start)
a=a[:start]+nav('解析')+table+'\n'+a[end:]
idx=q.index('## 【');q=q[:idx]+nav('题目')+q[idx:]
for p,t in [(ap,a),(qp,q)]:
    t=re.sub(r'(?m)^modify: .*$', 'modify: 2026-10-07',t)
    t=t.replace('> 返回：[[777习题集目录]]','> 返回目录：[[777习题集目录]]',1)
    raw=p.read_bytes();bom=b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    p.write_bytes(bom+t.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
print('adv3 navigation, paired anchors, local question statements and summary complete')

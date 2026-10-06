from pathlib import Path
import re
import pymupdf

root=Path('D:/obsidian')
base=root/'控制理论/777习题集'
qp=next(base.glob('现控200题基础 第2章*（题目）.md'))
ap=next(base.glob('现控200题基础 第2章*（答案与解析）.md'))
def read(p): return p.read_bytes().decode('utf-8-sig').replace('\r\n','\n')
def write(p,t):
    old=p.read_bytes(); nl='\r\n' if b'\r\n' in old else '\n'
    p.write_bytes((b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+t.replace('\n',nl).encode('utf-8'))
q=read(qp); a=read(ap)
assert '## 🔎 题号直达' not in a
# Separate all long inline data expressions into display blocks.
q=re.sub(r'(?<!\$)\$([^$\n]{55,})\$(?!\$)',lambda m:'\n\n$$\n'+m[1]+'\n$$\n\n',q)
# Distinct initial states and trajectories must each have room to read.
q=q.replace('},\\quad\nx_1(t)', '}\n$$\n\n$$\nx_1(t)').replace('};\\qquad\nx_2(0)', '}\n$$\n\n$$\nx_2(0)').replace('},\\quad\nx_2(t)', '}\n$$\n\n$$\nx_2(t)')
matches=list(re.finditer(r'^\*\*(2-\d+)(.*?)\*\*',q,re.M))
questions={}
for i,m in enumerate(matches):
    end=matches[i+1].start() if i+1<len(matches) else len(q)
    part=q[m.end():end].split('\n## ')[0].strip()
    questions[m[1]]=m[2]+' '+part
assert len(questions)==12
q=re.sub(r'^\*\*(2-\d+)(.*?)\*\*',lambda m:'#### ✏️ '+m[1]+'　题目\n\n[['+ap.stem+'#✏️ '+m[1]+'　解析|查看解析]]\n\n'+m[2],q,flags=re.M)
def head(m):
    num=m[1]; point=m[3]
    body=questions[num].strip()
    quoted='\n'.join('> '+s if s else '>' for s in body.splitlines())
    return '#### ✏️ '+num+'　解析\n\n[['+qp.stem+'#✏️ '+num+'　题目|查看题目]] · [[#🔎 题号直达|返回题号导航]]\n\n> [!note]- 本题题设\n'+quoted+'\n\n'+point
a=re.sub(r'^\*\*(2-\d+)　(.*?)\*\*(（考点：.*）)$',head,a,flags=re.M)
assert len(re.findall(r'^#### ✏️ 2-\d+　解析$',a,re.M))==12
nav=['## 🔎 题号直达','','| 题号范围 | 直达解析 |','| :-- | :-- |']
for st in range(1,13,5):
    en=min(st+4,12)
    nav.append(f'| 2-{st}～2-{en} | '+' · '.join(f'[[#✏️ 2-{i}　解析\\|2-{i}]]' for i in range(st,en+1))+' |')
a=a.replace('## 答案速查','\n'.join(nav)+'\n\n## 答案速查',1)
a=re.sub(r'(?<=\| )(2-\d+)(?= \|)',lambda m:'[[#✏️ '+m[1]+'　解析\\|'+m[1]+']]',a)
a=a.replace('（sympy 复验）','').replace('（$\\mathrm{rank}$ 均 sympy 复验）','').replace('，sympy 验证 $\\Phi(t)x(0)\\equiv[2\\ \\ 5]^T$','')
# Disambiguate the two given trajectories from the scalar state components.
a=a.replace('将两组自由运动数据按列拼成', '本题题面中的 $x_1(t)$、$x_2(t)$ 表示两条二阶状态轨迹，均为列向量，并非同一状态的两个分量。将两组自由运动数据按列拼成',1)
a=a.replace('对角元素分别约为', '对角元素分别约分为')
a=a.replace('为了直接求逆，令', '上式的星号表示伴随矩阵。为了直接求逆，令',1)
# Keep an unknown observation time distinct from the time variable of a trajectory.
st=a.index('#### ✏️ 2-7　解析'); en=a.index('#### ✏️ 2-8　解析')
part=a[st:en]
part=part.replace('又 $x(t)=\\Phi(t)x(0)$，故 $x(0)=\\Phi^{-1}(t)x(t)$，而 $\\Phi^{-1}(t)=\\Phi(-t)$：','记观测到 $x(t_0)=[2\\ \\ 5]^T$ 的时刻为 $t_0$。由 $x(t_0)=\\Phi(t_0)x(0)$ 及 $\\Phi^{-1}(t_0)=\\Phi(-t_0)$：')
p0=part.index('\\begin{aligned}\nx(0)')
p1=part.index('\\end{aligned}',p0)
part=part[:p0]+part[p0:p1].replace('(-t)','(-t_0)').replace('2t}', '2t_0}').replace('^{-t}', '^{-t_0}')+part[p1:]
part=part.replace('（上式即 $\\Phi(-t)[2\\ \\ 5]^T$）','（上式即 $\\Phi(-t_0)[2\\ \\ 5]^T$）')
part=part.replace('原书亦按此参数形式作答。','原书亦按此参数形式作答。若将该向量理解为所有时刻都保持不变，则与状态方程矛盾，因为 $A[2\\ \\ 5]^T=[5\\ \\ -1]^T\\ne0$。')
a=a[:st]+part+a[en:]
# Complete model and sampling convention in the two discretization questions.
a=a.replace('（2）先将输入列乘入状态转移矩阵：','（2）按零阶保持离散化，令 $x(k)=x(kT)$，$u(k)$ 在每个采样区间保持不变。先将输入列乘入状态转移矩阵：')
a=a.replace('此时离散化系统完全能控且完全能观。','完整离散方程为\n\n$$\nx(k+1)=Gx(k)+Hu(k)\n$$\n\n$$\ny(k)=[2\\ \\ 0]x(k)\n$$\n\n此时离散化系统完全能控且完全能观。')
a=a.replace('由零输入方程，先有', '按零阶保持离散化，记 $B=[0\\ \\ 1]^T$、$x(k)=x(kT)$。由零输入方程，先有')
a=a.replace('当 $t\\ge1$ 时 $u=1$，输入积分', '由于状态方程不含冲激，$x(1^+)=x(1^-)$；输出含直通项 $u$，故 $y(1^+)-y(1^-)=1$。当 $t\\ge1$ 时 $u=1$，输入积分')
# Split top-level comma-separated formulas; nested matrix commas are untouched.
for content in list(re.finditer(r'(?m)^\$\$\n([\s\S]*?)\n\$\$',a))[::-1]:
    s=content[1]
    if '\\begin{aligned}' in s: continue
    depth=0; pos=0; out=''
    for token in re.finditer(r'\\begin\{[^}]+\}|\\end\{[^}]+\}|[,;]?\s*\\(?:qquad|quad)\s*',s):
        out+=s[pos:token.start()]; t=token[0]
        if t.startswith('\\begin'): depth+=1
        elif t.startswith('\\end'): depth-=1
        out+= '\n$$\n\n$$\n' if ('quad' in t and depth==0) else t
        pos=token.end()
    out+=s[pos:]
    a=a[:content.start(1)]+out+a[content.end(1):]
write(qp,q); write(ap,a)
# Recrop the original figure with all of the bottom feedback box and extra margin.
pdf=next(Path('E:/BaiduNetdiskDownload/777现控200题➕答案').glob('*现控200题【题目册】.pdf'))
doc=pymupdf.open(pdf); page=doc[26]; r=page.rect
clip=pymupdf.Rect(r.width*.27,r.height*.202,r.width*.885,r.height*.401)
page.get_pixmap(dpi=220,clip=clip).save(root/'附件/现控2-9-采样系统方框图.png')
print('updated chapter 2 pair and source figure')

from pathlib import Path
import re

root=Path('D:/obsidian')
base=root/'控制理论/777习题集'

def read(p):
    data=p.read_bytes()
    return data.decode('utf-8-sig').replace('\r\n','\n'),data.startswith(b'\xef\xbb\xbf'),b'\r\n' in data

def save(p,s,bom,crlf):
    p.write_bytes((b'\xef\xbb\xbf' if bom else b'')+s.replace('\n','\r\n' if crlf else '\n').encode('utf-8'))

def nav(ch,n,kind):
    rows=['## 🔎 题号直达','','| 题号范围 | 直达'+kind+' |','| :-- | :-- |']
    for lo in range(1,n+1,5):
        hi=min(lo+4,n)
        links=' · '.join(f'[[#✏️ {ch}-{i}　{kind}\\|{ch}-{i}]]' for i in range(lo,hi+1))
        rows.append(f'| {ch}-{lo}～{ch}-{hi} | {links} |')
    return '\n'.join(rows)+'\n\n'

def display_long(s):
    # Move long inline expressions into their own display without changing algebra.
    lines=s.splitlines(); out=[]; inside=False
    for line in lines:
        if line.strip()=='$$': inside=not inside
        if not inside and not line.startswith(('|','>','#')) and line.strip()!='$$':
            line=re.sub(r'(?<!\$)\$([^$\n]{75,})\$(?!\$)',lambda m:'\n\n$$\n'+m[1]+'\n$$\n\n',line)
        out.append(line)
    return re.sub(r'\n{3,}','\n\n','\n'.join(out))+'\n'

for ch,n in [(3,27),(4,19)]:
    qp=next(base.glob(f'现控200题基础 第{ch}章*（题目）.md'))
    ap=next(base.glob(f'现控200题基础 第{ch}章*（答案与解析）.md'))
    q,qbom,qcrlf=read(qp); a,abom,acrlf=read(ap)
    statements={}
    pat=rf'^\*\*({ch}-\d+)(.*?)\*\*(.*?)(?=^\*\*{ch}-\d+|^## |\Z)'
    for m in re.finditer(pat,q,re.M|re.S):
        body=(m[2]+m[3]).strip()
        body=re.sub(r'\n> \[!tip\][^\n]*\n(?:>[^\n]*\n?)*','\n',body)
        body=display_long(body).strip()
        statements[m[1]]=body
    assert len(statements)==n
    q=re.sub(rf'^\*\*({ch}-\d+)(.*?)\*\*',lambda m:f'#### ✏️ {m[1]}　题目\n\n> [[{ap.stem}#✏️ {m[1]}　解析|查看本题解析]] · [[#🔎 题号直达|返回题号导航]]\n\n'+m[2],q,flags=re.M)
    ix=q.index('## 【题型1】');q=q[:ix]+nav(ch,n,'题目')+q[ix:]
    q=display_long(q)
    # Original heading was a bold paragraph, so no prior question-level heading links exist.
    def answer(m):
        num=m[1]; summary=m[2].lstrip('： ').strip(); point=m[3]
        fold='> [!note]- 本题题设\n'+'\n'.join('> '+x if x else '>' for x in statements[num].splitlines())
        return (f'#### ✏️ {num}　解析\n\n> [[{qp.stem}#✏️ {num}　题目|查看题目页]] · [[#🔎 题号直达|返回题号导航]]\n\n'
                +fold+'\n\n'+point+'\n\n**答案：** '+summary)
    a=re.sub(rf'^\*\*({ch}-\d+)　答案(.*?)\*\*(.*)$',answer,a,flags=re.M)
    assert len(re.findall(r'^#### ✏️',a,re.M))==n
    a=a.replace('## 答案速查',nav(ch,n,'解析')+'## 答案速查',1)
    a=re.sub(rf'(?<=\| )({ch}-\d+)(?= \|)',lambda m:f'[[#✏️ {m[1]}　解析\\|{m[1]}]]',a)
    # A constant nonsingular coordinate map is required in 3-11.
    if ch==3:
        a=a.replace('具体代入时，$P$ 为常数，故：','这里 $P$ 为常数非奇异矩阵；具体代入时，故：')
        def rename(m):
            num=m[1]; body=m[0]
            if num not in ['3-2','3-3','3-24']: return body
            if num=='3-2':
                body=body.replace('Q_c=[b\\ \\ Ab]','Q_c=[B\\ \\ AB]').replace(r'\begin{bmatrix}c\\cA\end{bmatrix}',r'\begin{bmatrix}C\\CA\end{bmatrix}')
                intro='本题 $b,c$ 是标量参数；输入列记为 $B=[2\\quad2b]^T$，输出行记为 $C=[1\\quad2c]$，$A$ 为题设的系统矩阵。'
            else:
                body=body.replace(r'b=\begin{bmatrix}0\\0\\1\end{bmatrix}',r'B=\begin{bmatrix}0\\0\\1\end{bmatrix}')
                body=body.replace(r'$b=[0\ \ 0\ \ 1]^T$',r'$B=[0\ \ 0\ \ 1]^T$')
                body=body.replace('c=[b','C=[b').replace(r'\begin{bmatrix}c\\cA\\cA^2\end{bmatrix}',r'\begin{bmatrix}C\\CA\\CA^2\end{bmatrix}')
                body=body.replace('b=1,\\qquad c=1','B=1,\\qquad C=1')
                intro='本题保留原题标量参数 $b$；所构造实现的输入列、输出行分别记为 $B,C$。'
            point=body.index('**答案：**')
            return body[:point]+intro+'\n\n'+body[point:]
        a=re.sub(r'^#### ✏️ (3-\d+)　解析.*?(?=^#### ✏️ |^## |\Z)',rename,a,flags=re.M|re.S)
    a=display_long(a)
    save(qp,q,qbom,qcrlf);save(ap,a,abom,acrlf)
    print(ch,n,'question headings and answer headings updated')

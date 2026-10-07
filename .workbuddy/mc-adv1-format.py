from pathlib import Path
import re
root=Path('D:/obsidian');base='现控200题强化 专题一 状态空间描述'
ap=root/'控制理论/777习题集'/f'{base}（答案与解析）.md'
t=ap.read_text(encoding='utf-8')
t=t.replace('现控强化1-23-ans-观测器结构图.png|430','现控强化1-23-精确观测器结构图.png|520')
t=t.replace('现控强化1-25-ans-闭环结构图.png|430','现控强化1-25-完整闭环结构图.png|520')
t=t.replace('（3）系统全维状态观测器结构图如下','（3）下图采用向量积分器 $E_3/s$（即三个并列积分器）；$A,B,C$ 为本题题设矩阵，$h$ 为上式精确增益。系统全维状态观测器结构图如下')
t=t.replace('（3）结构图为','（3）下图采用两个二维向量积分器 $E_2/s$，分别实现系统与观测器的状态积分；矩阵 $A,b,c$ 均取本题题设值，参考输入为 $v$，实际控制输入为 $u=v+k\hat x$。结构图为')
def split_top(s,delims):
    depth=0;env=[];i=0;last=0;res=[]
    while i<len(s):
        m=re.match(r'\\(begin|end)\{([^}]+)\}',s[i:])
        if m:
            if m[1]=='begin':env.append(m[2])
            else:
                assert env and env[-1]==m[2],s
                env.pop()
            i+=len(m[0]);continue
        if s[i]=='{' and (i==0 or s[i-1]!='\\'):depth+=1
        if s[i]=='}' and (i==0 or s[i-1]!='\\'):depth-=1
        if not depth and not env:
            found=False
            for d in delims:
                if s.startswith(d,i):
                    res.append(s[last:i]);i+=len(d);last=i;found=True;break
            if found:continue
        i+=1
    assert depth==0 and not env,s
    return res+[s[last:]]
def fmt(match):
    prefix=match[1];s=match[2]
    # Unquote callout formula before transforming.
    if prefix:s='\n'.join(re.sub(r'^> ?', '',x) for x in s.splitlines())
    s=s.strip()
    if not s:return match[0]
    parts=split_top(s,[',\\qquad ', ',\\quad ', '\\qquad ', '\\quad '])
    # Only break independent scalar/matrix statements, not explanatory spacing.
    if len(parts)>1 and all('=' in x or '\\Rightarrow' in x for x in parts):
        blocks=parts
    else:blocks=[s]
    out=[]
    for b in blocks:
        if len(b)>170 and '\\begin{aligned}' not in b:
            eq=split_top(b,['='])
            if len(eq)>2:
                b='\\begin{aligned}\n'+eq[0]+'&='+eq[1]+'\n'+''.join('\\\\\n&='+x+'\n' for x in eq[2:])+'\\end{aligned}'
            elif len(eq)==2:
                # Break a state equation before its input matrix where possible.
                ps=split_top(eq[1],['+'])
                if len(ps)==2 and ps[1].startswith(('\\begin{bmatrix}','\\begin{pmatrix}')):
                    b='\\begin{aligned}\n'+eq[0]+'&='+ps[0]+'\\\\\n&+'+ps[1]+'\n\\end{aligned}'
        out.append('$$\n'+b+'\n$$')
    r='\n\n'.join(out)
    if prefix:r='\n'.join('> '+x if x else '>' for x in r.splitlines())
    return r
# Keep complete environments; never split within boxed expressions or matrices.
t=re.sub(r'(?m)^(> )?\$\$\n(.*?)\n(?:> )?\$\$',fmt,t,flags=re.S)
ap.write_bytes(t.replace('\n','\r\n').encode('utf-8'))
print('formatted')

from pathlib import Path
import re
p=next(Path('D:/obsidian/控制理论/777习题集').glob('现控200题强化 专题一*答案*'))
t=p.read_text(encoding='utf-8')
# State equations in cases: give each equation its own aligned block.
def cases(m):
    s=m[1]
    if len(s)<170 or not s.startswith(r'\begin{cases}') or not s.endswith(r'\end{cases}'):
        return m[0]
    body=s[len(r'\begin{cases}'):-len(r'\end{cases}')]
    if r'\Rightarrow' in body:return m[0]
    # The compact matrix forms use [6pt] only between state/output equations.
    rows=re.split(r'\\\\\[(?:4|6)pt\]',body)
    if len(rows)<2:return m[0]
    blocks=[]
    for row in rows:
        row=row.strip()
        lhs,rhs=row.split('=',1)
        # Matrices have their own row breaks; retain them intact.
        if r'\begin' not in rhs:
            terms=re.split(r'(?=[+-]\\frac)',rhs)
            if len(terms)>3:rhs=''.join(terms[:2])+r'\\'+'\n&'+''.join(terms[2:])
        else:
            rhs=rhs.replace(r'x+\begin',r'x\\'+'\n&+'+r'\begin')
        blocks.append('$$\n'+r'\begin{aligned}'+'\n'+lhs+'&='+rhs+'\n'+r'\end{aligned}'+'\n$$')
    return '\n\n'.join(blocks)
t=re.sub(r'(?m)^\$\$\n(.*?)\n\$\$',cases,t,flags=re.S)
t=t.replace('\\end{cases}\n\\Rightarrow\n\\begin{cases}\n1+(a-1)', '\\end{cases}\n$$\n\n代入输出表达式：\n\n$$\n\\begin{cases}\n1+(a-1)')
old=r'''\dot{\hat x}=\begin{bmatrix}-\frac{13}{2}&-\frac{15}{2}\\\frac12&-\frac52\end{bmatrix}\hat x
+\begin{bmatrix}1\\0\end{bmatrix}u
+\begin{bmatrix}\frac{17}{2}\\-\frac12\end{bmatrix}y'''
new=r'''\begin{aligned}
\dot{\hat x}&=\begin{bmatrix}-\frac{13}{2}&-\frac{15}{2}\\\frac12&-\frac52\end{bmatrix}\hat x\\
&+\begin{bmatrix}1\\0\end{bmatrix}u\\
&+\begin{bmatrix}\frac{17}{2}\\-\frac12\end{bmatrix}y
\end{aligned}'''
assert old in t
t=t.replace(old,new)
# Split the compact scalar sum in the 1-9 callout for narrow screens.
old=next(x for x in t.splitlines() if x.startswith('> 复算：$W='))
new=r'''> 验算时先写闭环传递函数：
>
> $$
> W=\frac{W_1}{1+W_1W_2}
> $$
>
> $$
> 1+W_1W_2=\frac{(s+1)^3(s+2)+s(s+3)}{(s+1)^3(s+2)}
> $$
>
> 展开分母：
>
> $$
> \begin{aligned}
> (s+1)^3(s+2)+s(s+3)
> &=s^4+5s^3+9s^2+7s+2\\
> &\quad+s^2+3s\\
> &=s^4+5s^3+10s^2+10s+2
> \end{aligned}
> $$
>
> 与官方勘误图一致。'''
t=t.replace(old,new)
p.write_bytes(t.replace('\n','\r\n').encode('utf-8'))

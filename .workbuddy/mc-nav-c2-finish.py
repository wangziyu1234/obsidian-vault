from pathlib import Path
import re
import pymupdf
root=Path('D:/obsidian'); base=root/'控制理论/777习题集'
ap=next(base.glob('现控200题基础 第2章*（答案与解析）.md')); qp=next(base.glob('现控200题基础 第2章*（题目）.md'))
for p in [qp,ap]:
    data=p.read_bytes(); text=data.decode('utf-8').replace('\r\n','\n')
    # Repair punctuation left by promotion of long formulas out of prose.
    text=re.sub(r'(?m)^(> )?，',lambda m:m[1] or '',text)
    text=re.sub(r'(?m)^(> )?；',lambda m:m[1] or '',text)
    text=re.sub(r'(?m)^(> )?。',lambda m:m[1] or '',text)
    if p==ap:
        start=text.index('| 题号 | 答案 | 题号 | 答案 |'); end=text.index('\n## 【题型1】',start)
        answers=[
          r'$A=\begin{bmatrix}-3&4\\-1&1\end{bmatrix}$；$\Phi(t)$ 见解析',
          r'$e^{At}=e^t[I+t(A-I)]$，其中 $(A-I)^2=0$',
          r'$W(s)=\frac{2(s+5)}{(s+2)(s+3)}$；完全能控、完全能观',
          r'$y(t)=\frac23(e^{3t}-1)+e^{-t}$',
          r'$x(t)=e^{At}x(0)$；$a\ne b$ 与 $a=b$ 两种表达见解析',
          r'$W(s)=\frac{s+5}{s+3}$；状态连续，输出在 $t=1$ 跳变 $1$',
          r'设 $x(t_0)=[2\ \ 5]^T$；$x(0)=[-e^{2t_0}+3e^{-t_0}\ \ 2e^{2t_0}+3e^{-t_0}]^T$',
          r'$\lambda=-\frac32$，$x(0)=[-2\ \ 2]^T$',
          r'$q=e^{-1}$；$K_d=[\frac{29}{25(1-q)}\ \ \frac{q(71-100q)}{50(1-q)^2}]$',
          r'$A=\begin{bmatrix}0&4\\-4&0\end{bmatrix}$；能控能观要求 $T>0$ 且 $T\ne\frac{k\pi}{4}$（$k=1,2,\ldots$）',
          r'$A=\begin{bmatrix}0&1\\-2&-3\end{bmatrix}$，$b=[1\ \ -1]^T$；精确离散矩阵见解析',
          r'$q=e^{-2}$；$G=\begin{bmatrix}1&\frac{1-q}2\\0&q\end{bmatrix}$，$H=[\frac{1+q}4\ \ \frac{1-q}2]^T$'
        ]
        table='| 题号 | 结论与关键结果 |\n| :-- | :-- |\n'+'\n'.join(f'| [[#✏️ 2-{i}　解析\\|2-{i}]] | {s} |' for i,s in enumerate(answers,1))+'\n'
        text=text[:start]+table+text[end:]
        text=text.replace('x(k+1)=\\begin{bmatrix}0.75&0.25\\\\-0.5&0\\end{bmatrix}x(k)+\\begin{bmatrix}0.5\\\\-0.5\\end{bmatrix}u(k)',r'x(k+1)=\begin{bmatrix}\frac34&\frac14\\-\frac12&0\end{bmatrix}x(k)+\begin{bmatrix}\frac12\\-\frac12\end{bmatrix}u(k)')
    p.write_bytes(text.replace('\n','\r\n' if b'\r\n' in data else '\n').encode('utf-8'))
pdf=next(Path('E:/BaiduNetdiskDownload/777现控200题➕答案').glob('*现控200题【题目册】.pdf'))
doc=pymupdf.open(pdf); page=doc[26]; r=page.rect
page.get_pixmap(dpi=220,clip=pymupdf.Rect(r.width*.27,r.height*.192,r.width*.885,r.height*.401)).save(root/'附件/现控2-9-采样系统方框图.png')

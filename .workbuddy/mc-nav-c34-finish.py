from pathlib import Path
import re
base=Path('D:/obsidian/控制理论/777习题集')
def patch_text(p,s):
    raw=p.read_bytes(); nl='\r\n' if b'\r\n' in raw else '\n'
    p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\n',nl).encode('utf8'))

short={10:'由两组自由响应求出 $A$；精确离散模型与采样周期条件见下。',12:'$A$ 可对角化；变换阵及完整状态转移矩阵见下。',13:'按能控 I 型建立三阶实现，该实现完全能观。',14:'能控 I 型与 II 型均可实现原传递函数；两组矩阵及系数匹配见下。',15:'能控 I 型的输出行为 $c=[25\\quad25\\quad6]$，具体矩阵见下。',17:'原系统取能控 I 型；对偶系统将 $A$ 转置并交换输入、输出，矩阵与结构图见下。',18:'第一列需一阶、第二列需二阶；拼合后的三阶实现完全能控能观，原书六阶实现非最小。',19:'系统不完全能观；分解为一维能观块和一维不能观块。',20:'系统不完全能控；分解为二维能控块和一维不能控块。',21:'第（1）问用 $A=\\dot\\Phi(0)$ 求解；第（2）问按独立题设分解为二维能观块和一维不能观块。',23:'最小实现为二阶；分别用三阶能观型、能控型构造不完全能控与不完全能观实现。',24:'能控标准型见下；$a=5,b=6$ 时得到一阶最小实现。',25:'三阶能控标准型不完全能观，能观矩阵秩为 2，故非最小。',26:'取三阶能控标准型，第二输出含直通项 $D_2=1$；矩阵见下。'}
definitions={1:'记题设中的状态矩阵为 $A$、输入列为 $b$，即 $\\dot x=Ax+bu$。',4:'记题设状态矩阵、输入列与输出行分别为 $A,b,c$，即 $\\dot x=Ax+bu$、$y=cx$。',6:'按题设记 $\\dot x=Ax+bu$、$y=cx+du$，本题直通项 $d=0$。',7:'按题设记 $\\dot x=Ax+Bu$、$y=Cx$；$B,C$ 均为二阶矩阵。',8:'输入列记为 $b=[b_1\\quad b_2\\quad b_3\\quad b_4]^T$，输出行记为 $c=[c_1\\quad c_2\\quad c_3\\quad c_4]$。',9:'记离散模型为 $x(k+1)=Gx(k)+Hu(k)$、$y(k)=cx(k)$，$G,H,c$ 分别为题设状态矩阵、输入列与输出行。',14:'将题设模型记为 $\\dot x=Ax+bu$、$y=cx$；下面先求传递函数，再建立等价实现。',19:'将题设系数依次记作 $A,B,C$，即 $\\dot x=Ax+Bu$、$y=Cx$。',20:'将题设系数依次记作 $A,B,C$，即 $\\dot x=Ax+Bu$、$y=Cx$。'}

def split_equations(content):
    # Split only top-level horizontal separators, never matrix columns or cases.
    parts=[]; start=0; env=[]; brace=0;i=0
    while i<len(content):
        m=re.match(r'\\(begin|end)\{([^}]+)\}',content[i:])
        if m:
            if m[1]=='begin':env.append(m[2])
            elif env:env.pop()
            i+=len(m[0]);continue
        if content[i]=='{':brace+=1
        elif content[i]=='}':brace-=1
        m=re.match(r'[,;]?\s*\\qquad\s*|,\s*\\quad\s*',content[i:])
        if m and not env and brace==0:
            part=content[start:i].strip().rstrip(',;')
            if part:parts.append(part)
            i+=len(m[0]);start=i;continue
        i+=1
    parts.append(content[start:].strip())
    return [p for p in parts if p]

for ch in [3,4]:
    for p in base.glob(f'现控200题基础 第{ch}章*.md'):
        s=p.read_text(encoding='utf-8-sig')
        if ch==4:
            s=s.replace('如果系统在平衡状态 $x_e=(0,0)$ 处渐近稳定','如果系统在平衡状态 $x_e=(0,0,0)^T$ 处渐近稳定')
            # Add the same source correction immediately below the problem in both views.
            marker='试用李雅普诺夫第一法求 $a$ 的取值范围。'
            s=s.replace(marker,marker+'\n'+('>\n> 原书此处写成二维原点；由三维状态方程，应为 $x_e=(0,0,0)^T$。' if '答案与解析' in p.name else '\n> [!note] 原书维数笔误\n> 原书此处写成二维原点；由三维状态方程，应为 $x_e=(0,0,0)^T$。'),1)
        if '答案与解析' in p.name:
            def body_edit(m):
                num=int(m[1]); b=m[0]
                if ch==3:
                    if num in short:b=re.sub(r'^\*\*答案：\*\* .*$',lambda _: '**答案：** '+short[num],b,flags=re.M)
                    if num in definitions:b=b.replace('**答案：**',definitions[num]+'\n\n**答案：**',1)
                    if num==11:b=b.replace('这里 $P$ 为常数非奇异矩阵；具体代入时，故：','这里 $P$ 为常数非奇异矩阵，因此：')
                    if num==27:b=b.replace('能控分块友阵的 $B=[0\\ \\ E]^T$','这里 $E=I_2$ 是二阶单位阵。能控分块友阵的 $B=[0\\ \\ E]^T$')
                else:
                    if num in [1,3,11,12]:b=b.replace('**答案：**','以下判断零输入内部稳定性，令 $u=0$；$A$ 为本题状态矩阵。\n\n**答案：**',1)
                    if num==2:b=b.replace('（1）能控性与能观性','将题设三组系数记为 $A,B,C$。\n\n（1）能控性与能观性',1)
                    if num==15:b=b.replace('由 $(I-G)x_e=0$','记题设的三阶状态矩阵为 $G$。由 $(I-G)x_e=0$',1)
                return b
            s=re.sub(rf'^#### ✏️ {ch}-(\d+)　解析.*?(?=^#### ✏️ |^## |\Z)',body_edit,s,flags=re.M|re.S)
            # Short exact fractions are easier to read than decimal arithmetic here.
            if ch==4:s=s.replace('z_{1,2}=0.5\\pm0.5\\mathrm j',r'z_{1,2}=\frac{1\pm\mathrm j}{2}').replace(r'\sqrt{0.5^2+0.5^2}',r'\sqrt{\frac14+\frac14}')
        def blocks(m):
            prefix=m[1]; content=m[2]
            if prefix:content='\n'.join(line[2:] if line.startswith('> ') else line[1:] if line.startswith('>') else line for line in content.splitlines())
            pieces=split_equations(content)
            sep='\n>\n' if prefix else '\n\n'
            return sep.join(prefix+'$$\n'+'\n'.join(prefix+line for line in part.splitlines())+'\n'+prefix+'$$' for part in pieces)
        s=re.sub(r'^(> )?\$\$\n(.*?)\n(?:> )?\$\$',lambda m:blocks(type('Match',(),{'__getitem__':lambda self,i: (m[i] or '')})()),s,flags=re.M|re.S)
        s=s.replace('\n，$y=', '\n输出为 $y=').replace('\n> ，$y=', '\n> 输出为 $y=')
        patch_text(p,s)
        print(p.name)

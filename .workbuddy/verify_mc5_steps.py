from pathlib import Path
import re
import sympy as S
p=next(Path('控制理论/777习题集').glob('*基础 第5*答案*'))
s=p.read_text(encoding='utf-8')
print('unwrapped long blocks:',[(s[:m.start()].count('\n')+1,len(m.group(1))) for m in re.finditer(r'\$\$(.*?)\$\$',s,re.S) if len(m.group(1))>170 and 'aligned' not in m.group(1)])
assert s.count('$$')%2==0
stack=[]
for token,name in re.findall(r'\\(begin|end)\{([^}]+)\}',s):
    if token=='begin': stack.append(name)
    else: assert stack.pop()==name
assert not stack
l,w,g1,g2,g3,g4=S.symbols('l w g1 g2 g3 g4')
A=S.Matrix([[0,1,0,0],[3*w*w,0,0,2*w],[0,0,0,1],[0,-2*w,0,0]])
C=S.Matrix([[0,0,1,0]])
O=S.Matrix.vstack(C,C*A,C*A**2,C*A**3)
assert O.det()==-12*w**4
G=S.Matrix([g1,g2,g3,g4])
f=l*l*(l*l+w*w)+g3*l*(l*l+w*w)+g4*(l*l-3*w*w)-2*w*g2*l-6*w**3*g1
assert S.expand((l*S.eye(4)-A+G*C).det()-f)==0
A=S.Matrix([[1,2,0],[3,-1,1],[0,2,0]])
C=S.Matrix([[0,0,1]])
f=(l-1)*((l+1)*(l+g3)+2*g2-2)-6*(l+g3)+6*g1
assert S.expand((l*S.eye(3)-A+S.Matrix([g1,g2,g3])*C).det()-f)==0
print('Symbolic assertions passed.')

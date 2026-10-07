from pathlib import Path
import re,sympy as S
s,t,K=S.symbols('s t K',real=True)
d=-3+S.sqrt(3)
assert S.simplify(-d*(d+3)*(d+6)-6*S.sqrt(3))==0
assert S.expand((s+8)*(s*s+s+10))==s**3+9*s*s+18*s+80
assert S.factor(s**3+9*s*s+18*s+162)==(s+9)*(s*s+18)
Gc=(1+s)/(1+s/3);G0=2/(s*(s+1))
assert S.simplify(Gc*G0-6/(s*(s+3)))==0
v=S.simplify((Gc*G0).subs(s,S.I*S.sqrt(3)))
assert S.simplify(v-(-S.Rational(1,2)-S.I*S.sqrt(3)/2))==0
A=S.Matrix([[0,1],[0,0]]);B=S.Matrix([0,1]);F=S.Matrix([[8,4]])
assert S.expand((s*S.eye(2)-(A-B*F)).det())==s*s+4*s+8
y=1-S.exp(-2*t)*(S.cos(2*t)+S.sin(2*t))
assert S.simplify(S.diff(y,t,2)+4*S.diff(y,t)+8*y-8)==0
assert y.subs(t,0)==0 and S.diff(y,t).subs(t,0)==0
seq=[S.Rational(0)]
for _ in range(4):seq.append(1-seq[-1]/2)
assert seq==[0,1,S.Rational(1,2),S.Rational(3,4),S.Rational(5,8)]
r=Path(r'D:/obsidian')
for f in (r/'控制理论/青岛大学825真题/777改编模拟卷/Markdown笔记').glob('01 *.md'):
 text=f.read_text(encoding='utf-8')
 assert len(re.findall(r'^## 第\d+题',text,re.M))==17
 assert len(re.findall(r'^# ',text,re.M))==1
 assert len(re.findall(r'^\$\$$',text,re.M))%2==0
 for target in re.findall(r'\[\[([^]|]+)',text):
  if '#' not in target:continue
  path,anchor=target.split('#',1)
  actual=r/(path+'.md')
  assert actual.exists(),str(actual)
  assert anchor in actual.read_text(encoding='utf-8'),(path,anchor)
print('PASS: 17 questions, H1, display pairs, source anchors; exact root locus, lead frequency, feedback polynomial and ODE, discrete recurrence')


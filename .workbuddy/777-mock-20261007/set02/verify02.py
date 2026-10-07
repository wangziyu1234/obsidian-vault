from pathlib import Path
import re
import sympy as S
s,t,z=S.symbols('s t z', real=True)
k=S.symbols('k', integer=True, nonnegative=True)
checks=[]
def eq(name,a,b):
    assert S.simplify(a-b)==0,(name,S.simplify(a-b))
    checks.append(name)
eq('Q2 step',S.laplace_transform(1-2*S.exp(-2*t)+S.exp(-4*t),t,s,noconds=True)*s,8/((s+2)*(s+4)))
eq('Q3 dominant poles',s*s+2*s+2,(s+1-S.I)*(s+1+S.I))
eq('Q3 damping exponent',(1/S.sqrt(2))/S.sqrt(1-S.Rational(1,2)),1)
eq('Q7 ZOH', (1-S.exp(-S.I*S.pi))/(S.I*S.pi),-2*S.I/S.pi)
p=-1+S.I*S.sqrt(3)
eq('Q4 gain',(p+1)*(p+2)*(p+4)+12,0)
eq('Q5 closed response',2/(3+3*S.I),(1-S.I)/3)
eq('Q8 roots',(1+2*S.I)**2-2*(1+2*S.I)+5,0)
P=S.exp(-t)*S.Matrix([[1,t],[0,1]])
assert P.diff(t).subs(t,0)==S.Matrix([[-1,1],[0,-1]])
checks.append('Q10 derivative')
b=S.symbols('b')
A=S.Matrix([[-1,0],[-3,-S.Rational(3,2)]])
B=S.Matrix([2,2*b])
eq('Q11 determinant',B.row_join(A*B).det(),-2*(b+6))
eq('Q12 transform',S.laplace_transform(t*S.exp(-2*t),t,s,noconds=True),1/(s+2)**2)
eq('Q13 desired polynomial',s*(s+1)*(s+3)+2*s*s+9*s+8,(s+2)**3)
eq('Q13 error transform',S.laplace_transform(S.exp(-2*t)*(1-t*t/2),t,s,noconds=True),(s+1)*(s+3)/(s+2)**3)
eq('Q13 ramp final',S.limit((s+1)*(s+3)/(s+2)**3,s,0),S.Rational(3,8))
K=S.symbols('K', positive=True)
gain=-s*(s+1)/((s+2)*(s+3))
for sign in [1,-1]:
    d=(-3+sign*S.sqrt(3))/2
    eq('Q14 break point '+str(sign),S.diff(gain,s).subs(s,d),0)
    eq('Q14 break gain '+str(sign),gain.subs(s,d),7-sign*4*S.sqrt(3))
sig=-(1+5*K)/(2*(1+K))
mag=6*K/(1+K)
eq('Q14 circle',mag+3*sig+S.Rational(9,4),S.Rational(3,4))
eq('Q14 discriminant',(1+5*K)**2-24*K*(1+K),K*K-14*K+1)
eq('Q14 damping minimum',(1+5*K)**2/(24*K*(1+K))-S.Rational(2,3),(3*K-1)**2/(24*K*(1+K)))
eq('Q14 optimal poles',(s+1-S.I/S.sqrt(2))*(s+1+S.I/S.sqrt(2)),s*s+2*s+S.Rational(3,2))
y=1-3*S.Rational(1,2)**k+2*S.Rational(1,4)**k
eq('Q15 recurrence',y.subs(k,k+2)-S.Rational(3,4)*y.subs(k,k+1)+S.Rational(1,8)*y,S.Rational(3,8))
eq('Q15 initial0',y.subs(k,0),0)
eq('Q15 initial1',y.subs(k,1),0)
eq('Q15 partial fraction',z/(z-1)-3*z/(z-S.Rational(1,2))+2*z/(z-S.Rational(1,4)),3*z/(8*(z-1)*(z-S.Rational(1,2))*(z-S.Rational(1,4))))
eq('Q16 first energy',(-2*t)**2+4*(1-t*t),4)
eq('Q16 second energy',(-2+2*t)**2-4*(-2*t+t*t),4)
A=S.Matrix([[-5,-1],[6,0]])
B=S.Matrix([0,2]); C=S.Matrix([[0,1]]); I=S.eye(2)
eq('Q17 transfer',(C*(s*I-A).inv()*B)[0],2*(s+5)/((s+2)*(s+3)))
eq('Q17 controllable',B.row_join(A*B).det(),4)
eq('Q17 observable',C.col_join(C*A).det(),-6)
P=(A+3*I)*S.exp(-2*t)-(A+2*I)*S.exp(-3*t)
assert P.subs(t,0)==I and S.simplify(P.diff(t)-A*P)==S.zeros(2)
checks.append('Q17 state transition initial and ODE')
out=S.Rational(5,3)-3*S.exp(-2*t)+S.Rational(4,3)*S.exp(-3*t)
eq('Q17 step',S.laplace_transform(out,t,s,noconds=True),2*(s+5)/(s*(s+2)*(s+3)))
root=Path('D:/obsidian')
folder=root/'控制理论/青岛大学825真题/777改编模拟卷/Markdown笔记'
for path in folder.glob('02 *.md'):
    text=path.read_text(encoding='utf-8')
    assert len(re.findall(r'^# ',text,re.M))==1
    assert len(re.findall(r'^## 第\d+题',text,re.M))==17
    assert text.count('$$')%2==0
    assert re.findall(r'\\begin\{([^}]+)\}',text)==re.findall(r'\\end\{([^}]+)\}',text)
    for target in re.findall(r'\[\[([^]|]+)',text):
        name,sep,anchor=target.partition('#')
        if name=='777改编模拟卷目录': continue
        found=list(root.rglob(name+'.md')) if '/' not in name else [root/(name+'.md')]
        assert found,(path.name,target)
        if sep:
            source=found[0].read_text(encoding='utf-8-sig')
            assert any(re.sub(r'^#+\s*','',line)==anchor for line in source.splitlines()),target
    checks.append(path.name+' structural and source links')
report='PASS '+str(len(checks))+' checks\n'+'\n'.join(checks)+'\n'
Path(__file__).with_name('verification.txt').write_text(report,encoding='utf-8')
print(report.encode('ascii','backslashreplace').decode())

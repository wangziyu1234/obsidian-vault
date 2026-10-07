from pathlib import Path
import re
import sympy as S
s,t=S.symbols('s t',real=True)
checks=[]
def eq(n,a,b):
    assert S.simplify(a-b)==0,(n,S.simplify(a-b))
    checks.append(n)
eq('Q2 response',S.laplace_transform(1+S.exp(-t),t,s,noconds=True),(2*s+1)/(s*(s+1)))
assert sum(int(bool(S.re(r)>0)) for r in S.nroots(s**3+2*s*s+s+4))==2
checks.append('Q3 RHP count')
eq('Q4 centroid',S.Rational(-4+2,2),-1)
eq('Q5 phase margin',S.pi-3*S.pi/4,S.pi/4)
th=S.symbols('theta',real=True)
eq('Q8 cubic sine coefficient',S.integrate(S.sin(th)**4,(th,0,2*S.pi))/S.pi,S.Rational(3,4))
eq('Q10 minimum transfer',(s+1)/(s*s+3*s+2),1/(s+2))
A=S.Matrix([[0,1],[-1,0]])
assert A+A.T==S.zeros(2)
checks.append('Q11 energy')
a,b,c,d,e,f,g,h,i=S.symbols('a b c d e f g h i')
Y2,Y3,Y4,Y5,Y6=S.symbols('Y2 Y3 Y4 Y5 Y6')
sol=S.solve([Y2-a+g*Y3+i*Y5,Y3-c*Y2,Y4-d*Y3-b*Y2+h*Y5,Y5-e*Y4,Y6-f*Y5],[Y2,Y3,Y4,Y5,Y6])
delta=1+c*g+e*h+c*d*e*i+b*e*i+c*g*e*h
eq('Q13 full transfer',sol[Y6],(a*c*d*e*f+a*b*e*f)/delta)
eq('Q13 intermediate transfer',sol[Y3],a*c*(1+e*h)/delta)
eq('Q13 numeric',sol[Y6].subs({v:1 for v in [a,b,c,d,e,f,g,h,i]}),S.Rational(1,3))
k,T=S.symbols('k T',positive=True)
G=k/(s*(s*s+4*s+8))
eq('Q14 error final',S.limit(s*(3/s+2/s**2)/(1+G),s,0),16/k)
eq('Q14 marginal factor',s**3+4*s*s+8*s+32,(s+4)*(s*s+8))
G1=k/(s*(T*s+1)); G2=2*k/(s*(T*s/2+1))
eq('Q15 scaling',G2,G1.subs(s,s/2))
eq('Q15 original cutoff magnitude square',(S.sqrt(2)/(s*(s+1))).subs(s,S.I)*S.conjugate((S.sqrt(2)/(s*(s+1))).subs(s,S.I)),1)
q=S.symbols('q',positive=True)
P=S.Matrix([[1,(1-S.exp(-2*t))/2],[0,S.exp(-2*t)]])
H=S.integrate(P,(t,0,1))
Hq=S.Matrix([[1,(1+q)/4],[0,(1-q)/2]])
assert S.simplify(H-Hq.subs(q,S.exp(-2)))==S.zeros(2)
assert S.simplify(Hq*S.Matrix([(1-3*q)/(2*(1-q)),2/(1-q)]))==S.Matrix([1,1])
checks.append('Q16 ZOH integral and one step input')
A=S.Matrix([[0,1],[-2,-3]]); B=S.Matrix([0,2]); C=S.Matrix([[1,0]]); L=S.Matrix([7,1])
eq('Q17 realization',(C*(s*S.eye(2)-A).inv()*B)[0],2/((s+1)*(s+2)))
eq('Q17 observer poles',(s*S.eye(2)-A+L*C).det(),(s+4)*(s+6))
err=S.Matrix([-S.exp(-4*t)/2+3*S.exp(-6*t)/2,-3*S.exp(-4*t)/2+3*S.exp(-6*t)/2])
assert err.subs(t,0)==S.Matrix([1,0]) and S.simplify(err.diff(t)-(A-L*C)*err)==S.zeros(2,1)
checks.append('Q17 error initial and ODE')
root=Path('D:/obsidian')
folder=root/'控制理论/青岛大学825真题/777改编模拟卷/Markdown笔记'
for path in folder.glob('04 *.md'):
    text=path.read_text(encoding='utf-8')
    nums=re.findall(r'^## 第(\d+)题（(\d+)分）',text,re.M)
    assert nums==[(str(n),str(5 if n<=12 else 18)) for n in range(1,18)]
    assert sum(int(v) for n,v in nums)==150
    assert len(re.findall(r'^# ',text,re.M))==1
    assert text.count('$$')%2==0
    assert re.findall(r'\\begin\{([^}]+)\}',text)==re.findall(r'\\end\{([^}]+)\}',text)
    for target in re.findall(r'\[\[([^]|]+)',text):
        name,sep,anchor=target.partition('#')
        if name=='777改编模拟卷目录':continue
        found=list(root.rglob(name+'.md')) if '/' not in name else [root/(name+'.md')]
        assert found,(path.name,target)
        if sep:
            source=found[0].read_text(encoding='utf-8-sig')
            assert any(re.sub(r'^#+\s*','',line)==anchor for line in source.splitlines()),target
    checks.append(path.name+' structure scores and links')
out='PASS '+str(len(checks))+' checks\n'+'\n'.join(checks)+'\n'
Path(__file__).with_name('verification04.txt').write_text(out,encoding='utf-8')
print(out.encode('ascii','backslashreplace').decode())

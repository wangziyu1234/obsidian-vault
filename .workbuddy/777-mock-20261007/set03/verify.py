from pathlib import Path
import re,json
import sympy as s
root=Path(r"D:\obsidian")
out=root/".workbuddy/777-mock-20261007/set03"
base=root/"控制理论/青岛大学825真题/777改编模拟卷/Markdown笔记"
results=[]
for p in base.glob("03 *.md"):
    text=p.read_text(encoding="utf-8-sig")
    assert len(re.findall(r"^## 第\d+题",text,re.M))==17,p
    assert len(re.findall(r"^# ",text,re.M))==1,p
    assert len(re.findall(r"^\$\$",text,re.M))%2==0,p
    for ref in re.findall(r"\[\[([^\]]+)\]\]",text):
        target=ref.split("|")[0]
        if target=="777改编模拟卷目录": continue
        f,_,h=target.partition("#")
        fp=root/(f+".md")
        assert fp.exists(),ref
        if h:
            headings=re.findall(r"^#{1,6} (.+)$",fp.read_text(encoding="utf-8-sig"),re.M)
            assert h in headings,(ref,headings)
    results.append(str(p.name)+": 17 questions, H1, display delimiters, source anchors passed")
z,k,t,q=s.symbols("z k t q",real=True)
D=z*z+(2-k)*z+k
assert s.expand(D.subs(z,z-s.Rational(1,2))-(z*z+(1-k)*z+3*k/2-s.Rational(3,4)))==0
sigma,w=s.symbols("sigma w",real=True)
circle=s.expand(s.re(D.subs({z:sigma+s.I*w,k:2*sigma+2})))
assert s.expand(circle+(sigma-1)**2+w*w-3)==0
A=s.Matrix([[0,1],[0,-2]])
Phi=s.Matrix([[1,(1-s.exp(-2*t))/2],[0,s.exp(-2*t)]])
assert s.simplify(Phi.diff(t)-A*Phi)==s.zeros(2)
assert Phi.subs(t,0)==s.eye(2)
H=s.Matrix([[1,(1+q)/4],[0,(1-q)/2]])
assert s.simplify(s.integrate(Phi,(t,0,1))-H.subs(q,s.exp(-2)))==s.zeros(2)
u=s.Matrix([(1-3*q)/(2*(1-q)),2/(1-q)])
assert s.simplify(H*u)==s.ones(2,1)
T=s.Matrix([[1,1],[0,1]])
assert T*A*T.inv()==s.Matrix([[0,-1],[0,-2]])
eta=s.Matrix([[3,4]])
assert eta*A==-5*eta+15*s.Matrix([[1,1]])
assert eta*s.Matrix([0,1])==s.Matrix([4])
obsA=s.diag(-1,-2)-s.Matrix([6,-1])*s.Matrix([[1,2]])
assert s.expand((z*s.eye(2)-obsA).det())==z*z+7*z+12
G0=k*(1+2*z)/(z*(1+z)**2*(1+z/4))
Gc=(1+z)**2/((1+2*z)*(1+z/2))
G=k/(z*(1+z/2)*(1+z/4))
assert s.cancel(G0*Gc-G)==0
assert s.simplify(s.Abs(G.subs({z:2*s.I,k:s.sqrt(10)})))==1
relay=k/(z*(z+1)*(z+2))
assert s.simplify(relay.subs(z,s.I*s.sqrt(2)))==-k/6
results.append("symbolic: shifted roots, circle, transition matrix, ZOH integration, one-step input, transformed system, observer error, dual gain, compensator, exact crossover, relay phase passed")
out.mkdir(parents=True,exist_ok=True)
(out/"verification.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
print("\n".join(results))


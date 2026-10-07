from pathlib import Path
import re,json
import sympy as s
root=Path(r"D:\obsidian")
base=root/"控制理论/青岛大学825真题/777改编模拟卷/Markdown笔记"
out=root/".workbuddy/777-mock-20261007/set05"
results=[]
for p in base.glob("05 *.md"):
    text=p.read_text(encoding="utf-8-sig")
    ids=list(map(int,re.findall(r"^## 第(\d+)题",text,re.M)))
    assert all(i in ids for i in range(7,18))
    assert len(ids)==len(set(ids))
    assert len(re.findall(r"^# ",text,re.M))==1
    assert len(re.findall(r"^\$\$",text,re.M))%2==0
    for ref in re.findall(r"\[\[([^\]]+)\]\]",text):
        target=ref.split("|")[0]
        f,_,h=target.partition("#")
        if f=="777改编模拟卷目录": continue
        if "/" in f: fp=root/(f if Path(f).suffix else f+".md")
        else:
            files=list(root.rglob(f if Path(f).suffix else f+".md"))
            assert files,ref
            fp=files[0]
        assert fp.exists(),ref
        if h:
            headings=re.findall(r"^#{1,6} (.+)$",fp.read_text(encoding="utf-8-sig"),re.M)
            assert h in headings,ref
    results.append(f"{p.name}: Q7-Q17, H1, math display parity, links and anchors passed")
z,k,t,d=s.symbols("z k t d",real=True)
A=s.Matrix([[-4,2],[2,-4]])
B=s.Matrix([12,0])
C=s.Matrix([[2,2]])
T=s.Matrix([[1,1],[1,-1]])
assert T*A*T.inv()==s.diag(-2,-6)
assert T*B==s.Matrix([12,12])
assert C*T.inv()==s.Matrix([[2,0]])
assert B.row_join(A*B).rank()==2
assert C.col_join(C*A).rank()==1
assert s.cancel((C*(z*s.eye(2)-A).inv()*B)[0]-24/(z+2))==0
x=s.exp(-6*t)*s.Matrix([1,-1])
assert s.simplify(x.diff(t)-A*x)==s.zeros(2,1)
assert C*x==s.zeros(1,1)
poly=z*(z+4)*(z+6)+k
assert s.expand(poly-(z**3+10*z*z+24*z+k))==0
assert s.expand(poly.subs(z,z-1)-(z**3+7*z**2+7*z+k-15))==0
assert s.expand(poly.subs({z:z-1,k:64})-(z+7)*(z*z+7))==0
assert s.expand(poly.subs({z:z-1,k:15})).subs(z,0)==0
assert (s.Rational(64)-70)/7==-s.Rational(6,7)
assert 70-15==55
P=d*(1+2*d)/((1-d)*(1-d/2))
D=(1-d/2)/(3+2*d)
phi=d/3+2*d*d/3
S=(1-d)*(1+2*d/3)
assert s.cancel(D*P/(1+D*P)-phi)==0
assert s.expand(phi+S)==1
assert s.cancel(D*S-(1-d/2)*(1-d)/3)==0
assert s.cancel(P*S-d*(1+2*d)*(1+2*d/3)/(1-d/2))==0
assert s.limit(phi/(1-d)*(1-d),d,1)==1
assert s.series(phi/(1-d),d,0,4).removeO()==d/3+d*d+d**3
assert s.cancel(-(z+1)**2/z**3-(-1/z-2/z**2-1/z**3))==0
u=-1-2*t-t*t/2
assert s.simplify(s.laplace_transform(u,t,z,noconds=True)+(z+1)**2/z**3)==0
relay=k/(z*(z+1)*(z+2))
assert s.simplify(relay.subs(z,s.I*s.sqrt(2)))==-k/6
assert s.simplify(s.Abs(relay.subs({z:s.I,k:s.pi*s.sqrt(10)/4})))-s.pi/4==0
Ac=s.Matrix([[0,1],[-1,-2]])
Bc=s.Matrix([1,-1])
assert Bc.row_join(Ac*Bc).rank()==1
results.append("Symbolic: coordinate transform, controllability/observability, transfer function, invisible initial response, shifted polynomial and boundary, minimum-time controller identity, internal transfer functions, sampled sequence, op-amp ramp inverse transform, relay harmonics, MATLAB rank passed")
out.mkdir(parents=True,exist_ok=True)
(out/"verification.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
print("PASS: source links and all symbolic assertions")


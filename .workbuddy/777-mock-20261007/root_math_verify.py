import sympy as S
import json
from pathlib import Path
s,t,z,k=S.symbols('s t z k',real=True)
R=S.Rational
checks=[]
def ok(i,c):
    assert c,i
    checks.append(i)
def eq(a,b=0):return S.simplify(a-b)==0

# Each check starts from the problem's physical equation or characteristic model.
ok('01-13',eq((2+(2*S.sqrt(2)-2))/4,1/S.sqrt(2)) and eq(2*S.sqrt(2),2*(S.sqrt(2)/2)*2))
p=s*(s+3)*(s+6)
ok('01-14',eq(-p.subs(s,-3+S.sqrt(3)),6*S.sqrt(3)) and eq(p+162,(s+9)*(s*s+18)) and eq(p+80,(s+8)*(s*s+s+10)))
L=2/(s*(s+1))*(1+s)/(1+s/3)
ok('01-15',eq(L.subs(s,S.I*S.sqrt(3)),R(-1,2)-S.I*S.sqrt(3)/2) and S.limit(s*L,s,0)==2)
n=S.symbols('n',integer=True,nonnegative=True)
c=R(2,3)*(1-(-R(1,2))**n)
ok('01-16',eq(c.subs(n,n+1),1-c/2) and c.subs(n,0)==0 and c.subs(n,1)==1)
y=1-S.exp(-2*t)*(S.cos(2*t)+S.sin(2*t))
ok('01-17',eq(S.diff(y,t,2)+4*S.diff(y,t)+8*y,8) and y.subs(t,0)==0 and S.diff(y,t).subs(t,0)==0)
D=s*(s+1)*(s+3)+2*s*s+9*s+8
ok('02-13',eq(D,(s+2)**3) and eq((s+1)*(s+3)/D,1/(s+2)-1/(s+2)**3))
disc=(1+5*k)**2-24*k*(1+k)
ok('02-14',eq(disc,k*k-14*k+1) and eq((1+5*k)**2/(24*k*(1+k))-R(2,3),(3*k-1)**2/(24*k*(1+k))))
y=1-3*R(1,2)**n+2*R(1,4)**n
ok('02-15',eq(y.subs(n,n+2)-R(3,4)*y.subs(n,n+1)+y/8,R(3,8)) and y.subs(n,0)==0 and y.subs(n,1)==0)
ok('02-16',eq((-2*t)**2+4*(1-t*t),4) and eq(4*S.sqrt(R(2,2)),4))
A=S.Matrix([[-5,-1],[6,0]]);B=S.Matrix([0,2]);C=S.Matrix([[0,1]])
G=(C*(s*S.eye(2)-A).inv()*B)[0]
ystep=R(5,3)-3*S.exp(-2*t)+R(4,3)*S.exp(-3*t)
ok('02-17',eq(G,2*(s+5)/((s+2)*(s+3))) and eq(S.laplace_transform(ystep,t,s,noconds=True),G/s))
D=s*s+(2-k)*s+k
ok('03-13',eq(D.subs(s,z-R(1,2)),z*z+(1-k)*z+R(3,2)*k-R(3,4)))
G=S.sqrt(10)/(s*(1+s/2)*(1+s/4))
ok('03-14',eq(G.subs(s,2*S.I),(-3-S.I)/S.sqrt(10)) and eq(S.expand(s*(1+s/2)*(1+s/4)),s**3/8+3*s*s/4+s))
G=k/(s*(s+1)*(s+2))
ok('03-15',eq(G.subs(s,S.I*S.sqrt(2)),-k/6) and eq(8/(S.pi*2)*(-3*S.pi/2)/6,-1))
pd=1/(2*(z-1));dc=2*(z-R(3,4))/(z-1);phi=S.cancel(pd*dc/(1+pd*dc));y=1+(n-1)/2**n
ok('03-16',eq(phi,(z-R(3,4))/(z-R(1,2))**2) and eq(y.subs(n,n+2)-y.subs(n,n+1)+y/4,R(1,4)) and y.subs(n,0)==0 and y.subs(n,1)==1)
A=S.Matrix([[0,1],[0,-2]]);C=S.Matrix([[1,1]]);Q=S.Matrix([[1,1],[0,1]])
ok('03-17',Q*A*Q.inv()==S.Matrix([[0,-1],[0,-2]]) and (Q*S.Matrix([0,1]))==S.Matrix([1,1]) and -2-(-3)*(-1)==-5)
a,b,c,d,e,f,g,h,i=S.symbols('a b c d e f g h i')
M=S.Matrix([[1,g,0,i],[-c,1,0,0],[-b,-d,1,h],[0,0,-e,1]])
x=M.inv()*S.Matrix([a,0,0,0]);delta=1+c*g+e*h+c*d*e*i+b*e*i+c*g*e*h
ok('04-13',eq(M.det(),delta) and eq(f*x[3],a*e*f*(c*d+b)/delta) and eq(x[1],a*c*(1+e*h)/delta))
ok('04-14',eq(s**3+4*s*s+8*s+32,(s+4)*(s*s+8)) and R(16,32)==R(1,2))
T,K=S.symbols('T K',positive=True);G1=K/(s*(T*s+1));G2=2*K/(s*((T/2)*s+1))
ok('04-15',eq(G2,G1.subs(s,s/2)))
q=S.symbols('q',positive=True);H=S.Matrix([[1,(1+q)/4],[0,(1-q)/2]]);u=S.Matrix([(1-3*q)/(2*(1-q)),2/(1-q)])
ok('04-16',S.simplify(H*u-S.ones(2,1))==S.zeros(2,1) and eq(H.det(),(1-q)/2))
F=S.Matrix([[-7,1],[-3,-3]]);v=S.Matrix([-S.exp(-4*t)/2+3*S.exp(-6*t)/2,-3*S.exp(-4*t)/2+3*S.exp(-6*t)/2])
ok('04-17',S.simplify(v.diff(t)-F*v)==S.zeros(2,1) and v.subs(t,0)==S.Matrix([1,0]))
out=-1-2*t-t*t/2
ok('05-13',eq(S.laplace_transform(out,t,s,noconds=True),-(s+1)**2/s**3))
D=s*(s+4)*(s+6)+k
ok('05-14',eq(D.subs(s,z-1),z**3+7*z*z+7*z+k-15) and eq(D.subs({s:z-1,k:64}),(z+7)*(z*z+7)))
delay=S.pi/4-S.atan(R(1,2));G=(S.pi*S.sqrt(10)/4)/(s*(s+1)*(s+2))
ok('05-15',abs(complex((4/S.pi)*G.subs(s,S.I)*S.exp(-S.I*delay))+1)<1e-12)
P=(z+2)/((z-1)*(z-R(1,2)));phi=(z+2)/(3*z*z);dc=(1-R(1,2)/z)/(3+2/z)
ok('05-16',eq(P*dc/(1+P*dc),phi) and eq(phi.subs(z,1),1) and eq(phi/P,(z-1)*(z-R(1,2))/(3*z*z)))
A=S.Matrix([[-4,2],[2,-4]]);B=S.Matrix([12,0]);C=S.Matrix([[2,2]]);Q=S.Matrix([[1,1],[1,-1]])
ok('05-17',Q*A*Q.inv()==S.diag(-2,-6) and eq((C*(s*S.eye(2)-A).inv()*B)[0],24/(s+2)) and C*S.Matrix([1,-1])==S.zeros(1,1))
Path(__file__).with_suffix('.json').write_text(json.dumps({'passed':checks,'count':len(checks)},indent=2),encoding='utf8')
print('ROOT_COMPREHENSIVE_CHECKS='+str(len(checks)))

import sympy as S
M=S.Matrix;s,t,a,b,c=S.symbols('s t a b c');k1,k2,k3=S.symbols('k1 k2 k3')
checks=[]
def eq(tag,l,r):
    d=S.simplify(l-r)
    assert d==(S.zeros(*d.shape) if isinstance(d,S.MatrixBase) else 0),(tag,d)
    checks.append(tag)
def char(A):return (s*S.eye(A.rows)-A).det()
def gain(A,B,C,K,poly,sgn=-1,tf=None):
    eq(str(len(checks))+' poles',char(A+sgn*B*K),poly)
    if tf is not None:eq(str(len(checks))+' transfer',(C*(s*S.eye(A.rows)-A-sgn*B*K).inv()*B)[0],tf)
gain(M([[0,1],[2,-1]]),M([0,1]),M([[3,1]]),M([[5,3]]),(s+1)*(s+3),tf=1/(s+1))
gain(M([[0,1,0],[0,0,1],[-6,-11,-6]]),M([0,0,1]),M([[10,0,0]]),M([[154,45,8]]),(s+10)*(s*s+4*s+16))
A=M([[0,1,0],[0,-a,c],[0,0,-b]]);B=M([0,1,1]);C=M([[1,0,0]])
eq('3-3 controllability',M.hstack(B,A*B,A*A*B).det(),(b+c)*(a-b-c))
eq('3-3 model',(C*(s*S.eye(3)-A).inv()*B)[0],(s+b+c)/(s*(s+a)*(s+b)))
gain(M([[0,1,0],[0,0,1],[6,5,-2]]),M([0,0,1]),M([[-2,1,1]]),M([[18,21,5]]),(s+2)**2*(s+3),tf=(s-1)/((s+2)*(s+3)))
A=M([[0,1],[-k1,-k2]]);D=M([1,-2]);C=M([[6,3]])
eq('3-5 disturbance',(C*(s*S.eye(2)-A).inv()*D)[0],(6*k2-3*k1-12)/(s*s+k2*s+k1))
A=M([[-2,1,0],[0,-2,1],[0,0,-2]]);B=M([0,0,1]);C=M([[1,0,0]])
eq('3-6 response',(C*(A*t).exp()*M([1,0,1]))[0],S.exp(-2*t)*(1+t*t/2))
gain(A,B,C,M([[6,-4,1]]),(s+5)*(s*s+2*s+2))
gain(M([[0,1,0],[0,0,1],[0,2,0]]),B,M([[1,1,0]]),M([[5,11,5]]),(s+1)*(s*s+4*s+5),tf=1/(s*s+4*s+5))
A=M([[-2,0,0],[0,1,1],[0,0,1]]);B=M([[1,0],[1,0],[0,1]]);C=M([[0,1,0]])
eq('3-8 rank',S.Integer(M.hstack(B,A*B,A*A*B).rank()),3)
eq('3-8 output feedback',char(A+B*M([-4,-5])*C),(s+2)*(s*s+2*s+2))
gain(M([[0,1,0],[0,0,1],[0,-2,-3]]),M([0,0,1]),M([[10,0,0]]),M([[-4,-4,-1]]),(s+2)*(s*s+2*s+2),1)
A=M([[0,0],[1,-4]]);B=M([1,2]);C=M([[0,1]])
xt=M([t+4,S.Rational(23,16)+t/4-S.Rational(7,16)*S.exp(-4*t)])
eq('3-10 ODE',xt.diff(t),A*xt+B);eq('3-10 initial',xt.subs(t,0),M([4,1]))
gain(A,B,C,M([[S.Rational(1,2),-1]]),(s+2)*(s+S.Rational(1,2)),tf=2/(s+2))
A=S.diag(M([[-2,1],[0,-2]]),M([[1,1,0],[0,1,1],[0,0,1]]));B=M([1,0,0,1,1])
eq('3-11 rank',S.Integer(M.hstack(*[A**i*B for i in range(5)]).rank()),4)
eq('3-11 feedback',char(A-B*M([[0,k2,12,4,3]])),(s+1)**2*(s+2)**3)
for tag,A,C,H,target in [
('3-12',M([[0,0,0],[1,0,-4],[0,1,-3]]),M([[0,0,1]]),M([27,23,6]),(s+3)**3),
('3-13',M([[1,1],[0,-2]]),M([[2,1]]),M([11,-12]),(s+5)*(s+6)),
('3-14',M([[-2,1],[0,-1]]),M([[1,0]]),M([3,4]),(s+3)**2),
('3-15',M([[0,1],[0,-5]]),M([[1,0]]),M([95,2025]),(s+50)**2),
('3-17',M([[0,1],[-5,-6]]),M([[1,0]]),M([-3,15]),(s+1)*(s+2)),
('3-18',M([[0,1],[-2,3]]),M([[2,0]]),M([S.Rational(23,2),S.Rational(167,2)]),(s+10)**2),
('3-19',M([[0,1],[0,-1]]),M([[1,0]]),M([19,81]),(s+10)**2),
('3-20',M([[-1,1],[-2,-4]]),M([[1,0]]),M([13,22]),(s+8)*(s+10)),
('3-21',M([[-5,-1],[6,0]]),M([[0,1]]),M([S.Rational(119,6),15]),s*s+20*s+200),
('3-22',M([[0,1,0],[0,0,1],[2,-5,4]]),M([[0,0,1]]),M([13,4,10]),(s+1)*(s+2)*(s+3))
]:eq(tag+' observer',char(A-H*C),target)
gain(M([[1,1],[0,-2]]),M([1,1]),M([[2,1]]),M([[-S.Rational(13,4),S.Rational(1,4)]]),s*s+4*s+8,1)
gain(M([[0,1],[0,-5]]),M([0,100]),M([[1,0]]),M([[a*a/50,(2*a-5)/100]]),s*s+2*a*s+2*a*a)
A=M([[a+3,0],[3,a-2]]);C=M([[1,0]]);eq('3-16 tf',(C*(s*S.eye(2)-A).inv()*M([1,1]))[0],1/(s-a-3))
gain(M([[0,1],[-5,-6]]),M([0,1]),M([[1,0]]),M([[-43,-8]]),(s+6)*(s+8),1)
A=M([[0,1],[-2,3]]);B=M([0,1]);C=M([[2,0]]);H=M([S.Rational(23,2),S.Rational(167,2)]);K=M([[-6,-7]])
P=M([[-S.Rational(5,4),S.Rational(1,4)],[S.Rational(1,4),-S.Rational(1,4)]])
eq('3-18 Lyapunov',A.T*P+P*A,-S.eye(2))
F=A.row_join(B*K).col_join((H*C).row_join(A-H*C+B*K))
eq('3-18 augmented',F,M([[0,1,0,0],[-2,3,-6,-7],[23,0,-23,1],[167,0,-175,-4]]))
eq('3-18 separation',char(F),(s*s+4*s+8)*(s+10)**2)
gain(M([[-1,1],[-2,-4]]),B,M([[1,0]]),M([[10,4]]),(s+4)*(s+5))
gain(M([[-5,-1],[6,0]]),M([0,2]),M([[0,1]]),M([[-S.Rational(19,2),S.Rational(5,2)]]),s*s+10*s+50)
gain(M([[0,1,0],[0,0,1],[2,-5,4]]),M([0,0,1]),M([[0,0,1]]),M([[4,0,8]]),(s+1)**2*(s+2),tf=s*s/((s+1)**2*(s+2)))
A=M([[0,0,0],[1,0,-2],[0,1,-3]]);B=M([1,0,0]);G=M([36,12]);F=A[:2,:2]-G*A[2:,:2]
eq('3-23 reduced',F,M([[0,-36],[1,-12]]));eq('3-23 injection',F*G+A[:2,2:]-G*A[2,2],M([-324,-74]))
gain(A,B,M([[0,0,1]]),M([[-3,1,-5]]),(s+4)*(s*s+2*s+2),1)
A=M([[0,1,0],[0,0,1],[0,-2,-3]]);B=M([0,0,1]);T=M([[0,0,1],[0,1,0],[1,0,0]]);G=M([2,7]);Ab=T.inv()*A*T
eq('3-24 transformed input',T.inv()*B,M([1,0,0]))
F=Ab[:2,:2]-G*Ab[2:,:2];eq('3-24 reduced poles',char(F),(s+5)**2);eq('3-24 injection',F*G+Ab[:2,2:]-G*Ab[2,2],M([-34,-47]))
gain(A,B,M([[1,0,0]]),M([[3,2,1]]),s**3+4*s*s+4*s+3,tf=1/(s**3+4*s*s+4*s+3))
A=S.diag(1,-1,0);B=M([1,1,0]);C=M([[1,1,0]])
eq('3-31 first moment',(C*A*B)[0],0);eq('3-31 last moment',(C*A*A*B)[0],2);eq('3-31 rank',S.Integer(M.hstack(B,A*B,A*A*B).rank()),2)
A=S.diag(-S.Rational(1,2),-1);B=S.diag(S.Rational(1,2),1);C=M([[1,1],[2,1]]);F=M([[-2,2],[2,-1]])
eq('3-32 decoupled state',A+B, S.zeros(2));eq('3-32 decoupled input',C*B*F,S.eye(2))
A=M([[0,5],[2,-1]]);B=M([1,0]);C=M([[1,0]]);P=M([[S.Rational(1,4),-S.Rational(1,4)],[-S.Rational(1,4),-S.Rational(3,4)]])
eq('3-33 Lyapunov',A.T*P+P*A,-S.eye(2));gain(A,B,C,M([[5,S.Rational(13,2)]]),(s+2)*(s+4),tf=(s+1)/((s+2)*(s+4)))
print('Passed',len(checks),'independent exact checks for topic 3')

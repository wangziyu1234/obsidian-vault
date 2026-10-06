import sympy as S
s,t,T,a,b,c,k1,k2=S.symbols('s t T a b c k1 k2', real=True)
M=S.Matrix
def qc(A,B): return M.hstack(*[A**i*B for i in range(A.rows)])
def qo(A,C): return M.vstack(*[C*A**i for i in range(A.rows)])
def tf(A,B,C,D=None):
    return S.simplify(C*(s*S.eye(A.rows)-A).inv()*B+(S.zeros(C.rows,B.cols) if D is None else D))
def chk(label,actual,expected):
    assert S.simplify(actual-expected)==S.zeros(*actual.shape) if isinstance(actual,S.MatrixBase) else S.simplify(actual-expected)==0, (label,actual,expected)
    print(label,'OK')
def companion(den):
    co=S.Poly(den,s).all_coeffs(); n=len(co)-1; A=S.zeros(n)
    for i in range(n-1): A[i,i+1]=1
    A[n-1,:]=M([[-x for x in co[:0:-1]]]); B=S.zeros(n,1);B[n-1]=1
    return A,B
A=M([[2,0,-1],[0,-2,0],[-1,0,1]]);B=M([0,0,1]);chk('3-1 Q',qc(A,B),M([[0,-1,-3],[0,0,0],[1,1,2]]));chk('3-1 char',(s*S.eye(3)-A).det(),(s+2)*(s*s-3*s+1))
A=M([[-1,0],[-3,-S.Rational(3,2)]]);chk('3-2 Qc',qc(A,M([2,2*b])).det(),-2*(b+6));chk('3-2 Qo',qo(A,M([[1,2*c]])).det(),c*(12*c-1))
A,B=companion((s+1)*(s+2)*(s+3));chk('3-3 Qo',qo(A,M([[b,1,0]])).det(),(b-1)*(b-2)*(b-3))
A=M([[0,1],[0,0]]);chk('3-4 Qo',qo(A,M([[k1,k2]])).det(),k1*k1)
A=M([[0,1],[-3,-2]]);print('3-5 ranks',qc(A,M([0,1])).rank(),qo(A,M([[1,0]])).rank());chk('3-5 factor',s**4+10*s**3+35*s*s+50*s+24,(s+1)*(s+2)*(s+3)*(s+4))
A=M([[0,1],[-1,-2]]);B=M([1,-1]);print('3-6 ranks',qc(A,B).rank(),(M([[1,0]])*qc(A,B)).rank())
A=M([[-3,1],[1,-3]]);B=M([[1,1],[1,1]]);C=M([[1,1],[1,-1]]);P=M([[1,1],[1,-1]]);chk('3-7 diag',P.inv()*A*P,S.diag(-2,-4));print('3-7 ranks',qc(A,B).rank(),qo(A,C).rank())
A=M([[-1,1,0,0],[0,-1,0,0],[0,0,-2,0],[0,0,0,-3]]); print('3-8 missing b3 rank',qc(A,M([1,1,0,1])).rank()); print('3-8 c1=0, c1=c2=0 ranks',qo(A,M([[0,1,1,1]])).rank(),qo(A,M([[0,0,1,1]])).rank())
G=M([[S.cos(T),S.sin(T)],[-S.sin(T),S.cos(T)]]);H=M([1-S.cos(T),S.sin(T)]);chk('3-9 Qc',S.trigsimp(qc(G,H).det()),2*S.sin(T)*(S.cos(T)-1));chk('3-9 Qo',qo(G,M([[1,0]])).det(),S.sin(T))
A=M([[0,4],[-4,0]]);B=M([0,4]);Phi=M([[S.cos(4*t),S.sin(4*t)],[-S.sin(4*t),S.cos(4*t)]]);chk('3-10 derivative',Phi.diff(t),A*Phi);chk('3-10 H',S.integrate(Phi*B,(t,0,T)),M([1-S.cos(4*T),S.sin(4*T)]))
A=M([[0,1,0],[0,0,1],[0,3,2]]);P=M([[1,1,1],[0,3,-1],[0,9,1]]);chk('3-12 diag',P.inv()*A*P,S.diag(0,3,-1)); F=M([[1,S.Rational(2,3)+S.exp(3*t)/12-3*S.exp(-t)/4,-S.Rational(1,3)+S.exp(3*t)/12+S.exp(-t)/4],[0,S.exp(3*t)/4+3*S.exp(-t)/4,(S.exp(3*t)-S.exp(-t))/4],[0,3*(S.exp(3*t)-S.exp(-t))/4,3*S.exp(3*t)/4+S.exp(-t)/4]]);chk('3-12 Phi',F,P*S.diag(1,S.exp(3*t),S.exp(-t))*P.inv())
A,B=companion(s**3+3*s*s+2*s+1);chk('3-13 tf',tf(A,B,M([[1,1,0]]))[0],(s+1)/(s**3+3*s*s+2*s+1));print('3-13 detQo',qo(A,M([[1,1,0]])).det())
A=M([[-2,2,-1],[0,-2,0],[1,-4,0]]);B=M([0,1,0]);C=M([[2,1,1]]);W=(s*s+2*s+3)/(s**3+4*s*s+5*s+2);chk('3-14 original tf',tf(A,B,C)[0],W);A1,B1=companion(s**3+4*s*s+5*s+2);chk('3-14 type1 tf',tf(A1,B1,M([[3,2,1]]))[0],W);chk('3-14 type2 tf',tf(A1.T,M([1,0,0]),M([[1,-2,6]]))[0],W)
A,B=companion((s+1)*(s+2)*(s+3));chk('3-15 tf',tf(A,B,M([[25,25,6]]))[0],(6*s*s+25*s+25)/((s+1)*(s+2)*(s+3)))
A,B=companion((s+1)*(s+3)*(s+6));chk('3-16 detQo',qo(A,M([[a,1,0]])).det(),(a-1)*(a-3)*(a-6));chk('3-16 partial',tf(S.diag(-1,-3,-6),S.ones(3,1),M([[(a-1)/10,(3-a)/6,(a-6)/15]]))[0],(s+a)/((s+1)*(s+3)*(s+6)))
A,B=companion(s**3+2*s*s+5*s+3);C=M([[1,2,1]]);chk('3-17 tf',tf(A,B,C)[0],(s*s+2*s+1)/(s**3+2*s*s+5*s+3));chk('3-17 dual',tf(A.T,C.T,B.T),tf(A,B,C))
A=M([[-1,0,0],[0,0,1],[0,-6,-5]]);B=M([[1,0],[0,0],[0,1]]);C=M([[1,2,1],[5,-27,-9]]);D=S.diag(1,5);W=M([[(s+2)/(s+1),1/(s+3)],[5/(s+1),(5*s+1)/(s+2)]]);chk('3-18 min tf',tf(A,B,C,D),W);print('3-18 min ranks',qc(A,B).rank(),qo(A,C).rank());A=M([[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1],[-6,0,-11,0,-6,0],[0,-6,0,-11,0,-6]]);B=M([[0,0],[0,0],[0,0],[0,0],[1,0],[0,1]]);C=M([[6,2,5,3,1,1],[30,-27,25,-36,5,-9]]);chk('3-18 sixth tf',tf(A,B,C,D),W);print('3-18 sixth ranks',qc(A,B).rank(),qo(A,C).rank())
A=M([[-4,2],[2,-4]]);Rinv=M([[2,2],[0,1]]);chk('3-19 decompA',Rinv*A*Rinv.inv(),M([[-2,0],[1,-6]]));chk('3-19 decompB',Rinv*M([12,0]),M([24,0]));chk('3-19 decompC',M([[2,2]])*Rinv.inv(),M([[1,0]]))
A=M([[0,0,1],[1,0,3],[0,1,1]]);B=M([1,1,0]);R=M([[1,0,0],[1,1,0],[0,1,1]]);chk('3-20 decompA',R.inv()*A*R,M([[0,1,1],[1,2,2],[0,0,-1]]));chk('3-20 decompB',R.inv()*B,M([1,0,0]));print('3-20 ranks',qc(A,B).rank())
F=M([[S.exp(t),-S.exp(t)+S.exp(4*t),2*t*S.exp(4*t)],[0,S.exp(4*t),2*t*S.exp(4*t)],[0,0,S.exp(4*t)]]);A=M([[1,3,2],[0,4,2],[0,0,4]]);chk('3-21 Phi',F.diff(t),A*F);A=M([[1,3,0],[0,4,0],[0,2,4]]);Rinv=M([[1,0,0],[1,3,0],[0,0,1]]);chk('3-21 decompA',Rinv*A*Rinv.inv(),M([[0,1,0],[-4,5,0],[-S.Rational(2,3),S.Rational(2,3),4]]));chk('3-21 decompB',Rinv*M([0,1,2]),M([0,3,2]));print('3-21 rankQo',qo(A,M([[1,0,0]])).rank())
A,B=companion(s**3-4*s*s-s+2);C=M([[-2,1,0]]);chk('3-22 tf',tf(A,B,C)[0],(s-2)/(s**3-4*s*s-s+2));print('3-22 dets',qc(A,B).det(),qo(A,C).det(), 'den_at_2',(s**3-4*s*s-s+2).subs(s,2))
A,B=companion((s+1)*(s+2));chk('3-23 min tf',tf(A,B,M([[3,1]]))[0],(s+3)/((s+1)*(s+2)));A,B=companion((s+1)**2*(s+2));C=M([[3,4,1]]);print('3-23 ranks',qc(A,B).rank(),qo(A,C).rank());chk('3-23 Qo',qo(A,C),M([[3,4,1],[-2,-2,0],[0,-2,-2]]))
chk('3-24 cancellation',(s*s+5*s+6)/((s+1)*(s+2)*(s+3)),1/(s+1))
A,B=companion((s+1)*(s+2)*(s-1));C=M([[1,1,0]]);chk('3-25 Qo',qo(A,C),M([[1,1,0],[0,1,1],[2,1,-1]]));print('3-25 ranks',qc(A,B).rank(),qo(A,C).rank())
A,B=companion((s+1)*(s+2)*(s+3));C=M([[9,6,1],[2,3,1]]);chk('3-26 tf',tf(A,B,C,M([0,1])),M([[(s+3)/((s+1)*(s+2))],[(s+4)/(s+3)]]))
R=S.Rational;A=M([[0,0,1,0],[0,0,0,1],[R(1,100),0,0,0],[0,R(1,100),0,0]]);B=M([[0,0],[0,0],[1,0],[0,1]]);C=M([[R(101,1000),-R(1,100),-R(101,100),R(1,10)],[R(1,100),-R(99,1000),R(1,10),R(99,100)]]);D=M([[R(1,10),0],[1,R(1,10)]]);W=M([[(s-10)/(10*s+1),1/(10*s+1)],[10*s/(10*s-1),(s+10)/(10*s+1)]]);chk('3-27 controllable',tf(A,B,C,D),W);Bo=M.vstack(C[:,:2],C[:,2:]);chk('3-27 observable',tf(A.T,Bo,B.T,D),W);A=S.diag(-R(1,10),-R(1,10),R(1,10));B=M([[R(1,10),0],[0,R(1,10)],[R(1,10),0]]);C=M([[-R(101,10),1,0],[0,R(99,10),1]]);chk('3-27 minimal',tf(A,B,C,D),W);print('3-27 minimal ranks',qc(A,B).rank(),qo(A,C).rank())

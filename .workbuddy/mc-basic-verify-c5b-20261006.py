import sympy as S
M=S.Matrix;R=S.Rational
s,t,a,b,w=S.symbols('s t a b w',real=True)
count=0
def eq(x,y):
 global count
 d=x-y
 assert all(S.simplify(v)==0 for v in d) if isinstance(d,S.MatrixBase) else S.simplify(d)==0
 count+=1
def obs(A,C,L,f):
 eq((s*S.eye(A.rows)-A+L*C).det(),f)
 return A-L*C
G=M([[0,1],[a,-1]]);H=M([-2*b,b]);eq((s*S.eye(2)-G).det(),s*s+s-a);eq(H.row_join(G*H).det(),b*b*(4*a+1));eq((S.eye(2)-G).det(),2-a)
A=M([[0,1],[-2,-3]]);C=M([[2,0]])
eq(obs(A,C,M([R(17,2),R(47,2)]),(s+10)**2),M([[-17,1],[-49,-3]]))
eq(obs(S.diag(-1,-2),M([[1,2]]),M([4,-R(1,2)]),(s+3)**2),M([[-5,-8],[R(1,2),-1]]))
A=M([[1,2,0],[3,-1,1],[0,2,0]]);C=M([[0,0,1]]);B=M([2,1,1])
eq((C*(s*S.eye(3)-A).inv()*B)[0],(s*s+2*s+3)/(s**3-9*s+2));obs(A,C,M([52,42,15]),(s+5)**3)
obs(M([[0,1],[-2,-3]]),M([[2,0]]),M([R(1,2),0]),(s+2)**2+1)
A=M([[-5,-1],[6,0]]);B=M([0,2]);C=M([[0,1]])
obs(A,C,M([R(119,6),15]),(s+10)**2+100);eq((s*S.eye(2)-A-B*M([[R(19,2),-R(5,2)]])).det(),(s+5)**2+25)
A=M([[0,1,0],[0,0,1],[0,-6,-5]]);B=M([0,0,1]);C=M([[1,0,0]])
obs(A,C,M([4,1,-2]),(s+3)**3);eq((s*S.eye(3)-A-B*M([[-108,-48,-7]])).det(),(s+6)*((s+3)**2+9))
A=M([[0,1,0,0],[-12,-R(1,50),12,0],[0,0,0,1],[120,0,-120,-R(1,5)]]);B=M([0,0,0,20]);C=M([[1,0,0,0]])
eq(B.row_join(A*B).row_join(A*A*B).row_join(A**3*B),M([[0,0,0,240],[0,0,240,-R(264,5)],[0,20,-4,-R(11996,5)],[20,-4,-R(11996,5),R(23996,25)]]));eq(M.vstack(C,C*A,C*A*A,C*A**3).rank(),4)
obs(S.diag(-1,1),M([[3,2]]),M([-R(1,3),3]),(s+2)*(s+3))
A=M([[0,1,0,0],[3*w*w,0,0,2*w],[0,0,0,1],[0,-2*w,0,0]]);C=M([[0,0,1,0]])
obs(A,C,M([-R(89,2)*w,-R(115,2)*w*w,11*w,53*w*w]),(s+2*w)*(s+3*w)*((s+3*w)**2+9*w*w))
x1,x2,u,ww=S.symbols('x1 x2 u ww');eq((-5*x2+100*u)-5*x2,(-10*ww-50*x1+100*u).subs(ww,x2-5*x1))
F=M([[2,-10],[1,-4]]);eq((s*S.eye(2)-F).det(),(s+1)**2+1);eq(F*M([10,7])+M([1,0])+3*M([10,7]),M([-19,3]))
F=M([[0,-5],[2,-7]]);eq((s*S.eye(2)-F).det(),(s+2)*(s+5));eq(F*M([3,4])+M([0,3]),M([-20,-19]))
A=M([[-4,1],[0,-4]]);B=M([0,1]);C=M([[1,0]])
eq((s*S.eye(2)-A+B*M([[26,2]])).det(),(s+5)**2+25);obs(A,C,M([1,0]),(s+4)*(s+5))
eq((S.exp(A*t)*M([1,1])+S.integrate(S.exp(A*s)*B,(s,0,t)))[0],R(1,16)+S.exp(-4*t)*(R(15,16)+R(3,4)*t))
A=M([[0,1],[2,-1]]);eq((s*S.eye(2)-A+B*M([[7,1]])).det(),(s+1)**2+4);obs(A,C,M([8,14]),(s+4)*(s+5))
A=M([[0,1],[0,1]]);K=M([[2,3]]);L=M([8,20]);obs(A,C,L,(s+3)*(s+4));eq((s*S.eye(2)-A+B*K).det(),s*s+2*s+2)
F=(A.row_join(-B*K)).col_join((L*C).row_join(A-L*C-B*K));V=B.col_join(B);O=C.row_join(S.zeros(1,2))
eq((O*(s*S.eye(4)-F).inv()*V)[0],1/(s*s+2*s+2))
P=(S.eye(2).row_join(S.zeros(2))).col_join(S.eye(2).row_join(-S.eye(2)))
eq(P*V,B.col_join(S.zeros(2,1)));eq(P*F*P,(A-B*K).row_join(B*K).col_join(S.zeros(2).row_join(A-L*C)))
print('PASS',count,'independent exact checks for chapter 5 second half')

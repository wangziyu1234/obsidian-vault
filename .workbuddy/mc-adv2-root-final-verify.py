import sympy as s
M=s.Matrix; R=s.Rational
t,a,l=s.symbols('t a l', real=True)
A=M([[-2,3],[1,0]]); b=M([1,1]); x=M([s.exp(t)/2+3*s.exp(-3*t)/2-1,s.exp(t)/2-s.exp(-3*t)/2-1])
assert s.simplify(x.diff(t)-A*x-b)==s.zeros(2,1)
assert x.subs(t,0)==M([1,-1])
A=M([[l,0,0],[0,l,1],[0,0,l]])
assert (A-l*s.eye(3))**2==s.zeros(3)
A=M([[0,1,0],[0,0,1],[1,0,1]]);b=M([0,0,1])
assert M.hstack(b,A*b,A*A*b)==M([[0,0,1],[0,1,1],[1,1,1]])
A=M([[1,3,2],[0,2,0],[0,1,3]])
assert A*M([1,0,1])==3*M([1,0,1])
A=s.diag((-3+s.sqrt(5))/2,(-3-s.sqrt(5))/2);b=M([1,1]);c=M([[1/s.sqrt(5),-1/s.sqrt(5)]])
assert s.simplify((c*(l*s.eye(2)-A).inv()*b)[0]-1/(l*l+3*l+1))==0
assert s.simplify(M.hstack(b,A*b).det())==-s.sqrt(5)
assert s.simplify(M.vstack(c,c*A).det())==1/s.sqrt(5)
A=M([[0,1],[-2,-3]]);b=M([0,1]);c=M([[1,a]]);T=M([[3-2*a,1],[1,a]])
assert T*A==M([[0,-2],[1,-3]])*T
assert T*b==M([1,a]) and M([[0,1]])*T==c
assert s.expand(T.det()+(a-1)*(2*a-1))==0
P=M([[R(5,4),R(1,4)],[R(1,4),R(1,4)]])
assert A.T*P+P*A==-s.eye(2)
A=M([[0,0,-1],[1,0,-3],[0,1,-3]]);b=M([1,1,0]);c=M([[0,1,-2]])
Ti=M([[1,0,0],[1,1,0],[0,1,1]]);T=Ti.inv()
assert T==M([[1,0,0],[-1,1,0],[1,-1,1]])
assert T*A*Ti==M([[0,-1,-1],[1,-2,-2],[0,0,-1]]) and T*b==M([1,0,0])
assert c*A*A==-c-2*c*A==M([[-2,3,-4]])
G=M([[R(4,5),1],[0,R(9,10)]]);P=M([[R(25,9),R(500,63)],[R(500,63),R(113800,1197)]])
assert G.T*P*G-P==-s.eye(2) and P.det()>0
print('2-17 determinant',P.det())
x1,x2=s.symbols('x1 x2');f=M([x1+x2-4*s.sin(x2),3*x1-s.exp(x1)+3*x2+2])
assert f.subs({x1:0,x2:0})==M([0,1])
J=f.jacobian([x1,x2]).subs({x1:0,x2:0});assert (l*s.eye(2)-J).det().expand()==l*l-4*l+9
A=M([[-1,0],[1,-2]]);b=M([1,0]);P=M([[R(7,12),R(1,12)],[R(1,12),R(1,4)]])
assert A.T*P+P*A==-s.eye(2) and P.det()==R(5,36)
assert A-b*M([[-1,2]])==M([[0,-2],[1,-2]])
V=x1**4+2*x2**2;f=M([x2,-x1**3-x2])
assert s.expand(s.diff(V,x1)*f[0]+s.diff(V,x2)*f[1])==-4*x2*x2
G=M([[0,R(1,2)],[R(1,2),0]]);assert (s.eye(2)-G).det()==R(3,4)
P=R(4,3)*s.eye(2);assert G.T*P*G-P==-s.eye(2)
assert s.cancel((l-1)/(l**3-l))==1/(l*l+l)
print('All reported topic 2 corrections independently verified.')

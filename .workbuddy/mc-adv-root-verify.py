import sympy as S
M=S.Matrix
s,t,q=S.symbols('s t q',real=True)
# adv1-23: exact original decimal poles.
A=M([[0,0,5],[1,0,1],[0,1,-3]]); C=M([[0,0,1]])
h=M([S.Rational('5.990888'),S.Rational('2.9892'),S.Rational('-1.99')])
want=(s+S.Rational('0.57'))*((s+S.Rational('0.22'))**2+S.Rational('1.3')**2)
assert S.expand((s*S.eye(3)-A+h*C).det()-want)==0
print('1-23',S.expand(want))
# adv1-25: observer and feedback augmented plant.
A=M([[2,1],[0,-3]]);b=M([1,0]);c=M([[1,1]]);k=M([[-3,-4]])
h1,h2=S.symbols('h1 h2'); h=M([h1,h2])
obs=S.solve(S.Poly((s*S.eye(2)-A+h*c).det()-(s+4)*(s+5),s).coeffs(),[h1,h2]);h=h.subs(obs)
F=A.row_join(b*k).col_join((h*c).row_join(A+b*k-h*c));B=b.col_join(b);C=c.row_join(S.zeros(1,2))
Qc=M.hstack(*[F**i*B for i in range(4)]);Qo=M.vstack(*[C*F**i for i in range(4)])
assert S.simplify((C*(s*S.eye(4)-F).inv()*B)[0]-1/(s+1))==0
assert (Qc.rank(),Qo.rank())==(1,4)
print('1-25 h',h.T,'eigen',F.eigenvals(),'ranks',Qc.rank(),Qo.rank())
for v in [-1,-3,-4,-5]:print('1-25 PBH',v,(v*S.eye(4)-F).row_join(B).rank(),(v*S.eye(4)-F).col_join(C).rank())
# adv1-28 Jordan chain.
A=M([[-2,2,-1],[0,-2,0],[1,4,0]]);B=M([0,0,1]);C=M([[1,0,0]])
P=M.hstack(M([-1,0,1]),M([1,0,0]),M([-4,S.Rational(1,2),1]));J=M([[-1,1,0],[0,-1,0],[0,0,-2]])
assert A*P==P*J
assert P.inv()*B==M([1,1,0])
assert C*P==M([[-1,1,-4]])
print('1-28 detP',P.det(),'J',J)
# adv1-30/31 exact ZOH input.
A=M([[-3,-2],[1,0]]);B=M([0,1]);Phi=A.exp() if False else (A*t).exp()
H=S.integrate(Phi*B,(t,0,S.Rational(1,10)))
target=M([-(1-S.exp(-S.Rational(1,10)))**2,(3-4*S.exp(-S.Rational(1,10))+S.exp(-S.Rational(1,5)))/2])
assert S.simplify(H-target)==S.zeros(2,1)
print('1-30/31 Phi',Phi,'H correct')
# adv3-31 missing i=0 counterexample.
A=S.diag(1,-1,0);b=M([1,1,0]);c=M([[1,1,0]])
assert (c*A*b)[0]==0 and (c*A*A*b)[0]==2
assert M.hstack(b,A*b,A*A*b).rank()==2 and M.vstack(c,c*A,c*A*A).rank()==2
print('3-31 counterexample confirmed')

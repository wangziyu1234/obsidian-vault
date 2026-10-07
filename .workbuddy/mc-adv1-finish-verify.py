import sympy as s
M=s.Matrix
l,a,b,c,t=s.symbols('l a b c t',real=True)
A=M([[0,0,5],[1,0,1],[0,1,-3]]);C=M([[0,0,1]])
h=M([5+a*(b*b+c*c),1+b*b+c*c+2*a*b,a+2*b-3])
assert s.expand((l*s.eye(3)-A+h*C).det()-(l+a)*((l+b)**2+c*c))==0
p=l**3+2*l*l+4*l-1
assert p.subs(l,0)<0 and p.subs(l,1)>0 and p.subs(l,-1)!=0
A=M([[-5,-1],[6,0]]);B=M([0,2]);C=M([[0,1]])
assert M.hstack(B,A*B).det()==4
assert M.vstack(C,C*A).det()==-6
x=(A*t).exp()*M([0,3])
assert s.simplify((C*x)[0]-(9*s.exp(-2*t)-6*s.exp(-3*t)))==0
A=M([[-3,-2],[1,0]]);B=M([0,1]);T=s.symbols('T',positive=True);q=s.exp(-T)
H=s.integrate((A*t).exp()*B,(t,0,T))
assert s.simplify(H-M([-(1-q)**2,(3-4*q+q*q)/2]))==s.zeros(2,1)
print('PASS: symbolic observer gain, unstable pole existence, controllability/observability and response, exact ZOH')

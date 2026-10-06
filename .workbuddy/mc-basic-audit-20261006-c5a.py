import sympy as S

M = S.Matrix
s, k1, k2, k3, k4, a, b, h1, h2, F = S.symbols('s k1 k2 k3 k4 a b h1 h2 F', real=True)
checks = 0

def eq(x, y):
    global checks
    if isinstance(x, S.MatrixBase):
        assert (x-y).applyfunc(S.simplify) == S.zeros(*x.shape), (x, y)
    else:
        assert S.simplify(x-y) == 0, (x, y)
    checks += 1

def cp(A):
    return A.charpoly(s).as_expr().subs({S.Symbol('s'): s})

def tf(A, B, C):
    return S.factor((C*(s*S.eye(A.rows)-A).inv()*B)[0])

def qc(A, B):
    return M.hstack(*[A**i*B for i in range(A.rows)])

# 5-1
A=M([[-2,1],[0,-1]]); B=M([1,0]); K=M([[k1,k2]])
eq(qc(A,B),M([[1,-2],[0,0]])); eq(cp(A-B*K),(s+2+k1)*(s+1))
# 5-2
A=M([[0,1,0],[0,0,1],[0,-10,-7]]); B=M([0,0,1])
eq(tf(A,B,M([[10,0,0]])),10/(s*(s+5)*(s+2)))
eq(cp(A+B*M([[-10,-2,0]])),(s+5)*((s+1)**2+1))
eq(cp(A+B*M([[0,-2,-10]])),s**3+17*s**2+12*s)
# 5-3
A=M([[2,1,-1],[0,-1,0],[1,0,0]]); B=M([1,0,0]); P=M([[1,2,0],[0,0,1],[0,1,0]])
eq(qc(A,B),M([[1,2,3],[0,0,0],[0,1,2]]))
eq(P.inv()*A*P,M([[0,-1,1],[1,2,0],[0,0,-1]])); eq(P.inv()*B,M([1,0,0]))
eq(M([[4,8,0]])*P.inv(),M([[4,0,0]]))
eq(cp(A-B*M([[4,k2,0]])),(s+1)**3)
# 5-4
A=M([[-1,0],[1,-2]]); B=M([0,1])
eq(qc(A,B),M([[0,0],[1,-2]])); eq(cp(A-B*M([[k1,3]])),(s+1)*(s+5))
# 5-5
A=M([[0,2],[-3,-5]]); B=M([1,0])
eq(qc(A,B),M([[1,0],[0,-3]]))
eq(cp(A-B*M([[k1,k2]])),s**2+(k1+5)*s+5*k1-3*k2+6)
eq(cp(A-B*M([[S.sqrt(2)-5,(5*S.sqrt(2)-20)/3]])),s**2+S.sqrt(2)*s+1)
# 5-6
A=M([[0,1],[0,0]]); B=M([0,1])
eq(cp(A+B*M([[-S.Rational(5,4),-2]])),(s+1)**2+S.Rational(1,4))
# 5-7
A=M([[-1,0],[-3,-S.Rational(3,2)]]); B=M([2,0])
eq(qc(A,B),M([[2,-2],[0,-6]]))
eq(cp(A+B*M([[k1,k2]])),s**2+(S.Rational(5,2)-2*k1)*s+6*k2-3*k1+S.Rational(3,2))
eq(cp(A+B*M([[-S.Rational(1,4),S.Rational(9,8)]])),s**2+3*s+9)
# 5-8
A=M([[0,1],[-3,-4]]); B=M([0,1])
eq(cp(A+B*M([[k1,k2]])),s**2+(4-k2)*s+3-k1)
eq(S.discriminant(cp(A+B*M([[k1,k2]])),s),(4-k2)**2-4*(3-k1))
# 5-9
A=M([[0,1],[0,-1]]); B=M([0,2]); C=M([[1,0]])
eq(tf(A-B*M([[k1,k2]]),B,C),2/(s*s+(2*k2+1)*s+2*k1))
q=S.log(S.Rational(20000,567)); zeta=q/S.sqrt(S.pi**2+q*q)
eq(S.sqrt(2)*zeta-S.Rational(1,2),(2*zeta*S.sqrt(2)-1)/2)
eq((tf(A-B*M([[1,k2]]),B,C)).subs(s,0),1)
# 5-10
A=M([[0,1,0],[0,0,1],[0,-2,-3]]); B=M([0,0,1])
eq(tf(A,B,M([[100,0,0]])),100/(s*(s+1)*(s+2)))
eq(cp(A+B*M([[-40,-26,-6]])),(s+5)*((s+2)**2+4))
# 5-11
eq(cp(A+B*M([[-4,-4,-1]])),(s+2)*((s+1)**2+1))
eq(tf(A+B*M([[-4,-4,-1]]),B,M([[10,0,0]])),10/((s+2)*(s*s+2*s+2)))
# 5-12
A=M([[0,1],[-1,0]]); B=M([1,0]); C=M([[0,1]])
eq(cp(A),s*s+1); eq(cp(A+B*M([[k1,k2]])),s*s-k1*s+1+k2)
eq(cp(A-B*F*C),s*s+1-F); eq(cp(A-M([h1,h2])*C),s*s+h2*s+1-h1)
# 5-13
A=M([[0,1,0],[0,0,1],[0,2,0]]); B=M([0,0,1]); C=M([[1,1,0]])
eq(tf(A,B,C),(s+1)/(s**3-2*s)); eq(cp(A-B*M([[5,11,5]])),(s+1)*(s*s+4*s+5))
eq(tf(A-B*M([[5,11,5]]),B,C),1/(s*s+4*s+5))
# 5-14
A=M([[1,1,1,1],[0,1,1,1],[0,0,-1,1],[0,0,0,-1]]); B=M([0,1,0,0]); C=M([[1,0,1,1]])
eq(tf(A,B,C),1/(s-1)**2)
eq(M.hstack(S.eye(4)-A,B).rank(),4); eq(M.hstack(-S.eye(4)-A,B).rank(),3)
eq(cp(A+B*M([[k1,k2,k3,k4]])),(s+1)**2*((s-1)*(s-1-k2)-k1))
eq(cp(A+B*M([[-4,-4,k3,k4]])),(s+1)**4)
# 5-15
A=M([[a,-1],[b,-1]]); B=M([1,0]); C=M([[0,1]])
eq(M.vstack(C,C*A),M([[0,1],[b,-1]])); eq(tf(A.subs(a,0),B,C),b/(s*s+s+b))
eq(tf(A.subs({a:0,b:0}),B,C),0)
eq(cp(A-B*M([[k1,k2]])),s*s+(k1-a+1)*s+k1+b*k2-a+b)
eq(cp(A-B*M([[a+1,-1]])),(s+1)**2)
eq(cp(A.subs(b,0)-B*M([[a+1,k2]])),(s+1)**2)
eq(A.subs(b,0)-M([-1,0])*C,S.diag(a,-1))
# 5-16
A=M([[1,3,2],[0,2,0],[0,1,3]]); B=M([[2,1],[1,1],[-1,-1]]); R=M([[2,1,0],[1,1,0],[-1,-1,1]])
eq(qc(A,B),M([[2,1,3,2,5,4],[1,1,2,2,4,4],[-1,-1,-2,-2,-4,-4]]))
eq(R.inv()*A*R,M([[1,0,2],[1,2,-2],[0,0,3]])); eq(R.inv()*B,M([[1,0],[0,1],[0,0]]))
# 5-17
A=M([[-2,4],[1,1]]); B=M([1,0]); C=M([[1,-1]])
eq(qc(A,B),M([[1,-2],[0,1]])); eq(M.vstack(C,C*A),M([[1,-1],[-3,3]]))
eq(cp(A),(s+3)*(s-2)); eq(tf(A,B,C),1/(s+3))
print('PASS:',checks,'exact symbolic checks for exercises 5-1 through 5-17')
